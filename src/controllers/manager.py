"""
MIDI and hardware controller support
"""

from __future__ import annotations

import json
import logging
import os
from typing import Callable

logger = logging.getLogger(__name__)

# ── Default profile paths ─────────────────────────────────────────────────────
_PROFILES_DIR = os.path.expanduser("~/.violet_dj/controller_profiles")

# ── Thread-safe Qt signal emitter ────────────────────────────────────────────
# Emits action_triggered(action_name, value) safely from the MIDI callback
# thread into the Qt main thread via an auto-connection (queued if cross-thread).
try:
    from PyQt6.QtCore import QObject, pyqtSignal

    class MidiActionEmitter(QObject):
        """Bridges the rtmidi callback thread to the Qt UI thread."""
        action_triggered = pyqtSignal(str, int)   # (action_name, value 0-127)
        learn_completed  = pyqtSignal(str, int, str)  # (controller_id, cc, action)

    _EMITTER_AVAILABLE = True
except ImportError:
    _EMITTER_AVAILABLE = False
    MidiActionEmitter = None  # type: ignore


class ControllerManager:
    """Manages MIDI controllers, mappings, and hardware devices."""

    SUPPORTED_CONTROLLERS = {
        'pioneer_ddj':       'Pioneer DDJ Series',
        'pioneer_cdj':       'Pioneer CDJ Series',
        'pioneer_djm':       'Pioneer DJM Mixers',
        'numark':            'Numark Controllers',
        'reloop':            'Reloop Controllers',
        'traktor':           'Native Instruments Traktor',
        'denon':             'Denon DJ Controllers',
        'rane':              'Rane Seventy Series',
        'xone':              'Allen & Heath Xone',
        'akai':              'Akai Professional',
        'technics':          'Technics SL-1200',
        'stanton':           'Stanton Turntables',
        'vestax':            'Vestax Controllers',
        'korg':              'Korg Instruments',
        'roland':            'Roland Devices',
        'yamaha':            'Yamaha Instruments',
        'native_instruments':'Native Instruments',
    }

    # Standard DJ actions available for mapping
    MAPPABLE_ACTIONS = [
        "play_pause_deck_a",
        "play_pause_deck_b",
        "cue_deck_a",
        "cue_deck_b",
        "sync_deck_a",
        "sync_deck_b",
        "loop_in_deck_a",
        "loop_in_deck_b",
        "loop_out_deck_a",
        "loop_out_deck_b",
        "crossfader",
        "volume_deck_a",
        "volume_deck_b",
        "eq_hi_deck_a",
        "eq_mid_deck_a",
        "eq_low_deck_a",
        "eq_hi_deck_b",
        "eq_mid_deck_b",
        "eq_low_deck_b",
        "filter_deck_a",
        "filter_deck_b",
        "fx_1_on",
        "fx_2_on",
        "fx_3_on",
        "fx_depth",
        "master_volume",
        "headphone_volume",
        "headphone_cue_mix",
        "jog_wheel_deck_a",
        "jog_wheel_deck_b",
        "pitch_deck_a",
        "pitch_deck_b",
        "hot_cue_1_deck_a",
        "hot_cue_2_deck_a",
        "hot_cue_3_deck_a",
        "hot_cue_4_deck_a",
        "hot_cue_1_deck_b",
        "hot_cue_2_deck_b",
        "hot_cue_3_deck_b",
        "hot_cue_4_deck_b",
    ]

    # Enhancement 20 – built-in preset profiles for common controllers
    BUILTIN_PRESETS: dict[str, dict] = {
        "Pioneer DDJ-400": {
            "controller": "pioneer_ddj",
            "mappings": {
                "default": {
                    "0": "play_pause_deck_a",
                    "1": "play_pause_deck_b",
                    "2": "cue_deck_a",
                    "3": "cue_deck_b",
                    "8": "volume_deck_a",
                    "9": "volume_deck_b",
                    "16": "eq_hi_deck_a",
                    "17": "eq_mid_deck_a",
                    "18": "eq_low_deck_a",
                    "19": "eq_hi_deck_b",
                    "20": "eq_mid_deck_b",
                    "21": "eq_low_deck_b",
                    "31": "crossfader",
                    "48": "pitch_deck_a",
                    "49": "pitch_deck_b",
                }
            },
        },
        "Numark Mixtrack Pro": {
            "controller": "numark",
            "mappings": {
                "default": {
                    "0": "play_pause_deck_a",
                    "1": "play_pause_deck_b",
                    "2": "cue_deck_a",
                    "3": "cue_deck_b",
                    "7": "volume_deck_a",
                    "11": "volume_deck_b",
                    "22": "eq_hi_deck_a",
                    "23": "eq_mid_deck_a",
                    "24": "eq_low_deck_a",
                    "26": "eq_hi_deck_b",
                    "27": "eq_mid_deck_b",
                    "28": "eq_low_deck_b",
                    "30": "crossfader",
                    "33": "master_volume",
                }
            },
        },
        "Akai APC Mini": {
            "controller": "akai",
            "mappings": {
                "default": {
                    "48": "hot_cue_1_deck_a",
                    "49": "hot_cue_2_deck_a",
                    "50": "hot_cue_3_deck_a",
                    "51": "hot_cue_4_deck_a",
                    "56": "hot_cue_1_deck_b",
                    "57": "hot_cue_2_deck_b",
                    "58": "hot_cue_3_deck_b",
                    "59": "hot_cue_4_deck_b",
                    "64": "play_pause_deck_a",
                    "65": "play_pause_deck_b",
                    "66": "cue_deck_a",
                    "67": "cue_deck_b",
                }
            },
        },
    }

    def __init__(self):
        logger.info("Initializing Controller Manager")
        os.makedirs(_PROFILES_DIR, exist_ok=True)
        self._midi_in = None
        self._midi_out = None
        self._init_midi()
        self.controllers: dict = {}
        # mappings: { controller_id: { str(midi_cc): action_name } }
        self.mappings: dict[str, dict[str, str]] = {}
        # action dispatch callbacks (non-Qt path for headless/test use)
        self._action_callbacks: dict[str, list[Callable]] = {}
        # MIDI learn state
        self._learn_mode: bool = False
        self._learn_target_action: str | None = None
        self._learn_controller_id: str | None = None
        # Thread-safe Qt emitter (None in headless/test environments)
        self.emitter: MidiActionEmitter | None = (
            MidiActionEmitter() if _EMITTER_AVAILABLE else None
        )

    def _init_midi(self):
        """Try to initialise rtmidi; degrade gracefully if unavailable."""
        try:
            import rtmidi
            self._midi_in = rtmidi.MidiIn()
            self._midi_out = rtmidi.MidiOut()
            logger.info("rtmidi initialised")
        except Exception as e:
            logger.warning(f"rtmidi unavailable: {e} — running without MIDI hardware support")

    # ── Port discovery ────────────────────────────────────────────────────────
    def list_available_controllers(self) -> list[str]:
        """Return all detected MIDI input port names."""
        if self._midi_in is None:
            return []
        try:
            ports = self._midi_in.get_ports()
            return ports if ports else []
        except Exception as e:
            logger.warning(f"Port list error: {e}")
            return []

    # ── Connection ────────────────────────────────────────────────────────────
    def connect_controller(self, controller_name: str) -> bool:
        """Open the first MIDI port matching controller_name."""
        if self._midi_in is None:
            return False
        try:
            ports = self._midi_in.get_ports()
            for i, port in enumerate(ports):
                if controller_name.lower() in port.lower():
                    self._midi_in.open_port(i)
                    self._midi_in.set_callback(self._midi_callback)
                    controller_id = f"ctrl_{i}"
                    self.controllers[controller_id] = {"port": port, "index": i}
                    if controller_id not in self.mappings:
                        self.mappings[controller_id] = {}
                    logger.info(f"Connected to controller: {port}")
                    return True
        except Exception as e:
            logger.error(f"Failed to connect controller: {e}")
        return False

    # ── Auto-detect ───────────────────────────────────────────────────────────
    def detect_controllers(self) -> list[dict]:
        """Auto-detect connected controllers by matching port names."""
        detected = []
        try:
            ports = self.list_available_controllers()
            for port in ports:
                for ctrl_type, friendly_name in self.SUPPORTED_CONTROLLERS.items():
                    keywords = [ctrl_type.replace('_', ' '), friendly_name.lower()]
                    if any(kw in port.lower() for kw in keywords):
                        detected.append({
                            'type': ctrl_type,
                            'name': friendly_name,
                            'port': port,
                        })
            logger.info(f"Detected {len(detected)} controllers")
        except Exception as e:
            logger.warning(f"Controller detection error: {e}")
        return detected

    # ── Mapping ───────────────────────────────────────────────────────────────
    def map_control(self, controller_id: str, midi_cc: int, action: str) -> None:
        """Map a MIDI CC number to a named action for a controller."""
        if action not in self.MAPPABLE_ACTIONS:
            raise ValueError(f"Unknown action: {action}")
        if controller_id not in self.mappings:
            self.mappings[controller_id] = {}
        self.mappings[controller_id][str(midi_cc)] = action
        logger.info(f"[{controller_id}] CC {midi_cc} → {action}")

    def unmap_control(self, controller_id: str, midi_cc: int) -> None:
        """Remove a CC mapping."""
        if controller_id in self.mappings:
            self.mappings[controller_id].pop(str(midi_cc), None)

    def get_mappings(self, controller_id: str) -> dict[str, str]:
        """Return { str(cc): action } for a controller."""
        return dict(self.mappings.get(controller_id, {}))

    def clear_mappings(self, controller_id: str) -> None:
        """Remove all mappings for a controller."""
        self.mappings[controller_id] = {}

    # ── Profile persistence ───────────────────────────────────────────────────
    def load_mapping_profile(self, profile_path: str) -> dict:
        """Load mappings from a JSON profile file. Returns the loaded data."""
        try:
            with open(profile_path) as f:
                data = json.load(f)
            controller_id = data.get("controller_id", "default")
            self.mappings[controller_id] = {
                str(k): v for k, v in data.get("mappings", {}).items()
            }
            logger.info(f"Loaded profile: {profile_path} ({len(self.mappings[controller_id])} mappings)")
            return data
        except Exception as e:
            logger.error(f"Failed to load profile {profile_path}: {e}")
            return {}

    def save_mapping_profile(self, profile_path: str, controller_id: str = "default") -> bool:
        """Save current mappings for controller_id to a JSON profile file."""
        try:
            data = {
                "controller_id": controller_id,
                "controller_name": self.controllers.get(controller_id, {}).get("port", controller_id),
                "mappings": self.mappings.get(controller_id, {}),
            }
            with open(profile_path, "w") as f:
                json.dump(data, f, indent=2)
            logger.info(f"Saved profile: {profile_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save profile {profile_path}: {e}")
            return False

    def load_builtin_preset(self, preset_name: str, controller_id: str = "default") -> bool:
        """Load a built-in preset by name."""
        preset = self.BUILTIN_PRESETS.get(preset_name)
        if not preset:
            logger.warning(f"No preset named: {preset_name}")
            return False
        self.mappings[controller_id] = dict(
            preset["mappings"].get("default", {})
        )
        logger.info(f"Loaded preset '{preset_name}' into {controller_id}")
        return True

    def list_saved_profiles(self) -> list[str]:
        """Return filenames of saved profiles in the profiles directory."""
        try:
            return [f for f in os.listdir(_PROFILES_DIR) if f.endswith(".json")]
        except Exception:
            return []

    # ── Action callbacks ──────────────────────────────────────────────────────
    def register_action(self, action: str, callback: Callable) -> None:
        """Register a callback to fire when action is triggered via MIDI."""
        if action not in self._action_callbacks:
            self._action_callbacks[action] = []
        self._action_callbacks[action].append(callback)

    def _dispatch_action(self, action: str, value: int) -> None:
        """Fire all registered callbacks for an action."""
        for cb in self._action_callbacks.get(action, []):
            try:
                cb(value)
            except Exception as e:
                logger.warning(f"Action callback error [{action}]: {e}")

    # ── MIDI callback ─────────────────────────────────────────────────────────
    def _midi_callback(self, message_data, _data=None):
        """Receive raw MIDI message and dispatch to mapped action or learn.

        Called on the rtmidi background thread — never touch Qt widgets here
        directly.  Instead emit Qt signals (queued connection → main thread).
        """
        message, _delta_time = message_data
        if len(message) < 3:
            return
        status, cc, value = message[0], message[1], message[2]
        # Handle note-on (0x90) as button presses (value > 0) and
        # control-change (0xB0) as knob/fader movements.
        msg_type = status & 0xF0
        if msg_type not in (0x90, 0xB0):
            return
        # Normalise note-on to 0-127 the same way as CC
        logger.debug(f"MIDI type=0x{msg_type:02X} cc/note={cc} value={value}")

        # MIDI learn: capture the very next message
        if self._learn_mode and self._learn_target_action and self._learn_controller_id:
            self.map_control(self._learn_controller_id, cc, self._learn_target_action)
            captured_action = self._learn_target_action
            captured_ctrl   = self._learn_controller_id
            self._learn_mode = False
            self._learn_target_action = None
            self._learn_controller_id = None
            logger.info(f"MIDI Learn captured: CC {cc} → {captured_action}")
            # Notify UI via Qt signal (thread-safe)
            if self.emitter:
                self.emitter.learn_completed.emit(captured_ctrl, cc, captured_action)
            return

        # Dispatch to registered plain callbacks and Qt signal
        for mapping in self.mappings.values():
            action = mapping.get(str(cc))
            if action:
                self._dispatch_action(action, value)
                if self.emitter:
                    self.emitter.action_triggered.emit(action, value)
                return

    # ── Enhancement 16: MIDI Learn ────────────────────────────────────────────
    def start_learn(self, controller_id: str, action: str) -> None:
        """Enter MIDI learn mode: next incoming CC is mapped to action."""
        if action not in self.MAPPABLE_ACTIONS:
            raise ValueError(f"Unknown action: {action}")
        self._learn_controller_id = controller_id
        self._learn_target_action = action
        self._learn_mode = True
        logger.info(f"MIDI Learn started for action: {action}")

    def cancel_learn(self) -> None:
        """Exit MIDI learn mode without mapping."""
        self._learn_mode = False
        self._learn_target_action = None
        self._learn_controller_id = None
        logger.info("MIDI Learn cancelled")

    @property
    def is_learning(self) -> bool:
        return self._learn_mode
