import pygame
from ship import Ship
from settings import *



# Define the Player class, which is a subclass of Ship
class Player(Ship):

    # Initialize the player with position, health, and specific attributes
    def __init__(self, x, y, hp=100):
        super().__init__(x, y, hp)
        self.ship_img = SPACE_SHIP
        self.laser_img = BLUE_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = hp

    # Move the player's lasers and handle collisions with a list of objects
    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    
    # Draw the player on the game window
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    # Draw the player's health bar on the game window
    def healthbar(self, window):
        pygame.draw.rect(window, "red", (self.x - self.ship_img.get_width() / 2, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, "light blue",(self.x - self.ship_img.get_width() / 2, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health / self.max_health), 10))
