"""
Main window for Violet DJ Mixer with mixing board interface
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTabWidget, QLabel, QPushButton, QSlider, QDial,
                             QGridLayout, QComboBox, QSpinBox, QDoubleSpinBox,
                             QCheckBox, QProgressBar, QStatusBar, QMenuBar,
                             QMenu, QMessageBox, QFileDialog, QDialog)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread, QSize
from PyQt6.QtGui import QIcon, QFont, QColor, QPalette
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
import logging

logger = logging.getLogger(__name__)

class VioletDJMixer(QMainWindow):
    """Main application window for Violet DJ Mixer"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Violet DJ Mixer - Professional Digital Mixing Board")
        self.setGeometry(100, 100, 1600, 900)
        
        # Apply styling
        self.setStyle()
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create main tab interface
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Add mixer panel
        self.tabs.addTab(self.create_mixer_panel(), "Mixer")
        
        # Add device panel
        self.tabs.addTab(self.create_device_panel(), "Devices")
        
        # Add controller panel
        self.tabs.addTab(self.create_controller_panel(), "Controllers")
        
        # Add effects panel
        self.tabs.addTab(self.create_effects_panel(), "Effects")
        
        # Add settings panel
        self.tabs.addTab(self.create_settings_panel(), "Settings")
        
        # Create status bar
        self.statusBar().showMessage("Ready | No devices connected")
        
        # Initialize device detection
        self.device_detector = None
        self.start_device_detection()
        
        logger.info("Violet DJ Mixer initialized successfully")
    
    def setStyle(self):
        """Apply professional dark theme styling"""
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(45, 45, 48))
        dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(30, 30, 35))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 60))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
        dark_palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 60))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
        
        self.setPalette(dark_palette)
        
        # Set font
        font = QFont("Segoe UI, Ubuntu")
        font.setPointSize(10)
        self.setFont(font)
    
    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction("Open Track", self.open_track)
        file_menu.addAction("Open Playlist", self.open_playlist)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction("Preferences", self.show_preferences)
        edit_menu.addAction("Controller Mapping", self.show_controller_mapping)
        
        # View menu
        view_menu = menubar.addMenu("View")
        view_menu.addAction("Toggle Visualization")
        view_menu.addAction("Full Screen")
        
        # Device menu
        device_menu = menubar.addMenu("Devices")
        device_menu.addAction("Refresh Devices", self.refresh_devices)
        device_menu.addAction("Audio Settings", self.show_audio_settings)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("Documentation", self.show_documentation)
        help_menu.addAction("About Violet DJ", self.show_about)
    
    def create_mixer_panel(self):
        """Create main mixer panel with channels, sliders, knobs"""
        mixer_widget = QWidget()
        layout = QHBoxLayout(mixer_widget)
        
        # Master channel
        master_group = self.create_channel("Master")
        layout.addWidget(master_group)
        
        # DJ Deck 1
        deck1_group = self.create_deck("Deck 1")
        layout.addWidget(deck1_group)
        
        # Mixer Controls (EQ, Crossfader, etc)
        mixer_controls = self.create_mixer_controls()
        layout.addWidget(mixer_controls)
        
        # DJ Deck 2
        deck2_group = self.create_deck("Deck 2")
        layout.addWidget(deck2_group)
        
        # Visualizer
        visualizer = self.create_visualizer()
        layout.addWidget(visualizer)
        
        return mixer_widget
    
    def create_channel(self, name):
        """Create a mixer channel with fader, knobs, buttons"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        layout.addWidget(QLabel(name))
        
        # Level meter
        meter = QProgressBar()
        meter.setMaximum(100)
        meter.setValue(30)
        layout.addWidget(meter)
        
        # Fader (vertical slider)
        fader = QSlider(Qt.Orientation.Vertical)
        fader.setMaximum(100)
        fader.setValue(75)
        fader.setMinimumHeight(250)
        layout.addWidget(fader)
        
        # Knobs for EQ
        eq_layout = QHBoxLayout()
        for label in ['Low', 'Mid', 'High']:
            knob_layout = QVBoxLayout()
            knob_layout.addWidget(QLabel(label, alignment=Qt.AlignmentFlag.AlignCenter))
            knob = QDial()
            knob.setMaximum(100)
            knob.setValue(50)
            knob.setMaximumSize(QSize(60, 60))
            knob_layout.addWidget(knob)
            eq_layout.addLayout(knob_layout)
        
        layout.addLayout(eq_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        for btn_name in ['Cue', 'Solo', 'Mute']:
            btn = QPushButton(btn_name)
            btn.setCheckable(True)
            btn.setMaximumWidth(80)
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)
        
        return widget
    
    def create_deck(self, name):
        """Create a DJ deck with track info and controls"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        layout.addWidget(QLabel(f"<b>{name}</b>"))
        
        # Track info
        track_info = QLabel("No track loaded")
        track_info.setWordWrap(True)
        layout.addWidget(track_info)
        
        # Waveform display area
        waveform_label = QLabel("[Waveform Display Area]")
        waveform_label.setMinimumHeight(100)
        waveform_label.setStyleSheet("border: 2px solid #2a82da; border-radius: 4px;")
        layout.addWidget(waveform_label)
        
        # Playback controls
        control_layout = QHBoxLayout()
        for btn_name in ['Load', 'Play', 'Pause', 'Cue']:
            btn = QPushButton(btn_name)
            btn.setMaximumWidth(70)
            control_layout.addWidget(btn)
        layout.addLayout(control_layout)
        
        # Pitch/Speed control
        pitch_layout = QVBoxLayout()
        pitch_layout.addWidget(QLabel("Pitch:"))
        pitch_slider = QSlider(Qt.Orientation.Horizontal)
        pitch_slider.setMaximum(200)
        pitch_slider.setValue(100)
        pitch_layout.addWidget(pitch_slider)
        layout.addLayout(pitch_layout)
        
        # Position
        pos_layout = QVBoxLayout()
        pos_layout.addWidget(QLabel("Position:"))
        pos_slider = QSlider(Qt.Orientation.Horizontal)
        pos_slider.setMaximum(100)
        pos_layout.addWidget(pos_slider)
        layout.addLayout(pos_layout)
        
        return widget
    
    def create_mixer_controls(self):
        """Create main mixer controls"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        layout.addWidget(QLabel("<b>Mixer</b>"))
        
        # Crossfader
        xfade_layout = QVBoxLayout()
        xfade_layout.addWidget(QLabel("Crossfader:"))
        xfader = QSlider(Qt.Orientation.Horizontal)
        xfader.setMaximum(100)
        xfader.setValue(50)
        xfade_layout.addWidget(xfader)
        layout.addLayout(xfade_layout)
        
        # Master volume
        master_layout = QVBoxLayout()
        master_layout.addWidget(QLabel("Master:"))
        master = QSlider(Qt.Orientation.Vertical)
        master.setMaximum(100)
        master.setValue(80)
        master.setMinimumHeight(150)
        master_layout.addWidget(master)
        layout.addLayout(master_layout)
        
        layout.addStretch()
        
        return widget
    
    def create_visualizer(self):
        """Create audio visualizer"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        layout.addWidget(QLabel("<b>Visualizer</b>"))
        
        # Placeholder for waveform visualization
        viz_area = QLabel("[Audio Visualization\nWaveform & Spectrum Analyzer]")
        viz_area.setMinimumSize(200, 200)
        viz_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        viz_area.setStyleSheet("border: 2px solid #2a82da; border-radius: 4px; background: #1e1e23;")
        layout.addWidget(viz_area)
        
        return widget
    
    def create_device_panel(self):
        """Create device detection and management panel"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        layout.addWidget(QLabel("<b>Connected Devices</b>"))
        
        # Device list
        device_list_label = QLabel("Scanning for devices...")
        device_list_label.setStyleSheet("border: 1px solid #2a82da; padding: 10px; border-radius: 4px;")
        device_list_label.setMinimumHeight(200)
        layout.addWidget(device_list_label)
        
        # Controls
        control_layout = QHBoxLayout()
        control_layout.addWidget(QPushButton("Refresh"))
        control_layout.addWidget(QPushButton("Remove Selected"))
        control_layout.addWidget(QPushButton("Configure"))
        layout.addLayout(control_layout)
        
        # Device details
        layout.addWidget(QLabel("<b>Device Details</b>"))
        details = QLabel("Select a device to view details")
        details.setStyleSheet("border: 1px solid #2a82da; padding: 10px; border-radius: 4px;")
        details.setMinimumHeight(150)
        layout.addWidget(details)
        
        return widget
    
    def create_controller_panel(self):
        """Create MIDI controller mapping panel"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        layout.addWidget(QLabel("<b>MIDI Controller Configuration</b>"))
        
        # Controller selection
        control_layout = QHBoxLayout()
        control_layout.addWidget(QLabel("Controller:"))
        control_layout.addWidget(QComboBox())
        control_layout.addWidget(QPushButton("Detect"))
        layout.addLayout(control_layout)
        
        # Mapping table
        mapping_label = QLabel("MIDI Control Mappings")
        layout.addWidget(mapping_label)
        
        mapping_area = QLabel("[MIDI Mapping Table - Drag & Drop Support]")
        mapping_area.setStyleSheet("border: 1px solid #2a82da; padding: 10px; border-radius: 4px;")
        mapping_area.setMinimumHeight(300)
        layout.addWidget(mapping_area)
        
        return widget
    
    def create_effects_panel(self):
        """Create audio effects panel"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        layout.addWidget(QLabel("<b>Audio Effects</b>"))
        
        # Effects selection
        effects = ['Echo', 'Reverb', 'Chorus', 'Flanger', 'Phaser', 'Distortion', 'Delay']
        
        for effect in effects:
            effect_layout = QHBoxLayout()
            effect_layout.addWidget(QCheckBox(effect))
            effect_layout.addWidget(QLabel("Mix:"))
            effect_layout.addWidget(QSlider(Qt.Orientation.Horizontal))
            effect_layout.addWidget(QLabel("Time:"))
            effect_layout.addWidget(QSlider(Qt.Orientation.Horizontal))
            layout.addLayout(effect_layout)
        
        layout.addStretch()
        
        return widget
    
    def create_settings_panel(self):
        """Create settings panel"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        layout.addWidget(QLabel("<b>Settings</b>"))
        
        # Audio settings
        layout.addWidget(QLabel("<b>Audio Configuration</b>"))
        
        audio_layout = QVBoxLayout()
        
        # Audio backend
        backend_layout = QHBoxLayout()
        backend_layout.addWidget(QLabel("Audio Backend:"))
        backend_combo = QComboBox()
        backend_combo.addItems(['PulseAudio', 'ALSA', 'JACK'])
        backend_layout.addWidget(backend_combo)
        audio_layout.addLayout(backend_layout)
        
        # Sample rate
        sample_layout = QHBoxLayout()
        sample_layout.addWidget(QLabel("Sample Rate:"))
        sample_combo = QComboBox()
        sample_combo.addItems(['44100 Hz', '48000 Hz', '96000 Hz'])
        sample_combo.setCurrentText('48000 Hz')
        sample_layout.addWidget(sample_combo)
        audio_layout.addLayout(sample_layout)
        
        # Buffer size
        buffer_layout = QHBoxLayout()
        buffer_layout.addWidget(QLabel("Buffer Size:"))
        buffer_spin = QSpinBox()
        buffer_spin.setValue(256)
        buffer_layout.addWidget(buffer_spin)
        audio_layout.addLayout(buffer_layout)
        
        layout.addLayout(audio_layout)
        
        # Bluetooth settings
        layout.addWidget(QLabel("<b>Bluetooth Configuration</b>"))
        layout.addWidget(QCheckBox("Enable Bluetooth Audio Input"))
        layout.addWidget(QCheckBox("Enable Multiple Bluetooth Connections"))
        layout.addWidget(QCheckBox("Auto-connect to paired devices"))
        
        # Network settings
        layout.addWidget(QLabel("<b>Network Configuration</b>"))
        layout.addWidget(QCheckBox("Enable Wi-Fi Device Discovery"))
        layout.addWidget(QCheckBox("Allow Remote Control"))
        
        layout.addStretch()
        
        return widget
    
    def start_device_detection(self):
        """Start device detection in background"""
        from src.devices.detector import DeviceDetector
        
        self.device_detector = DeviceDetector()
        self.device_detector.devices_found.connect(self.on_devices_found)
        self.device_detector.start()
    
    def on_devices_found(self, devices):
        """Handle device detection results"""
        count = len(devices)
        self.statusBar().showMessage(f"Ready | {count} device(s) connected")
        logger.info(f"Detected {count} devices")
    
    def open_track(self):
        """Open audio track"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Track", "", 
                                                   "Audio Files (*.mp3 *.wav *.flac *.ogg)")
        if file_path:
            logger.info(f"Loading track: {file_path}")
    
    def open_playlist(self):
        """Open playlist"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Playlist", "", 
                                                   "Playlist Files (*.m3u *.pls)")
        if file_path:
            logger.info(f"Loading playlist: {file_path}")
    
    def show_preferences(self):
        """Show preferences dialog"""
        QMessageBox.information(self, "Preferences", "Preferences dialog - Coming soon!")
    
    def show_controller_mapping(self):
        """Show controller mapping dialog"""
        QMessageBox.information(self, "Controller Mapping", 
                               "Controller mapping dialog - Coming soon!")
    
    def show_audio_settings(self):
        """Show audio settings dialog"""
        QMessageBox.information(self, "Audio Settings", 
                               "Audio settings dialog - Coming soon!")
    
    def show_documentation(self):
        """Open documentation"""
        import webbrowser
        webbrowser.open("https://violet-dj.github.io/docs")
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About Violet DJ Mixer",
                         """<b>Violet DJ Mixer v1.0.0</b><br><br>
                         Professional digital mixing board for Ubuntu<br><br>
                         Free and open-source under GPL-3.0<br><br>
                         For industry-standard DJ equipment<br><br>
                         <a href='https://violet-dj.github.io'>Visit Website</a>""")
    
    def refresh_devices(self):
        """Refresh device list"""
        self.statusBar().showMessage("Scanning for devices...")
        self.start_device_detection()
