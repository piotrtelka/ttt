#!/bin/bash

# Get the directory where the install script is located
SCRIPT_DIR=$(dirname "$(realpath "$0")")
TTT_SCRIPT="$SCRIPT_DIR/ttt"
TTT_COMPLETION_SCRIPT="$SCRIPT_DIR/ttt_completion.bash"
BASHRC="$HOME/.bashrc"
PROFILE="$HOME/.profile"

# Make the ttt script executable
chmod +x $TTT_SCRIPT

# Add the script directory to PATH if not already present
if ! grep -q "$SCRIPT_DIR" <<< "$PATH"; then
    echo "export PATH=\"\$PATH:$SCRIPT_DIR\"" >> $PROFILE
    echo "Added $SCRIPT_DIR to PATH in $PROFILE"
fi

# Add source to bashrc for autocompletion
if ! grep -q "$TTT_COMPLETION_SCRIPT" "$BASHRC"; then
    echo "source $TTT_COMPLETION_SCRIPT" >> $BASHRC
    echo "Added source command for $TTT_COMPLETION_SCRIPT to $BASHRC"
fi

# Reload bashrc to apply changes
source $BASHRC

echo "Installation complete. Please restart your terminal or run 'source $BASHRC' to apply changes."
