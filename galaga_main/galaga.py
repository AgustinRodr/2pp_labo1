import pygame
import random
import sys
from colores import BLACK, WHITE
from load_images import *
from biblioteca_parcial import *
from data import *

# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH = 800
HEIGHT = 600

# Timer
clock = pygame.time.Clock()

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

    def shoot(self):
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

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            bullets.remove(self)

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

    def update(self):
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

def start_stage(stage):
    global enemy_move_delay
    stage_text = "Stage " + str(stage)
    
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


# Inicialización de la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaxia")

# Fuente para el texto
font = pygame.font.SysFont("Bauhaus 93", 20)

# Jugador
player = Player()

#grupos de instancias
bullets = []
enemies = []

# Estado del juego
game_over = False
game_started = False
game_paused = False
level_completed = False  # Nuevo estado

# Pantalla de inicio
start_text = font.render("Presiona ESPACIO para comenzar", True, WHITE)
start_text_rect = start_text.get_rect()
start_text_rect.center = (WIDTH // 2, HEIGHT // 2)

# Texto de pausa
pause_text = font.render("PAUSE", True, WHITE)
pause_text_rect = pause_text.get_rect()
pause_text_rect.center = (WIDTH // 2, HEIGHT // 2)

# Temporizador
score = 0
lives = 3

# Carga de sonidos
pygame.mixer.music.load("galaga_main/theme.mp3")
pygame.mixer.music.play(-1)
shoot_sound = pygame.mixer.Sound("galaga_main/shoot.mp3")
collision_sound = pygame.mixer.Sound("galaga_main/collision.mp3")


# Pantallas de etapa
stage_text = font.render("", True, WHITE)
stage_text_rect = stage_text.get_rect()
stage_text_rect.center = (WIDTH // 2, HEIGHT // 2)


# Pedir nombre usuario
player_name = get_user_name()

# Loop principal del juego

running = True
start_time = pygame.time.get_ticks()  # Obtener el tiempo de inicio del juego
stage = 1
stage_text = start_stage(stage)

show_main_menu()
while running:
    elapsed_time = pygame.time.get_ticks() - start_time
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game_started and not game_paused:
                if event.key == pygame.K_SPACE:
                    game_started = True
            elif event.key == pygame.K_SPACE:
                if game_over:
                    # Reiniciar el juego desde el nivel 0
                    stage = 0
                    bullets = []
                    enemies = []
                    start_stage(stage)
                    player.rect.centerx = WIDTH // 2
                    player.rect.bottom = HEIGHT - 10
                    score = 0
                    game_time = 0
                    game_over = False
                    game_started = False
                    start_time = pygame.time.get_ticks()
                else:
                    player.shoot()
                    shoot_sound.play()
            elif event.key == pygame.K_p:
                game_paused = not game_paused
                if game_paused:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

    if game_paused:
        screen.blit(pause_text, pause_text_rect)
        pygame.display.flip()
        continue

   # Actualización de instancias
    if game_started and not game_paused and not game_over:
        player.update()
        for bullet in bullets:
            bullet.update()
        for enemy in enemies:
            enemy.start_movement()
            enemy.update()

        # # Colisiones del jugador con los enemigos
        collided_enemies = []  # Lista para almacenar los enemigos con los que colisionó el jugador
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                collided_enemies.append(enemy)
                collision_sound.play()  # Reproducir sonido de colisión

        # Restar una vida por cada enemigo colisionado
        for enemy in collided_enemies:
            lives -= 1
            enemies.remove(enemy)  # Eliminar el enemigo colisionado de la lista de enemigos
    
        if lives <= 0:
            game_over = True

        enemy_height = 30
        for enemy in enemies:
            if enemy.rect.y + enemy_height >= HEIGHT:  # Verificar si el enemigo ha alcanzado la parte inferior de la pantalla
                # Restar una vida a la nave
                lives -= 1
                enemies.remove(enemy)
                if lives <= 0:
                    game_over = True

        # Colisiones de las balas con los enemigos
        collided_bullets = []
        collided_enemies = []
        for bullet in bullets:
            for enemy in enemies:
                if bullet.rect.colliderect(enemy.rect):
                    collided_bullets.append(bullet)
                    collided_enemies.append(enemy)
                    score += 100
                    collision_sound.play()  # Reproducir sonido de colisión
                    break

        for bullet in collided_bullets:
            bullets.remove(bullet)

        for enemy in collided_enemies:
            if enemy in enemies:
                enemies.remove(enemy)


        # Verificar si se han eliminado todos los enemigos
        if not enemies and not game_over:
        # Pasar al siguiente nivel
            stage += 1
            bullets = []
            enemies = []
            start_stage(stage)  # Actualizar el nivel
            # Crear la nave del jugador
            player = Player()
            player.rect.centerx = WIDTH // 2  # Establecer la posición horizontal en el centro de la pantalla
            player.rect.bottom = HEIGHT - 10  # Establecer la posición vertical en la parte inferior de la pantalla
            show_level_completed(screen, font)
            level_completed = True

    # Dibujado en la pantalla
    background_image = load_images_background()
    screen.blit(background_image, (0, 0))
    
    if not game_started:
        show_start_screen(screen, start_text, start_text_rect)
    elif game_over:
        show_game_over_screen(screen, font, player_name, score)
    else:
        draw_game_screen(screen, player, bullets, enemies)

    # Mostrar el puntaje, las vidas y el tiempo si el juego no ha terminado
    if not game_over:
        draw_score(screen, font, score)
        draw_lives(screen, font, lives)
        draw_time(screen, font, elapsed_time)

    # Dibujar el texto de "Nivel completado" si el estado es verdadero
    if level_completed:
        show_level_completed(screen, font)
        level_completed = False  # Restablecer el estado

    pygame.display.flip()
# Salir del juego
pygame.quit()