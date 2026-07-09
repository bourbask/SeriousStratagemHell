import pygame
import random
import time
import json

from Config import SCREEN_WIDTH

# Load level speed from JSON file
with open('./Data/level_speed.json', 'r') as file:
    LEVEL_SPEED = json.load(file)

# Load combos from JSON file
with open('./Data/combos.json', 'r') as file:
    COMBOS_DATA = json.load(file)

# Load key codes from JSON file
with open('./Data/key_codes.json', 'r') as file:
    KEY_CODES_DATA = json.load(file)

# Define color constants
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
GREEN_COLOR = (0, 255, 0)

# Define margins
MARGIN_WIDTH = 50
MARGIN_HEIGHT = 50

class Game:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.theme = None
        self.stratagem = None
        self.button_inputs = []
        self.stratagem_title = None
        self.start_time = None
        self.chrono_duration = None
        self.chrono_end = None
        self.input_colors = [BLACK_COLOR] * len(self.button_inputs)  # Initialize all inputs to black
        self.bar_length = SCREEN_WIDTH - 100  # Length of the time bar
        self.bar_height = 20  # Height of the time bar
        self.bar_color = (0, 255, 0)  # Color of the time bar

    def select_combo(self, level):
        theme = random.choice(list(COMBOS_DATA['themes'].keys()))
        stratagem = random.choice(COMBOS_DATA['themes'][theme])
        return theme, stratagem

    def start_game(self):
        self.theme, self.stratagem = self.select_combo(1)
        self.button_inputs = self.stratagem['button_inputs']
        self.stratagem_title = self.stratagem['name']
        self.start_time = time.time()
        self.chrono_duration = LEVEL_SPEED['1']
        self.chrono_end = self.start_time + self.chrono_duration

        while True:
            self.screen.fill(WHITE_COLOR)
            self.display_layout([MARGIN_WIDTH, MARGIN_HEIGHT])

            if not self.handle_time():
                return False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if not self.handle_combo_input(event.key):
                        return False  # Return False if combo input is incorrect

                    if not self.handle_general_keys(event.key):
                        return False  # Return False if general key handling fails

            pygame.display.update()

    def display_layout(self, margins):
        self.display_general_controls(margins)
        self.display_game_info([margins[0], margins[1] + 100])
        self.display_combo_input([margins[0], margins[1] + 200])

    def display_combo_input(self, position: [int, int]):
        self.display_text("Press the following inputs:", position[0], position[1])
        self.display_text(", ".join(self.button_inputs), position[0] + 150, position[1] + 50)

    def display_general_controls(self, position: [int, int]):
        self.display_text("Press P to resume game", position[0], position[1])
        self.display_text("Press M to toggle music", position[0] + 300, position[1])
        self.draw_time_bar(position)

    def display_game_info(self, position: [int, int]):
        self.display_text("Stratagem: {}".format(self.stratagem_title), position[0], position[1])
        self.display_text("Level: {}".format(1), position[0], position[1] + 50)

    def handle_combo_input(self, key):
        if len(self.button_inputs) > 0 and key == KEY_CODES_DATA[self.button_inputs[0]]:
            self.button_inputs.pop(0)
            print(self.button_inputs, self.input_colors)
            self.input_colors.append(GREEN_COLOR)
            if len(self.button_inputs) == 0:
                print("Combo complete!")
                self.reset_inputs()
                return True  # Combo input is correct
        elif key in [pygame.K_z, pygame.K_q, pygame.K_s, pygame.K_d]:
            # Wrong input for the combo
            print("Wrong input!")
            self.reset_inputs()
            return False  # Combo input is incorrect

        return True  # No relevant combo input event

    def handle_general_keys(self, key):
        if key == pygame.K_r:
            # Resume game
            return True
        elif key == pygame.K_m:
            # Mute/unmute music
            return True
        # Add more general key handling logic as needed

        return True  # No relevant general key event

    def draw_time_bar(self, position: [int, int]):
        # Calculate remaining time percentage
        remaining_time = max(self.chrono_end - time.time(), 0)
        percentage = remaining_time / self.chrono_duration

        # Calculate width of the bar based on percentage
        bar_width = int(self.bar_length * percentage)

        # Draw the time bar
        pygame.draw.rect(self.screen, self.bar_color, (position[0], position[1] + 350, bar_width, self.bar_height))

    def render_inputs(self):
        for i, (input_text, color) in enumerate(zip(self.button_inputs, self.input_colors)):
            self.display_text(input_text, x=300 + i * 50, y=200, color=color)

    def reset_inputs(self):
        self.button_inputs, self.input_colors = self.select_combo(1)  # Reset inputs and colors for the next combo

    def handle_time(self):
        remaining_time = self.chrono_duration - (time.time() - self.start_time)
        if remaining_time <= 0:
            print("Out of time! Game over.")
            return False
        else:
            return True

    def display_text(self, text, x, y, color=(0, 0, 0)):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
