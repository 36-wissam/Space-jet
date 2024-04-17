from settings import *
from laser import *


# Define the Ship class
class Ship:
    COOLDOWN = 30

    # Initialize the ship with position, health, and other attributes
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    # Draw the ship on the game window
    def draw(self, window):
        window.blit(self.ship_img, (self.x - self.ship_img.get_width() / 2, self.y))
        for laser in self.lasers:
            laser.draw(window)

    # Move the ship's lasers and handle collisions with another object
    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    # Manage the cooldown for shooting lasers
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    # Create and shoot a laser from the ship
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    # Get the width of the ship image
    def get_width(self):
        return self.ship_img.get_width()

    # Get the height of the ship image
    def get_height(self):
        return self.ship_img.get_height()
