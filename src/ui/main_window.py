"""
Main window for Violet DJ Mixer
Pioneer DJM-800 + DJS-1000 Hardware-Inspired Interface
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from datetime import datetime

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTabWidget, QLabel, QPushButton, QSlider, QDial,
                             QGridLayout, QComboBox, QSpinBox, QDoubleSpinBox,
                             QCheckBox, QProgressBar, QFrame, QMessageBox,
                             QFileDialog, QListWidget, QListWidgetItem,
                             QMenu, QTableWidget, QTableWidgetItem,
                             QHeaderView, QSplitter, QInputDialog,
                             QAbstractItemView, QTreeWidget, QTreeWidgetItem,
                             QLineEdit, QScrollArea, QGroupBox)
from PyQt6.QtCore import Qt, QSize, QTimer, pyqtSlot, pyqtSignal
from PyQt6.QtGui import (QFont, QColor, QLinearGradient, QPainter,
                         QShortcut, QKeySequence, QAction, QPen)
import logging

# ── Optional sub-modules (graceful degradation) ───────────────────────────────
try:
    from src.ui.vu_meter import VUMeter
    _HAS_VU = True
except Exception:
    _HAS_VU = False

try:
    from src.ui.waveform import WaveformDisplay
    _HAS_WAVE = True
except Exception:
    _HAS_WAVE = False

try:
    from src.audio.metadata import read_metadata, format_duration
    _HAS_META = True
except Exception:
    _HAS_META = False

try:
    from src.audio.recorder import Recorder, RECORDINGS_DIR
    _HAS_REC = True
except Exception:
    _HAS_REC = False

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
#  Pioneer Hardware-Inspired Stylesheet
#  DJM-800 dark gray body · amber CUE accents · LED meters · chrome faders
#  DJS-1000 performance pads · LCD effects display · beat sync controls
# ─────────────────────────────────────────────────────────────────────────────
HARDWARE_STYLESHEET = """

/* ══════════════════════════════════════════════════════════
   VIOLET DJ  ·  Hardware Dark Theme
   ══════════════════════════════════════════════════════════ */

QMainWindow { background: #111111; }

QWidget { background: transparent; color: #cccccc;
    font-family: "Inter", "Segoe UI", "Ubuntu", sans-serif; font-size: 10px; }

/* ── Panel frames ───────────────────────────────────────── */
QFrame#channelStrip {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #212121, stop:1 #1a1a1a);
    border: 1px solid #303030;
    border-top: 2px solid #3a3a3a;
    border-radius: 6px;
}

QFrame#panelLeft, QFrame#panelRight {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #1e1e1e, stop:1 #171717);
    border: 1px solid #2e2e2e;
    border-top: 2px solid #383838;
    border-radius: 6px;
}

QFrame#crossfaderPanel {
    background: #161616;
    border: 1px solid #2a2a2a;
    border-radius: 5px;
}

QFrame#glassCard {
    background: #181818;
    border: 1px solid #2a2a2a;
    border-radius: 5px;
}

QFrame#lcdFrame {
    background: #00070f;
    border: 2px solid #0a2030;
    border-radius: 4px;
}

/* ── Typography ─────────────────────────────────────────── */
QLabel { color: #777777; background: transparent; font-size: 9px; }

QLabel#sectionLabel {
    color: #555555; font-size: 8px; font-weight: bold;
    letter-spacing: 1.5px;
}

QLabel#channelNum {
    color: #ff8800; font-size: 13px; font-weight: bold;
    background: transparent;
}

QLabel#panelTitle {
    color: #999999; font-size: 9px; font-weight: bold;
    letter-spacing: 2px; background: transparent;
}

QLabel#effectName {
    color: #55aaff; background: #00070f;
    font-size: 16px; font-weight: bold;
    font-family: "Courier New", monospace;
    letter-spacing: 3px;
    border: 1px solid #0a2030;
    border-radius: 3px;
    padding: 5px 8px;
}

QLabel#bpmValue {
    color: #ffffff; background: #00070f;
    font-size: 22px; font-weight: bold;
    font-family: "Courier New", monospace;
    letter-spacing: 2px;
    border: 1px solid #0a2030;
    border-radius: 3px;
    padding: 3px 8px;
}

QLabel#msValue {
    color: #aaaaff; background: #00070f;
    font-size: 13px; font-weight: bold;
    font-family: "Courier New", monospace;
    border: 1px solid #0a2030;
    border-radius: 3px;
    padding: 3px 8px;
}

QLabel#waveformDisplay {
    background: #060606;
    border: 1px solid #222222;
    border-radius: 3px;
    color: #1a5522;
    font-size: 9px;
}

QLabel#deviceList, QLabel#deviceDetails, QLabel#mappingArea {
    background: #0e0e0e; border: 1px solid #262626;
    border-radius: 6px; color: #444444; padding: 12px;
    font-size: 10px;
}

/* ── Buttons ─────────────────────────────────────────────── */
QPushButton {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #2e2e2e, stop:1 #212121);
    color: #888888;
    border: 1px solid #3e3e3e;
    border-top: 1px solid #484848;
    border-radius: 4px;
    padding: 7px 16px;
    font-size: 10px; font-weight: bold;
    min-height: 28px; min-width: 52px;
    letter-spacing: 0.5px;
}

QPushButton:hover {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #3a3a3a, stop:1 #2c2c2c);
    color: #cccccc; border-color: #555555;
}

QPushButton:pressed {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #1a1a1a, stop:1 #222222);
    border-top-color: #222222; color: #999999;
    padding-top: 8px; padding-bottom: 6px;
}

QPushButton:checked {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #383838, stop:1 #2a2a2a);
    color: #ffffff; border-color: #ff8800;
}

/* CUE — Pioneer amber */
QPushButton#btnCue {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #7a3a00, stop:1 #4a2200);
    color: #cc7700; border: 1px solid #5a3200;
    border-top: 1px solid #8a4400; border-radius: 4px;
    font-size: 12px; font-weight: bold; letter-spacing: 2px;
    min-height: 38px; min-width: 70px; padding: 9px 8px;
}
QPushButton#btnCue:hover {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #9a4a00, stop:1 #6a3200);
    color: #ff9922; border-color: #8a4400;
}
QPushButton#btnCue:checked, QPushButton#btnCue:pressed {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #ff9900, stop:1 #cc5500);
    color: #ffffff; border-color: #ffaa22;
    border-top-color: #ffcc55;
}

/* Play — green */
QPushButton#btnPlay {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #1a4422, stop:1 #102a16);
    color: #447744; border-color: #1e3a22;
}
QPushButton#btnPlay:hover {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #225530, stop:1 #163a22);
    color: #66cc66;
}
QPushButton#btnPlay:checked {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #00aa33, stop:1 #006622);
    color: #ffffff; border-color: #00cc44;
    border-top-color: #33ee66;
}

/* Pause */
QPushButton#btnPause:checked {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #cc8800, stop:1 #885500);
    color: #ffffff; border-color: #ffbb00;
}

/* Load */
QPushButton#btnLoad {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #242436, stop:1 #1a1a28);
    color: #6688aa; border-color: #303044;
}
QPushButton#btnLoad:hover {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #303048, stop:1 #222235);
    color: #88aacc; border-color: #4a4a66;
}

/* Mute */
QPushButton#btnMute:checked {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #cc2222, stop:1 #881818);
    color: #ffffff; border-color: #ff3333;
}

/* Solo */
QPushButton#btnSolo:checked {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #0066cc, stop:1 #003388);
    color: #ffffff; border-color: #0088ff;
}

/* TAP button — large green circle */
QPushButton#btnTap {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #00aa33, stop:1 #006622);
    color: #ffffff; border: 2px solid #00cc44;
    border-radius: 28px; font-size: 11px; font-weight: bold;
    min-width: 56px; max-width: 56px;
    min-height: 56px; max-height: 56px;
}
QPushButton#btnTap:hover {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #00cc44, stop:1 #008833);
    border-color: #33ee66;
}
QPushButton#btnTap:pressed {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #009922, stop:1 #005511);
}

/* ON/OFF big amber button */
QPushButton#btnOnOff {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #ff8800, stop:1 #cc5500);
    color: #ffffff; border: 2px solid #ffaa22;
    border-radius: 28px; font-size: 11px; font-weight: bold;
    min-width: 56px; max-width: 56px;
    min-height: 56px; max-height: 56px;
}
QPushButton#btnOnOff:checked {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #5a3000, stop:1 #3a2000);
    color: #cc7700; border-color: #5a3200;
}

/* Beat sync buttons */
QPushButton#btnSync {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #2a2a2a, stop:1 #1e1e1e);
    color: #888888; border-color: #3a3a3a;
    padding: 6px 14px; font-size: 10px;
}
QPushButton#btnMaster {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #7a3a00, stop:1 #4a2200);
    color: #cc7700; border-color: #5a3200;
    padding: 6px 14px; font-size: 10px;
}

/* Performance pads */
QPushButton#pad {
    border: 2px solid rgba(0,0,0,0.5);
    border-radius: 7px;
    color: rgba(255,255,255,0.75);
    font-size: 11px; font-weight: bold;
    min-width: 70px; min-height: 70px;
    max-width: 90px; max-height: 90px;
}
QPushButton#pad:pressed {
    border-color: rgba(255,255,255,0.6);
    padding-top: 3px; padding-bottom: 1px;
}

