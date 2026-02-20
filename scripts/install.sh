#!/bin/bash
# Installation script for Violet DJ Mixer from source

set -e

echo "======================================"
echo "Violet DJ Mixer - Installation Script"
echo "======================================"
echo ""

# Check if running on Ubuntu
if [ ! -f /etc/lsb-release ]; then
    echo "❌ Error: This script is designed for Ubuntu/Debian systems"
    exit 1
fi

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then 
    echo "ℹ️  Some steps require sudo access"
    echo "Please run: sudo ./scripts/install.sh"
fi

echo "Step 1: Installing system dependencies..."

# Update package manager
apt-get update

# Install required packages
apt-get install -y \
    python3 python3-pip python3-dev python3-venv \
    pulseaudio alsa-utils libasound2-dev \
    libpulse-dev \
    bluetooth bluez libbluetooth-dev \
    qt6-base-dev libqt6core6 \
    libssl-dev libffi-dev \
    git build-essential \
    ffmpeg \
    libavformat-dev libavcodec-dev \
    libsndfile1-dev

echo "✅ System dependencies installed"
echo ""

echo "Step 2: Creating virtual environment..."

# Create virtual environment
python3 -m venv /opt/violet-dj/venv

# Activate virtual environment
source /opt/violet-dj/venv/bin/activate

echo "✅ Virtual environment created"
echo ""

echo "Step 3: Installing Python dependencies..."

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install requirements
pip install -r requirements.txt

echo "✅ Python dependencies installed"
echo ""

echo "Step 4: Setting up application files..."

# Create directories
mkdir -p /opt/violet-dj
mkdir -p /usr/share/applications
mkdir -p /usr/share/icons/hicolor/256x256/apps
mkdir -p /usr/local/bin
mkdir -p ~/.violet_dj
mkdir -p ~/.config/violet-dj

# Copy files
cp -r src /opt/violet-dj/
cp main.py /opt/violet-dj/
cp requirements.txt /opt/violet-dj/
cp LICENSE /opt/violet-dj/

# Create executable
cat > /usr/local/bin/violet-dj << 'EOF'
#!/bin/bash
source /opt/violet-dj/venv/bin/activate
python3 /opt/violet-dj/main.py "$@"
EOF
chmod +x /usr/local/bin/violet-dj

# Create desktop entry
cat > /usr/share/applications/violet-dj.desktop << 'EOF'
[Desktop Entry]
Name=Violet DJ Mixer
Comment=Professional Digital Mixing Board
Exec=violet-dj
Icon=audio-mixer
Type=Application
Categories=Audio;Mixer;
Terminal=false
StartupNotify=true
EOF

echo "✅ Application files installed"
echo ""

echo "Step 5: Configuring user permissions..."

# Add current user to audio group
CURRENT_USER=${SUDO_USER:-$(whoami)}
if [ "$CURRENT_USER" != "root" ]; then
    if getent group audio > /dev/null 2>&1; then
        usermod -a -G audio $CURRENT_USER
        echo "✅ Added $CURRENT_USER to audio group"
    fi
fi

# Configure udev rules for MIDI
cat > /etc/udev/rules.d/90-violet-dj-midi.rules << 'UDEVRULES'
# Violet DJ Mixer - MIDI Device Rules
SUBSYSTEM=="usb", MODE:="0666", GROUP:="audio"
SUBSYSTEM=="sound", MODE:="0666", GROUP:="audio"
UDEVRULES

udevadm control --reload-rules
udevadm trigger

echo "✅ Permissions configured"
echo ""

echo "======================================"
echo "✅ Installation Complete!"
echo "======================================"
echo ""
echo "To launch Violet DJ Mixer:"
echo "  violet-dj"
echo ""
echo "To launch from source:"
echo "  cd /opt/violet-dj"
echo "  source venv/bin/activate"
echo "  python3 main.py"
echo ""
echo "Documentation: /usr/share/doc/violet-dj/"
echo "Configuration: ~/.config/violet-dj/"
echo ""
