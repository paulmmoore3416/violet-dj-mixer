"""
MIDI and hardware controller support
"""

import logging
import rtmidi

logger = logging.getLogger(__name__)

class ControllerManager:
    """Manages MIDI controllers and hardware devices"""
    
    SUPPORTED_CONTROLLERS = {
        'pioneer_ddj': 'Pioneer DDJ Series',
        'pioneer_cdj': 'Pioneer CDJ Series',
        'pioneer_djm': 'Pioneer DJM Mixers',
        'numark': 'Numark Controllers',
        'reloop': 'Reloop Controllers',
        'traktor': 'Native Instruments Traktor',
        'denon': 'Denon DJ Controllers',
        'rane': 'Rane Seventy Series',
        'xone': 'Allen & Heath Xone',
        'akai': 'Akai Professional',
        'technics': 'Technics SL-1200',
        'stanton': 'Stanton Turntables',
        'vestax': 'Vestax Controllers',
        'korg': 'Korg Instruments',
        'roland': 'Roland Devices',
        'yamaha': 'Yamaha Instruments',
        'native_instruments': 'Native Instruments',
    }
    
    def __init__(self):
        logger.info("Initializing Controller Manager")
        self.midi_in = rtmidi.MidiIn()
        self.midi_out = rtmidi.MidiOut()
        self.controllers = {}
        self.mappings = {}
    
    def list_available_controllers(self):
        """List all detected MIDI controllers"""
        midi_inputs = self.midi_in.get_ports()
        return midi_inputs if midi_inputs else ['Virtual Input']
    
    def connect_controller(self, controller_name):
        """Connect to a MIDI controller"""
        try:
            ports = self.midi_in.get_ports()
            for i, port in enumerate(ports):
                if controller_name.lower() in port.lower():
                    self.midi_in.open_port(i)
                    logger.info(f"Connected to controller: {controller_name}")
                    return True
        except Exception as e:
            logger.error(f"Failed to connect controller: {e}")
        return False
    
    def detect_controllers(self):
        """Auto-detect connected controllers"""
        detected = []
        try:
            ports = self.midi_in.get_ports()
            for port in ports:
                for controller_type, friendly_name in self.SUPPORTED_CONTROLLERS.items():
                    if any(keyword in port.lower() for keyword in 
                           [controller_type.replace('_', ' '), friendly_name.lower()]):
                        detected.append({
                            'type': controller_type,
                            'name': friendly_name,
                            'port': port
                        })
            
            logger.info(f"Detected {len(detected)} controllers")
        except Exception as e:
            logger.warning(f"Controller detection error: {e}")
        
        return detected
    
    def map_control(self, controller_id, midi_cc, action):
        """Map a MIDI control to an action"""
        if controller_id not in self.mappings:
            self.mappings[controller_id] = {}
        
        self.mappings[controller_id][midi_cc] = action
        logger.info(f"Mapped MIDI CC {midi_cc} to {action}")
    
    def load_mapping_profile(self, profile_path):
        """Load a controller mapping profile"""
        logger.info(f"Loading mapping profile: {profile_path}")
    
    def save_mapping_profile(self, profile_path):
        """Save current mapping profile"""
        logger.info(f"Saving mapping profile: {profile_path}")
