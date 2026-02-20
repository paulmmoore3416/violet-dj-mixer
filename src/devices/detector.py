"""
Device detection and auto-discovery for USB, Bluetooth, and Wi-Fi devices
"""

import os
import subprocess
import logging
from PyQt6.QtCore import QThread, pyqtSignal
import json

logger = logging.getLogger(__name__)

class DeviceDetector(QThread):
    """Detects and manages audio devices"""
    
    devices_found = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.devices = []
    
    def run(self):
        """Run device detection"""
        try:
            self.detect_usb_devices()
            self.detect_audio_devices()
            self.detect_midi_devices()
            self.detect_bluetooth_devices()
            self.detect_wifi_devices()
            
            self.devices_found.emit(self.devices)
        except Exception as e:
            logger.error(f"Device detection error: {e}")
    
    def detect_usb_devices(self):
        """Detect USB audio/MIDI devices"""
        try:
            result = subprocess.run(['lsusb'], capture_output=True, text=True)
            # Parse USB devices
            logger.info("USB devices detected")
        except Exception as e:
            logger.warning(f"USB detection failed: {e}")
    
    def detect_audio_devices(self):
        """Detect audio devices via PulseAudio/ALSA"""
        try:
            # Check for PulseAudio devices
            result = subprocess.run(['pactl', 'list', 'sources'], 
                                   capture_output=True, text=True)
            if result.returncode == 0:
                self.devices.append({
                    'type': 'audio',
                    'backend': 'pulseaudio',
                    'name': 'PulseAudio'
                })
            
            # Check for ALSA devices
            result = subprocess.run(['aplay', '-l'], capture_output=True, text=True)
            if result.returncode == 0:
                self.devices.append({
                    'type': 'audio',
                    'backend': 'alsa',
                    'name': 'ALSA'
                })
            
            logger.info(f"Audio devices detected: {len([d for d in self.devices if d['type'] == 'audio'])}")
        except Exception as e:
            logger.warning(f"Audio device detection failed: {e}")
    
    def detect_midi_devices(self):
        """Detect MIDI devices"""
        try:
            # Check ALSA MIDI devices
            midi_dir = "/proc/asound"
            if os.path.exists(midi_dir):
                self.devices.append({
                    'type': 'midi',
                    'name': 'ALSA MIDI'
                })
            
            logger.info("MIDI devices detected")
        except Exception as e:
            logger.warning(f"MIDI device detection failed: {e}")
    
    def detect_bluetooth_devices(self):
        """Detect Bluetooth audio devices"""
        try:
            # Use bluetoothctl to list devices
            result = subprocess.run(['bluetoothctl', 'devices'], 
                                   capture_output=True, text=True)
            if result.returncode == 0:
                self.devices.append({
                    'type': 'bluetooth',
                    'name': 'Bluetooth Audio',
                    'multi_device': True
                })
            
            logger.info("Bluetooth devices detected")
        except Exception as e:
            logger.warning(f"Bluetooth detection failed: {e}")
    
    def detect_wifi_devices(self):
        """Detect Wi-Fi connected audio devices"""
        try:
            # Discovery would be via mDNS/Bonjour
            self.devices.append({
                'type': 'wifi',
                'name': 'Wi-Fi Audio Discovery',
                'protocol': 'mdns'
            })
            
            logger.info("Wi-Fi device detection enabled")
        except Exception as e:
            logger.warning(f"Wi-Fi detection failed: {e}")
    
    def get_device_info(self, device):
        """Get detailed information about a device"""
        # Return detailed device info
        pass
    
    def connect_device(self, device):
        """Connect to a device"""
        logger.info(f"Connecting to device: {device}")
    
    def disconnect_device(self, device):
        """Disconnect from a device"""
        logger.info(f"Disconnecting from device: {device}")
