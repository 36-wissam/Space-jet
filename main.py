import pygame
import os
import random

# Initialize pygame and set up the window
pygame.font.init()
WIDTH, HEIGHT = 1080, 780
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space jet")

# Load images for the game
SPACE_SHIP = pygame.image.load(os.path.join("assets","player-ship.png"))
RED_SPACE_MONSTER = pygame.image.load(os.path.join("assets", "monsters", "red-monster.png"))
GREEN_SPACE_MONSTER = pygame.image.load(os.path.join("assets", "monsters", "green-monster.png"))
WHITE_SPACE_MONSTER = pygame.image.load(os.path.join("assets", "monsters", "blue-monster.png"))
RED_LASER = pygame.image.load(os.path.join("assets", "laser", "red-laser.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "laser", "green-laser.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "laser", "blue-laser.png"))
WHITE_LASER = pygame.image.load(os.path.join("assets", "laser", "white-laser.png"))
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.jpg")), (WIDTH, HEIGHT))
BG_SPEED = 2 
bg_y = 0




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

# Function to check collision between two objects based on their masks
def collision(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None



# Main game loop
def main():
    global bg_y
    run = True
    FPS = 60
    level = 0
    lives = 10
    font = pygame.font.SysFont("Bahnschrift", 20)
    lose_font = pygame.font.SysFont("Bahnschrift", 60)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5
    laser_vel = 5

    player = Player(300, 630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    # Function to redraw the game window
    def redraw_window():
        global bg_y
        bg_y = (bg_y + BG_SPEED) % HEIGHT
        WIN.blit(BG, (0, bg_y))
        WIN.blit(BG, (0, bg_y - HEIGHT))

        lives_label = font.render(f"Lives: {lives}", 1, 'white')
        level_label = font.render(f"Level: {level}", 1, 'white')

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lose_font.render("You Lost", 1, "white")
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

        pygame.display.update()



    # Main game loop
    while run:
        clock.tick(FPS)
        redraw_window()

        # Check if player has lost
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        # Check if all enemies are defeated and spawn a new wave
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100),
                              random.choice(["red", "white", "green"]))
                enemies.append(enemy)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Player movement based on key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        # Update enemy positions, check collisions, and handle enemy shooting
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()

            if collision(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        # Move player's lasers and check for collisions with enemies
        player.move_lasers(-laser_vel, enemies)

# Function to display the main menu
def main_menu():
    title_font = pygame.font.SysFont("Bahnschrift", 40)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("SPACE TO START", 1, "white")
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                main()
    pygame.quit()

# Start
main_menu()