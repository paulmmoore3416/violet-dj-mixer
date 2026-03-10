"""
Animated VU meter widget — simulates signal levels with attack/decay envelope
and a peak-hold indicator.  Designed to replace static QProgressBar instances.
"""
from __future__ import annotations

import random

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QLinearGradient, QPainter
from PyQt6.QtWidgets import QWidget


class VUMeter(QWidget):
    """Vertical animated VU meter with peak-hold LED."""

    # Colour stops used for the bar gradient (bottom → top)
    _GRAD = [
        (0.00, "#00aa44"),
        (0.56, "#00aa44"),
        (0.72, "#ffaa00"),
        (0.86, "#ff4400"),
        (1.00, "#ff0000"),
    ]

    def __init__(self, parent=None, *, channels: int = 2, bar_width: int = 8,
                 gap: int = 3, padding: int = 2) -> None:
        super().__init__(parent)
        self._n      = channels
        self._bw     = bar_width
        self._gap    = gap
        self._pad    = padding
        self._active = False

        # Per-channel state
        self._level:     list[float] = [0.0] * channels   # current smoothed level
        self._target:    list[float] = [0.0] * channels   # goal level
        self._peak:      list[float] = [0.0] * channels   # peak hold level
        self._peak_hold: list[int]   = [0]   * channels   # frames remaining

        # Fixed width; height is flexible
        total_w = padding * 2 + channels * bar_width + max(0, channels - 1) * gap
        self.setFixedWidth(total_w)
        self.setMinimumHeight(60)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(40)   # ~25 fps

    # ── Public API ────────────────────────────────────────────────────────────

    def set_active(self, active: bool) -> None:
        """Enable/disable animation.  When False, levels decay to zero."""
        self._active = active
        if not active:
            self._target = [0.0] * self._n

    def set_level(self, level: float, channel: int = 0) -> None:
        """Set target level 0.0–1.0 for *channel*."""
        if 0 <= channel < self._n:
            self._target[channel] = max(0.0, min(1.0, float(level)))

    def set_levels(self, levels: list[float]) -> None:
        """Set all channel levels at once."""
        for i, lv in enumerate(levels[:self._n]):
            self._target[i] = max(0.0, min(1.0, float(lv)))

    def simulate(self, base: float = 0.5) -> None:
        """Feed a pseudo-random level based on *base* (0.0–1.0)."""
        for i in range(self._n):
            noise = random.gauss(0, 0.08)
            self._target[i] = max(0.0, min(1.0, base + noise))

    # ── Internal ──────────────────────────────────────────────────────────────

    def _tick(self) -> None:
        for i in range(self._n):
            cur = self._level[i]
            tgt = self._target[i]

            # Fast attack (0.7), slow decay (0.05/frame)
            if tgt > cur:
                self._level[i] = min(1.0, cur + (tgt - cur) * 0.65)
            else:
                self._level[i] = max(0.0, cur - 0.05)

            lv = self._level[i]

            # Peak hold: reset if new peak, else count down then fall
            if lv >= self._peak[i]:
                self._peak[i]      = lv
                self._peak_hold[i] = 25       # ~1 s at 25 fps
            else:
                if self._peak_hold[i] > 0:
                    self._peak_hold[i] -= 1
                else:
                    self._peak[i] = max(0.0, self._peak[i] - 0.02)

        self.update()

    def paintEvent(self, _event) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, False)

        h   = self.height() - self._pad * 2
        bw  = self._bw

        for i in range(self._n):
            x = self._pad + i * (bw + self._gap)

            # Dark background track
            p.fillRect(x, self._pad, bw, h, QColor("#080808"))

            lv     = self._level[i]
            fill_h = int(h * lv)
            y_top  = self._pad + (h - fill_h)

            if fill_h > 0:
                grad = QLinearGradient(x, self._pad + h, x, self._pad)
                for stop, color in self._GRAD:
                    grad.setColorAt(stop, QColor(color))
                p.fillRect(x, y_top, bw, fill_h, grad)

            # Peak indicator (2 px bright line)
            pk = self._peak[i]
            if pk > 0.01:
                py = self._pad + int(h * (1.0 - pk))
                if pk > 0.9:
                    pk_color = QColor("#ff2222")
                elif pk > 0.7:
                    pk_color = QColor("#ffaa00")
                else:
                    pk_color = QColor("#00ee66")
                p.fillRect(x, py, bw, 2, pk_color)

        p.end()
