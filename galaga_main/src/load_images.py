import os, pygame
from colores import BLACK, WHITE

def load_image(filename):
    path = os.path.join("galaga_main", "assets", "images", filename)
    return pygame.image.load(path).convert_alpha()


def load_sound(filename):
    return pygame.mixer.Sound(os.path.join("assets", "sounds", filename))

def load_images_player():
    player_image = load_image("nave.png")
    player_image.set_colorkey(BLACK)
    return player_image

def load_images_bullet():
    bullet_image = load_image("bullet.png").convert_alpha()
    bullet_image.set_colorkey(BLACK)
    return bullet_image


def load_images_enemy():
    enemy_image = load_image("enemigo.png").convert_alpha()
    enemy_image.set_colorkey(WHITE)
    return enemy_image

def load_images_background():
    background_image = load_image("fondo.png").convert()
    return background_image

def load_images_enemy2():
    enemy2_image = load_image("enemi2.png").convert_alpha()
    enemy2_image.set_colorkey(WHITE)
    return enemy2_image

def load_images_enemy3():
    enemy3_image = load_image("enemi3.png").convert_alpha()
    enemy3_image.set_colorkey(WHITE)
    return enemy3_image
