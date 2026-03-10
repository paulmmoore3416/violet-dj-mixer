"""
Unit tests for src/controllers/manager.py — ControllerManager
"""
from __future__ import annotations

import json
import os
import tempfile
import unittest


class TestControllerManagerInit(unittest.TestCase):
    def _make_mgr(self):
        from src.controllers.manager import ControllerManager
        return ControllerManager()

    def test_import(self):
        from src.controllers.manager import ControllerManager
        self.assertTrue(callable(ControllerManager))

    def test_initial_mappings_empty(self):
        mgr = self._make_mgr()
        self.assertEqual(mgr.mappings, {})

    def test_initial_controllers_empty(self):
        mgr = self._make_mgr()
        self.assertEqual(mgr.controllers, {})

    def test_learn_mode_off_by_default(self):
        mgr = self._make_mgr()
        self.assertFalse(mgr.is_learning)

    def test_supported_controllers_count(self):
        from src.controllers.manager import ControllerManager
        self.assertGreaterEqual(len(ControllerManager.SUPPORTED_CONTROLLERS), 17)

    def test_mappable_actions_non_empty(self):
        from src.controllers.manager import ControllerManager
        self.assertGreater(len(ControllerManager.MAPPABLE_ACTIONS), 30)

    def test_builtin_presets_exist(self):
        from src.controllers.manager import ControllerManager
        self.assertIn("Pioneer DDJ-400", ControllerManager.BUILTIN_PRESETS)
        self.assertIn("Numark Mixtrack Pro", ControllerManager.BUILTIN_PRESETS)
        self.assertIn("Akai APC Mini", ControllerManager.BUILTIN_PRESETS)


class TestControllerManagerMapping(unittest.TestCase):
    def setUp(self):
        from src.controllers.manager import ControllerManager
        self.mgr = ControllerManager()

    def test_map_valid_action(self):
        self.mgr.map_control("ctrl_0", 31, "crossfader")
        self.assertEqual(self.mgr.mappings["ctrl_0"]["31"], "crossfader")

    def test_map_invalid_action_raises(self):
        with self.assertRaises(ValueError):
            self.mgr.map_control("ctrl_0", 10, "not_a_real_action")

    def test_map_multiple_ccs(self):
        self.mgr.map_control("ctrl_0", 8,  "volume_deck_a")
        self.mgr.map_control("ctrl_0", 9,  "volume_deck_b")
        self.mgr.map_control("ctrl_0", 31, "crossfader")
        mappings = self.mgr.get_mappings("ctrl_0")
        self.assertEqual(len(mappings), 3)
        self.assertEqual(mappings["8"],  "volume_deck_a")
        self.assertEqual(mappings["9"],  "volume_deck_b")
        self.assertEqual(mappings["31"], "crossfader")

    def test_unmap_removes_entry(self):
        self.mgr.map_control("ctrl_0", 31, "crossfader")
        self.mgr.unmap_control("ctrl_0", 31)
        self.assertNotIn("31", self.mgr.get_mappings("ctrl_0"))

    def test_unmap_nonexistent_is_safe(self):
        self.mgr.unmap_control("ctrl_0", 99)   # Should not raise

    def test_clear_mappings(self):
        self.mgr.map_control("ctrl_0", 0, "play_pause_deck_a")
        self.mgr.map_control("ctrl_0", 1, "play_pause_deck_b")
        self.mgr.clear_mappings("ctrl_0")
        self.assertEqual(self.mgr.get_mappings("ctrl_0"), {})

    def test_get_mappings_unknown_controller(self):
        result = self.mgr.get_mappings("ctrl_unknown")
        self.assertEqual(result, {})

    def test_cc_stored_as_string(self):
        self.mgr.map_control("ctrl_0", 7, "master_volume")
        self.assertIn("7", self.mgr.get_mappings("ctrl_0"))

    def test_overwrite_mapping(self):
        self.mgr.map_control("ctrl_0", 7, "master_volume")
        self.mgr.map_control("ctrl_0", 7, "headphone_volume")
        self.assertEqual(self.mgr.get_mappings("ctrl_0")["7"], "headphone_volume")


class TestControllerManagerPresets(unittest.TestCase):
    def setUp(self):
        from src.controllers.manager import ControllerManager
        self.mgr = ControllerManager()

    def test_load_pioneer_preset(self):
        ok = self.mgr.load_builtin_preset("Pioneer DDJ-400")
        self.assertTrue(ok)
        mappings = self.mgr.get_mappings("default")
        self.assertGreater(len(mappings), 5)
        self.assertIn("crossfader", mappings.values())

    def test_load_numark_preset(self):
        ok = self.mgr.load_builtin_preset("Numark Mixtrack Pro")
        self.assertTrue(ok)
        mappings = self.mgr.get_mappings("default")
        self.assertIn("30", mappings)
        self.assertEqual(mappings["30"], "crossfader")

    def test_load_akai_preset(self):
        ok = self.mgr.load_builtin_preset("Akai APC Mini")
        self.assertTrue(ok)
        mappings = self.mgr.get_mappings("default")
        self.assertIn("play_pause_deck_a", mappings.values())

    def test_load_unknown_preset_returns_false(self):
        ok = self.mgr.load_builtin_preset("Nonexistent Controller 9000")
        self.assertFalse(ok)

    def test_preset_overwrites_existing_mappings(self):
        self.mgr.map_control("default", 99, "master_volume")
        self.mgr.load_builtin_preset("Pioneer DDJ-400", "default")
        # CC 99 should be gone — preset replaces, not merges
        self.assertNotIn("99", self.mgr.get_mappings("default"))


