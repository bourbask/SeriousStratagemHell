import pygame

from Classes.game import Game
from Classes.menu import Menu
from Classes.end_screen import EndScreen
from Classes.music_player import MusicPlayer
from Classes.scoreboard import add_score
from Config import MUSIC_BASEPATH, SCREEN_WIDTH, SCREEN_HEIGHT

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Serious Stratagem Hell")

font = pygame.font.SysFont(None, 36)

game = Game(screen, font)
menu = Menu(screen, font)
end_screen = EndScreen(screen, font)
music_player = MusicPlayer(MUSIC_BASEPATH)

running = True
music_started = False

while running:
    if not menu.run():
        running = False
        break

    if not music_started:
        music_player.play_music_in_loop()
        music_started = True

    score = game.run()
    if score is None:
        running = False
        break

    rank = add_score(score)
    if not end_screen.show(score, rank):
        running = False
        break

music_player.stop_music()
pygame.quit()
