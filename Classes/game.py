import pygame
import random
import time
import json

from Config import SCREEN_WIDTH

with open("./Data/level_speed.json") as f:
    LEVEL_SPEED: dict[str, float] = json.load(f)

with open("./Data/combos.json") as f:
    COMBOS_DATA: dict = json.load(f)

with open("./Data/key_codes.json") as f:
    KEY_CODES: dict[str, int] = json.load(f)

MARGIN_X = 50
MARGIN_Y = 50
BAR_WIDTH = SCREEN_WIDTH - 100
BAR_HEIGHT = 20


class Game:
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font):
        self.screen = screen
        self.font = font
        self.level = 1
        self.score = 0
        self.theme_name = ""
        self.stratagem_name = ""
        self.combo_keys: list[str] = []
        self.combo_index = 0
        self.level_speed = 10.0
        self.round_start = 0.0
        self.round_end = 0.0
        self.feedback: list[tuple[str, int]] = []

    def reset(self) -> None:
        self.level = 1
        self.score = 0
        self.combo_keys = []
        self.combo_index = 0
        self.feedback = []

    def start_round(self) -> None:
        theme_name = random.choice(list(COMBOS_DATA["themes"].keys()))
        stratagem = random.choice(COMBOS_DATA["themes"][theme_name])
        self.theme_name = theme_name
        self.stratagem_name = stratagem["name"]
        self.combo_keys = stratagem["button_inputs"]
        self.combo_index = 0
        key = str(min(self.level, len(LEVEL_SPEED)))
        self.level_speed = LEVEL_SPEED[key]
        self.round_start = time.time()
        self.round_end = self.round_start + self.level_speed
        self.feedback = []

    def run(self) -> int | None:
        self.reset()
        self.start_round()
        clock = pygame.time.Clock()

        while self.level >= 0:
            clock.tick(60)
            now = time.time()

            if now > self.round_end:
                return self.score

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    result = self.handle_key(event.key)
                    if result is False:
                        return self.score
                    if result is True:
                        self.advance_round()

            self.draw()

        return self.score

    def handle_key(self, key: int) -> bool | None:
        expected = self.combo_keys[self.combo_index] if self.combo_index < len(self.combo_keys) else None
        if expected is None:
            return None

        mapped = KEY_CODES.get(expected)
        if mapped == key:
            self.combo_index += 1
            if self.combo_index >= len(self.combo_keys):
                return True
            return None

        is_direction = key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
                               pygame.K_z, pygame.K_q, pygame.K_s, pygame.K_d)
        if is_direction:
            return False

        return None

    def advance_round(self) -> None:
        combo_len = len(self.combo_keys)
        self.score += combo_len * 10 * self.level
        self.level += 1
        self.start_round()

    def draw(self) -> None:
        self.screen.fill((255, 255, 255))
        self.draw_time_bar()
        self.draw_combo_display()
        self.draw_info()
        self.draw_feedback()
        pygame.display.update()

    def draw_info(self) -> None:
        white = (255, 255, 255)
        black = (0, 0, 0)
        self.screen.fill(white)
        self.draw_text(f"Level: {self.level}  Score: {self.score}", MARGIN_X, MARGIN_Y, black)
        self.draw_text(f"Theme: {self.theme_name}", MARGIN_X, MARGIN_Y + 40, black)
        self.draw_text(f"Stratagem: {self.stratagem_name}", MARGIN_X, MARGIN_Y + 80, black)

    def draw_combo_display(self) -> None:
        arrow_map = {"Up": "↑", "Down": "↓", "Left": "←", "Right": "→"}
        start_x = MARGIN_X
        y = MARGIN_Y + 130

        for i, key_name in enumerate(self.combo_keys):
            arrow = arrow_map.get(key_name, "?")
            color = (0, 180, 0) if i < self.combo_index else (0, 0, 0)
            if i == self.combo_index:
                color = (0, 0, 220)

            label = self.font.render(arrow, True, color)
            label_rect = label.get_rect(center=(start_x + i * 55 + 25, y + 15))
            pygame.draw.rect(self.screen, (220, 220, 255) if i == self.combo_index else (240, 240, 240),
                             (start_x + i * 55, y, 50, 50), border_radius=6)
            self.screen.blit(label, label_rect)

    def draw_time_bar(self) -> None:
        remaining = max(self.round_end - time.time(), 0)
        ratio = remaining / self.level_speed
        r = int(255 * (1 - ratio))
        g = int(255 * ratio)
        bar_x = MARGIN_X
        bar_y = MARGIN_Y + 200
        current_w = int(BAR_WIDTH * ratio)
        pygame.draw.rect(self.screen, (200, 200, 200), (bar_x, bar_y, BAR_WIDTH, BAR_HEIGHT), border_radius=4)
        pygame.draw.rect(self.screen, (r, g, 0), (bar_x, bar_y, current_w, BAR_HEIGHT), border_radius=4)

    def draw_feedback(self) -> None:
        fy = MARGIN_Y + 250
        self.draw_text("↑ ↓ ← →  or  Z Q S D", MARGIN_X, fy, (120, 120, 120))

    def draw_text(self, text: str, x: int, y: int, color: tuple[int, int, int] = (0, 0, 0)) -> None:
        surf = self.font.render(text, True, color)
        self.screen.blit(surf, (x, y))
