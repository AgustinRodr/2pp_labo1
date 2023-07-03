import pygame
from colores import WHITE
from load_images import *
from player import *
from enemy import *
from biblioteca_parcial import *
from data import *

# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH = 800
HEIGHT = 600

# Timer
clock = pygame.time.Clock()

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

# Inicializo
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

# Pedir nombre al usuario
player_name = get_user_name()

# Loop principal del juego
running = True
start_time = pygame.time.get_ticks()  # Obtener el tiempo de inicio del juego
stage = 1
stage_text = start_stage(stage, enemies)
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
                    start_stage(stage, enemies)
                    player.rect.centerx = WIDTH // 2
                    player.rect.bottom = HEIGHT - 10
                    score = 0
                    game_time = 0
                    game_over = False
                    game_started = False
                    start_time = pygame.time.get_ticks()
                else: 
                    player.shoot(bullets)
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
            bullet.update(bullets)
        for enemy in enemies:
            enemy.start_movement()
            enemy.update(enemies)

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
            if enemy.rect.y + enemy_height >= HEIGHT:  # Verificar si el enemigo alcanzo la parte inferior de la pantalla
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
            start_stage(stage, enemies)  # Actualizar el nivel
            # Crear la nave del jugador
            player = Player()
            player.rect.centerx = WIDTH // 2  # posicion horizontal en el centro de la pantalla
            player.rect.bottom = HEIGHT - 10  # posicion vertical en la parte inferior de la pantalla
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

    # Mostrar el puntaje, las vidas y el tiempo si el juego no termino
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