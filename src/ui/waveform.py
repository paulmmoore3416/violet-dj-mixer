"""
Waveform display widget — draws an audio waveform using QPainter.
When real sample data is unavailable it generates a deterministic
pseudo-waveform from the track's filename hash so each track looks distinct.
"""
from __future__ import annotations

import hashlib
import math
import random

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import QWidget


# ── Waveform data generation ──────────────────────────────────────────────────

def _synth_waveform(seed: int, n: int = 512) -> list[float]:
    """Generate a convincing-looking pseudo waveform using seeded RNG."""
    rng   = random.Random(seed)
    freqs = [rng.uniform(0.003, 0.12) for _ in range(6)]
    amps  = [rng.uniform(0.08, 0.45)  for _ in range(6)]
    phase = [rng.uniform(0, 2 * math.pi) for _ in range(6)]
    data  = []
    for t in range(n):
        v = sum(a * math.sin(2 * math.pi * f * t + p)
                for a, f, p in zip(amps, freqs, phase))
        v += rng.gauss(0, 0.06)
        # Occasional transient spikes to simulate drums
        if rng.random() < 0.015:
            v += rng.uniform(0.4, 0.9) * rng.choice([-1, 1])
        data.append(max(-1.0, min(1.0, v)))
    return data


# ── Widget ────────────────────────────────────────────────────────────────────

class WaveformDisplay(QWidget):
    """Waveform bar display with playback cursor and loop-region overlay."""

    BG_COLOR      = QColor("#060606")
    WAVE_COLOR    = QColor(40, 110, 60)      # dim green
    WAVE_BRIGHT   = QColor(50, 180, 85)      # near-cursor highlight
    CURSOR_COLOR  = QColor("#ff8800")
    LOOP_COLOR    = QColor(80, 140, 255, 35)
    EMPTY_COLOR   = QColor(30, 40, 30)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setMinimumHeight(44)
        self.setMinimumWidth(80)
        self.setCursor(Qt.CursorShape.CrossCursor)

        self._data:     list[float] = []
        self._position: float       = 0.0     # 0.0–1.0
        self._loop_in:  float       = -1.0
        self._loop_out: float       = -1.0
        self._phase:    float       = 0.0     # animation shimmer

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._animate)
        self._timer.start(80)   # ~12 fps shimmer

    # ── Public API ────────────────────────────────────────────────────────────

    def load_track(self, file_path: str) -> None:
        """Generate waveform data deterministically from the file path."""
        seed = int(hashlib.md5(file_path.encode()).hexdigest()[:8], 16)
        self._data    = _synth_waveform(seed, 512)
        self._position = 0.0
        self._loop_in  = -1.0
        self._loop_out = -1.0
        self.update()

    def clear(self) -> None:
        self._data     = []
        self._position = 0.0
        self.update()

    def set_position(self, fraction: float) -> None:
        """Set playback cursor position (0.0 = start, 1.0 = end)."""
        self._position = max(0.0, min(1.0, fraction))
        self.update()

    def set_loop(self, in_frac: float, out_frac: float) -> None:
        self._loop_in  = in_frac
        self._loop_out = out_frac
        self.update()

    def clear_loop(self) -> None:
        self._loop_in  = -1.0
        self._loop_out = -1.0
        self.update()

    # ── Internal ──────────────────────────────────────────────────────────────

    def _animate(self) -> None:
        self._phase = (self._phase + 0.04) % (2 * math.pi)
        if self._data:
            self.update()

    def paintEvent(self, _event) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, False)

        w, h = self.width(), self.height()
        mid  = h // 2

        p.fillRect(0, 0, w, h, self.BG_COLOR)

        if not self._data:
            # Flat placeholder line
            p.setPen(QPen(self.EMPTY_COLOR, 1))
            for x in range(0, w, 4):
                p.drawPoint(x, mid)
            p.end()
            return

        # Loop region shading
        if 0.0 <= self._loop_in < self._loop_out <= 1.0:
            lx1 = int(self._loop_in  * w)
            lx2 = int(self._loop_out * w)
            p.fillRect(lx1, 0, max(1, lx2 - lx1), h, self.LOOP_COLOR)

        n    = len(self._data)
        step = max(1.0, w / n)

        for i, val in enumerate(self._data):
            x       = int(i * step)
            bar_h   = max(1, int(abs(val) * (mid - 2)))
            # Proximity to playback cursor → brighter colour
            dist    = abs(i / n - self._position)
            shimmer = 0.5 + 0.5 * math.sin(self._phase + i * 0.04)
            if dist < 0.04:
                color = self.WAVE_BRIGHT
            elif dist < 0.12 and shimmer > 0.7:
                r = int(self.WAVE_COLOR.red()   + shimmer * 20)
                g = int(self.WAVE_COLOR.green() + shimmer * 40)
                b = int(self.WAVE_COLOR.blue()  + shimmer * 10)
                color = QColor(min(255, r), min(255, g), min(255, b))
            else:
                color = self.WAVE_COLOR
            p.fillRect(x, mid - bar_h, max(1, int(step)), bar_h * 2, color)

        # Playback cursor
        cx = int(self._position * w)
        p.fillRect(cx, 0, 2, h, self.CURSOR_COLOR)

        p.end()

    def mousePressEvent(self, event) -> None:
        """Click to seek (emits nothing — caller can override or subclass)."""
        if self._data and event.button() == Qt.MouseButton.LeftButton:
            frac = event.position().x() / max(1, self.width())
            self._position = max(0.0, min(1.0, frac))
            self.update()
        super().mousePressEvent(event)
