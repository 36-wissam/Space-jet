import pygame
from ship import Ship
from settings import *
from laser import *




# Define the Enemy class, which is also a subclass of Ship
class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_MONSTER, RED_LASER),
        "green": (GREEN_SPACE_MONSTER, GREEN_LASER),
        "white": (WHITE_SPACE_MONSTER, WHITE_LASER)
    }

    def __init__(self, x, y, color, hp=100):
        super().__init__(x, y, hp)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    # Move the enemy vertically based on velocity
    def move(self, vel):
        self.y += vel

    # Create and shoot a laser from the enemy
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
