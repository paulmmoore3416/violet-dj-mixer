#!/bin/bash
# Build script for creating .deb Ubuntu package

set -e

VERSION="2.0.0"
ARCHITECTURE="amd64"
PROJECT_NAME="violet-dj-mixer"
MAINTAINER="Violet DJ Community <support@violet-dj.github.io>"

echo "Building Violet DJ Mixer $VERSION .deb package..."

# Create build directory
mkdir -p build/${PROJECT_NAME}_${VERSION}_${ARCHITECTURE}
cd build/${PROJECT_NAME}_${VERSION}_${ARCHITECTURE}

# Create directory structure
mkdir -p DEBIAN
mkdir -p usr/bin
mkdir -p usr/share/applications
mkdir -p usr/share/icons/hicolor/256x256/apps
mkdir -p usr/share/doc/${PROJECT_NAME}
mkdir -p opt/violet-dj

# Copy application files
echo "Copying application files..."
cp -r ../../src opt/violet-dj/
cp ../../main.py opt/violet-dj/
cp ../../requirements.txt opt/violet-dj/
cp ../../LICENSE opt/violet-dj/

# Create executable wrapper
cat > usr/bin/violet-dj << 'EOF'
#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, '/opt/violet-dj')
from main import main
if __name__ == '__main__':
    main()
EOF
chmod +x usr/bin/violet-dj

# Create desktop entry
cat > usr/share/applications/violet-dj.desktop << 'EOF'
[Desktop Entry]
Name=Violet DJ Mixer
Comment=Professional Digital Mixing Board
Exec=violet-dj
Icon=violet-dj
Type=Application
Categories=Audio;Mixer;AudioVideo;
Terminal=false
StartupNotify=true
Keywords=dj;mixer;audio;music;
EOF

# Create control file
cat > DEBIAN/control << EOF
Package: ${PROJECT_NAME}
Version: ${VERSION}
Architecture: ${ARCHITECTURE}
Maintainer: ${MAINTAINER}
Depends: python3 (>= 3.8), python3-pyqt6, python3-pyaudio, python3-pip, pulseaudio, alsa-utils, bluez, bluetooth
Description: Professional Digital DJ Mixing Board for Ubuntu
 Violet DJ Mixer is a free, open-source DJ mixing software for Ubuntu.
 Compatible with all industry-standard DJ controllers and audio devices.
 .
 Features:
  - Professional mixing board with multiple channels and effects
  - Support for USB, Bluetooth, and Wi-Fi devices
  - Compatible with Pioneer, Numark, Reloop, and 100+ controllers
  - Real-time waveform visualization
  - Multiple audio format support (MP3, WAV, FLAC, etc.)
  - Customizable MIDI mapping
  - Built-in audio effects and equalizer
EOF

# Create postinst script
cat > DEBIAN/postinst << 'EOF'
#!/bin/bash
set -e

# Create user config directory
mkdir -p /root/.violet_dj
mkdir -p /root/.config/violet-dj

# Note: All Python dependencies are installed via apt (pyqt6, pyaudio, etc.)
# No additional pip installation needed

# Create symlink for easy launching
ln -sf /opt/violet-dj/main.py /usr/local/bin/violet-dj-mixer

# Install udev rules for MIDI devices
cat > /etc/udev/rules.d/90-violet-dj-midi.rules << 'UDEVRULES'
# Violet DJ Mixer - MIDI device rules
SUBSYSTEM=="usb", ATTRS{idProduct}=="001e", ATTRS{idVendor}=="0582", MODE:="0666"
SUBSYSTEM=="usb", ATTRS{idProduct}=="1010", ATTRS{idVendor}=="09e8", MODE:="0666"
SUBSYSTEM=="usb", ATTRS{idProduct}=="0010", ATTRS{idVendor}=="0944", MODE:="0666"
UDEVRULES

# Reload udev rules
udevadm control --reload-rules
udevadm trigger

# Add user to audio group
if [ -f /etc/group ]; then
    if getent group audio > /dev/null 2>&1; then
        # usermod would be done by system administrator if needed
        echo "Remember to add your user to audio group: sudo usermod -a -G audio \$USER"
    fi
fi

echo "Violet DJ Mixer installed successfully!"
echo "Run 'violet-dj' to launch the application"
EOF

chmod +x DEBIAN/postinst

# Create preinst script  
cat > DEBIAN/preinst << 'EOF'
#!/bin/bash
# Ensure previous installation can be upgraded
if [ -d /opt/violet-dj ]; then
    chmod -R 755 /opt/violet-dj || true
fi
EOF

chmod +x DEBIAN/preinst

# Create copyright file
cat > usr/share/doc/${PROJECT_NAME}/copyright << 'EOF'
Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: Violet DJ Mixer
Upstream-Contact: Violet DJ Community <support@violet-dj.github.io>
Source: https://github.com/violet-dj/violet-dj-mixer

Files: *
Copyright: 2024 Violet DJ Community
License: GPL-3.0-or-later

License: GPL-3.0-or-later
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 .
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 .
 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <https://www.gnu.org/licenses/>.
EOF

# Create changelog
cat > usr/share/doc/${PROJECT_NAME}/changelog.Debian.gz << 'EOF'
violet-dj-mixer (1.0.0) stable; urgency=medium

  * Initial release
  * Professional DJ mixing board with dual decks
  * Support for 100+ MIDI controllers
  * USB, Bluetooth, and Wi-Fi device support
  * Real-time waveform visualization
  * Complete audio codec support
  * Comprehensive documentation

 -- Violet DJ Community <support@violet-dj.github.io>  Thu, 20 Feb 2024 10:00:00 +0000
EOF

# Build the .deb package
echo "Building .deb package..."
cd ..
dpkg-deb --build ${PROJECT_NAME}_${VERSION}_${ARCHITECTURE}

# Move to dist folder
mkdir -p ../../dist
mv ${PROJECT_NAME}_${VERSION}_${ARCHITECTURE}.deb ../../dist/

echo "✅ Package created: dist/${PROJECT_NAME}_${VERSION}_${ARCHITECTURE}.deb"
echo ""
echo "Installation:"
echo "  sudo apt install ./dist/${PROJECT_NAME}_${VERSION}_${ARCHITECTURE}.deb"
