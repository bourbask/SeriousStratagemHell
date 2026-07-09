import os
import wave
import math
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Access the environment variable
MUSIC_BASEPATH = os.getenv("MUSIC_BASEPATH")

def generate_music_wav_hd2_theme_progressive():
    # Define the mapping of notes to frequencies
    note_to_frequency = {
        'A': 466,
        'G': 415,
        'F': 370,
        'E': 349,
        'D': 311,
        'C': 277,
        'B': 247,
        'Rest': 0
    }

    # Define the chord progression and rhythm based on the breakdown
    chord_progression = [
        'A', 'G', 'F', 'E', 'D', 'C', 'B', 'A', 'G', 'F', 'E', 'D', 'C', 'B', 'A', 'G',  # Measure 1-16
        'F', 'E', 'D', 'C', 'B', 'A', 'G', 'F', 'E', 'D', 'C', 'B', 'A', 'G', 'F', 'E'   # Measure 17-32
    ]

    # Define the rhythm based on the breakdown
    rhythm = [
        1, 1, 0.5, 0.5, 1, 1, 0.5, 0.5,  # Measure 1-8
        1, 1, 0.5, 0.5, 1, 1, 0.5, 0.5,  # Measure 9-16
        1, 1, 0.5, 0.5, 1, 1, 0.5, 0.5,  # Measure 17-24
        1, 1, 0.5, 0.5, 1, 1, 0.5, 0.5   # Measure 25-32
    ]

    # Define the audio parameters
    SAMPLE_RATE = 44100  # Sample rate in Hz
    BIT_DEPTH = 16  # Bit depth in bits
    CHANNELS = 1  # Number of audio channels (mono)

    # Create a WAV file
    with wave.open(MUSIC_BASEPATH + "stratagem_hell_theme_progressive.wav", 'w') as wave_file:
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(BIT_DEPTH // 8)
        wave_file.setframerate(SAMPLE_RATE)

        # Calculate the number of samples per beat
        samples_per_beat = int((60 / 160) * SAMPLE_RATE)  # Faster tempo for a rock melody

        # Iterate over the music sequence and add the corresponding notes to the WAV file
        for chord, beat in zip(chord_progression, rhythm):
            frequency = note_to_frequency.get(chord, 0)  # Get the frequency for the chord (0 if not found)
            if frequency:
                # Generate a sine wave for the chord's frequency and write it to the WAV file
                for _ in range(int(0.5 * beat * samples_per_beat)):  # Each beat is 0.5 seconds long
                    value = int(32767.0 * math.sin(2.0 * math.pi * frequency * _ / SAMPLE_RATE)) + 32767
                    wave_file.writeframesraw(value.to_bytes(2, 'little'))

# Usage example
generate_music_wav_hd2_theme_progressive()
