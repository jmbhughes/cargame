# Imports
import pygame
from pygame.locals import *
import random
import time
import sys
from pathlib import Path

# Initializing
pygame.init()

# Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Creating colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# File path
ASSETS_PATH = Path("assets")

# Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
score = 0

# Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, WHITE)

background = pygame.image.load(ASSETS_PATH / "AnimatedStreet.png")

# Create a white screen
display_surface = pygame.display.set_mode((400, 600))
display_surface.fill(WHITE)
pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(ASSETS_PATH / "Enemy.png")
        self.surf = pygame.Surface((42, 70))
        self.rect = self.surf.get_rect(center=(random.randint(40, SCREEN_WIDTH - 40), 0))

    def move(self):
        global score
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > SCREEN_HEIGHT:
            score += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(ASSETS_PATH / "Player.png")
        self.surf = pygame.Surface((40, 75))
        self.rect = self.surf.get_rect(center=(160, 520))

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0:
            if pressed_keys[K_LEFT] or pressed_keys[K_a]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
                self.rect.move_ip(5, 0)


if __name__ == "__main__":
    # Setting up Sprites
    player = Player()
    enemy = Enemy()

    # Creating Sprites Groups
    enemies = pygame.sprite.Group()
    enemies.add(enemy)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(enemy)

    # Adding a new User event
    INC_SPEED = pygame.USEREVENT + 1
    pygame.time.set_timer(INC_SPEED, 1000)

    # Game Loop
    while True:
        # Cycles through all events occurring
        for event in pygame.event.get():
            if event.type == INC_SPEED:
                SPEED += 0.25
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        display_surface.blit(background, (0, 0))
        scores = font_small.render(str(score), True, BLACK)
        display_surface.blit(scores, (10, 10))

        # Moves and Re-draws all Sprites
        for entity in all_sprites:
            display_surface.blit(entity.image, entity.rect)
            entity.move()

        # To be run if collision occurs between Player and Enemy
        if pygame.sprite.spritecollideany(player, enemies):
            pygame.mixer.Sound(ASSETS_PATH / 'crash.wav').play()
            time.sleep(1)

            display_surface.fill(BLACK)
            display_surface.blit(game_over, (30, 250))

            pygame.display.update()
            for entity in all_sprites:
                entity.kill()
            time.sleep(2)
            pygame.quit()
            sys.exit()

        pygame.display.update()
        FramePerSec.tick(FPS)
