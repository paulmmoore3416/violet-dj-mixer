"""
Main window for Violet DJ Mixer
Pioneer DJM-800 + DJS-1000 Hardware-Inspired Interface
"""

from __future__ import annotations

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTabWidget, QLabel, QPushButton, QSlider, QDial,
                             QGridLayout, QComboBox, QSpinBox, QDoubleSpinBox,
                             QCheckBox, QProgressBar, QFrame, QMessageBox,
                             QFileDialog)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor, QLinearGradient, QPainter
import logging

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

    VERSION = "1.1.0"

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Violet DJ Mixer v{self.VERSION} — Professional Digital Mixing Board")
        self.setGeometry(100, 60, 1700, 960)
        self.setMinimumSize(1400, 800)

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

        self.tabs.addTab(self.create_mixer_panel(),  "  Mixer  ")
        self.tabs.addTab(self.create_sampler_panel(), "  Sampler  ")
        self.tabs.addTab(self.create_effects_panel(), "  Effects  ")
        self.tabs.addTab(self.create_device_panel(),  "  Devices  ")
        self.tabs.addTab(self.create_controller_panel(), "  Controllers  ")
        self.tabs.addTab(self.create_settings_panel(), "  Settings  ")

        sb = self.statusBar()
        if sb:
            sb.showMessage(f"Violet DJ Mixer v{self.VERSION}  ·  Ready  ·  No devices connected")

        self.device_detector = None
        self.start_device_detection()

        logger.info(f"Violet DJ Mixer v{self.VERSION} initialized")

    # ── Menu ────────────────────────────────────────────────────────────────
    def create_menu_bar(self):
        mb = self.menuBar()
        assert mb is not None
        fm = mb.addMenu("File")
        fm.addAction("Open Track",    self.open_track)
        fm.addAction("Open Playlist", self.open_playlist)
        fm.addSeparator()
        fm.addAction("Exit", self.close)

        em = mb.addMenu("Edit")
        em.addAction("Preferences",        self.show_preferences)
        em.addAction("Controller Mapping", self.show_controller_mapping)

        vm = mb.addMenu("View")
        vm.addAction("Toggle Visualization")
        vm.addAction("Full Screen")

        dm = mb.addMenu("Devices")
        dm.addAction("Refresh Devices", self.refresh_devices)
        dm.addAction("Audio Settings",  self.show_audio_settings)

        hm = mb.addMenu("Help")
        hm.addAction("Documentation", self.show_documentation)
        hm.addAction("About",         self.show_about)

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

        lo.addWidget(_hline())

        # TRIM knob
        trim_lo, _ = _knob_col("TRIM", 60, 48)
        lo.addLayout(trim_lo)

        lo.addWidget(_hline())

        # EQ knobs
        eq_lo = QVBoxLayout()
        eq_lo.setSpacing(2)
        for eq_name, eq_val in (("HI", 50), ("MID", 50), ("LOW", 50)):
            klo, _ = _knob_col(eq_name, eq_val, 44)
            eq_lo.addLayout(klo)
        lo.addLayout(eq_lo)

        lo.addWidget(_section_label("EQ"))
        lo.addWidget(_hline())

        # Level meter + COLOR knob side by side
        meter_row = QHBoxLayout()
        meter_row.setSpacing(8)

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

        # CUE button
        cue_btn = _btn("CUE", "btnCue", checkable=True, min_h=38)
        cue_btn.setMinimumWidth(9999)  # full width
        lo.addWidget(cue_btn)

        # Fader
        fader_wrap = QHBoxLayout()
        fader_wrap.setContentsMargins(0, 4, 0, 0)
        fader = QSlider(Qt.Orientation.Vertical)
        fader.setObjectName("channelFader")
        fader.setMaximum(100)
        fader.setValue(80)
        fader.setMinimumHeight(180)
        fader.setMaximumWidth(50)
        fader_wrap.addStretch()
        fader_wrap.addWidget(fader)
        fader_wrap.addStretch()
        lo.addLayout(fader_wrap)

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

        # BPM
        lo.addWidget(_section_label("BPM"))
        bpm_lbl = QLabel("120")
        bpm_lbl.setObjectName("bpmValue")
        bpm_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lo.addWidget(bpm_lbl)

        ms_lbl = QLabel("2000 ms")
        ms_lbl.setObjectName("msValue")
        ms_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lo.addWidget(ms_lbl)

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

        # TAP + CUE
        tap_cue_row = QHBoxLayout()
        tap_cue_row.setSpacing(8)
        tap_btn = _btn("TAP", "btnTap", min_w=56, min_h=56)
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

        right_knobs = QVBoxLayout()
        right_knobs.setSpacing(4)
        for label in ("BALANCE", "BOOTH"):
            klo, _ = _knob_col(label, 50, 40)
            right_knobs.addLayout(klo)
        master_row.addLayout(right_knobs)
        master_row.addStretch()
        lo.addLayout(master_row)

        lo.addStretch()

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

        b_lbl = QLabel("B  》")
        b_lbl.setStyleSheet("color:#ff8800; font-size:13px; font-weight:bold; background:transparent;")
        lo.addWidget(b_lbl)

        lo.addSpacing(20)
        lo.addWidget(_section_label("Curve"))
        for shape in ("⌒", "—", "⌓"):
            b = QPushButton(shape)
            b.setCheckable(True)
            b.setFixedSize(QSize(28, 28))
            b.setStyleSheet("""
                QPushButton { background:#1a1a1a; color:#555; border:1px solid #2e2e2e;
                    border-radius:3px; font-size:12px; }
                QPushButton:checked { color:#ff8800; border-color:#ff8800; }
            """)
            lo.addWidget(b)

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
    #  EFFECTS TAB
    # ════════════════════════════════════════════════════════════════════════
    def create_effects_panel(self) -> QWidget:
        root = QWidget()
        root.setStyleSheet("background:transparent;")
        lo = QVBoxLayout(root)
        lo.setContentsMargins(4, 4, 4, 4)
        lo.setSpacing(8)

        main_frame = QFrame()
        main_frame.setObjectName("panelLeft")
        main_lo = QVBoxLayout(main_frame)
        main_lo.setContentsMargins(16, 14, 16, 14)
        main_lo.setSpacing(8)

        main_lo.addWidget(_panel_title("Beat Effects"))

        effects = [
            ("Echo",       "delay/repeat"),
            ("Reverb",     "room/space"),
            ("Chorus",     "shimmer/width"),
            ("Flanger",    "sweep/comb"),
            ("Phaser",     "phase shift"),
            ("Distortion", "overdrive/clip"),
            ("Delay",      "multi-tap"),
        ]

        for name, hint in effects:
            row_frame = QFrame()
            row_frame.setObjectName("glassCard")
            row_lo = QHBoxLayout(row_frame)
            row_lo.setContentsMargins(12, 8, 12, 8)
            row_lo.setSpacing(12)

            chk = QCheckBox(name)
            chk.setMinimumWidth(100)
            row_lo.addWidget(chk)

            hl = QLabel(hint)
            hl.setMinimumWidth(90)
            row_lo.addWidget(hl)

            for param in ("Mix", "Time"):
                row_lo.addWidget(QLabel(f"{param}:"))
                sl = QSlider(Qt.Orientation.Horizontal)
                sl.setMaximum(100)
                sl.setValue(50 if param == "Mix" else 30)
                sl.setMinimumWidth(110)
                row_lo.addWidget(sl)

            row_lo.addStretch()
            main_lo.addWidget(row_frame)

        lo.addWidget(main_frame)
        lo.addStretch()
        return root

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
    #  CONTROLLERS TAB
    # ════════════════════════════════════════════════════════════════════════
    def create_controller_panel(self) -> QWidget:
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

        panel_lo.addWidget(_panel_title("MIDI Controller Configuration"))

        ctrl_row = QHBoxLayout()
        ctrl_row.setSpacing(8)
        ctrl_row.addWidget(QLabel("Controller:"))
        combo = _combo(["— Select Controller —"])
        ctrl_row.addWidget(combo)
        ctrl_row.addWidget(QPushButton("Detect Devices"))
        ctrl_row.addStretch()
        panel_lo.addLayout(ctrl_row)

        panel_lo.addWidget(_panel_title("MIDI Mapping"))
        mapping = QLabel("  Drag & drop MIDI controls to map them\n\n  No mappings configured")
        mapping.setObjectName("mappingArea")
        mapping.setMinimumHeight(280)
        mapping.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_lo.addWidget(mapping)

        lo.addWidget(panel)
        lo.addStretch()
        return root

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
    def open_track(self):
        p, _ = QFileDialog.getOpenFileName(
            self, "Open Track", "", "Audio Files (*.mp3 *.wav *.flac *.ogg)")
        if p:
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
