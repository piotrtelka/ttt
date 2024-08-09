#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

pip install -r requirements.txt

TTT_SCRIPT="$SCRIPT_DIR/ttt"
TTT_COMPLETION_SCRIPT="$SCRIPT_DIR/ttt_completion.bash"
BASHRC="$HOME/.bashrc"

# Make the ttt script executable
chmod +x $TTT_SCRIPT

# Add the script directory to PATH if not already present
if ! grep -q "$SCRIPT_DIR" <<< "$PATH"; then
    echo "export PATH=\"\$PATH:$SCRIPT_DIR\"" >> $BASHRC
    echo "Added $SCRIPT_DIR to PATH in $BASHRC"
fi

# Add source to bashrc for autocompletion
if ! grep -q "$TTT_COMPLETION_SCRIPT" "$BASHRC"; then
    echo "source $TTT_COMPLETION_SCRIPT" >> $BASHRC
    echo "Added source command for $TTT_COMPLETION_SCRIPT to $BASHRC"
fi

# Reload bashrc to apply changes
source $BASHRC

echo "Installation complete. Please restart your terminal or run 'source $BASHRC' to apply changes."
