import pygame
import os




WIDTH, HEIGHT = 1080, 780

# Load images for the game
SPACE_SHIP = pygame.image.load(os.path.join("assets","player_ship.png"))
RED_SPACE_MONSTER = pygame.image.load(os.path.join("assets", "monsters", "red-monster.png"))
GREEN_SPACE_MONSTER = pygame.image.load(os.path.join("assets", "monsters", "green-monster.png"))
WHITE_SPACE_MONSTER = pygame.image.load(os.path.join("assets", "monsters", "blue-monster.png"))
RED_LASER = pygame.image.load(os.path.join("assets", "laser", "red-laser.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "laser", "green-laser.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "laser", "blue-laser.png"))
WHITE_LASER = pygame.image.load(os.path.join("assets", "laser", "white-laser.png"))


BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.jpg")), (WIDTH, HEIGHT))
BG_SPEED = 2 

