import pygame

class Menu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def display_menu(self):
        self.screen.fill((255, 255, 255))
        self.display_text("Welcome to Stratagem Hell!", 50, 50)
        self.display_text("Press SPACE to start or Q to quit", 50, 150)
        pygame.display.update()

    def wait_for_input(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return True
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()

    def display_text(self, text, x, y, color=(0, 0, 0)):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
