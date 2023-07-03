import pygame 
import random
import sys
from load_images import *

pygame.init()
pygame.font.init()

# Dimensiones de la pantalla
WIDTH = 800
HEIGHT = 600

# Timer
clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Fuente para el texto
font = pygame.font.SysFont("Bauhaus 93", 20)

# Clase de las naves enemigas
class Enemy:
    def __init__(self, x=None):
        enemy_image = load_images_enemy()
        self.image = pygame.transform.scale(enemy_image, (30, 30))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x if x is not None else random.randrange(WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed_x = 0
        self.speed_y = 0
        self.move_direction = random.choice([-1, 1])
        self.start_moving = False
        self.move_timer = 0

    def update(self, enemies):
        if not self.start_moving:
            return
        self.move_timer += clock.get_time()  # Incrementar el temporizador de movimiento
        if self.move_timer >= enemy_move_delay:
            self.rect.y += self.speed_y
            self.rect.x += self.speed_x * self.move_direction
            if self.rect.left <= 0 or self.rect.right >= WIDTH:
                self.move_direction *= -1
            if self.rect.top > HEIGHT:
                enemies.remove(self)  # Eliminar enemigo cuando sale de la pantalla
            # Reiniciar el temporizador de movimiento
            self.move_timer = 0

    def start_movement(self):
        self.start_moving = True
        self.speed_x = random.choice([-1, 1]) * random.uniform(1, 3)
        self.speed_y = random.uniform(1, 3)

def start_stage(stage, enemies):
    global enemy_move_delay
    stage_text = "Stage " + str(stage)
    enemy_image = None

    if stage == 1:
        enemy_move_delay = 150  # Establecer el retraso de movimiento para el nivel 1
        enemy_image = pygame.image.load("galaga_main/enemigo.png").convert_alpha()
        stage_text = font.render("STAGE 1", True, WHITE)
    elif stage == 2:
        enemy_move_delay = 60  # Establecer el retraso de movimiento para el nivel 2
        enemy_image = pygame.image.load("galaga_main/enemi2.png").convert_alpha()
        enemy_image.set_colorkey(WHITE)
        stage_text = font.render("STAGE 2", True, WHITE)
    elif stage == 3:
        enemy_move_delay = 30  # Ajusta el retraso de movimiento para el nivel 3
        enemy_image = pygame.image.load("galaga_main/enemi3.png").convert_alpha()
        stage_text = font.render("STAGE 3", True, WHITE)
    elif stage == 4:
        enemy_move_delay = 20  # Ajusta el retraso de movimiento para el nivel 3
        enemy_image = pygame.image.load("galaga_main/enemi4.png").convert_alpha()
        stage_text = font.render("STAGE 4", True, WHITE)

    if enemy_image is not None:
        enemy_image = pygame.transform.scale(enemy_image, (30, 30))
        enemy_image.set_colorkey(WHITE)

    enemy_rows = 7  # Número de filas de enemigos
    enemy_columns = [12, 10, 8, 6, 4, 2, 1]  # Número de enemigos por columna en cada fila

    enemy_width = 30
    enemy_height = 30
    enemy_padding_x = 10  # Espaciado horizontal entre enemigos
    enemy_padding_y = 10  # Espaciado vertical entre enemigos

    start_y = 50  # Posición y de la primer fila de enemigos

    for row in range(enemy_rows):
        num_enemies = enemy_columns[row]
        enemy_row_width = num_enemies * enemy_width + (num_enemies - 1) * enemy_padding_x
        row_start_x = (WIDTH - enemy_row_width) // 2

        for column in range(num_enemies):
            x = row_start_x + (enemy_width + enemy_padding_x) * column
            y = start_y + (enemy_height + enemy_padding_y) * row
            enemy = Enemy(x)
            enemy.image = enemy_image  # Cambiar la imagen del enemigo
            enemy.rect.x = x
            enemy.rect.y = y
            enemies.append(enemy)

    return stage_text

def get_user_name():
    user_input = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return user_input
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode
        
        screen.fill(BLACK)
        font = pygame.font.SysFont("Bauhaus 93", 20)
        input_text = font.render("Ingrese su nombre: " + user_input, True, WHITE)
        input_text_rect = input_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(input_text, input_text_rect)
        pygame.display.flip()
        clock.tick(60)