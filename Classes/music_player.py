import os
import pygame
import subprocess
import threading

class MusicPlayer:
    def __init__(self, music_basepath, sound_font_path):
        self.music_basepath = music_basepath
        self.sound_font_path = sound_font_path
        self.music_playing = False
        self.music_thread = None
        self.music_type = "midi"

    def play_music_in_loop(self):
        self.music_playing = True
        wav_files = [file for file in os.listdir(self.music_basepath) if file.endswith(".wav")]
        midi_files = [file for file in os.listdir(self.music_basepath) if file.endswith(".mid")]            

        def play_music_wav():
            current_index = 0
            while self.music_playing:
                wav_files[current_index].play()
                while pygame.mixer.get_busy():
                    pygame.time.Clock().tick(30)  # Control the frame rate
                current_index = (current_index + 1) % len(wav_files)  # Move to the next sound file

        def play_music_midi():
            current_index = 0
            while self.music_playing:
                midi_file_path = os.path.join(self.music_basepath, midi_files[current_index])
                subprocess.run(["fluidsynth", "-a", "alsa", "-g", "5.0", "-i", self.sound_font_path + "FluidR3_GM.sf2", midi_file_path])
                current_index = (current_index + 1) % len(midi_files)

        if self.music_type == "wav":
            self.music_thread = threading.Thread(target=play_music_wav)
        else:
            self.music_thread = threading.Thread(target=play_music_midi)

        self.music_thread.start()

    def stop_music(self):
        self.music_playing = False
        if self.music_thread:
            self.music_thread.join()  # Wait for the music thread to finish

    def toggle_music(self):
        if self.music_playing:
            self.stop_music()
        else:
            self.play_music_in_loop()