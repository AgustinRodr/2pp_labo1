import pygame
from data import *
from load_images import *
from colores import *

# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH = 800
HEIGHT = 600

# Ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Timer
clock = pygame.time.Clock()

# Fuente para el texto
font = pygame.font.SysFont("Bauhaus 93", 20)

def show_main_menu():
    background_image = pygame.image.load("galaga_main/space.jpg")  # Ruta de la imagen de fondo
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Salir del bucle y terminar
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False  # Salir del bucle y comenzar

        # Dibujar la pantalla principal
        screen.blit(background_image, (0, 0))  # Dibujar la imagen de fondo en la posición (0, 0)
        main_menu_text = font.render("Presiona ESPACIO para comenzar", True, WHITE)
        main_menu_text_rect = main_menu_text.get_rect()
        main_menu_text_rect.center = (WIDTH // 2, HEIGHT // 2)
        screen.blit(main_menu_text, main_menu_text_rect)

        pygame.display.flip()
        clock.tick(60)

def show_game_over_screen(player_name, score):
    screen.fill(BLACK)
    font = pygame.font.SysFont("Bauhaus 93", 20)
    player_text = font.render(f"Jugador: {player_name}", True, WHITE)
    score_text = font.render(f"Puntaje: {score}", True, WHITE)
    player_text_rect = player_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    score_text_rect = score_text.get_rect(center=(WIDTH // 2, (HEIGHT // 2) + 50))
    screen.blit(player_text, player_text_rect)
    screen.blit(score_text, score_text_rect)

    pygame.display.flip()
    pygame.time.wait(2000)

def show_level_completed(screen, font):
    stage_completed_text = font.render("Nivel completado", True, WHITE)
    stage_completed_text_rect = stage_completed_text.get_rect()
    stage_completed_text_rect.center = (WIDTH // 2, HEIGHT // 2)  
    screen.blit(stage_completed_text, stage_completed_text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)  # Esperar 2 segundos (2000 milisegundos)

def draw_score(screen, font, score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    score_text_rect = score_text.get_rect()
    score_text_rect.topright = (WIDTH - 10, 10)
    screen.blit(score_text, score_text_rect)

def draw_lives(screen, font, lives):
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    lives_text_rect = lives_text.get_rect()
    lives_text_rect.topright = (WIDTH - 10, 40)
    screen.blit(lives_text, lives_text_rect)

def draw_time(screen, font, elapsed_time):
    game_time = elapsed_time // 1000  # Obtener el tiempo transcurrido en segundos
    time_text = font.render(f"Time: {game_time}", True, WHITE)
    time_text_rect = time_text.get_rect()
    time_text_rect.topright = (WIDTH - 10, 70)
    screen.blit(time_text, time_text_rect)

def show_start_screen(screen, start_text, start_text_rect):
    screen.blit(start_text, start_text_rect)

def show_game_over_screen(screen, font, player_name, score):
    game_over_text = font.render("GAME OVER", True, WHITE)
    game_over_text_rect = game_over_text.get_rect()
    game_over_text_rect.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(game_over_text, game_over_text_rect)
    pygame.mixer.music.stop()  # Detener la reproducción de la música
    # Guardar el puntaje en la base de datos
    save_score(player_name, score)
    # Obtener el top 5 de los mejores puntajes
    top_scores = get_scores()
    # Mostrar el top 5 de los mejores puntajes
    title_text = font.render("TOP 5", True, WHITE)
    title_text_rect = title_text.get_rect()
    title_text_rect.topleft = (10, 10)
    screen.blit(title_text, title_text_rect)

    for i, (name, score) in enumerate(top_scores[:5]):
        entry_text = font.render(f"{i+1}. {name}: {score}", True, WHITE)
        entry_text_rect = entry_text.get_rect()
        entry_text_rect.topleft = (10, 40 + (i * 20))
        screen.blit(entry_text, entry_text_rect)

def draw_game_screen(screen, player, bullets, enemies):
    screen.blit(player.image, player.rect)
    for bullet in bullets:
        screen.blit(bullet.image, bullet.rect)
    for enemy in enemies:
        screen.blit(enemy.image, enemy.rect)
