import pygame
import random
from settings import *
from laser import *
from player import Player
from enemy import Enemy



pygame.font.init()


# set up the window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space jet")



class Spacejet:
    def __init__(self):
        self.run = True
        self.FPS = 60
        self.level = 0
        self.lives = 10
        self.font = pygame.font.SysFont("Bahnschrift", 20)
        self.lose_font = pygame.font.SysFont("Bahnschrift", 60)
        self.enemies = []
        self.wave_length = 5
        self.enemy_vel = 1
        self.player_vel = 5
        self.laser_vel = 5
        self.player = Player(300, 630)
        self.clock = pygame.time.Clock()
        self.lost = False
        self.lost_count = 0
        self.title_font = pygame.font.SysFont("Bahnschrift", 40)
        self.bg_y = 0 

    def run_game(self):
        while self.run:
            self.clock.tick(self.FPS)
            self.redraw_window()

            if self.lives <= 0 or self.player.health <= 0:
                self.lost = True
                self.lost_count += 1

            if self.lost:
                if self.lost_count > self.FPS * 3:
                    self.run = False
                else:
                    continue

            if len(self.enemies) == 0:
                self.level += 1
                self.wave_length += 5
                for i in range(self.wave_length):
                    enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100),
                                  random.choice(["red", "white", "green"]))
                    self.enemies.append(enemy)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and self.player.x - self.player_vel > 0:
                self.player.x -= self.player_vel
            if keys[pygame.K_d] and self.player.x + self.player_vel + self.player.get_width() < WIDTH:
                self.player.x += self.player_vel
            if keys[pygame.K_w] and self.player.y - self.player_vel > 0:
                self.player.y -= self.player_vel
            if keys[pygame.K_s] and self.player.y + self.player_vel + self.player.get_height() + 15 < HEIGHT:
                self.player.y += self.player_vel
            if keys[pygame.K_SPACE]:
                self.player.shoot()

            for enemy in self.enemies[:]:
                enemy.move(self.enemy_vel)
                enemy.move_lasers(self.laser_vel, self.player)

                if random.randrange(0, 2 * 60) == 1:
                    enemy.shoot()

                if collision(enemy, self.player):
                    self.player.health -= 10
                    self.enemies.remove(enemy)
                elif enemy.y + enemy.get_height() > HEIGHT:
                    self.lives -= 1
                    self.enemies.remove(enemy)

            self.player.move_lasers(-self.laser_vel, self.enemies)

    def redraw_window(self):
        self.bg_y = (self.bg_y + BG_SPEED) % HEIGHT
        WIN.blit(BG, (0, self.bg_y))
        WIN.blit(BG, (0, self.bg_y - HEIGHT))

        lives_label = self.font.render(f"Lives: {self.lives}", 1, 'white')
        level_label = self.font.render(f"Level: {self.level}", 1, 'white')

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in self.enemies:
            enemy.draw(WIN)

        self.player.draw(WIN)

        if self.lost:
            lost_label = self.lose_font.render("You Lost", 1, "white")
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))
            
        pygame.display.update()


    def main_menu(self):
        while True:
            
            WIN.blit(BG, (0, 0))
            title_label = self.title_font.render("SPACE TO START", 1, "white")
            WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 350))
            pygame.display.update()

            # Event handling loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.run_game()
                    return


if __name__ == '__main__':
    game = Spacejet()
    game.main_menu()