class TestControllerManagerProfile(unittest.TestCase):
    def setUp(self):
        from src.controllers.manager import ControllerManager
        self.mgr = ControllerManager()
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_save_and_reload_profile(self):
        self.mgr.map_control("default", 8,  "volume_deck_a")
        self.mgr.map_control("default", 31, "crossfader")
        path = os.path.join(self.tmpdir, "test_profile.json")
        ok = self.mgr.save_mapping_profile(path, "default")
        self.assertTrue(ok)
        self.assertTrue(os.path.exists(path))

        # Fresh manager, load the saved profile
        from src.controllers.manager import ControllerManager
        mgr2 = ControllerManager()
        data = mgr2.load_mapping_profile(path)
        self.assertEqual(data.get("controller_id"), "default")
        self.assertEqual(mgr2.get_mappings("default")["8"],  "volume_deck_a")
        self.assertEqual(mgr2.get_mappings("default")["31"], "crossfader")

    def test_save_profile_creates_valid_json(self):
        self.mgr.map_control("default", 0, "play_pause_deck_a")
        path = os.path.join(self.tmpdir, "out.json")
        self.mgr.save_mapping_profile(path, "default")
        with open(path) as f:
            data = json.load(f)
        self.assertIn("mappings", data)
        self.assertIn("controller_id", data)

    def test_load_missing_profile_returns_empty(self):
        result = self.mgr.load_mapping_profile("/does/not/exist.json")
        self.assertEqual(result, {})

    def test_load_corrupt_profile_returns_empty(self):
        path = os.path.join(self.tmpdir, "bad.json")
        with open(path, "w") as f:
            f.write("not valid json {{{")
        result = self.mgr.load_mapping_profile(path)
        self.assertEqual(result, {})

    def test_list_saved_profiles_returns_list(self):
        result = self.mgr.list_saved_profiles()
        self.assertIsInstance(result, list)


class TestControllerManagerMidiLearn(unittest.TestCase):
    def setUp(self):
        from src.controllers.manager import ControllerManager
        self.mgr = ControllerManager()

    def test_start_learn(self):
        self.mgr.start_learn("default", "crossfader")
        self.assertTrue(self.mgr.is_learning)

    def test_cancel_learn(self):
        self.mgr.start_learn("default", "crossfader")
        self.mgr.cancel_learn()
        self.assertFalse(self.mgr.is_learning)

    def test_start_learn_invalid_action(self):
        with self.assertRaises(ValueError):
            self.mgr.start_learn("default", "totally_fake_action")

    def test_learn_captures_cc_via_callback(self):
        self.mgr.start_learn("default", "crossfader")
        # Simulate a MIDI CC message arriving on the callback thread
        # message format: (status, cc, value), delta_time
        self.mgr._midi_callback(([0xB0, 55, 64], 0.0))
        self.assertFalse(self.mgr.is_learning)
        self.assertEqual(self.mgr.get_mappings("default").get("55"), "crossfader")

    def test_learn_ignores_non_cc_messages(self):
        self.mgr.start_learn("default", "master_volume")
        # Program change message (0xC0) — should be ignored
        self.mgr._midi_callback(([0xC0, 10, 0], 0.0))
        self.assertTrue(self.mgr.is_learning)  # still in learn mode

    def test_learn_resets_after_capture(self):
        self.mgr.start_learn("default", "crossfader")
        self.mgr._midi_callback(([0xB0, 31, 64], 0.0))
        self.assertIsNone(self.mgr._learn_target_action)
        self.assertIsNone(self.mgr._learn_controller_id)


class TestControllerManagerDispatch(unittest.TestCase):
    def setUp(self):
        from src.controllers.manager import ControllerManager
        self.mgr = ControllerManager()

    def test_register_and_dispatch_action(self):
        received = []
        self.mgr.register_action("crossfader", lambda v: received.append(v))
        self.mgr.map_control("ctrl_0", 31, "crossfader")
        self.mgr._midi_callback(([0xB0, 31, 80], 0.0))
        self.assertEqual(received, [80])

    def test_dispatch_fires_all_registered_callbacks(self):
        results = []
        self.mgr.register_action("master_volume", lambda v: results.append(("a", v)))
        self.mgr.register_action("master_volume", lambda v: results.append(("b", v)))
        self.mgr.map_control("ctrl_0", 7, "master_volume")
        self.mgr._midi_callback(([0xB0, 7, 100], 0.0))
        self.assertIn(("a", 100), results)
        self.assertIn(("b", 100), results)

    def test_dispatch_tolerates_callback_exception(self):
        def bad_cb(v):
            raise RuntimeError("oops")
        self.mgr.register_action("crossfader", bad_cb)
        self.mgr.map_control("ctrl_0", 31, "crossfader")
        # Should not propagate the exception
        try:
            self.mgr._midi_callback(([0xB0, 31, 64], 0.0))
        except RuntimeError:
            self.fail("Callback exception leaked out of _dispatch_action")

    def test_unmapped_cc_fires_nothing(self):
        received = []
        self.mgr.register_action("crossfader", lambda v: received.append(v))
        # CC 99 is not mapped
        self.mgr._midi_callback(([0xB0, 99, 64], 0.0))
        self.assertEqual(received, [])

    def test_short_message_ignored(self):
        # Messages with fewer than 3 bytes are silently dropped
        try:
            self.mgr._midi_callback(([0xB0, 31], 0.0))
        except Exception:
            self.fail("Short message raised an exception")


if __name__ == "__main__":
    unittest.main()
