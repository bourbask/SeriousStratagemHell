import os
import pygame


class MusicPlayer:
    def __init__(self, music_basepath: str):
        self.music_basepath = music_basepath
        self.music_playing = False

    def play_music_in_loop(self) -> None:
        wav_files = sorted([
            f for f in os.listdir(self.music_basepath)
            if f.endswith(".wav")
        ])
        if not wav_files:
            return

        self.music_playing = True
        current_index = 0

        while self.music_playing:
            path = os.path.join(self.music_basepath, wav_files[current_index])
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() and self.music_playing:
                pygame.time.Clock().tick(30)
            current_index = (current_index + 1) % len(wav_files)

    def stop_music(self) -> None:
        self.music_playing = False
        pygame.mixer.music.stop()

    def toggle_music(self) -> None:
        if self.music_playing:
            self.stop_music()
        else:
            self.play_music_in_loop()
