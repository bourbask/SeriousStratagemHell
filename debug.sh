#!/bin/bash

# Define function to kill the fluidsynth process
kill_music() {
    system_platform=$(uname)
    if [ "$system_platform" == "Linux" ] || [ "$system_platform" == "Darwin" ]; then
        # Use pgrep to find the PID of the process
        pid=$(pgrep fluidsynth)
        if [ -n "$pid" ]; then
            kill "$pid"
            echo "fluidsynth process has been terminated."
        else
            echo "fluidsynth process is not running."
        fi
    else
        echo "Unsupported platform."
    fi
}

# Define function to generate WAV music
generate_music() {
    python3 Tools/music_generator_hd2_theme.py
}

# Parse command-line arguments
case "$1" in
    --kill_music)
        kill_music
        ;;
    --generate_music)
        generate_music
        ;;
    *)
        echo "Usage: $0 [--kill_music] [--generate_music]"
        exit 1
        ;;
esac

exit 0
