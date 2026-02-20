#!/usr/bin/env python3
"""
Violet DJ Mixer - Professional Digital Mixing Board for Ubuntu
A free, open-source DJ mixing software compatible with industry-standard controllers.

Author: Violet DJ Community
License: GPL-3.0-or-later
"""

import sys
import os
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.expanduser('~/.violet_dj/violet_dj.log')),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main entry point for Violet DJ Mixer"""
    logger.info("Starting Violet DJ Mixer...")
    
    try:
        from src.ui.main_window import VioletDJMixer
        from PyQt6.QtWidgets import QApplication
        
        app = QApplication(sys.argv)
        mixer = VioletDJMixer()
        mixer.show()
        
        sys.exit(app.exec())
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        print("Error: Missing required dependencies.")
        print("Please install: sudo apt install violet-dj")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
