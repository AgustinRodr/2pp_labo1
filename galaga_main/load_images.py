import pygame
from colores import BLACK, WHITE

def load_images_player():
    player_image = pygame.image.load("galaga_main/nave.png").convert_alpha()
    player_image.set_colorkey(BLACK)
    return player_image

def load_images_bullet():
    bullet_image = pygame.image.load("galaga_main/bullet.png").convert_alpha()
    bullet_image.set_colorkey(BLACK)
    return bullet_image


def load_images_enemy():
    enemy_image = pygame.image.load("galaga_main/enemigo.png").convert_alpha()
    enemy_image.set_colorkey(WHITE)
    return enemy_image

def load_images_background():
    background_image = pygame.image.load("galaga_main/fondo.png").convert()
    return background_image

def load_images_enemy2():
    enemy2_image = pygame.image.load("galaga_main/enemi2.png").convert_alpha()
    enemy2_image.set_colorkey(WHITE)
    return enemy2_image

def load_images_enemy3():
    enemy3_image = pygame.image.load("galaga_main/enemi3.png").convert_alpha()
    enemy3_image.set_colorkey(WHITE)
    return enemy3_image
