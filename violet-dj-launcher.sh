#!/bin/bash
# Violet DJ Mixer - Professional Launcher
# Handles snap library conflicts on Ubuntu systems

set -e

# Store original environment
ORIGINAL_PATH="$PATH"
ORIGINAL_LD_LIBRARY_PATH="$LD_LIBRARY_PATH"
ORIGINAL_PYTHONPATH="$PYTHONPATH"

# Clear problematic snap environment variables
unset SNAP
unset SNAP_NAME
unset SNAP_REVISION
unset SNAP_LIBRARY_PATH
unset SNAPCRAFT_SETUP_DONE
unset SNAPCRAFT_BUILD_INFO

# Use system libraries instead of snap's
export LD_LIBRARY_PATH="/usr/lib/x86_64-linux-gnu:/usr/lib:/lib:${ORIGINAL_LD_LIBRARY_PATH}"
export PYTHONPATH="/usr/lib/python3/dist-packages:${ORIGINAL_PYTHONPATH}"

# Ensure config directories exist
mkdir -p ~/.violet_dj
mkdir -p ~/.config/violet-dj

# Launch application
echo "🎛️  Starting Violet DJ Mixer..."
exec /usr/bin/python3 /opt/violet-dj/main.py "$@"
