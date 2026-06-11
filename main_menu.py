import pygame
import sys
from game_handler import run_game_handler

pygame.init()
pygame.mixer.init()


WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
DARK_BLUE = (40, 90, 130)
GRAY = (180, 180, 180)

title_font = pygame.font.SysFont("Arial", 60)
font = pygame.font.SysFont("Arial", 32)
small_font = pygame.font.SysFont("Arial", 24)

volume = 0.5

pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(-1)

# Optional background music
# Put your music file in the same folder and uncomment these lines:
# pygame.mixer.music.load("background_music.mp3")
# pygame.mixer.music.play(-1)
# pygame.mixer.music.set_volume(volume)


def draw_button(text, x, y, width, height):
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)

    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, DARK_BLUE, button_rect)
    else:
        pygame.draw.rect(screen, BLUE, button_rect)

    button_text = font.render(text, True, WHITE)
    screen.blit(
        button_text,
        (
            x + width // 2 - button_text.get_width() // 2,
            y + height // 2 - button_text.get_height() // 2
        )
    )

    return button_rect


def draw_volume_bar(x, y, width, height, volume):
    pygame.draw.rect(screen, GRAY, (x, y, width, height))

    filled_width = int(width * volume)
    pygame.draw.rect(screen, BLUE, (x, y, filled_width, height))

    volume_text = small_font.render(f"Volume: {int(volume * 100)}%", True, BLACK)
    screen.blit(volume_text, (x, y - 35))


def main_menu():
    global volume

    running = True

    while running:
        clock.tick(60)
        screen.fill(WHITE)

        title_text = title_font.render("Food Frenzy", True, BLUE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        start_button = draw_button("Start", 300, 240, 200, 65)
        quit_button = draw_button("Quit", 300, 330, 200, 65)

        volume_down_button = draw_button("-", 250, 470, 60, 50)
        volume_up_button = draw_button("+", 490, 470, 60, 50)

        draw_volume_bar(320, 485, 160, 20, volume)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    run_game_handler(screen, clock, volume)

                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

                elif volume_down_button.collidepoint(event.pos):
                    volume -= 0.1
                    if volume < 0:
                        volume = 0
                    pygame.mixer.music.set_volume(volume)

                elif volume_up_button.collidepoint(event.pos):
                    volume += 0.1
                    if volume > 1:
                        volume = 1
                    pygame.mixer.music.set_volume(volume)

        pygame.display.update()


main_menu()