import pygame

from Config import SCREEN_WIDTH, SCREEN_HEIGHT


class EndScreen:
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font):
        self.screen = screen
        self.font = font
        self.title_font = pygame.font.SysFont(None, 64)
        self.final_score = 0
        self.rank: int | None = None

    def show(self, score: int, rank: int | None) -> bool:
        self.final_score = score
        self.rank = rank
        self.draw()
        return self.wait()

    def draw(self) -> None:
        self.screen.fill((255, 255, 255))
        title = self.title_font.render("Game Over!", True, (180, 0, 0))
        rect = title.get_rect(center=(SCREEN_WIDTH // 2, 120))
        self.screen.blit(title, rect)

        self.draw_text(f"Score: {self.final_score}", SCREEN_WIDTH // 2, 220, (0, 0, 0))

        if self.rank is not None:
            self.draw_text(f"New High Score! Rank #{self.rank}", SCREEN_WIDTH // 2, 270, (0, 140, 0))

        self.draw_text("Press SPACE to play again", SCREEN_WIDTH // 2, 350, (60, 60, 60))
        self.draw_text("Press Q to quit", SCREEN_WIDTH // 2, 390, (60, 60, 60))

        pygame.display.update()

    def wait(self) -> bool:
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
