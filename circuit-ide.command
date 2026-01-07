#!/bin/bash
# Circuit IDE Launcher
# Double-click this file to launch Circuit IDE in its own terminal window

cd "$(dirname "$0")"

# Clear screen and set title
clear
echo -e "\033]0;Circuit IDE v5.0\007"

# Run the IDE
python3.11 -m circuit_ide "$@"
