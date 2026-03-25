import pygame
from load_images import *

# Dimensiones de la pantalla
WIDTH = 800
HEIGHT = 600

# Clase de la nave
class Player:
    def __init__(self):
        player_image = load_images_player()
        self.image = pygame.transform.scale(player_image, (30, 30))  # Cambiar el tamaño de la imagen
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -2 #velocidad jugador
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 2 #velocidad jugador
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self, bullets):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullets.append(bullet)

# Clase de las balas
class Bullet:
    def __init__(self, x, y):
        bullet_image = load_images_bullet()
        self.image = pygame.transform.scale(bullet_image, (15, 15))  # Redimensionar la imagen
        self.image.set_colorkey(WHITE) 
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self, bullets):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            bullets.remove(self)
