import pygame

from Classes.scoreboard import load_scores
from Config import SCREEN_WIDTH, SCREEN_HEIGHT


class Menu:
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font):
        self.screen = screen
        self.font = font
        self.title_font = pygame.font.SysFont(None, 64)

    def draw(self) -> None:
        self.screen.fill((255, 255, 255))
        title = self.title_font.render("Stratagem Hell", True, (0, 0, 0))
        rect = title.get_rect(center=(SCREEN_WIDTH // 2, 120))
        self.screen.blit(title, rect)

        self.draw_text("Press SPACE to start", SCREEN_WIDTH // 2, 250, (60, 60, 60))
        self.draw_text("Press Q to quit", SCREEN_WIDTH // 2, 290, (60, 60, 60))

        scores = load_scores()
        if scores:
            self.draw_text("-- High Scores --", SCREEN_WIDTH // 2, 370, (0, 0, 0))
            for i, s in enumerate(scores[:5]):
                self.draw_text(f"{i + 1}. {s}", SCREEN_WIDTH // 2, 410 + i * 36, (80, 80, 80))

        pygame.display.update()

    def run(self) -> bool:
        self.draw()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return True
                    if event.key == pygame.K_q:
                        return False

    def draw_text(self, text: str, x: int, y: int, color: tuple[int, int, int] = (0, 0, 0)) -> None:
        surf = self.font.render(text, True, color)
        rect = surf.get_rect(center=(x, y))
        self.screen.blit(surf, rect)
