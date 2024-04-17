import pygame



# Function to check collision between two objects based on their masks
def collision(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


# Define the Laser class
class Laser:

    # Initialize the laser with position and image
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    # Draw the laser on the game window
    def draw(self, window):
        window.blit(self.img, (self.x - self.img.get_width() / 2, self.y))
    
    # Move the laser vertically based on velocity
    def move(self, vel):
        self.y += vel

    # Check if the laser is off the screen
    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)
    
    # Check for collision between the laser and another object
    def collision(self, obj):
        return collision(self, obj)