QPushButton[padColor="orange_red"] { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #ff5020,stop:1 #cc2a10); }
QPushButton[padColor="orange"]     { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #ff8020,stop:1 #cc5010); }
QPushButton[padColor="amber"]      { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #ffaa30,stop:1 #cc7a10); }
QPushButton[padColor="yellow"]     { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #ffcc40,stop:1 #cc9a20); }
QPushButton[padColor="lime"]       { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #88ee50,stop:1 #50aa20); }
QPushButton[padColor="green"]      { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #50cc30,stop:1 #308810); }
QPushButton[padColor="teal"]       { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #30cc80,stop:1 #108850); }
QPushButton[padColor="mint"]       { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #50ee90,stop:1 #28aa55); }
QPushButton[padColor="sky"]        { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #30a0ff,stop:1 #1060cc); }
QPushButton[padColor="blue"]       { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #3060ff,stop:1 #1030cc); }
QPushButton[padColor="purple"]     { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #7030ff,stop:1 #4010cc); }
QPushButton[padColor="violet"]     { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #9055ff,stop:1 #6020cc); }
QPushButton[padColor="pink"]       { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #ff3090,stop:1 #cc1060); }
QPushButton[padColor="rose"]       { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #ff50a0,stop:1 #cc2070); }
QPushButton[padColor="magenta"]    { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #ff30c0,stop:1 #cc1090); }
QPushButton[padColor="fuchsia"]    { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #dd30ff,stop:1 #aa10cc); }

/* Hot-cue strip buttons (small) */
QPushButton[padColor="orange_red"]#hotCue,
QPushButton[padColor="orange"]#hotCue,
QPushButton[padColor="amber"]#hotCue,
QPushButton[padColor="yellow"]#hotCue,
QPushButton[padColor="lime"]#hotCue,
QPushButton[padColor="green"]#hotCue,
QPushButton[padColor="teal"]#hotCue,
QPushButton[padColor="sky"]#hotCue,
QPushButton[padColor="blue"]#hotCue,
QPushButton[padColor="purple"]#hotCue,
QPushButton[padColor="violet"]#hotCue,
QPushButton[padColor="pink"]#hotCue,
QPushButton[padColor="rose"]#hotCue,
QPushButton[padColor="magenta"]#hotCue,
QPushButton[padColor="fuchsia"]#hotCue {
    min-width: 38px; max-width: 50px;
    min-height: 32px; max-height: 40px;
    font-size: 9px; border-radius: 5px;
}

/* ── Level meters ───────────────────────────────────────── */
QProgressBar {
    background: #080808; border: 1px solid #1e1e1e;
    border-radius: 2px; color: transparent;
    max-width: 10px; text-align: center;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0.5,y1:1,x2:0.5,y2:0,
        stop:0.00 #00aa44, stop:0.56 #00aa44,
        stop:0.72 #ffaa00, stop:0.86 #ff4400, stop:1.00 #ff0000);
    border-radius: 1px;
}

/* ── Sliders ─────────────────────────────────────────────── */
QSlider::groove:horizontal {
    height: 4px; background: #0a0a0a;
    border: 1px solid #222222; border-radius: 2px; margin: 0;
}
QSlider::groove:vertical {
    width: 4px; background: #0a0a0a;
    border: 1px solid #222222; border-radius: 2px; margin: 0;
}
QSlider::sub-page:horizontal { background: #ff8800; border-radius: 2px; }
QSlider::add-page:vertical   { background: #ff8800; border-radius: 2px; }

QSlider::handle:horizontal {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #666666, stop:0.5 #aaaaaa, stop:1 #444444);
    border: 1px solid #888888; width: 12px; height: 12px;
    border-radius: 6px; margin: -4px 0;
}
QSlider::handle:vertical {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #333333, stop:0.3 #777777,
        stop:0.5 #cccccc, stop:0.7 #777777, stop:1 #333333);
    border: 1px solid #888888; width: 26px; height: 12px;
    border-radius: 3px; margin: 0 -11px;
}
QSlider::handle:hover {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #888888, stop:0.5 #eeeeee, stop:1 #666666);
    border-color: #bbbbbb;
}

/* Channel fader */
QSlider#channelFader::groove:vertical {
    width: 6px; background: #060606;
    border: 1px solid #1a1a1a; border-radius: 3px;
}
QSlider#channelFader::handle:vertical {
    width: 34px; height: 16px; border-radius: 4px; margin: 0 -14px;
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #1e1e1e, stop:0.2 #666666,
        stop:0.5 #c8c8c8, stop:0.8 #666666, stop:1 #1e1e1e);
    border: 1px solid #999999;
}
QSlider#channelFader::add-page:vertical { background: transparent; }
QSlider#channelFader::sub-page:vertical { background: transparent; }

/* Master fader */
QSlider#masterFader::groove:vertical {
    width: 8px; background: #060606;
    border: 1px solid #1c1c1c; border-radius: 4px;
}
QSlider#masterFader::handle:vertical {
    width: 36px; height: 18px; border-radius: 5px; margin: 0 -14px;
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #1e1e1e, stop:0.2 #888888,
        stop:0.5 #eeeeee, stop:0.8 #888888, stop:1 #1e1e1e);
    border: 2px solid #aaaaaa;
}
QSlider#masterFader::add-page:vertical { background: transparent; }
QSlider#masterFader::sub-page:vertical { background: transparent; }

/* Tempo/pitch fader */
QSlider#tempoFader::groove:vertical {
    width: 8px; background: #080808;
    border: 1px solid #1e1e1e; border-radius: 4px;
}
QSlider#tempoFader::handle:vertical {
    width: 28px; height: 60px; border-radius: 4px; margin: 0 -10px;
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #1e1e1e, stop:0.2 #666666,
        stop:0.5 #c8c8c8, stop:0.8 #666666, stop:1 #1e1e1e);
    border: 1px solid #999999;
}
QSlider#tempoFader::add-page:vertical { background: rgba(50,130,50,60); }
QSlider#tempoFader::sub-page:vertical { background: rgba(50,130,50,60); }

/* Crossfader */
QSlider#crossfader::groove:horizontal {
    height: 10px; background: #060606;
    border: 1px solid #1c1c1c; border-radius: 5px;
}
QSlider#crossfader::handle:horizontal {
    width: 32px; height: 32px;
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #999999, stop:0.35 #dddddd,
        stop:0.65 #dddddd, stop:1 #666666);
    border: 2px solid #888888; border-radius: 4px; margin: -11px 0;
}

/* ── Dials ───────────────────────────────────────────────── */
QDial { background: #1c1c1c; }

/* ── Tabs ────────────────────────────────────────────────── */
QTabWidget::pane {
    background: #181818; border: 1px solid #2a2a2a;
    border-top: none; border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px; padding: 14px;
}
QTabWidget > QWidget { background: transparent; }
QTabBar { background: transparent; }
QTabBar::tab {
    background: #181818; color: #555555;
    border: 1px solid #282828; border-bottom: none;
    padding: 10px 26px; margin-right: 3px;
    border-top-left-radius: 7px; border-top-right-radius: 7px;
    font-size: 11px; font-weight: bold; min-width: 80px;
    letter-spacing: 0.5px;
}
QTabBar::tab:hover { background: #222222; color: #999999; }
QTabBar::tab:selected {
    background: #181818; color: #ffffff;
    border-color: #333333; border-bottom: 2px solid #ff8800;
}

/* ── ComboBox ───────────────────────────────────────────── */
QComboBox {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #2a2a2a, stop:1 #1e1e1e);
    color: #999999; border: 1px solid #3a3a3a;
    border-top: 1px solid #444444; border-radius: 4px;
    padding: 5px 10px; min-height: 28px; min-width: 100px; font-size: 10px;
}
QComboBox:hover { color: #cccccc; border-color: #555555; }
QComboBox::drop-down { border: none; width: 20px; }
QComboBox::down-arrow {
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid #888888;
}
QComboBox QAbstractItemView {
    background: #1e1e1e; color: #aaaaaa;
    border: 1px solid #3a3a3a; border-radius: 4px;
    selection-background-color: #ff8800; selection-color: #ffffff;
    padding: 4px;
}
QComboBox QAbstractItemView::item { padding: 6px 10px; min-height: 26px; }

/* ── SpinBox ─────────────────────────────────────────────── */
QSpinBox, QDoubleSpinBox {
    background: #1e1e1e; color: #aaaaaa;
    border: 1px solid #3a3a3a; border-radius: 4px;
    padding: 5px 8px; min-height: 28px; font-size: 10px;
}
QSpinBox:hover, QDoubleSpinBox:hover { border-color: #555555; }
QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
    background: #2a2a2a; border: none; border-radius: 3px; width: 18px;
}
QSpinBox::up-button:hover, QSpinBox::down-button:hover { background: #ff8800; }

/* ── CheckBox ───────────────────────────────────────────── */
QCheckBox { color: #999999; spacing: 8px; padding: 4px 0; background: transparent; }
QCheckBox::indicator {
    width: 16px; height: 16px; border: 2px solid #3a3a3a;
    border-radius: 3px; background: #1a1a1a;
}
QCheckBox::indicator:hover { border-color: #ff8800; }
QCheckBox::indicator:checked { background: #ff8800; border-color: #ffaa22; }

/* ── Status / Menu bars ─────────────────────────────────── */
QStatusBar {
    background: #0a0a0a; color: #555555;
    border-top: 1px solid #1e1e1e; font-size: 10px;
    padding: 0 10px; min-height: 22px;
}
QMenuBar {
    background: #0a0a0a; color: #777777;
    border-bottom: 1px solid #1e1e1e; padding: 2px 6px; font-size: 11px;
}
QMenuBar::item { padding: 5px 12px; border-radius: 4px; background: transparent; }
QMenuBar::item:selected, QMenuBar::item:pressed {
    background: #ff8800; color: #ffffff;
}
QMenu {
    background: #1e1e1e; color: #aaaaaa;
    border: 1px solid #3a3a3a; border-radius: 6px; padding: 5px 3px;
}
QMenu::item { padding: 7px 20px; border-radius: 4px; }
QMenu::item:selected { background: #ff8800; color: #ffffff; }
QMenu::separator { height: 1px; background: #333333; margin: 3px 8px; }

/* ── Scrollbars ─────────────────────────────────────────── */
QScrollBar:vertical {
    background: #0a0a0a; width: 6px; border-radius: 3px; margin: 0;
}
QScrollBar::handle:vertical {
    background: #333333; border-radius: 3px; min-height: 20px;
}
QScrollBar::handle:vertical:hover { background: #ff8800; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none; border: none; height: 0;
}
"""


# ─────────────────────────────────────────────────────────────────────────────
#  Background widget
# ─────────────────────────────────────────────────────────────────────────────
class HardwareBackground(QWidget):
    def paintEvent(self, a0):
        p = QPainter(self)
        g = QLinearGradient(0, 0, 0, self.height())
        g.setColorAt(0.0, QColor(20, 20, 20))
        g.setColorAt(1.0, QColor(13, 13, 13))
        p.fillRect(self.rect(), g)
        super().paintEvent(a0)


# ─────────────────────────────────────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────────────────────────────────────
def _section_label(text: str) -> QLabel:
    lbl = QLabel(text.upper())
    lbl.setObjectName("sectionLabel")
    return lbl


def _panel_title(text: str) -> QLabel:
    lbl = QLabel(text.upper())
    lbl.setObjectName("panelTitle")
    return lbl


def _channel_frame() -> tuple[QFrame, QVBoxLayout]:
    f = QFrame()
    f.setObjectName("channelStrip")
    lo = QVBoxLayout(f)
    lo.setContentsMargins(10, 12, 10, 14)
    lo.setSpacing(6)
    return f, lo


def _side_frame() -> tuple[QFrame, QVBoxLayout]:
    f = QFrame()
    f.setObjectName("panelLeft")
    lo = QVBoxLayout(f)
    lo.setContentsMargins(12, 14, 12, 14)
    lo.setSpacing(8)
    return f, lo


def _card(margins=(8, 6, 8, 6), spacing=4) -> tuple[QFrame, QVBoxLayout]:
    f = QFrame()
    f.setObjectName("glassCard")
    lo = QVBoxLayout(f)
    lo.setContentsMargins(*margins)
    lo.setSpacing(spacing)
    return f, lo


def _hline() -> QFrame:
    ln = QFrame()
    ln.setFrameShape(QFrame.Shape.HLine)
    ln.setStyleSheet("background:#2a2a2a; max-height:1px; border:none;")
    return ln


def _knob_col(label: str, value=50, size=52) -> tuple[QVBoxLayout, QDial]:
    lo = QVBoxLayout()
    lo.setSpacing(2)
    knob = QDial()
    knob.setMaximum(100)
    knob.setValue(value)
    knob.setNotchesVisible(True)
    knob.setFixedSize(QSize(size, size))
    lo.addWidget(knob, alignment=Qt.AlignmentFlag.AlignCenter)
    lbl = QLabel(label)
    lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
    lo.addWidget(lbl)
    return lo, knob


def _btn(text: str, name: str, checkable=False, min_w=60, min_h=30) -> QPushButton:
    b = QPushButton(text)
    b.setObjectName(name)
    b.setCheckable(checkable)
    b.setMinimumWidth(min_w)
    b.setMinimumHeight(min_h)
    return b


class _CurvePreview(QWidget):
    """Mini crossfader curve preview drawn with QPainter."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._curve = "linear"
        self.setStyleSheet("background:#0a0a0a; border:1px solid #1e1e1e; border-radius:3px;")

    def set_curve(self, curve: str) -> None:
        self._curve = curve
        self.update()

    def paintEvent(self, _event) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        w, h = self.width(), self.height()
        p.fillRect(0, 0, w, h, QColor("#0a0a0a"))
        pen = QPen(QColor("#ff8800"), 1)
        p.setPen(pen)
        import math
        pts = []
        steps = 40
        for i in range(steps + 1):
            t = i / steps          # 0.0 → 1.0  (crossfader position)
            if self._curve == "smooth":
                v = 0.5 * (1 - math.cos(math.pi * t))   # smooth S-curve
            elif self._curve == "cut":
                v = 0.0 if t < 0.5 else 1.0             # hard cut
            else:
                v = t                                     # linear
            px = int(t * (w - 4)) + 2
            py = int((1.0 - v) * (h - 4)) + 2
            pts.append((px, py))
        for i in range(len(pts) - 1):
            p.drawLine(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1])
        p.end()


def _combo(items: list, default: str | None = None) -> QComboBox:
    cb = QComboBox()
    cb.addItems(items)
    if default:
        cb.setCurrentText(default)
    return cb


def _spinbox(value: int, lo=0, hi=9999, step=1) -> QSpinBox:
    sb = QSpinBox()
    sb.setMinimum(lo)
    sb.setMaximum(hi)
    sb.setSingleStep(step)
    sb.setValue(value)
    return sb


# ─────────────────────────────────────────────────────────────────────────────
#  Main Window
# ─────────────────────────────────────────────────────────────────────────────
class VioletDJMixer(QMainWindow):
    """Violet DJ Mixer — hardware-inspired Pioneer DJM-800/DJS-1000 UI."""

    VERSION = "2.1.0"

    # Accent colour options for Enhancement 7
    ACCENT_COLORS = {
        "Amber (Default)": "#ff8800",
        "Blue":            "#4488ff",
        "Green":           "#44cc66",
        "Red":             "#dd3333",
        "Purple":          "#aa44ff",
    }

    # Max recent tracks stored (Enhancement 1)
    MAX_RECENT = 10

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Violet DJ Mixer v{self.VERSION} — Professional Digital Mixing Board")
        self.setGeometry(100, 60, 1700, 960)
        self.setMinimumSize(1400, 800)

        # ── Runtime state ────────────────────────────────────────────────────
        self._app_dir = os.path.expanduser("~/.violet_dj")
        os.makedirs(self._app_dir, exist_ok=True)
        os.makedirs(os.path.join(self._app_dir, "sessions"), exist_ok=True)

        # Enhancement 1 – recent tracks
        self._recent_tracks: list[str] = self._load_recent_tracks()

        # Enhancement 3 – tap tempo
        self._tap_times: list[float] = []
        self._bpm_display: QLabel | None = None

        # Enhancement 5 – per-deck track labels (filled in create_mixer_panel)
        self._deck_labels: dict[int, QLabel] = {}

        # MIDI→UI control references (populated during mixer panel construction)
        # keyed by action name from ControllerManager.MAPPABLE_ACTIONS
        self._midi_controls: dict[str, QSlider | QDial | QPushButton] = {}

        # Enhancement 6 – session timer
        self._session_start = time.time()

        # Enhancement 10 – persisted config
        self._config = self._load_config()
        self._accent_color: str = self._config.get("accent_color", "#ff8800")

        # Feature 3: Track metadata cache per deck {deck: metadata_dict}
        self._deck_metadata: dict[int, dict] = {}

        # Feature 5: Loop state per deck
        self._loop_state: dict[int, dict] = {
            i: {"active": False, "in": 0.0, "out": 0.0} for i in range(1, 5)
        }

        # Feature 6: Hot cue storage {track_hash: {slot: position_seconds}}
        self._hot_cues: dict[str, dict[str, float]] = {}
        self._hot_cue_btns: dict[int, list[QPushButton]] = {}  # deck→buttons

        # Feature 7: Recorder
        self._recorder: Recorder | None = Recorder() if _HAS_REC else None  # type: ignore[misc]
        self._rec_timer = QTimer(self)
        self._rec_timer.timeout.connect(self._update_rec_display)
        self._rec_elapsed_lbl: QLabel | None = None

        # Feature 1: VU meter references {channel: VUMeter}
        self._vu_meters: dict[int, VUMeter] = {}  # type: ignore[type-arg]
        self._vu_sim_timer = QTimer(self)
        self._vu_sim_timer.timeout.connect(self._vu_simulate)
        self._vu_sim_timer.start(80)

        # Feature 2: Waveform displays per deck
        self._waveforms: dict[int, WaveformDisplay] = {}  # type: ignore[type-arg]

        # Feature 12: Per-deck BPM override labels
        self._deck_bpm: dict[int, float] = {1: 120.0, 2: 120.0, 3: 120.0, 4: 120.0}
        self._deck_bpm_spins: dict[int, QDoubleSpinBox] = {}

        # Feature 11: Keyboard shortcut map {action_name: QShortcut}
        self._shortcut_map: dict[str, QShortcut] = {}

        # Feature 10: Themes dir
        os.makedirs(os.path.join(self._app_dir, "themes"), exist_ok=True)
        os.makedirs(os.path.join(self._app_dir, "recordings"), exist_ok=True)

        self.setStyleSheet(HARDWARE_STYLESHEET)
        font = QFont()
        font.setFamilies(["Inter", "SF Pro Display", "Segoe UI", "Ubuntu"])
        font.setPointSize(10)
        self.setFont(font)

        central = HardwareBackground()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(14, 6, 14, 6)
        root.setSpacing(6)

        self.create_menu_bar()

        self.tabs = QTabWidget()
        root.addWidget(self.tabs)

        self.tabs.addTab(self.create_mixer_panel(),      "  Mixer  ")
        self.tabs.addTab(self.create_sampler_panel(),    "  Sampler  ")
        self.tabs.addTab(self.create_effects_panel(),    "  Effects  ")
        self.tabs.addTab(self.create_queue_panel(),      "  Queue  ")
        self.tabs.addTab(self.create_library_panel(),    "  Library  ")
        self.tabs.addTab(self.create_recording_panel(),  "  Record  ")
        self.tabs.addTab(self.create_device_panel(),     "  Devices  ")
        self.tabs.addTab(self.create_controller_panel(), "  Controllers  ")
        self.tabs.addTab(self.create_settings_panel(),   "  Settings  ")

        sb = self.statusBar()
        if sb:
            sb.showMessage(f"Violet DJ Mixer v{self.VERSION}  ·  Ready  ·  No devices connected")

        # Enhancement 6 – clock timer updates status bar every second
        self._clock_timer = QTimer(self)
        self._clock_timer.timeout.connect(self._update_clock)
        self._clock_timer.start(1000)

        self.device_detector = None
        self.start_device_detection()

        # Enhancement 2 – keyboard shortcuts
        self._setup_keyboard_shortcuts()

        # Wire MIDI action signals → UI controls
        self._wire_controller_actions()

        logger.info(f"Violet DJ Mixer v{self.VERSION} initialized")

    # ── Menu ────────────────────────────────────────────────────────────────
    def create_menu_bar(self):
        mb = self.menuBar()
        assert mb is not None
        fm = mb.addMenu("File")
        assert fm is not None
        fm.addAction("Open Track  [Ctrl+O]", self.open_track)
        fm.addAction("Open Playlist",        self.open_playlist)
        fm.addSeparator()

        # Enhancement 1 – Recent Files submenu
        self._recent_menu = QMenu("Recent Tracks", self)
        self._rebuild_recent_menu()
        fm.addMenu(self._recent_menu)
        fm.addSeparator()

        fm.addAction("View Session Log", self.show_session_log)
        fm.addSeparator()
        fm.addAction("Exit", self.close)

        em = mb.addMenu("Edit")
        assert em is not None
        em.addAction("Preferences",        self.show_preferences)
        em.addAction("Controller Mapping", self.show_controller_mapping)

        vm = mb.addMenu("View")
        assert vm is not None
        vm.addAction("Toggle Visualization")
        vm.addAction("Full Screen  [F11]", self._toggle_fullscreen)

        dm = mb.addMenu("Devices")
        assert dm is not None
        dm.addAction("Refresh Devices", self.refresh_devices)
        dm.addAction("Audio Settings",  self.show_audio_settings)

        hm = mb.addMenu("Help")
        assert hm is not None
        hm.addAction("Keyboard Shortcuts", self.show_shortcuts)
        hm.addAction("Documentation",      self.show_documentation)
        hm.addAction("About",              self.show_about)

    # ════════════════════════════════════════════════════════════════════════
    #  MIXER TAB  (DJM-800 style 4-channel layout)
    # ════════════════════════════════════════════════════════════════════════
    def create_mixer_panel(self) -> QWidget:
        root = QWidget()
        root.setStyleSheet("background:transparent;")
        outer = QVBoxLayout(root)
        outer.setContentsMargins(2, 4, 2, 4)
        outer.setSpacing(8)

        # ── Top row: panels + channels ─────────────────────────────────────
        top_row = QHBoxLayout()
        top_row.setSpacing(8)

        top_row.addWidget(self._create_mic_panel(), 0)

        for ch in range(1, 5):
            top_row.addWidget(self._create_channel_strip(ch), 1)

        top_row.addWidget(self._create_master_fx_panel(), 0)
        outer.addLayout(top_row, 1)

        # ── Crossfader row ─────────────────────────────────────────────────
        outer.addWidget(self._create_crossfader_row(), 0)

        return root

    def _create_mic_panel(self) -> QFrame:
        frame, lo = _side_frame()
        frame.setMaximumWidth(130)

        lo.addWidget(_panel_title("Mic"))

        for mic_name in ("MIC 1", "MIC 2"):
            lo.addWidget(_section_label(mic_name))
            knob_lo, _ = _knob_col("LEVEL", 50, 44)
            lo.addLayout(knob_lo)

        lo.addWidget(_hline())
        lo.addWidget(_panel_title("Headphones"))
        lo.addWidget(_section_label("Mixing"))
        mix_lo, _ = _knob_col("CUE ◂▸ MSTR", 50, 44)
        lo.addLayout(mix_lo)
        lo.addWidget(_section_label("Level"))
        lvl_lo, _ = _knob_col("", 70, 44)
        lo.addLayout(lvl_lo)

        lo.addStretch()

        lo.addWidget(_section_label("Sound Color FX"))
        btn_row = QGridLayout()
        btn_row.setSpacing(4)
        for i, (name, col) in enumerate([("HARM", "blue"), ("SWEEP", "blue"),
                                          ("CRUSH", "blue"), ("FILTER", "blue")]):
            b = QPushButton(name)
            b.setCheckable(True)
            b.setStyleSheet(f"""
                QPushButton {{ background:#001540; color:#4488bb;
                    border:1px solid #003060; border-radius:3px;
                    padding:5px 4px; font-size:9px; font-weight:bold; }}
                QPushButton:checked {{ background:#0055cc; color:#ffffff;
                    border-color:#0088ff; }}
                QPushButton:hover {{ border-color:#0066aa; color:#66aadd; }}
            """)
            btn_row.addWidget(b, i // 2, i % 2)
        lo.addLayout(btn_row)

        lo.addWidget(_section_label("Fader Start"))
        fs_row = QHBoxLayout()
        fs_row.setSpacing(3)
        for ch in range(1, 5):
            b = QPushButton(str(ch))
            b.setCheckable(True)
            b.setFixedSize(QSize(26, 26))
            b.setStyleSheet("""
                QPushButton { background:#7a3800; color:#cc7700;
                    border:1px solid #5a3000; border-radius:13px;
                    font-size:10px; font-weight:bold; padding:0; }
                QPushButton:checked { background:#ff8800; color:#ffffff;
                    border-color:#ffaa22; }
            """)
            fs_row.addWidget(b)
        lo.addLayout(fs_row)

        return frame

    def _create_channel_strip(self, ch: int) -> QFrame:
        frame, lo = _channel_frame()

        # Input selector
        sel = _combo(["CD/DIGITAL", "LINE", "PHONO"])
        lo.addWidget(sel)

        # Channel number
        num_lbl = QLabel(str(ch))
        num_lbl.setObjectName("channelNum")
        num_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        num_lbl.setFixedHeight(22)
        lo.addWidget(num_lbl)

        # Feature 2: Waveform display
        if _HAS_WAVE:
            wf = WaveformDisplay()
            wf.setMinimumHeight(36)
            wf.setMaximumHeight(36)
            lo.addWidget(wf)
            self._waveforms[ch] = wf

        # Enhancement 5 – track info label for this deck
        deck_lbl = QLabel("— No Track —")
        deck_lbl.setObjectName("deckTrackLabel")
        deck_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        deck_lbl.setStyleSheet(
            "color:#556677; font-size:8px; background:#0a0f14; "
            "border:1px solid #1a2530; border-radius:3px; padding:2px 4px;"
        )
        deck_lbl.setMaximumWidth(120)
        lo.addWidget(deck_lbl)
        self._deck_labels[ch] = deck_lbl

        # Feature 12: Per-deck BPM spinbox
        bpm_row = QHBoxLayout()
        bpm_row.setSpacing(3)
        bpm_row.addWidget(_section_label("BPM"))
        bpm_spin = QDoubleSpinBox()
        bpm_spin.setRange(60.0, 220.0)
        bpm_spin.setDecimals(1)
        bpm_spin.setSingleStep(0.1)
        bpm_spin.setValue(self._deck_bpm.get(ch, 120.0))
        bpm_spin.setFixedWidth(68)
        bpm_spin.setStyleSheet(
            "QDoubleSpinBox { background:#0a0a0a; color:#ff8800; "
            "border:1px solid #2a2a2a; border-radius:3px; font-size:9px; "
            "font-weight:bold; padding:1px 4px; }"
        )
        bpm_spin.valueChanged.connect(lambda v, d=ch: self._on_deck_bpm_changed(d, v))
        self._deck_bpm_spins[ch] = bpm_spin
        bpm_row.addWidget(bpm_spin)
        # Nudge buttons ±1
        for delta, sym in ((-1.0, "−"), (+1.0, "+")):
            nb = QPushButton(sym)
            nb.setFixedSize(QSize(18, 18))
            nb.setStyleSheet(
                "QPushButton { background:#1a1a1a; color:#888; border:1px solid #2e2e2e; "
                "border-radius:3px; font-size:10px; font-weight:bold; padding:0; }"
                "QPushButton:hover { background:#ff8800; color:#fff; }"
            )
            nb.clicked.connect(lambda _, d=ch, dv=delta: self._nudge_deck_bpm(d, dv))
            bpm_row.addWidget(nb)
        bpm_row.addStretch()
        lo.addLayout(bpm_row)

        lo.addWidget(_hline())

        # TRIM knob
        trim_lo, _ = _knob_col("TRIM", 60, 48)
        lo.addLayout(trim_lo)

        lo.addWidget(_hline())

        # EQ knobs — store refs for MIDI control (decks 1&2 only for A/B)
        deck_letter = "a" if ch <= 2 else "b"
        eq_lo = QVBoxLayout()
        eq_lo.setSpacing(2)
        for eq_name, eq_val in (("HI", 50), ("MID", 50), ("LOW", 50)):
            klo, eq_knob = _knob_col(eq_name, eq_val, 44)
            eq_lo.addLayout(klo)
            action_key = f"eq_{eq_name.lower()}_deck_{deck_letter}"
            self._midi_controls[action_key] = eq_knob
        lo.addLayout(eq_lo)

        lo.addWidget(_section_label("EQ"))
        lo.addWidget(_hline())

        # Feature 1: Animated VU Meter (replaces static QProgressBar)
        meter_row = QHBoxLayout()
        meter_row.setSpacing(8)

        if _HAS_VU:
            vu = VUMeter(channels=2, bar_width=7, gap=2)
            vu.setMinimumHeight(100)
            meter_row.addWidget(vu, alignment=Qt.AlignmentFlag.AlignHCenter)
            self._vu_meters[ch] = vu
        else:
            meter = QProgressBar()
            meter.setOrientation(Qt.Orientation.Vertical)
            meter.setMaximum(100)
            meter.setValue(25 + ch * 7)
            meter.setTextVisible(False)
            meter.setMaximumWidth(10)
            meter.setMinimumHeight(100)
            meter_row.addWidget(meter, alignment=Qt.AlignmentFlag.AlignHCenter)

        color_lo, _ = _knob_col("COLOR", 30, 42)
        meter_row.addLayout(color_lo)
        lo.addLayout(meter_row)

        lo.addWidget(_hline())

        # Enhancement 17 – MUTE + CUE row — store CUE for MIDI
        mute_cue_row = QHBoxLayout()
        mute_cue_row.setSpacing(4)
        mute_btn = QPushButton("MUTE")
        mute_btn.setObjectName("btnMute")
        mute_btn.setCheckable(True)
        mute_btn.setMinimumHeight(38)
        mute_btn.setStyleSheet("""
            QPushButton { background:#1a0808; color:#883333;
                border:1px solid #3a1a1a; border-radius:4px;
                font-size:9px; font-weight:bold; }
            QPushButton:checked { background:#cc2222; color:#ffffff;
                border-color:#ff4444; }
            QPushButton:hover { border-color:#993333; }
        """)
        mute_cue_row.addWidget(mute_btn, 1)

        cue_btn = _btn("CUE", "btnCue", checkable=True, min_h=38)
        self._midi_controls[f"cue_deck_{deck_letter}"] = cue_btn
        mute_cue_row.addWidget(cue_btn, 1)
        lo.addLayout(mute_cue_row)

        # Fader — store ref for MIDI volume control
        fader_wrap = QHBoxLayout()
        fader_wrap.setContentsMargins(0, 4, 0, 0)
        fader = QSlider(Qt.Orientation.Vertical)
        fader.setObjectName("channelFader")
        fader.setMaximum(100)
        fader.setValue(80)
        fader.setMinimumHeight(180)
        fader.setMaximumWidth(50)
        self._midi_controls[f"volume_deck_{deck_letter}"] = fader
        fader_wrap.addStretch()
        fader_wrap.addWidget(fader)
        fader_wrap.addStretch()
        lo.addLayout(fader_wrap)

        # Feature 5: Loop Controls
        lo.addWidget(_hline())
        lo.addWidget(_section_label("Loop"))
        loop_row1 = QHBoxLayout()
        loop_row1.setSpacing(3)
        loop_in_btn = QPushButton("IN")
        loop_in_btn.setFixedHeight(24)
        loop_in_btn.setStyleSheet("""
            QPushButton { background:#003320; color:#44cc66; border:1px solid #005530;
                border-radius:3px; font-size:9px; font-weight:bold; }
            QPushButton:hover { background:#00aa44; color:#fff; }
        """)
        loop_in_btn.clicked.connect(lambda _, d=ch: self._loop_in(d))
        loop_row1.addWidget(loop_in_btn)

        loop_out_btn = QPushButton("OUT")
        loop_out_btn.setFixedHeight(24)
        loop_out_btn.setStyleSheet("""
            QPushButton { background:#003320; color:#44cc66; border:1px solid #005530;
                border-radius:3px; font-size:9px; font-weight:bold; }
            QPushButton:hover { background:#00aa44; color:#fff; }
        """)
        loop_out_btn.clicked.connect(lambda _, d=ch: self._loop_out(d))
        loop_row1.addWidget(loop_out_btn)

        loop_active_btn = QPushButton("LOOP")
        loop_active_btn.setCheckable(True)
        loop_active_btn.setFixedHeight(24)
        loop_active_btn.setStyleSheet("""
            QPushButton { background:#1a1a1a; color:#555; border:1px solid #2e2e2e;
                border-radius:3px; font-size:9px; font-weight:bold; }
            QPushButton:checked { background:#00aa44; color:#fff; border-color:#00cc55; }
            QPushButton:hover { border-color:#44cc66; }
        """)
        loop_active_btn.toggled.connect(lambda on, d=ch: self._toggle_loop(d, on))
        loop_row1.addWidget(loop_active_btn)
        lo.addLayout(loop_row1)

        loop_size_combo = QComboBox()
        loop_size_combo.addItems(["1/8", "1/4", "1/2", "1", "2", "4", "8"])
        loop_size_combo.setCurrentText("1")
        loop_size_combo.setFixedHeight(22)
        loop_size_combo.setStyleSheet(
            "QComboBox { background:#0a0a0a; color:#aaa; border:1px solid #2a2a2a; "
            "border-radius:3px; font-size:9px; padding:1px 4px; }"
        )
        lo.addWidget(loop_size_combo)

        # Crossfade assign
        lo.addWidget(_section_label("CF Assign"))
        assign_row = QHBoxLayout()
        assign_row.setSpacing(4)
        for label in ("A", "THRU", "B"):
            b = QPushButton(label)
            b.setCheckable(True)
            b.setStyleSheet("""
                QPushButton { background:#1a1a1a; color:#555555;
                    border:1px solid #2e2e2e; border-radius:3px;
                    padding:3px 5px; font-size:9px; font-weight:bold; }
                QPushButton:checked { background:#ff8800; color:#ffffff;
                    border-color:#ffaa22; }
            """)
            if label == "THRU":
                b.setChecked(True)
            assign_row.addWidget(b)
        lo.addLayout(assign_row)

        return frame

    def _create_master_fx_panel(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("panelRight")
        frame.setMaximumWidth(210)
        lo = QVBoxLayout(frame)
        lo.setContentsMargins(12, 14, 12, 14)
        lo.setSpacing(8)

        # Effects LCD display
        lo.addWidget(_panel_title("Effect Select"))
        ef_lbl = QLabel("FLANGER")
        ef_lbl.setObjectName("effectName")
        ef_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lo.addWidget(ef_lbl)

        # CH select row
        lo.addWidget(_section_label("CH Select"))
        ch_row = QGridLayout()
        ch_row.setSpacing(3)
        for i, txt in enumerate(["1","2","3","4","MIC","A","B","MST"]):
            b = QPushButton(txt)
            b.setCheckable(True)
            b.setFixedSize(QSize(34, 24))
            b.setStyleSheet("""
                QPushButton { background:#1a1a1a; color:#555555;
                    border:1px solid #2e2e2e; border-radius:3px;
                    font-size:9px; font-weight:bold; padding:0; }
                QPushButton:checked { background:#2244aa; color:#ffffff;
                    border-color:#4466cc; }
            """)
            if txt == "1":
                b.setChecked(True)
            ch_row.addWidget(b, i // 4, i % 4)
        lo.addLayout(ch_row)

        lo.addWidget(_section_label("Parameter"))
        param_slider = QSlider(Qt.Orientation.Horizontal)
        param_slider.setMaximum(100)
        param_slider.setValue(60)
        lo.addWidget(param_slider)

        lo.addWidget(_hline())

        # Enhancement 3 – BPM with tap tempo wiring
        lo.addWidget(_section_label("BPM"))
        bpm_lbl = QLabel("120.0")
        bpm_lbl.setObjectName("bpmValue")
        bpm_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lo.addWidget(bpm_lbl)
        self._bpm_display = bpm_lbl  # store reference for tap updates

        ms_lbl = QLabel("500 ms")
        ms_lbl.setObjectName("msValue")
        ms_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lo.addWidget(ms_lbl)
        self._ms_display = ms_lbl

        # Beat arrows
        beat_row = QHBoxLayout()
        beat_row.setSpacing(4)
        for t in ("◀", "BEAT", "▶"):
            b = QPushButton(t)
            b.setStyleSheet("""
                QPushButton { background:#1a1a1a; color:#888888;
                    border:1px solid #2e2e2e; border-radius:3px;
                    padding:4px 8px; font-size:10px; }
                QPushButton:hover { background:#ff8800; color:#fff; }
            """)
            beat_row.addWidget(b)
        lo.addLayout(beat_row)

        lo.addWidget(_hline())

        # TAP + CUE — wire TAP to Enhancement 3 handler
        tap_cue_row = QHBoxLayout()
        tap_cue_row.setSpacing(8)
        tap_btn = _btn("TAP", "btnTap", min_w=56, min_h=56)
        tap_btn.clicked.connect(self._on_tap_tempo)
        cue_btn = _btn("CUE", "btnCue", checkable=True, min_w=56, min_h=56)
        tap_cue_row.addStretch()
        tap_cue_row.addWidget(tap_btn)
        tap_cue_row.addWidget(cue_btn)
        tap_cue_row.addStretch()
        lo.addLayout(tap_cue_row)

        lo.addWidget(_hline())

        # Master fader
        lo.addWidget(_panel_title("Master"))
        master_row = QHBoxLayout()
        master_row.setSpacing(8)

        master_fader = QSlider(Qt.Orientation.Vertical)
        master_fader.setObjectName("masterFader")
        master_fader.setMaximum(100)
        master_fader.setValue(80)
        master_fader.setMinimumHeight(120)
        master_row.addStretch()
        master_row.addWidget(master_fader)
        self._midi_controls["master_volume"] = master_fader

        right_knobs = QVBoxLayout()
        right_knobs.setSpacing(4)
        for label in ("BALANCE", "BOOTH"):
            klo, _ = _knob_col(label, 50, 40)
            right_knobs.addLayout(klo)
        master_row.addLayout(right_knobs)
        master_row.addStretch()
        lo.addLayout(master_row)

        lo.addWidget(_hline())

        # Feature 9: Master EQ — 5-band graphic
        lo.addWidget(_section_label("Master EQ"))
        eq_bands = [("32", 32), ("250", 250), ("1k", 1000), ("4k", 4000), ("16k", 16000)]
        self._master_eq_sliders: dict[str, QSlider] = {}
        eq_row = QHBoxLayout()
        eq_row.setSpacing(4)
        for band_name, _ in eq_bands:
            col = QVBoxLayout()
            col.setSpacing(2)
            sl = QSlider(Qt.Orientation.Vertical)
            sl.setRange(-12, 12)
            sl.setValue(0)
            sl.setFixedHeight(60)
            sl.setFixedWidth(18)
            sl.setStyleSheet("""
                QSlider::groove:vertical { width:3px; background:#0a0a0a;
                    border:1px solid #1a1a1a; border-radius:1px; }
                QSlider::handle:vertical { background:#888; border:1px solid #aaa;
                    height:8px; width:14px; margin:0 -5px; border-radius:2px; }
                QSlider::sub-page:vertical { background:#ff8800; border-radius:1px; }
                QSlider::add-page:vertical { background:#ff8800; border-radius:1px; }
            """)
            val_lbl = QLabel("0")
            val_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            val_lbl.setStyleSheet("font-size:7px; color:#666; background:transparent;")
            sl.valueChanged.connect(lambda v, l=val_lbl: l.setText(str(v)))
            self._master_eq_sliders[band_name] = sl
            col.addWidget(sl, alignment=Qt.AlignmentFlag.AlignHCenter)
            col.addWidget(val_lbl)
            bnd_lbl = QLabel(band_name)
            bnd_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            bnd_lbl.setStyleSheet("font-size:7px; color:#555; background:transparent;")
            col.addWidget(bnd_lbl)
            eq_row.addLayout(col)
        lo.addLayout(eq_row)

        # ON/OFF
        onoff_row = QHBoxLayout()
        onoff_row.addStretch()
        onoff_btn = _btn("ON/OFF", "btnOnOff", checkable=True, min_w=56, min_h=56)
        onoff_row.addWidget(onoff_btn)
        onoff_row.addStretch()
        lo.addLayout(onoff_row)

        return frame

    def _create_crossfader_row(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("crossfaderPanel")
        frame.setMaximumHeight(70)
        lo = QHBoxLayout(frame)
        lo.setContentsMargins(20, 10, 20, 10)
        lo.setSpacing(14)

        a_lbl = QLabel("《  A")
        a_lbl.setStyleSheet("color:#ff8800; font-size:13px; font-weight:bold; background:transparent;")
        lo.addWidget(a_lbl)

        xfader = QSlider(Qt.Orientation.Horizontal)
        xfader.setObjectName("crossfader")
        xfader.setMaximum(100)
        xfader.setValue(50)
        lo.addWidget(xfader, 1)
        self._midi_controls["crossfader"] = xfader

        b_lbl = QLabel("B  》")
        b_lbl.setStyleSheet("color:#ff8800; font-size:13px; font-weight:bold; background:transparent;")
        lo.addWidget(b_lbl)

        lo.addSpacing(20)
        lo.addWidget(_section_label("Curve"))
        self._xfade_curve = "linear"   # Feature 8 state
        curve_btns = []
        for shape, curve_id in (("⌒", "smooth"), ("—", "linear"), ("⌓", "cut")):
            b = QPushButton(shape)
            b.setCheckable(True)
            b.setChecked(curve_id == "linear")
            b.setFixedSize(QSize(28, 28))
            b.setStyleSheet("""
                QPushButton { background:#1a1a1a; color:#555; border:1px solid #2e2e2e;
                    border-radius:3px; font-size:12px; }
                QPushButton:checked { color:#ff8800; border-color:#ff8800; }
            """)
            b.clicked.connect(lambda _, cid=curve_id: self._set_xfade_curve(cid))
            b.setProperty("curveId", curve_id)
            curve_btns.append(b)
            lo.addWidget(b)
        self._xfade_curve_btns = curve_btns

        # Feature 8: mini curve preview (QPainter inline widget)
        self._curve_preview = _CurvePreview()
        self._curve_preview.setFixedSize(QSize(50, 40))
        lo.addWidget(self._curve_preview)

        return frame

    # ════════════════════════════════════════════════════════════════════════
    #  SAMPLER TAB  (DJS-1000 style)
    # ════════════════════════════════════════════════════════════════════════
    def create_sampler_panel(self) -> QWidget:
        root = QWidget()
        root.setStyleSheet("background:transparent;")
        lo = QHBoxLayout(root)
        lo.setContentsMargins(4, 4, 4, 4)
        lo.setSpacing(10)

        # ── Left controls ────────────────────────────────────────────────
        left, left_lo = _side_frame()
        left.setMaximumWidth(150)

        left_lo.addWidget(_panel_title("FX"))
        left_lo.addWidget(_section_label("Level / Depth"))
        lklo, _ = _knob_col("", 60, 50)
        left_lo.addLayout(lklo)

        onoff = _btn("ON/OFF", "btnOnOff", checkable=True, min_w=56, min_h=56)
        left_lo.addWidget(onoff, alignment=Qt.AlignmentFlag.AlignCenter)

        left_lo.addWidget(_hline())
        left_lo.addWidget(_section_label("Controls"))

        for name, obj in (("SHIFT", "btnShift"), ("REC/UNDO", "btnRec"),
                          ("STOP/GATE", "btnStop")):
            b = _btn(name, obj, checkable=(obj != "btnShift"), min_h=32)
            if obj == "btnRec":
                b.setStyleSheet("""
                    QPushButton { background:#2a0000; color:#aa3333;
                        border:1px solid #3a0000; border-radius:4px;
                        font-size:10px; font-weight:bold; min-height:32px; }
                    QPushButton:checked { background:#cc2222; color:#fff;
                        border-color:#ff3333; }
                """)
            left_lo.addWidget(b)

        left_lo.addWidget(_hline())

        play_btn = _btn("▶ PLAY/PAUSE", "btnPlay", checkable=True, min_h=44)
        left_lo.addWidget(play_btn)

        left_lo.addStretch()
        lo.addWidget(left)

        # ── Centre: mode bar + 4×4 pads + hot cues ───────────────────────
        centre = QWidget()
        centre.setStyleSheet("background:transparent;")
        centre_lo = QVBoxLayout(centre)
        centre_lo.setSpacing(8)
        centre_lo.setContentsMargins(0, 0, 0, 0)

        # Mode bar
        mode_frame = QFrame()
        mode_frame.setObjectName("glassCard")
        mode_frame.setMaximumHeight(50)
        mode_lo = QHBoxLayout(mode_frame)
        mode_lo.setContentsMargins(10, 6, 10, 6)
        mode_lo.setSpacing(8)
        mode_lo.addWidget(_section_label("Mode"))
        for mode in ("PITCH", "REPEAT", "USER1", "USER2"):
            b = QPushButton(mode)
            b.setCheckable(True)
            b.setStyleSheet("""
                QPushButton { background:#1a1a1a; color:#555555;
                    border:1px solid #2e2e2e; border-radius:4px;
                    padding:6px 14px; font-size:10px; font-weight:bold; }
                QPushButton:checked { background:#2a2a2a; color:#ffffff;
                    border-color:#ff8800; }
                QPushButton:hover { color:#aaaaaa; }
            """)
            mode_lo.addWidget(b)
        mode_lo.addStretch()
        for mode in ("MUTE", "HOT SLICE", "SLICE", "SCALE"):
            b = QPushButton(mode)
            b.setCheckable(True)
            b.setStyleSheet("""
                QPushButton { background:#1a1a1a; color:#666666;
                    border:1px solid #2e2e2e; border-radius:4px;
                    padding:6px 14px; font-size:10px; font-weight:bold; }
                QPushButton:checked { background:#2a2a2a; color:#ffffff;
                    border-color:#ff8800; }
                QPushButton:hover { color:#aaaaaa; }
            """)
            mode_lo.addWidget(b)
        centre_lo.addWidget(mode_frame)

        # 4×4 performance pad grid
        PAD_COLORS = [
            # row 4 (top) — pinks/purples
            "fuchsia", "magenta", "rose", "pink",
            # row 3 — blues/purples
            "sky", "blue", "purple", "violet",
            # row 2 — greens
            "lime", "green", "teal", "mint",
            # row 1 (bottom) — reds/oranges
            "orange_red", "orange", "amber", "yellow",
        ]
        pad_frame = QFrame()
        pad_frame.setObjectName("glassCard")
        pad_grid = QGridLayout(pad_frame)
        pad_grid.setSpacing(6)
        pad_grid.setContentsMargins(12, 12, 12, 12)
        for idx in range(16):
            row, col = 3 - (idx // 4), idx % 4
            pad_no = (3 - row) * 4 + col + 1
            btn = QPushButton(str(pad_no))
            btn.setObjectName("pad")
            btn.setProperty("padColor", PAD_COLORS[idx])
            btn.setCheckable(True)
            btn.setMinimumSize(QSize(70, 70))
            pad_grid.addWidget(btn, row, col)
        centre_lo.addWidget(pad_frame, 1)

        # Hot cue strips
        HOT_COLORS_1 = ["green","teal","sky","blue","amber","orange","rose","purple"]
        HOT_COLORS_2 = ["lime","mint","violet","fuchsia","yellow","orange_red","magenta","pink"]
        for strip_colors in (HOT_COLORS_1, HOT_COLORS_2):
            strip_frame = QFrame()
            strip_frame.setObjectName("glassCard")
            strip_lo = QHBoxLayout(strip_frame)
            strip_lo.setSpacing(4)
            strip_lo.setContentsMargins(8, 6, 8, 6)
            strip_lo.addStretch()
            for i, pad_color in enumerate(strip_colors):
                btn = QPushButton(str(i + 1 if strip_colors == HOT_COLORS_1 else i + 9))
                btn.setObjectName("hotCue")
                btn.setProperty("padColor", pad_color)
                btn.setCheckable(True)
                btn.setMinimumSize(QSize(40, 34))
                btn.setMaximumSize(QSize(52, 40))
                strip_lo.addWidget(btn)
            strip_lo.addStretch()
            centre_lo.addWidget(strip_frame)

        lo.addWidget(centre, 1)

        # ── Right: Tempo controls ────────────────────────────────────────
        right, right_lo = _side_frame()
        right.setMaximumWidth(160)
        right.setObjectName("panelRight")

        right_lo.addWidget(_panel_title("Beat Sync"))
        sync_row = QHBoxLayout()
        sync_row.setSpacing(6)
        sync_btn   = _btn("SYNC",   "btnSync",   min_w=52, min_h=32)
        master_btn = _btn("MASTER", "btnMaster", min_w=52, min_h=32)
        sync_row.addWidget(sync_btn)
        sync_row.addWidget(master_btn)
        right_lo.addLayout(sync_row)

        right_lo.addWidget(_hline())
        right_lo.addWidget(_panel_title("Tempo"))
        right_lo.addWidget(_section_label("±6 / ±10 / ±16 / WIDE"))

        tempo_fader = QSlider(Qt.Orientation.Vertical)
        tempo_fader.setObjectName("tempoFader")
        tempo_fader.setMinimum(-50)
        tempo_fader.setMaximum(50)
        tempo_fader.setValue(0)
        tempo_fader.setMinimumHeight(200)
        right_lo.addWidget(tempo_fader, alignment=Qt.AlignmentFlag.AlignHCenter)

        right_lo.addWidget(_section_label("Tempo Reset"))
        reset_btn = QPushButton("RESET")
        reset_btn.setStyleSheet("""
            QPushButton { background:#1a1a1a; color:#888888;
                border:1px solid #2e2e2e; border-radius:4px;
                padding:5px 12px; font-size:10px; font-weight:bold; }
            QPushButton:hover { background:#ff8800; color:#ffffff; }
        """)
        right_lo.addWidget(reset_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

        right_lo.addWidget(_hline())
        right_lo.addWidget(_section_label("Nudge"))
        nudge_row = QHBoxLayout()
        nudge_row.setSpacing(6)
        for sym in ("−", "+"):
            b = QPushButton(sym)
            b.setFixedSize(QSize(36, 36))
            b.setStyleSheet("""
                QPushButton { background:#1e1e1e; color:#aaaaaa;
                    border:1px solid #3a3a3a; border-radius:18px;
                    font-size:16px; font-weight:bold; }
                QPushButton:hover { background:#ff8800; color:#ffffff; }
            """)
            nudge_row.addWidget(b)
        right_lo.addLayout(nudge_row)

        right_lo.addWidget(_hline())
        right_lo.addWidget(_section_label("Channel"))
        ch_row_r = QGridLayout()
        ch_row_r.setSpacing(4)
        for i in range(1, 5):
            b = QPushButton(str(i))
            b.setCheckable(True)
            b.setFixedSize(QSize(32, 32))
            b.setStyleSheet("""
                QPushButton { background:#001030; color:#3355aa;
                    border:2px solid #1a2a4a; border-radius:3px;
                    font-size:11px; font-weight:bold; }
                QPushButton:checked { background:#0044cc; color:#ffffff;
                    border-color:#2266ee; }
            """)
            ch_row_r.addWidget(b, 0, i - 1)
        right_lo.addLayout(ch_row_r)

        right_lo.addStretch()
        lo.addWidget(right)

        return root

    # ════════════════════════════════════════════════════════════════════════
    #  EFFECTS TAB  —  Enhancement 18: Effects Chain Panel
    # ════════════════════════════════════════════════════════════════════════

    _EFFECT_DEFS = [
        ("Echo",       "delay/repeat",   "#004455"),
        ("Reverb",     "room/space",     "#003344"),
        ("Chorus",     "shimmer/width",  "#002244"),
        ("Flanger",    "sweep/comb",     "#001133"),
        ("Phaser",     "phase shift",    "#220044"),
        ("Distortion", "overdrive/clip", "#330000"),
        ("Filter",     "cutoff/resonance","#003300"),
        ("Delay",      "multi-tap",      "#002233"),
    ]

    def create_effects_panel(self) -> QWidget:
        root = QWidget()
        root.setStyleSheet("background:transparent;")
        outer = QHBoxLayout(root)
        outer.setContentsMargins(4, 4, 4, 4)
        outer.setSpacing(8)

        # ── Left: chain list ─────────────────────────────────────────────
        chain_frame = QFrame()
        chain_frame.setObjectName("panelLeft")
        chain_frame.setMaximumWidth(220)
        chain_lo = QVBoxLayout(chain_frame)
        chain_lo.setContentsMargins(10, 10, 10, 10)
        chain_lo.setSpacing(6)
        chain_lo.addWidget(_panel_title("FX Chain  (A → B)"))

        self._fx_chain_list = QListWidget()
        self._fx_chain_list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self._fx_chain_list.setDefaultDropAction(Qt.DropAction.MoveAction)
        self._fx_chain_list.setStyleSheet("""
            QListWidget { background:#0d0d0d; color:#aaaaaa;
                border:1px solid #2a2a2a; font-size:10px; }
            QListWidget::item { padding:6px 8px; border-bottom:1px solid #1a1a1a; }
            QListWidget::item:selected { background:#1a3050; color:#fff; }
        """)
        self._fx_chain_list.currentRowChanged.connect(self._fx_chain_selection_changed)
        chain_lo.addWidget(self._fx_chain_list)

        chain_btn_row = QHBoxLayout()
        chain_btn_row.setSpacing(4)
        for txt, slot in (("▲", self._fx_chain_move_up),
                          ("▼", self._fx_chain_move_down),
                          ("✕", self._fx_chain_remove)):
            b = QPushButton(txt)
            b.setFixedSize(QSize(28, 28))
            b.clicked.connect(slot)
            chain_btn_row.addWidget(b)
        chain_btn_row.addStretch()
        chain_lo.addLayout(chain_btn_row)
        outer.addWidget(chain_frame)

        # ── Centre: available effects to add ─────────────────────────────
        lib_frame = QFrame()
        lib_frame.setObjectName("panelLeft")
        lib_frame.setMaximumWidth(200)
        lib_lo = QVBoxLayout(lib_frame)
        lib_lo.setContentsMargins(10, 10, 10, 10)
        lib_lo.setSpacing(6)
        lib_lo.addWidget(_panel_title("Effect Library"))

        for name, hint, _ in self._EFFECT_DEFS:
            add_btn = QPushButton(f"  + {name}")
            add_btn.setStyleSheet(
                "QPushButton { background:#111; color:#aaa; border:1px solid #2a2a2a; "
                "border-radius:3px; text-align:left; padding:5px 8px; font-size:10px; }"
                "QPushButton:hover { background:#1a1a1a; color:#fff; }"
            )
            add_btn.setProperty("effectName", name)
            add_btn.clicked.connect(lambda _checked, n=name: self._fx_chain_add(n))
            lib_lo.addWidget(add_btn)
        lib_lo.addStretch()
        outer.addWidget(lib_frame)

        # ── Right: parameter editor for selected chain effect ─────────────
        param_frame = QFrame()
        param_frame.setObjectName("panelLeft")
        param_lo = QVBoxLayout(param_frame)
        param_lo.setContentsMargins(16, 14, 16, 14)
        param_lo.setSpacing(10)

        self._fx_param_title = QLabel("— Select an effect —")
        self._fx_param_title.setObjectName("effectName")
        self._fx_param_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        param_lo.addWidget(self._fx_param_title)

        self._fx_enabled_chk = QCheckBox("Enabled")
        self._fx_enabled_chk.setChecked(True)
        param_lo.addWidget(self._fx_enabled_chk)

        param_lo.addWidget(_hline())

        param_defs = [
            ("Mix",       0, 100, 50),
            ("Time / Rate", 0, 100, 35),
            ("Depth",     0, 100, 60),
            ("Feedback",  0, 100, 30),
            ("Wet / Dry", 0, 100, 50),
        ]
        self._fx_param_sliders: dict[str, QSlider] = {}
        for p_name, p_min, p_max, p_val in param_defs:
            row = QHBoxLayout()
            lbl = QLabel(p_name)
            lbl.setMinimumWidth(90)
            row.addWidget(lbl)
            sl = QSlider(Qt.Orientation.Horizontal)
            sl.setMinimum(p_min)
            sl.setMaximum(p_max)
            sl.setValue(p_val)
            sl.setMinimumWidth(160)
            row.addWidget(sl)
            val_lbl = QLabel(str(p_val))
            val_lbl.setMinimumWidth(28)
            val_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            sl.valueChanged.connect(lambda v, l=val_lbl: l.setText(str(v)))
            row.addWidget(val_lbl)
            param_lo.addLayout(row)
            self._fx_param_sliders[p_name] = sl

        param_lo.addWidget(_hline())

        # E19 – BPM sync indicator inside FX panel
        sync_row = QHBoxLayout()
        sync_row.addWidget(_section_label("BPM Sync:"))
        self._sync_badge = QLabel("● NOT SYNCED")
        self._sync_badge.setStyleSheet(
            "color:#884422; font-size:10px; font-weight:bold; background:transparent;"
        )
        sync_row.addWidget(self._sync_badge)
        sync_row.addStretch()
        sync_toggle = QPushButton("Sync Decks")
        sync_toggle.setCheckable(True)
        sync_toggle.toggled.connect(self._fx_toggle_sync)
        sync_row.addWidget(sync_toggle)
        param_lo.addLayout(sync_row)

        param_lo.addStretch()
        outer.addWidget(param_frame, 1)

        return root

    def _fx_chain_add(self, name: str):
        self._fx_chain_list.addItem(f"◆  {name}")
        self._fx_chain_list.setCurrentRow(self._fx_chain_list.count() - 1)

    @pyqtSlot()
    def _fx_chain_move_up(self):
        row = self._fx_chain_list.currentRow()
        if row > 0:
            item = self._fx_chain_list.takeItem(row)
            self._fx_chain_list.insertItem(row - 1, item)
            self._fx_chain_list.setCurrentRow(row - 1)

    @pyqtSlot()
    def _fx_chain_move_down(self):
        row = self._fx_chain_list.currentRow()
        if 0 <= row < self._fx_chain_list.count() - 1:
            item = self._fx_chain_list.takeItem(row)
            self._fx_chain_list.insertItem(row + 1, item)
            self._fx_chain_list.setCurrentRow(row + 1)

    @pyqtSlot()
    def _fx_chain_remove(self):
        row = self._fx_chain_list.currentRow()
        if row >= 0:
            self._fx_chain_list.takeItem(row)

    @pyqtSlot(int)
    def _fx_chain_selection_changed(self, row: int):
        if row < 0:
            return
        item = self._fx_chain_list.item(row)
        if item:
            name = item.text().replace("◆  ", "").strip()
            self._fx_param_title.setText(name)

    # E19 – BPM sync badge toggle
    @pyqtSlot(bool)
    def _fx_toggle_sync(self, synced: bool):
        if synced:
            self._sync_badge.setText("● SYNCED")
            self._sync_badge.setStyleSheet(
                "color:#44cc66; font-size:10px; font-weight:bold; background:transparent;"
            )
        else:
            self._sync_badge.setText("● NOT SYNCED")
            self._sync_badge.setStyleSheet(
                "color:#884422; font-size:10px; font-weight:bold; background:transparent;"
            )
        logger.info(f"BPM sync: {'on' if synced else 'off'}")

    # ════════════════════════════════════════════════════════════════════════
    #  DEVICES TAB
    # ════════════════════════════════════════════════════════════════════════
    def create_device_panel(self) -> QWidget:
        root = QWidget()
        root.setStyleSheet("background:transparent;")
        lo = QVBoxLayout(root)
        lo.setContentsMargins(4, 4, 4, 4)
        lo.setSpacing(10)

        panel = QFrame()
        panel.setObjectName("panelLeft")
        panel_lo = QVBoxLayout(panel)
        panel_lo.setContentsMargins(16, 14, 16, 14)
        panel_lo.setSpacing(10)

        panel_lo.addWidget(_panel_title("Connected Devices"))

        dev_list = QLabel("Scanning for devices…")
        dev_list.setObjectName("deviceList")
        dev_list.setMinimumHeight(180)
        dev_list.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        panel_lo.addWidget(dev_list)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        for t in ("Refresh", "Remove Selected", "Configure"):
            btn_row.addWidget(QPushButton(t))
        btn_row.addStretch()
        panel_lo.addLayout(btn_row)

        panel_lo.addWidget(_panel_title("Device Details"))
        details = QLabel("Select a device to view details")
        details.setObjectName("deviceDetails")
        details.setMinimumHeight(120)
        details.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        panel_lo.addWidget(details)

        lo.addWidget(panel)
        lo.addStretch()
        return root

    # ════════════════════════════════════════════════════════════════════════
    #  CONTROLLERS TAB  (E14 · E15 · E16 · E20)
    # ════════════════════════════════════════════════════════════════════════
    def create_controller_panel(self) -> QWidget:
        root = QWidget()
        root.setStyleSheet("background:transparent;")
        root_lo = QVBoxLayout(root)
        root_lo.setContentsMargins(4, 4, 4, 4)
        root_lo.setSpacing(8)

        # ── Top bar: port selector + actions ─────────────────────────────
        top_frame = QFrame()
        top_frame.setObjectName("glassCard")
        top_lo = QHBoxLayout(top_frame)
        top_lo.setContentsMargins(12, 8, 12, 8)
        top_lo.setSpacing(8)

        top_lo.addWidget(_section_label("MIDI Port:"))
        self._ctrl_port_combo = QComboBox()
        self._ctrl_port_combo.setMinimumWidth(220)
        self._ctrl_port_combo.setStyleSheet(
            "QComboBox { background:#0d0d0d; color:#cccccc; border:1px solid #2a2a2a; "
            "border-radius:3px; padding:3px 6px; }"
        )
        top_lo.addWidget(self._ctrl_port_combo)

        detect_btn = QPushButton("Detect")
        detect_btn.setFixedWidth(70)
        detect_btn.clicked.connect(self._ctrl_detect_ports)
        top_lo.addWidget(detect_btn)

        connect_btn = QPushButton("Connect")
        connect_btn.setFixedWidth(70)
        connect_btn.clicked.connect(self._ctrl_connect)
        top_lo.addWidget(connect_btn)

        top_lo.addSpacing(16)
        top_lo.addWidget(_section_label("Preset:"))
        self._preset_combo = QComboBox()
        self._preset_combo.setMinimumWidth(180)
        self._preset_combo.addItem("— load preset —")
        self._preset_combo.addItems(list(self._ctrl_manager().BUILTIN_PRESETS.keys()))
        self._preset_combo.setStyleSheet(
            "QComboBox { background:#0d0d0d; color:#cccccc; border:1px solid #2a2a2a; "
            "border-radius:3px; padding:3px 6px; }"
        )
        top_lo.addWidget(self._preset_combo)

        load_preset_btn = QPushButton("Load")
        load_preset_btn.setFixedWidth(55)
        load_preset_btn.clicked.connect(self._ctrl_load_preset)
        top_lo.addWidget(load_preset_btn)

        top_lo.addStretch()

        # Enhancement 16 – MIDI Learn toggle
        self._learn_btn = QPushButton("MIDI Learn")
        self._learn_btn.setCheckable(True)
        self._learn_btn.setFixedWidth(90)
        self._learn_btn.setStyleSheet("""
            QPushButton { background:#1a1a1a; color:#888888;
                border:1px solid #333; border-radius:4px; padding:5px; }
            QPushButton:checked { background:#cc5500; color:#ffffff;
                border-color:#ff6600; }
        """)
        self._learn_btn.toggled.connect(self._ctrl_toggle_learn)
        top_lo.addWidget(self._learn_btn)

        root_lo.addWidget(top_frame)

        # ── Splitter: mapping table (left) + action picker (right) ───────
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Mapping table – E14
        table_frame = QFrame()
        table_frame.setObjectName("panelLeft")
        table_lo = QVBoxLayout(table_frame)
        table_lo.setContentsMargins(10, 10, 10, 10)
        table_lo.setSpacing(6)
        table_lo.addWidget(_panel_title("MIDI Mappings  (CC → Action)"))

        self._mapping_table = QTableWidget(0, 3)
        self._mapping_table.setHorizontalHeaderLabels(["CC", "Action", "Controller"])
        self._mapping_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self._mapping_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self._mapping_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self._mapping_table.setAlternatingRowColors(True)
        self._mapping_table.setStyleSheet("""
            QTableWidget {
                background:#0d0d0d; color:#cccccc;
                border:1px solid #2a2a2a; gridline-color:#1a1a1a;
                font-size:10px;
            }
            QTableWidget::item:selected { background:#1a3050; color:#ffffff; }
            QTableWidget::item:alternate { background:#111111; }
            QHeaderView::section {
                background:#1a1a1a; color:#888888; border:none;
                border-bottom:1px solid #2a2a2a; padding:4px;
                font-size:9px; font-weight:bold; letter-spacing:1px;
            }
        """)
        table_lo.addWidget(self._mapping_table)

        map_btn_row = QHBoxLayout()
        map_btn_row.setSpacing(6)
        add_map_btn = QPushButton("+ Add Row")
        add_map_btn.clicked.connect(self._ctrl_add_mapping_row)
        map_btn_row.addWidget(add_map_btn)
        del_map_btn = QPushButton("Remove")
        del_map_btn.clicked.connect(self._ctrl_remove_mapping_row)
        map_btn_row.addWidget(del_map_btn)
        clear_map_btn = QPushButton("Clear All")
        clear_map_btn.clicked.connect(self._ctrl_clear_mappings)
        map_btn_row.addWidget(clear_map_btn)
        map_btn_row.addStretch()
        save_prof_btn = QPushButton("Save Profile")
        save_prof_btn.clicked.connect(self._ctrl_save_profile)
        map_btn_row.addWidget(save_prof_btn)
        load_prof_btn = QPushButton("Load Profile")
        load_prof_btn.clicked.connect(self._ctrl_load_profile)
        map_btn_row.addWidget(load_prof_btn)
        table_lo.addLayout(map_btn_row)

        splitter.addWidget(table_frame)

        # Action list – E15 (right pane)
        action_frame = QFrame()
        action_frame.setObjectName("panelLeft")
        action_frame.setMaximumWidth(260)
        action_lo = QVBoxLayout(action_frame)
        action_lo.setContentsMargins(10, 10, 10, 10)
        action_lo.setSpacing(6)
        action_lo.addWidget(_panel_title("Available Actions"))

        self._action_list = QListWidget()
        self._action_list.setStyleSheet("""
            QListWidget { background:#0d0d0d; color:#aaaaaa;
                border:1px solid #2a2a2a; font-size:10px; }
            QListWidget::item:selected { background:#1a3050; color:#fff; }
            QListWidget::item:hover { background:#141414; }
        """)
        from src.controllers.manager import ControllerManager as _CM
        for action in _CM.MAPPABLE_ACTIONS:
            self._action_list.addItem(QListWidgetItem(action))
        action_lo.addWidget(self._action_list)

        # MIDI Learn status label
        self._learn_status_lbl = QLabel("Select an action, then press MIDI Learn\nand move a knob/fader on your controller.")
        self._learn_status_lbl.setStyleSheet(
            "color:#556677; font-size:9px; background:transparent; padding:4px;"
        )
        self._learn_status_lbl.setWordWrap(True)
        action_lo.addWidget(self._learn_status_lbl)

        splitter.addWidget(action_frame)
        splitter.setSizes([700, 260])

        root_lo.addWidget(splitter, 1)

        # Populate ports immediately
        self._ctrl_detect_ports()
        return root

    def _ctrl_manager(self):
        """Lazy-init and cache ControllerManager."""
        if not hasattr(self, "_controller_manager"):
            from src.controllers.manager import ControllerManager
            self._controller_manager = ControllerManager()
        return self._controller_manager

    # E15 – detect ports
    @pyqtSlot()
    def _ctrl_detect_ports(self):
        mgr = self._ctrl_manager()
        ports = mgr.list_available_controllers()
        self._ctrl_port_combo.clear()
        if ports:
            self._ctrl_port_combo.addItems(ports)
        else:
            self._ctrl_port_combo.addItem("No MIDI devices found")
        logger.info(f"Controller ports refreshed: {ports}")

    # E15 – connect selected port
    @pyqtSlot()
    def _ctrl_connect(self):
        port = self._ctrl_port_combo.currentText()
        if not port or port == "No MIDI devices found":
            return
        mgr = self._ctrl_manager()
        ok = mgr.connect_controller(port)
        sb = self.statusBar()
        if sb:
            sb.showMessage(f"{'Connected to' if ok else 'Failed to connect:'} {port}", 4000)

    # E20 – load built-in preset into table
    @pyqtSlot()
    def _ctrl_load_preset(self):
        name = self._preset_combo.currentText()
        if name.startswith("—"):
            return
        mgr = self._ctrl_manager()
        mgr.load_builtin_preset(name, controller_id="default")
        self._refresh_mapping_table("default")
        sb = self.statusBar()
        if sb:
            sb.showMessage(f"Preset loaded: {name}", 3000)

    # E14 – populate table from manager mappings
    def _refresh_mapping_table(self, controller_id: str = "default"):
        mgr = self._ctrl_manager()
        mappings = mgr.get_mappings(controller_id)
        self._mapping_table.setRowCount(0)
        for cc, action in sorted(mappings.items(), key=lambda x: int(x[0])):
            row = self._mapping_table.rowCount()
            self._mapping_table.insertRow(row)
            self._mapping_table.setItem(row, 0, QTableWidgetItem(str(cc)))
            self._mapping_table.setItem(row, 1, QTableWidgetItem(action))
            self._mapping_table.setItem(row, 2, QTableWidgetItem(controller_id))

    @pyqtSlot()
    def _ctrl_add_mapping_row(self):
        selected_action_items = self._action_list.selectedItems()
        if not selected_action_items:
            QMessageBox.information(self, "Add Mapping", "Select an action from the list first.")
            return
        action = selected_action_items[0].text()
        cc_str, ok = QInputDialog.getText(self, "Add Mapping", f"Enter MIDI CC number for:\n{action}")
        if not ok or not cc_str.strip():
            return
        try:
            cc = int(cc_str.strip())
        except ValueError:
            QMessageBox.warning(self, "Invalid CC", "CC must be an integer (0–127).")
            return
        mgr = self._ctrl_manager()
        try:
            mgr.map_control("default", cc, action)
        except ValueError as e:
            QMessageBox.warning(self, "Mapping Error", str(e))
            return
        self._refresh_mapping_table("default")

    @pyqtSlot()
    def _ctrl_remove_mapping_row(self):
        row = self._mapping_table.currentRow()
        if row < 0:
            return
        cc_item = self._mapping_table.item(row, 0)
        ctrl_item = self._mapping_table.item(row, 2)
        if cc_item and ctrl_item:
            mgr = self._ctrl_manager()
            mgr.unmap_control(ctrl_item.text(), int(cc_item.text()))
            self._mapping_table.removeRow(row)

    @pyqtSlot()
    def _ctrl_clear_mappings(self):
        if QMessageBox.question(self, "Clear Mappings",
                                "Remove all mappings for this controller?") \
                == QMessageBox.StandardButton.Yes:
            self._ctrl_manager().clear_mappings("default")
            self._mapping_table.setRowCount(0)

    @pyqtSlot()
    def _ctrl_save_profile(self):
        from src.controllers.manager import _PROFILES_DIR
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Profile", _PROFILES_DIR, "JSON Profiles (*.json)")
        if path:
            ok = self._ctrl_manager().save_mapping_profile(path, "default")
            sb = self.statusBar()
            if sb:
                sb.showMessage(f"Profile {'saved' if ok else 'FAILED'}: {path}", 4000)

    @pyqtSlot()
    def _ctrl_load_profile(self):
        from src.controllers.manager import _PROFILES_DIR
        path, _ = QFileDialog.getOpenFileName(
            self, "Load Profile", _PROFILES_DIR, "JSON Profiles (*.json)")
        if path:
            self._ctrl_manager().load_mapping_profile(path)
            self._refresh_mapping_table("default")
            sb = self.statusBar()
            if sb:
                sb.showMessage(f"Profile loaded: {path}", 4000)

    # E16 – MIDI Learn toggle
    @pyqtSlot(bool)
    def _ctrl_toggle_learn(self, checked: bool):
        mgr = self._ctrl_manager()
        if checked:
            selected = self._action_list.selectedItems()
            if not selected:
                self._learn_btn.setChecked(False)
                QMessageBox.information(self, "MIDI Learn",
                                        "Select an action in the list first.")
                return
            action = selected[0].text()
            mgr.start_learn("default", action)
            self._learn_status_lbl.setText(
                f"Listening…\nMove a knob/fader/button on your controller\nto map it to:\n{action}"
            )
        else:
            mgr.cancel_learn()
            self._learn_status_lbl.setText(
                "Select an action, then press MIDI Learn\nand move a knob/fader on your controller."
            )

    # ════════════════════════════════════════════════════════════════════════
    #  SETTINGS TAB
    # ════════════════════════════════════════════════════════════════════════
    def create_settings_panel(self) -> QWidget:
        root = QWidget()
        root.setStyleSheet("background:transparent;")
        lo = QVBoxLayout(root)
        lo.setContentsMargins(4, 4, 4, 4)
        lo.setSpacing(10)

        row_lo = QHBoxLayout()
        row_lo.setSpacing(10)

        # Audio
        af, a_lo = _side_frame()
        a_lo.addWidget(_panel_title("Audio Configuration"))
        for lbl_text, widget_factory in (
            ("Audio Backend", lambda: _combo(["PulseAudio", "ALSA", "JACK"])),
            ("Sample Rate",   lambda: _combo(["44100 Hz", "48000 Hz", "96000 Hz"], "48000 Hz")),
            ("Buffer Size",   lambda: _spinbox(256, 64, 4096, 64)),
        ):
            row = QHBoxLayout()
            row.setSpacing(8)
            lbl = QLabel(lbl_text)
            lbl.setMinimumWidth(110)
            row.addWidget(lbl)
            row.addWidget(widget_factory())
            row.addStretch()
            a_lo.addLayout(row)
        a_lo.addStretch()
        row_lo.addWidget(af, 1)

        # Bluetooth
        bf, b_lo = _side_frame()
        bf.setObjectName("panelLeft")
        b_lo.addWidget(_panel_title("Bluetooth"))
        for text in ("Enable Bluetooth Audio Input",
                     "Allow Multiple BT Connections",
                     "Auto-connect to Paired Devices"):
            b_lo.addWidget(QCheckBox(text))
        b_lo.addStretch()
        row_lo.addWidget(bf, 1)

        # Network
        nf, n_lo = _side_frame()
        nf.setObjectName("panelLeft")
        n_lo.addWidget(_panel_title("Network"))
        for text in ("Enable Wi-Fi Device Discovery", "Allow Remote Control"):
            n_lo.addWidget(QCheckBox(text))
        n_lo.addStretch()
        row_lo.addWidget(nf, 1)

        lo.addLayout(row_lo)

        # Enhancement 7 – Accent colour selector row
        theme_frame, t_lo = _side_frame()
        theme_frame.setObjectName("panelLeft")
        t_lo.addWidget(_panel_title("Appearance"))
        accent_row = QHBoxLayout()
        accent_row.setSpacing(8)
        accent_row.addWidget(QLabel("Accent Color:"))
        accent_combo = _combo(list(self.ACCENT_COLORS.keys()))
        # Restore saved accent
        saved_name = next(
            (k for k, v in self.ACCENT_COLORS.items() if v == self._accent_color),
            "Amber (Default)"
        )
        accent_combo.setCurrentText(saved_name)
        accent_combo.currentTextChanged.connect(self._on_accent_changed)
        accent_row.addWidget(accent_combo)
        accent_row.addStretch()
        t_lo.addLayout(accent_row)

        # Feature 10: Theme export / import + built-in theme presets
        t_lo.addWidget(_hline())
        theme_preset_row = QHBoxLayout()
        theme_preset_row.setSpacing(6)
        theme_preset_row.addWidget(QLabel("Theme Preset:"))
        theme_preset_combo = _combo([
            "Dark Amber (Default)", "Dark Blue", "Red Alert",
            "Emerald", "Purple Haze",
        ])
        theme_preset_combo.currentTextChanged.connect(self._apply_theme_preset)
        theme_preset_row.addWidget(theme_preset_combo)
        t_lo.addLayout(theme_preset_row)

        theme_io_row = QHBoxLayout()
        theme_io_row.setSpacing(6)
        export_theme_btn = QPushButton("Export Theme…")
        export_theme_btn.clicked.connect(self._export_theme)
        import_theme_btn = QPushButton("Import Theme…")
        import_theme_btn.clicked.connect(self._import_theme)
        theme_io_row.addWidget(export_theme_btn)
        theme_io_row.addWidget(import_theme_btn)
        theme_io_row.addStretch()
        t_lo.addLayout(theme_io_row)

        # Enhancement 10 – Save / Reset config buttons
        cfg_row = QHBoxLayout()
        cfg_row.setSpacing(8)
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self._save_config)
        reset_btn = QPushButton("Reset Defaults")
        reset_btn.clicked.connect(self._reset_config)
        cfg_row.addWidget(save_btn)
        cfg_row.addWidget(reset_btn)
        cfg_row.addStretch()
        t_lo.addLayout(cfg_row)
        t_lo.addStretch()
        lo.addWidget(theme_frame)

        # Feature 11: Keyboard Shortcut Editor
        sc_frame, sc_lo = _side_frame()
        sc_frame.setObjectName("panelLeft")
        sc_lo.addWidget(_panel_title("Keyboard Shortcuts"))
        self._shortcut_table = QTableWidget(0, 2)
        self._shortcut_table.setHorizontalHeaderLabels(["Action", "Key"])
        hdr = self._shortcut_table.horizontalHeader()
        if hdr:
            hdr.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            hdr.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
            hdr.resizeSection(1, 100)
        self._shortcut_table.setStyleSheet("""
            QTableWidget { background:#0d0d0d; color:#cccccc;
                border:1px solid #2a2a2a; gridline-color:#1a1a1a; font-size:10px; }
            QTableWidget::item:selected { background:#1a3050; color:#fff; }
            QHeaderView::section { background:#1a1a1a; color:#888; border:none;
                border-bottom:1px solid #2a2a2a; padding:4px; font-size:9px; }
        """)
        self._shortcut_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self._populate_shortcut_table()
        sc_lo.addWidget(self._shortcut_table)

        sc_btn_row = QHBoxLayout()
        remap_btn = QPushButton("Remap Selected")
        remap_btn.clicked.connect(self._remap_shortcut)
        reset_sc_btn = QPushButton("Reset All")
        reset_sc_btn.clicked.connect(self._reset_shortcuts)
        sc_btn_row.addWidget(remap_btn)
        sc_btn_row.addWidget(reset_sc_btn)
        sc_btn_row.addStretch()
        sc_lo.addLayout(sc_btn_row)
        lo.addWidget(sc_frame)

        lo.addStretch()
        return root

    # ── Device detection ────────────────────────────────────────────────────
    def start_device_detection(self):
        from src.devices.detector import DeviceDetector
        self.device_detector = DeviceDetector()
        self.device_detector.devices_found.connect(self.on_devices_found)
        self.device_detector.start()

    def on_devices_found(self, devices):
        count = len(devices)
        sb = self.statusBar()
        if sb:
            sb.showMessage(f"Violet DJ Mixer v{self.VERSION}  ·  Ready  ·  {count} device(s) connected")
        logger.info(f"Detected {count} devices")

    # ── File / dialog actions ────────────────────────────────────────────────
    def open_track(self, deck: int = 1):
        # Enhancement 8 – all 9 supported formats in the filter
        p, _ = QFileDialog.getOpenFileName(
            self, "Open Track", "",
            "Audio Files (*.mp3 *.wav *.flac *.ogg *.aac *.m4a *.wma *.aiff *.alac);;"
            "MP3 Files (*.mp3);;WAV Files (*.wav);;FLAC Files (*.flac);;"
            "OGG Files (*.ogg);;AAC/M4A (*.aac *.m4a);;All Files (*)"
        )
        if p:
            # Enhancement 1 – record in recent tracks
            self._add_recent_track(p)
            # Enhancement 4 – log to session file
            self._log_track_played(p)
            name = os.path.basename(p)

            # Feature 3: Read track metadata
            meta: dict = {}
            if _HAS_META:
                try:
                    meta = read_metadata(p)
                    self._deck_metadata[deck] = meta
                    dur_str = format_duration(meta.get("duration", 0.0))
                    bpm_val = meta.get("bpm", 0.0)
                    artist  = meta.get("artist", "")
                    title   = meta.get("title", name)
                    label_text = f"{artist} – {title}" if artist else title
                    label_text += f"  [{dur_str}]"
                    if bpm_val:
                        label_text += f"  {bpm_val:.0f}bpm"
                        if deck in self._deck_bpm_spins:
                            self._deck_bpm_spins[deck].setValue(bpm_val)
                            self._deck_bpm[deck] = bpm_val
                except Exception as e:
                    logger.warning(f"Metadata read failed: {e}")
                    label_text = name
            else:
                label_text = name

            # Enhancement 5 – update deck label
            if deck in self._deck_labels:
                short = label_text[:28] + "…" if len(label_text) > 28 else label_text
                self._deck_labels[deck].setText(short)

            # Feature 2: Update waveform display
            if _HAS_WAVE and deck in self._waveforms:
                duration = meta.get("duration", 0.0) if meta else 0.0
                self._waveforms[deck].load_track(p)

            # Feature 6: Load hot cues for this track
            self._load_hot_cues(p, deck)

            # Feature 1: Activate VU simulation for this deck
            if deck in self._vu_meters:
                self._vu_meters[deck].set_active(True)

            # Enhancement 12 – add to queue list
            if hasattr(self, "_queue_list"):
                self._queue_list.addItem(QListWidgetItem(name))

            # Feature 4: Add to library recents if open
            if hasattr(self, "_lib_recent_list"):
                self._lib_recent_list.addItem(QListWidgetItem(name))

            logger.info(f"Loading track: {p}")

    def open_playlist(self):
        p, _ = QFileDialog.getOpenFileName(
            self, "Open Playlist", "", "Playlist Files (*.m3u *.pls)")
        if p:
            logger.info(f"Loading playlist: {p}")

    def show_preferences(self):
        QMessageBox.information(self, "Preferences", "Preferences — Coming soon!")

    def show_controller_mapping(self):
        QMessageBox.information(self, "Controller Mapping",
                                "Controller mapping dialog — Coming soon!")

    def show_audio_settings(self):
        QMessageBox.information(self, "Audio Settings",
                                "Audio settings dialog — Coming soon!")

    def show_documentation(self):
        import webbrowser
        webbrowser.open("https://violet-dj.github.io/docs")

    def show_about(self):
        QMessageBox.about(self, "About Violet DJ Mixer",
                          f"<b>Violet DJ Mixer v{self.VERSION}</b><br><br>"
                          "Professional digital mixing board for Ubuntu<br><br>"
                          "Pioneer DJM-800 + DJS-1000 inspired interface<br><br>"
                          "Free and open-source under GPL-3.0<br><br>"
                          "<a href='https://violet-dj.github.io'>Visit Website</a>")

    def refresh_devices(self):
        sb = self.statusBar()
        if sb:
            sb.showMessage("Scanning for devices…")
        self.start_device_detection()

    # ── Enhancement 1: Recent Tracks ────────────────────────────────────────
    def _load_recent_tracks(self) -> list[str]:
        path = os.path.join(os.path.expanduser("~/.violet_dj"), "recent_tracks.json")
        try:
            if os.path.exists(path):
                with open(path) as f:
                    data = json.load(f)
                return [str(x) for x in data if os.path.exists(str(x))]
        except Exception:
            pass
        return []

    def _save_recent_tracks(self):
        path = os.path.join(self._app_dir, "recent_tracks.json")
        try:
            with open(path, "w") as f:
                json.dump(self._recent_tracks, f, indent=2)
        except Exception as e:
            logger.warning(f"Could not save recent tracks: {e}")

    def _add_recent_track(self, file_path: str):
        if file_path in self._recent_tracks:
            self._recent_tracks.remove(file_path)
        self._recent_tracks.insert(0, file_path)
        self._recent_tracks = self._recent_tracks[:self.MAX_RECENT]
        self._save_recent_tracks()
        self._rebuild_recent_menu()

    def _rebuild_recent_menu(self):
        self._recent_menu.clear()
        if not self._recent_tracks:
            act = QAction("(none)", self)
            act.setEnabled(False)
            self._recent_menu.addAction(act)
            return
        for path in self._recent_tracks:
            act = QAction(os.path.basename(path), self)
            act.setData(path)
            act.triggered.connect(lambda checked, p=path: self._open_recent(p))
            self._recent_menu.addAction(act)
        self._recent_menu.addSeparator()
        clear_act = QAction("Clear Recent", self)
        clear_act.triggered.connect(self._clear_recent)
        self._recent_menu.addAction(clear_act)

    def _open_recent(self, path: str):
        self._add_recent_track(path)
        self._log_track_played(path)
        name = os.path.basename(path)
        if 1 in self._deck_labels:
            self._deck_labels[1].setText(name[:20] + "…" if len(name) > 20 else name)
        if hasattr(self, "_queue_list"):
            self._queue_list.addItem(QListWidgetItem(name))
        logger.info(f"Loading recent track: {path}")

    def _clear_recent(self):
        self._recent_tracks.clear()
        self._save_recent_tracks()
        self._rebuild_recent_menu()

    # ── Enhancement 2: Keyboard Shortcuts ───────────────────────────────────
    def _setup_keyboard_shortcuts(self):
        shortcuts = [
            ("Ctrl+O",     self.open_track),
            ("F11",        self._toggle_fullscreen),
            ("Space",      self._kb_play_pause),
            ("Ctrl+Left",  self._kb_cue_deck_a),
            ("Ctrl+Right", self._kb_cue_deck_b),
            ("Ctrl+Up",    self._kb_xfader_center),
            ("Ctrl+Down",  self._kb_xfader_center),
            ("F5",         self.refresh_devices),
        ]
        for seq, slot in shortcuts:
            sc = QShortcut(QKeySequence(seq), self)
            sc.activated.connect(slot)

    @pyqtSlot()
    def _kb_play_pause(self):
        logger.info("Keyboard: play/pause toggle")

    @pyqtSlot()
    def _kb_cue_deck_a(self):
        logger.info("Keyboard: CUE deck A")

    @pyqtSlot()
    def _kb_cue_deck_b(self):
        logger.info("Keyboard: CUE deck B")

    @pyqtSlot()
    def _kb_xfader_center(self):
        logger.info("Keyboard: crossfader center")

    def _toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    # ── Enhancement 3: Tap Tempo ─────────────────────────────────────────────
    @pyqtSlot()
    def _on_tap_tempo(self):
        now = time.time()
        # Reset if last tap was more than 3 seconds ago
        if self._tap_times and (now - self._tap_times[-1]) > 3.0:
            self._tap_times.clear()
        self._tap_times.append(now)
        if len(self._tap_times) > 8:
            self._tap_times = self._tap_times[-8:]
        if len(self._tap_times) >= 2:
            intervals = [self._tap_times[i+1] - self._tap_times[i]
                         for i in range(len(self._tap_times) - 1)]
            avg_interval = sum(intervals) / len(intervals)
            bpm = 60.0 / avg_interval
            bpm = max(20.0, min(300.0, bpm))
            ms = avg_interval * 1000
            if self._bpm_display:
                self._bpm_display.setText(f"{bpm:.1f}")
            if hasattr(self, "_ms_display"):
                self._ms_display.setText(f"{ms:.0f} ms")
            logger.info(f"Tap tempo: {bpm:.1f} BPM")

    # ── Enhancement 4: Session Logger ───────────────────────────────────────
    def _log_track_played(self, file_path: str):
        date_str = datetime.now().strftime("%Y%m%d")
        log_path = os.path.join(self._app_dir, "sessions", f"session_{date_str}.log")
        entry = {
            "timestamp": datetime.now().isoformat(),
            "track": file_path,
        }
        try:
            with open(log_path, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            logger.warning(f"Session log write failed: {e}")

    def show_session_log(self):
        date_str = datetime.now().strftime("%Y%m%d")
        log_path = os.path.join(self._app_dir, "sessions", f"session_{date_str}.log")
        if not os.path.exists(log_path):
            QMessageBox.information(self, "Session Log", "No tracks played in this session yet.")
            return
        try:
            with open(log_path) as f:
                lines = f.readlines()
            entries = []
            for line in lines:
                try:
                    e = json.loads(line)
                    ts = e.get("timestamp", "")[:19].replace("T", " ")
                    name = os.path.basename(e.get("track", ""))
                    entries.append(f"{ts}  {name}")
                except Exception:
                    pass
            text = "\n".join(entries) if entries else "No entries."
            QMessageBox.information(self, f"Session Log — {date_str}", text)
        except Exception as e:
            QMessageBox.warning(self, "Session Log", f"Could not read log: {e}")

    # ── Enhancement 6: Master Clock / Session Timer ──────────────────────────
    @pyqtSlot()
    def _update_clock(self):
        elapsed = int(time.time() - self._session_start)
        h, rem = divmod(elapsed, 3600)
        m, s = divmod(rem, 60)
        now_str = datetime.now().strftime("%H:%M:%S")
        session_str = f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
        sb = self.statusBar()
        if sb:
            sb.showMessage(
                f"Violet DJ Mixer v{self.VERSION}  ·  {now_str}  ·  Session {session_str}"
            )

    # ── Enhancement 7: Accent Colour ────────────────────────────────────────
    def _on_accent_changed(self, name: str):
        color = self.ACCENT_COLORS.get(name, "#ff8800")
        self._accent_color = color
        new_style = HARDWARE_STYLESHEET.replace("#ff8800", color).replace("#ffaa22", color)
        self.setStyleSheet(new_style)
        self._config["accent_color"] = color

    # ── Enhancement 10: Config Persistence ──────────────────────────────────
    def _config_path(self) -> str:
        return os.path.join(self._app_dir, "config.json")

    def _load_config(self) -> dict:
        try:
            if os.path.exists(self._config_path()):
                with open(self._config_path()) as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def _save_config(self):
        try:
            with open(self._config_path(), "w") as f:
                json.dump(self._config, f, indent=2)
            sb = self.statusBar()
            if sb:
                sb.showMessage("Settings saved.", 3000)
            logger.info("Config saved")
        except Exception as e:
            QMessageBox.warning(self, "Save Failed", f"Could not save settings: {e}")

    def _reset_config(self):
        self._config.clear()
        self._accent_color = "#ff8800"
        self.setStyleSheet(HARDWARE_STYLESHEET)
        sb = self.statusBar()
        if sb:
            sb.showMessage("Settings reset to defaults.", 3000)

    # ── Enhancement 2: shortcuts help dialog ────────────────────────────────
    def show_shortcuts(self):
        text = (
            "<b>Keyboard Shortcuts</b><br><br>"
            "<b>Ctrl+O</b> — Open Track<br>"
            "<b>Space</b> — Play / Pause<br>"
            "<b>Ctrl+Left</b> — CUE Deck A<br>"
            "<b>Ctrl+Right</b> — CUE Deck B<br>"
            "<b>Ctrl+Up / Down</b> — Crossfader Center<br>"
            "<b>F5</b> — Refresh Devices<br>"
            "<b>F11</b> — Toggle Full Screen<br>"
        )
        QMessageBox.information(self, "Keyboard Shortcuts", text)

    # ════════════════════════════════════════════════════════════════════════
    #  QUEUE TAB  — Enhancement 12: Playlist Queue Management
    # ════════════════════════════════════════════════════════════════════════
    def create_queue_panel(self) -> QWidget:
        root = QWidget()
        root.setStyleSheet("background:transparent;")
        lo = QVBoxLayout(root)
        lo.setContentsMargins(4, 4, 4, 4)
        lo.setSpacing(8)

        panel = QFrame()
        panel.setObjectName("panelLeft")
        p_lo = QVBoxLayout(panel)
        p_lo.setContentsMargins(16, 14, 16, 14)
        p_lo.setSpacing(8)

        p_lo.addWidget(_panel_title("Track Queue"))

        # Queue list widget
        self._queue_list = QListWidget()
        self._queue_list.setStyleSheet("""
            QListWidget {
                background: #0d0d0d; color: #aaaaaa;
                border: 1px solid #2a2a2a; border-radius: 4px;
                font-size: 11px;
            }
            QListWidget::item:selected {
                background: #1a3050; color: #ffffff;
            }
            QListWidget::item:hover {
                background: #1a1a2a;
            }
        """)
        self._queue_list.setMinimumHeight(300)
        p_lo.addWidget(self._queue_list)

        # Queue control buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        add_btn = QPushButton("+ Add Track")
        add_btn.clicked.connect(self.open_track)
        btn_row.addWidget(add_btn)

        remove_btn = QPushButton("Remove")
        remove_btn.clicked.connect(self._queue_remove_selected)
        btn_row.addWidget(remove_btn)

        up_btn = QPushButton("▲ Up")
        up_btn.clicked.connect(self._queue_move_up)
        btn_row.addWidget(up_btn)

        down_btn = QPushButton("▼ Down")
        down_btn.clicked.connect(self._queue_move_down)
        btn_row.addWidget(down_btn)

        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(self._queue_list.clear)
        btn_row.addWidget(clear_btn)

        btn_row.addStretch()
        p_lo.addLayout(btn_row)

        # Now-playing indicator
        p_lo.addWidget(_hline())
        now_row = QHBoxLayout()
        now_row.addWidget(_section_label("Now Playing:"))
        self._now_playing_lbl = QLabel("—")
        self._now_playing_lbl.setStyleSheet(
            "color:#ff8800; font-size:11px; font-weight:bold; background:transparent;"
        )
        now_row.addWidget(self._now_playing_lbl)
        now_row.addStretch()
        p_lo.addLayout(now_row)

        lo.addWidget(panel)
        lo.addStretch()
        return root

    @pyqtSlot()
    def _queue_remove_selected(self):
        row = self._queue_list.currentRow()
        if row >= 0:
            self._queue_list.takeItem(row)

    @pyqtSlot()
    def _queue_move_up(self):
        row = self._queue_list.currentRow()
        if row > 0:
            item = self._queue_list.takeItem(row)
            self._queue_list.insertItem(row - 1, item)
            self._queue_list.setCurrentRow(row - 1)

    @pyqtSlot()
    def _queue_move_down(self):
        row = self._queue_list.currentRow()
        if row >= 0 and row < self._queue_list.count() - 1:
            item = self._queue_list.takeItem(row)
            self._queue_list.insertItem(row + 1, item)
            self._queue_list.setCurrentRow(row + 1)

    # ════════════════════════════════════════════════════════════════════════
    #  MIDI → UI WIRING
    # ════════════════════════════════════════════════════════════════════════
    def _wire_controller_actions(self):
        """Connect ControllerManager's MidiActionEmitter signals to UI slots.

        Called once after all panels are built.  Safe to call even when
        rtmidi is unavailable — the emitter will simply never fire.
        """
        mgr = self._ctrl_manager()
        if mgr.emitter is None:
            logger.info("No MIDI emitter available — skipping MIDI→UI wiring")
            return

        mgr.emitter.action_triggered.connect(self._on_midi_action)
        mgr.emitter.learn_completed.connect(self._on_midi_learn_completed)
        logger.info("MIDI→UI signals connected")

    @pyqtSlot(str, int)
    def _on_midi_action(self, action: str, value: int):
        """Route an incoming MIDI action (main thread) to the matching UI control.

        `value` is 0–127 (raw MIDI); rescaled to 0–100 for sliders/dials.
        """
        ctrl = self._midi_controls.get(action)
        if ctrl is None:
            return

        val_100 = int(value * 100 / 127)

        if isinstance(ctrl, QSlider):
            ctrl.setValue(val_100)

        elif isinstance(ctrl, QDial):
            ctrl.setValue(val_100)

        elif isinstance(ctrl, QPushButton) and ctrl.isCheckable():
            # Treat value > 63 as button press, ≤ 63 as release
            ctrl.setChecked(value > 63)

        logger.debug(f"MIDI action applied: {action} = {value} → {val_100}")

    @pyqtSlot(str, int, str)
    def _on_midi_learn_completed(self, controller_id: str, cc: int, action: str):
        """Update the mapping table and status label after MIDI Learn captures a CC."""
        self._refresh_mapping_table(controller_id)
        self._learn_btn.setChecked(False)
        self._learn_status_lbl.setText(
            f"Mapped: CC {cc} → {action}\n\n"
            "Select another action and press MIDI Learn to continue."
        )
        sb = self.statusBar()
        if sb:
            sb.showMessage(f"MIDI Learn: CC {cc} mapped to '{action}'", 5000)
        logger.info(f"MIDI Learn UI updated: CC {cc} → {action}")

    # ════════════════════════════════════════════════════════════════════════
    #  Feature 4: LIBRARY TAB — file browser + search + track table
    # ════════════════════════════════════════════════════════════════════════
    def create_library_panel(self) -> QWidget:
        root = QWidget()
        root.setStyleSheet("background:transparent;")
        outer = QHBoxLayout(root)
        outer.setContentsMargins(4, 4, 4, 4)
        outer.setSpacing(8)

        # ── Left: folder tree ────────────────────────────────────────────
        tree_frame, tree_lo = _side_frame()
        tree_frame.setMaximumWidth(240)
        tree_lo.addWidget(_panel_title("Folders"))

        self._lib_folder_tree = QTreeWidget()
        self._lib_folder_tree.setHeaderHidden(True)
        self._lib_folder_tree.setStyleSheet("""
            QTreeWidget { background:#0d0d0d; color:#aaaaaa;
                border:1px solid #2a2a2a; font-size:10px; }
            QTreeWidget::item:selected { background:#1a3050; color:#fff; }
            QTreeWidget::item:hover { background:#141414; }
        """)
        # Seed with common music folders
        for folder in (
            os.path.expanduser("~/Music"),
            os.path.expanduser("~/Downloads"),
            "/media",
        ):
            if os.path.isdir(folder):
                item = QTreeWidgetItem([os.path.basename(folder)])
                item.setData(0, Qt.ItemDataRole.UserRole, folder)
                self._lib_folder_tree.addTopLevelItem(item)
                self._lib_scan_folder(item, folder, depth=1)
        self._lib_folder_tree.itemClicked.connect(self._lib_folder_clicked)
        tree_lo.addWidget(self._lib_folder_tree)

        browse_btn = QPushButton("Browse…")
        browse_btn.clicked.connect(self._lib_browse_folder)
        tree_lo.addWidget(browse_btn)
        outer.addWidget(tree_frame)

        # ── Right: search + track table ──────────────────────────────────
        right = QWidget()
        right.setStyleSheet("background:transparent;")
        right_lo = QVBoxLayout(right)
        right_lo.setContentsMargins(0, 0, 0, 0)
        right_lo.setSpacing(6)

        # Search bar
        search_frame = QFrame()
        search_frame.setObjectName("glassCard")
        search_lo = QHBoxLayout(search_frame)
        search_lo.setContentsMargins(8, 6, 8, 6)
        search_lo.setSpacing(6)
        search_lo.addWidget(_section_label("Search:"))
        self._lib_search = QLineEdit()
        self._lib_search.setPlaceholderText("Filter tracks by name, artist, or BPM…")
        self._lib_search.setStyleSheet(
            "QLineEdit { background:#0a0a0a; color:#cccccc; border:1px solid #2a2a2a; "
            "border-radius:3px; padding:4px 8px; font-size:10px; }"
            "QLineEdit:focus { border-color:#ff8800; }"
        )
        self._lib_search.textChanged.connect(self._lib_filter_tracks)
        search_lo.addWidget(self._lib_search)
        right_lo.addWidget(search_frame)

        # Track table
        self._lib_track_table = QTableWidget(0, 5)
        self._lib_track_table.setHorizontalHeaderLabels(
            ["Title", "Artist", "Duration", "BPM", "Format"])
        hdr = self._lib_track_table.horizontalHeader()
        if hdr:
            hdr.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            hdr.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            for c in (2, 3, 4):
                hdr.setSectionResizeMode(c, QHeaderView.ResizeMode.Fixed)
                hdr.resizeSection(c, 70)
        self._lib_track_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self._lib_track_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self._lib_track_table.setAlternatingRowColors(True)
        self._lib_track_table.setStyleSheet("""
            QTableWidget { background:#0d0d0d; color:#cccccc;
                border:1px solid #2a2a2a; gridline-color:#1a1a1a; font-size:10px; }
            QTableWidget::item:selected { background:#1a3050; color:#fff; }
            QTableWidget::item:alternate { background:#111111; }
            QHeaderView::section { background:#1a1a1a; color:#888; border:none;
                border-bottom:1px solid #2a2a2a; padding:4px; font-size:9px; }
        """)
        self._lib_track_table.doubleClicked.connect(self._lib_load_selected)
        right_lo.addWidget(self._lib_track_table)

        # Bottom row
        bottom_row = QHBoxLayout()
        load_a_btn = QPushButton("Load → Deck A")
        load_a_btn.clicked.connect(lambda: self._lib_load_to_deck(1))
        load_b_btn = QPushButton("Load → Deck B")
        load_b_btn.clicked.connect(lambda: self._lib_load_to_deck(2))
        queue_btn = QPushButton("Add to Queue")
        queue_btn.clicked.connect(self._lib_add_to_queue)
        self._lib_status_lbl = QLabel("0 tracks")
        self._lib_status_lbl.setStyleSheet("color:#555; font-size:9px; background:transparent;")
        bottom_row.addWidget(load_a_btn)
        bottom_row.addWidget(load_b_btn)
        bottom_row.addWidget(queue_btn)
        bottom_row.addStretch()
        bottom_row.addWidget(self._lib_status_lbl)
        right_lo.addLayout(bottom_row)

        # Recent tracks panel
        recent_frame = QFrame()
        recent_frame.setObjectName("glassCard")
        recent_lo = QVBoxLayout(recent_frame)
        recent_lo.setContentsMargins(8, 6, 8, 6)
        recent_lo.setSpacing(4)
        recent_lo.addWidget(_section_label("Recently Loaded"))
        self._lib_recent_list = QListWidget()
        self._lib_recent_list.setMaximumHeight(70)
        self._lib_recent_list.setStyleSheet("""
            QListWidget { background:#0a0a0a; color:#888; border:none; font-size:9px; }
            QListWidget::item:selected { background:#1a3050; color:#fff; }
        """)
        for t in self._recent_tracks[-8:]:
            self._lib_recent_list.addItem(QListWidgetItem(os.path.basename(t)))
        recent_lo.addWidget(self._lib_recent_list)
        right_lo.addWidget(recent_frame)

        outer.addWidget(right, 1)
        return root

    def _lib_scan_folder(self, parent_item: QTreeWidgetItem,
                          folder: str, depth: int = 0) -> None:
        if depth <= 0:
            return
        try:
            for entry in sorted(os.scandir(folder), key=lambda e: e.name):
                if entry.is_dir(follow_symlinks=False):
                    child = QTreeWidgetItem([entry.name])
                    child.setData(0, Qt.ItemDataRole.UserRole, entry.path)
                    parent_item.addChild(child)
                    self._lib_scan_folder(child, entry.path, depth - 1)
        except PermissionError:
            pass

    @pyqtSlot(QTreeWidgetItem)
    def _lib_folder_clicked(self, item: QTreeWidgetItem) -> None:
        folder = item.data(0, Qt.ItemDataRole.UserRole)
        if folder and os.path.isdir(folder):
            # Expand sub-folders on click
            if item.childCount() == 0:
                self._lib_scan_folder(item, folder, depth=1)
            self._lib_populate_tracks(folder)

    @pyqtSlot()
    def _lib_browse_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select Music Folder")
        if folder:
            self._lib_populate_tracks(folder)
            item = QTreeWidgetItem([os.path.basename(folder)])
            item.setData(0, Qt.ItemDataRole.UserRole, folder)
            self._lib_folder_tree.addTopLevelItem(item)

    def _lib_populate_tracks(self, folder: str) -> None:
        """Fill the track table from audio files in *folder*."""
        self._lib_track_table.setRowCount(0)
        exts = {".mp3", ".wav", ".flac", ".ogg", ".aac", ".m4a", ".aiff", ".alac"}
        try:
            files = sorted(
                e.path for e in os.scandir(folder)
                if e.is_file() and os.path.splitext(e.name)[1].lower() in exts
            )
        except PermissionError:
            return
        for path in files:
            self._lib_add_track_row(path)
        count = self._lib_track_table.rowCount()
        self._lib_status_lbl.setText(f"{count} track{'s' if count != 1 else ''}")

    def _lib_add_track_row(self, path: str) -> None:
        if _HAS_META:
            try:
                meta = read_metadata(path)
            except Exception:
                meta = {}
        else:
            meta = {}
        title   = meta.get("title",  os.path.splitext(os.path.basename(path))[0])
        artist  = meta.get("artist", "")
        dur     = format_duration(meta.get("duration", 0.0)) if _HAS_META else "--:--"
        bpm_val = meta.get("bpm", 0.0)
        bpm_str = f"{bpm_val:.0f}" if bpm_val else ""
        fmt     = meta.get("format", os.path.splitext(path)[1].lstrip(".").upper())
        row = self._lib_track_table.rowCount()
        self._lib_track_table.insertRow(row)
        for col, text in enumerate((title, artist, dur, bpm_str, fmt)):
            item = QTableWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, path)
            self._lib_track_table.setItem(row, col, item)

    @pyqtSlot(str)
    def _lib_filter_tracks(self, query: str) -> None:
        q = query.lower()
        for row in range(self._lib_track_table.rowCount()):
            row_text = " ".join(
                (self._lib_track_table.item(row, c) or QTableWidgetItem("")).text()
                for c in range(self._lib_track_table.columnCount())
            ).lower()
            self._lib_track_table.setRowHidden(row, bool(q) and q not in row_text)

    def _lib_selected_path(self) -> str | None:
        row = self._lib_track_table.currentRow()
        if row < 0:
            return None
        item = self._lib_track_table.item(row, 0)
        return item.data(Qt.ItemDataRole.UserRole) if item else None

    @pyqtSlot()
    def _lib_load_selected(self) -> None:
        path = self._lib_selected_path()
        if path:
            self.open_track.__func__(self, 1)   # delegate; simpler: just call open_track

    def _lib_load_to_deck(self, deck: int) -> None:
        path = self._lib_selected_path()
        if path:
            self._add_recent_track(path)
            self._log_track_played(path)
            name = os.path.basename(path)
            if deck in self._deck_labels:
                self._deck_labels[deck].setText(name[:28])
            if _HAS_WAVE and deck in self._waveforms:
                self._waveforms[deck].load_track(path)
            if deck in self._vu_meters:
                self._vu_meters[deck].set_active(True)
            sb = self.statusBar()
            if sb:
                sb.showMessage(f"Deck {deck}: {name}", 4000)

    @pyqtSlot()
    def _lib_add_to_queue(self) -> None:
        path = self._lib_selected_path()
        if path and hasattr(self, "_queue_list"):
            self._queue_list.addItem(QListWidgetItem(os.path.basename(path)))

    # ════════════════════════════════════════════════════════════════════════
    #  Feature 7: RECORDING TAB
    # ════════════════════════════════════════════════════════════════════════
    def create_recording_panel(self) -> QWidget:
        root = QWidget()
        root.setStyleSheet("background:transparent;")
        lo = QVBoxLayout(root)
        lo.setContentsMargins(4, 4, 4, 4)
        lo.setSpacing(10)

        # ── Controls panel ────────────────────────────────────────────────
        ctrl_frame, ctrl_lo = _side_frame()
        ctrl_lo.addWidget(_panel_title("Master Recorder"))

        # Status indicator
        self._rec_status_lbl = QLabel("● STOPPED")
        self._rec_status_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._rec_status_lbl.setStyleSheet(
            "color:#884444; font-size:14px; font-weight:bold; background:transparent;"
        )
        ctrl_lo.addWidget(self._rec_status_lbl)

        # Elapsed timer
        self._rec_elapsed_lbl = QLabel("00:00:00")
        self._rec_elapsed_lbl.setObjectName("bpmValue")
        self._rec_elapsed_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ctrl_lo.addWidget(self._rec_elapsed_lbl)

        # Output path
        path_row = QHBoxLayout()
        path_row.addWidget(_section_label("Output:"))
        self._rec_path_lbl = QLabel("~/.violet_dj/recordings/")
        self._rec_path_lbl.setStyleSheet("color:#556677; font-size:9px; background:transparent;")
        path_row.addWidget(self._rec_path_lbl)
        choose_btn = QPushButton("…")
        choose_btn.setFixedSize(QSize(28, 24))
        choose_btn.clicked.connect(self._rec_choose_path)
        path_row.addWidget(choose_btn)
        ctrl_lo.addLayout(path_row)

        ctrl_lo.addWidget(_hline())

        # Start / Stop / Discard
        rec_btn_row = QHBoxLayout()
        self._rec_start_btn = QPushButton("● Record")
        self._rec_start_btn.setMinimumHeight(40)
        self._rec_start_btn.setStyleSheet("""
            QPushButton { background:#330000; color:#cc4444; border:1px solid #550000;
                border-radius:4px; font-size:12px; font-weight:bold; }
            QPushButton:hover { background:#cc2222; color:#fff; }
        """)
        self._rec_start_btn.clicked.connect(self._start_recording)
        rec_btn_row.addWidget(self._rec_start_btn)

        self._rec_stop_btn = QPushButton("■ Stop")
        self._rec_stop_btn.setMinimumHeight(40)
        self._rec_stop_btn.setEnabled(False)
        self._rec_stop_btn.clicked.connect(self._stop_recording)
        rec_btn_row.addWidget(self._rec_stop_btn)
        ctrl_lo.addLayout(rec_btn_row)

        ctrl_lo.addWidget(_hline())

        # Format selector
        fmt_row = QHBoxLayout()
        fmt_row.addWidget(_section_label("Format:"))
        fmt_combo = _combo(["WAV 16-bit 44.1kHz", "WAV 24-bit 48kHz"])
        fmt_row.addWidget(fmt_combo)
        ctrl_lo.addLayout(fmt_row)

        ctrl_lo.addStretch()
        lo.addWidget(ctrl_frame)

        # ── Recordings list ───────────────────────────────────────────────
        list_frame, list_lo = _side_frame()
        list_lo.addWidget(_panel_title("Saved Recordings"))
        self._rec_list = QListWidget()
        self._rec_list.setStyleSheet("""
            QListWidget { background:#0d0d0d; color:#aaaaaa;
                border:1px solid #2a2a2a; font-size:10px; }
            QListWidget::item:selected { background:#1a3050; color:#fff; }
        """)
        self._rec_list.setMinimumHeight(200)
        self._refresh_recordings_list()
        list_lo.addWidget(self._rec_list)

        rec_list_btns = QHBoxLayout()
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self._refresh_recordings_list)
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self._delete_recording)
        rec_list_btns.addWidget(refresh_btn)
        rec_list_btns.addWidget(delete_btn)
        rec_list_btns.addStretch()
        list_lo.addLayout(rec_list_btns)
        lo.addWidget(list_frame)

        lo.addStretch()
        return root

    @pyqtSlot()
    def _start_recording(self) -> None:
        if not _HAS_REC or self._recorder is None:
            QMessageBox.warning(self, "Recording", "Recorder module not available.")
            return
        if self._recorder.is_recording:
            return
        path = self._recorder.start()
        self._rec_path_lbl.setText(path)
        self._rec_start_btn.setEnabled(False)
        self._rec_stop_btn.setEnabled(True)
        self._rec_status_lbl.setText("● RECORDING")
        self._rec_status_lbl.setStyleSheet(
            "color:#cc2222; font-size:14px; font-weight:bold; background:transparent;"
        )
        self._rec_timer.start(1000)
        sb = self.statusBar()
        if sb:
            sb.showMessage(f"Recording: {path}", 4000)

    @pyqtSlot()
    def _stop_recording(self) -> None:
        if not _HAS_REC or self._recorder is None:
            return
        path = self._recorder.stop()
        self._rec_timer.stop()
        self._rec_start_btn.setEnabled(True)
        self._rec_stop_btn.setEnabled(False)
        self._rec_status_lbl.setText("● STOPPED")
        self._rec_status_lbl.setStyleSheet(
            "color:#884444; font-size:14px; font-weight:bold; background:transparent;"
        )
        self._refresh_recordings_list()
        sb = self.statusBar()
        if sb:
            sb.showMessage(f"Recording saved: {path}", 5000)

    @pyqtSlot()
    def _update_rec_display(self) -> None:
        if _HAS_REC and self._recorder and self._recorder.is_recording:
            e = int(self._recorder.elapsed)
            h, rem = divmod(e, 3600)
            m, s = divmod(rem, 60)
            if self._rec_elapsed_lbl:
                self._rec_elapsed_lbl.setText(f"{h:02d}:{m:02d}:{s:02d}")

    @pyqtSlot()
    def _rec_choose_path(self) -> None:
        rec_dir = RECORDINGS_DIR if _HAS_REC else os.path.expanduser("~/.violet_dj/recordings")
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Recording", rec_dir, "WAV Files (*.wav)")
        if path:
            self._rec_path_lbl.setText(path)

    @pyqtSlot()
    def _refresh_recordings_list(self) -> None:
        self._rec_list.clear()
        if _HAS_REC and self._recorder:
            for name in self._recorder.list_recordings():
                self._rec_list.addItem(QListWidgetItem(name))

    @pyqtSlot()
    def _delete_recording(self) -> None:
        item = self._rec_list.currentItem()
        if not item:
            return
        rec_dir = RECORDINGS_DIR if _HAS_REC else os.path.expanduser("~/.violet_dj/recordings")
        path = os.path.join(rec_dir, item.text())
        if QMessageBox.question(self, "Delete Recording",
                                f"Delete {item.text()}?") == QMessageBox.StandardButton.Yes:
            try:
                os.remove(path)
                self._refresh_recordings_list()
            except Exception as e:
                QMessageBox.warning(self, "Delete Failed", str(e))

    # ════════════════════════════════════════════════════════════════════════
    #  Feature 1: VU Meter animation
    # ════════════════════════════════════════════════════════════════════════
    @pyqtSlot()
    def _vu_simulate(self) -> None:
        """Drive VU meters with a simulated signal when a deck is active."""
        import random
        for ch, vu in self._vu_meters.items():
            if vu._active:  # type: ignore[attr-defined]
                base = 0.55 + random.gauss(0, 0.1)
                vu.set_levels([
                    max(0.0, min(1.0, base + random.gauss(0, 0.05))),
                    max(0.0, min(1.0, base + random.gauss(0, 0.05))),
                ])

    # ════════════════════════════════════════════════════════════════════════
    #  Feature 5: Loop Controls
    # ════════════════════════════════════════════════════════════════════════
    def _loop_in(self, deck: int) -> None:
        pos = 0.3   # In a real engine this would be current playback position
        self._loop_state[deck]["in"] = pos
        if _HAS_WAVE and deck in self._waveforms:
            out = self._loop_state[deck].get("out", -1.0)
            if out > pos:
                self._waveforms[deck].set_loop(pos, out)
        logger.info(f"Deck {deck}: loop in @ {pos:.3f}")

    def _loop_out(self, deck: int) -> None:
        pos = 0.7
        self._loop_state[deck]["out"] = pos
        if _HAS_WAVE and deck in self._waveforms:
            in_p = self._loop_state[deck].get("in", -1.0)
            if 0 <= in_p < pos:
                self._waveforms[deck].set_loop(in_p, pos)
        logger.info(f"Deck {deck}: loop out @ {pos:.3f}")

    def _toggle_loop(self, deck: int, active: bool) -> None:
        self._loop_state[deck]["active"] = active
        if _HAS_WAVE and deck in self._waveforms:
            if active:
                in_p  = self._loop_state[deck].get("in",  0.3)
                out_p = self._loop_state[deck].get("out", 0.7)
                self._waveforms[deck].set_loop(in_p, out_p)
            else:
                self._waveforms[deck].clear_loop()
        logger.info(f"Deck {deck}: loop {'on' if active else 'off'}")

    # ════════════════════════════════════════════════════════════════════════
    #  Feature 6: Hot Cue Persistence
    # ════════════════════════════════════════════════════════════════════════
    def _hot_cue_dir(self) -> str:
        d = os.path.join(self._app_dir, "hot_cues")
        os.makedirs(d, exist_ok=True)
        return d

    def _track_key(self, path: str) -> str:
        import hashlib as _hl
        return _hl.md5(path.encode()).hexdigest()[:12]

    def _save_hot_cues(self, track_path: str, deck: int) -> None:
        key = self._track_key(track_path)
        cues = self._hot_cues.get(key, {})
        out = os.path.join(self._hot_cue_dir(), f"{key}.json")
        try:
            with open(out, "w") as f:
                json.dump({"track": track_path, "cues": cues}, f, indent=2)
        except Exception as e:
            logger.warning(f"Hot cue save failed: {e}")

    def _load_hot_cues(self, track_path: str, deck: int) -> None:
        key = self._track_key(track_path)
        src = os.path.join(self._hot_cue_dir(), f"{key}.json")
        if os.path.exists(src):
            try:
                with open(src) as f:
                    data = json.load(f)
                self._hot_cues[key] = data.get("cues", {})
                logger.info(f"Hot cues loaded for deck {deck}: {len(self._hot_cues[key])} cues")
            except Exception as e:
                logger.warning(f"Hot cue load failed: {e}")

    # ════════════════════════════════════════════════════════════════════════
    #  Feature 8: Crossfader Curve
    # ════════════════════════════════════════════════════════════════════════
    def _set_xfade_curve(self, curve_id: str) -> None:
        self._xfade_curve = curve_id
        if hasattr(self, "_curve_preview"):
            self._curve_preview.set_curve(curve_id)
        # Update button checked states
        for btn in getattr(self, "_xfade_curve_btns", []):
            btn.setChecked(btn.property("curveId") == curve_id)
        sb = self.statusBar()
        if sb:
            sb.showMessage(f"Crossfader curve: {curve_id}", 2500)

    # ════════════════════════════════════════════════════════════════════════
    #  Feature 10: Theme Export / Import
    # ════════════════════════════════════════════════════════════════════════
    _BUILTIN_THEMES = {
        "Dark Amber (Default)": {"accent": "#ff8800", "secondary": "#ffaa22"},
        "Dark Blue":            {"accent": "#4488ff", "secondary": "#66aaff"},
        "Red Alert":            {"accent": "#dd3333", "secondary": "#ff5555"},
        "Emerald":              {"accent": "#44cc66", "secondary": "#66ee88"},
        "Purple Haze":          {"accent": "#aa44ff", "secondary": "#cc77ff"},
    }

    def _apply_theme_preset(self, name: str) -> None:
        theme = self._BUILTIN_THEMES.get(name)
        if not theme:
            return
        accent = theme["accent"]
        self._accent_color = accent
        new_style = HARDWARE_STYLESHEET.replace("#ff8800", accent).replace(
            "#ffaa22", theme["secondary"])
        self.setStyleSheet(new_style)
        self._config["accent_color"] = accent
        self._config["theme_name"]   = name

    @pyqtSlot()
    def _export_theme(self) -> None:
        themes_dir = os.path.join(self._app_dir, "themes")
        path, _ = QFileDialog.getSaveFileName(
            self, "Export Theme", themes_dir, "JSON Theme (*.json)")
        if not path:
            return
        theme_data = {
            "accent":    self._accent_color,
            "secondary": self._config.get("secondary_color", "#ffaa22"),
            "name":      self._config.get("theme_name", "Custom"),
        }
        try:
            with open(path, "w") as f:
                json.dump(theme_data, f, indent=2)
            sb = self.statusBar()
            if sb:
                sb.showMessage(f"Theme exported: {os.path.basename(path)}", 3000)
        except Exception as e:
            QMessageBox.warning(self, "Export Failed", str(e))

    @pyqtSlot()
    def _import_theme(self) -> None:
        themes_dir = os.path.join(self._app_dir, "themes")
        path, _ = QFileDialog.getOpenFileName(
            self, "Import Theme", themes_dir, "JSON Theme (*.json)")
        if not path:
            return
        try:
            with open(path) as f:
                data = json.load(f)
            accent    = data.get("accent",    "#ff8800")
            secondary = data.get("secondary", "#ffaa22")
            self._accent_color = accent
            new_style = HARDWARE_STYLESHEET.replace("#ff8800", accent).replace(
                "#ffaa22", secondary)
            self.setStyleSheet(new_style)
            self._config["accent_color"]     = accent
            self._config["secondary_color"]  = secondary
            sb = self.statusBar()
            if sb:
                sb.showMessage(f"Theme imported: {data.get('name', 'Custom')}", 3000)
        except Exception as e:
            QMessageBox.warning(self, "Import Failed", str(e))

    # ════════════════════════════════════════════════════════════════════════
    #  Feature 11: Keyboard Shortcut Editor
    # ════════════════════════════════════════════════════════════════════════
    _DEFAULT_SHORTCUTS = {
        "Open Track":       "Ctrl+O",
        "Play / Pause":     "Space",
        "CUE Deck A":       "Ctrl+Left",
        "CUE Deck B":       "Ctrl+Right",
        "Full Screen":      "F11",
        "Refresh Devices":  "F5",
        "Loop In":          "I",
        "Loop Out":         "O",
        "Record Toggle":    "Ctrl+R",
        "BPM Nudge -0.1":  "Shift+Left",
        "BPM Nudge +0.1":  "Shift+Right",
    }

    def _populate_shortcut_table(self) -> None:
        saved = self._config.get("shortcuts", {})
        self._shortcut_table.setRowCount(0)
        for action, default_key in self._DEFAULT_SHORTCUTS.items():
            key = saved.get(action, default_key)
            row = self._shortcut_table.rowCount()
            self._shortcut_table.insertRow(row)
            self._shortcut_table.setItem(row, 0, QTableWidgetItem(action))
            self._shortcut_table.setItem(row, 1, QTableWidgetItem(key))

    @pyqtSlot()
    def _remap_shortcut(self) -> None:
        row = self._shortcut_table.currentRow()
        if row < 0:
            return
        action_item = self._shortcut_table.item(row, 0)
        if not action_item:
            return
        action = action_item.text()
        new_key, ok = QInputDialog.getText(
            self, "Remap Shortcut",
            f"Enter new key sequence for:\n{action}\n(e.g. Ctrl+Shift+P)"
        )
        if ok and new_key.strip():
            self._shortcut_table.setItem(row, 1, QTableWidgetItem(new_key.strip()))
            if "shortcuts" not in self._config:
                self._config["shortcuts"] = {}
            self._config["shortcuts"][action] = new_key.strip()
            sb = self.statusBar()
            if sb:
                sb.showMessage(f"Shortcut updated: {action} → {new_key.strip()}", 3000)

    @pyqtSlot()
    def _reset_shortcuts(self) -> None:
        self._config.pop("shortcuts", None)
        self._populate_shortcut_table()

    # ════════════════════════════════════════════════════════════════════════
    #  Feature 12: Per-deck BPM controls
    # ════════════════════════════════════════════════════════════════════════
    def _on_deck_bpm_changed(self, deck: int, value: float) -> None:
        self._deck_bpm[deck] = value
        # Update global BPM display if deck 1 or 2 is "master"
        if deck in (1, 2) and self._bpm_display:
            self._bpm_display.setText(f"{value:.1f}")
        logger.debug(f"Deck {deck} BPM → {value:.1f}")

    def _nudge_deck_bpm(self, deck: int, delta: float) -> None:
        current = self._deck_bpm.get(deck, 120.0)
        new_val = max(60.0, min(220.0, current + delta))
        self._deck_bpm[deck] = new_val
        if deck in self._deck_bpm_spins:
            self._deck_bpm_spins[deck].setValue(new_val)
