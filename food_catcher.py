import pygame
import random
import sys

# Initialize pygame
#pygame.init()

def run_food_catcher(screen, clock, time_remaining):
    # Screen setup
    WIDTH = 800
    HEIGHT = 600
    #screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Food Catcher Game")
    background = pygame.image.load("grocery.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    game_time = pygame.time.get_ticks()
    # Clock
    #clock = pygame.time.Clock()
    FPS = 60

    # Colors
    WHITE = (255, 255, 255)
    BLUE = (70, 130, 180)
    RED = (220, 50, 50)
    GREEN = (50, 180, 80)
    BLACK = (0, 0, 0)
    BROWN = (139, 69, 19)

    YELLOW = (255, 223, 0)
    ORANGE = (255, 140, 0)
    PURPLE = (160, 80, 200)

    foods = [
        {"name": "apple", "color": RED, "points": 1},
        {"name": "banana", "color": YELLOW, "points": 2},
        {"name": "broccoli", "color": GREEN, "points": 3},
        {"name": "burger", "color": BROWN, "points": 5}
    ]

    current_food = random.choice(foods)

    # Font
    font = pygame.font.SysFont("Arial", 30)

    # Cart setup
    cart_width = 120
    cart_height = 40
    cart_x = WIDTH // 2 - cart_width // 2
    cart_y = HEIGHT - 70
    cart_speed = 8

    # Food setup
    food_size = 35
    food_x = random.randint(0, WIDTH - food_size)
    food_y = -food_size
    food_speed = 5
    current_food = random.choice(foods)

    # Game variables
    score = 0
    lives = 3
    veggies_collected = 0
    meat_collected = 0
    fruit_collected = 0


    def draw_cart(x, y):
        """Draws the cart."""
        pygame.draw.rect(screen, BLUE, (x, y, cart_width, cart_height))
        pygame.draw.circle(screen, BLACK, (x + 25, y + cart_height), 10)
        pygame.draw.circle(screen, BLACK, (x + cart_width - 25, y + cart_height), 10)

    def draw_food(x, y, food):
        """Draws different foods based on the current food type."""

        if food["name"] == "apple":
            pygame.draw.circle(screen, RED, (x + food_size // 2, y + food_size // 2), food_size // 2)
            pygame.draw.rect(screen, BROWN, (x + food_size // 2 - 3, y, 6, 10))

        elif food["name"] == "banana":
            pygame.draw.ellipse(screen, YELLOW, (x, y + 8, food_size, food_size // 2))
            pygame.draw.ellipse(screen, WHITE, (x + 5, y + 5, food_size, food_size // 2))

        elif food["name"] == "broccoli":
            pygame.draw.circle(screen, GREEN, (x + 10, y + 15), 10)
            pygame.draw.circle(screen, GREEN, (x + 20, y + 10), 10)
            pygame.draw.circle(screen, GREEN, (x + 28, y + 16), 10)
            pygame.draw.rect(screen, BROWN, (x + 15, y + 18, 8, 15))

        elif food["name"] == "burger":
            pygame.draw.rect(screen, BROWN, (x, y + 8, food_size, 10))
            pygame.draw.rect(screen, GREEN, (x, y + 18, food_size, 6))
            pygame.draw.rect(screen, RED, (x, y + 24, food_size, 6))
            pygame.draw.rect(screen, BROWN, (x, y + 30, food_size, 8))

    def reset_food():
        """Resets food to the top and randomly chooses a new food."""
        new_x = random.randint(0, WIDTH - food_size)
        new_y = -food_size
        new_food = random.choice(foods)
        return new_x, new_y, new_food

    def show_text():
        """Displays score and lives."""
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        time_remaining_text = font.render(f"Time Remaining: {time_remaining}", True, WHITE)
        screen.blit(score_text, (20, 20))
        screen.blit(lives_text, (WIDTH - 120, 20))
        screen.blit(time_remaining_text, (WIDTH // 2 - 20, 20))

    # Main game loop
    running = True

    while running:
        print(screen)
        clock.tick(FPS)
        screen.blit(background, (0, 0))

        #decrease time remaining every second
        if game_time + 1000 <= pygame.time.get_ticks():
            time_remaining -= 1
            game_time = pygame.time.get_ticks()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Key movement
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and cart_x > 0:
            cart_x -= cart_speed

        if keys[pygame.K_RIGHT] and cart_x < WIDTH - cart_width:
            cart_x += cart_speed

        # Move food down
        food_y += food_speed

        # Create rectangles for collision
        cart_rect = pygame.Rect(cart_x, cart_y, cart_width, cart_height)
        food_rect = pygame.Rect(food_x, food_y, food_size, food_size)

        # Check if cart catches food
        if cart_rect.colliderect(food_rect):
            #increase the specific amount of food collected for the restaurant ingreedients
            if current_food["name"] == "apple" or ["name"] == "banana":
                fruit_collected += 1
            elif current_food["name"] == "broccoli":    
                veggies_collected += 1
            elif current_food["name"] == "burger":
                meat_collected += 1    
            score += current_food["points"]
            food_x, food_y, current_food = reset_food()

            # Make the game harder as score increases
            if score % 5 == 0:
                food_speed += 1

        # Check if food hits the ground
        if food_y > HEIGHT:
            lives -= 1
            food_x, food_y, current_food = reset_food()

        # Draw game objects
        draw_cart(cart_x, cart_y)
        draw_food(food_x, food_y, current_food)
        show_text()

        # Game over
        if lives <= 0:
            game_over_text = font.render("GAME OVER", True, RED)
            final_score_text = font.render(f"Final Score: {score}", True, YELLOW)
            returning_text = font.render("returning to restaurant", True, YELLOW)

            # Black box size
            box_width = 420
            box_height = 200

            # Center the box on the screen
            box_x = WIDTH // 2 - box_width // 2
            box_y = HEIGHT // 2 - box_height // 2

            # Draw black box
            pygame.draw.rect(screen, BLACK, (box_x, box_y, box_width, box_height))

            screen.blit(game_over_text, (WIDTH // 2 - 90, HEIGHT // 2 - 40))
            screen.blit(final_score_text, (WIDTH // 2 - 100, HEIGHT // 2))
            screen.blit(returning_text, (WIDTH // 2 - 90, HEIGHT // 2 + 50))

            pygame.display.update()
            pygame.time.wait(3000)
            #switch back to restaurant screen once done
            return "restaurant", time_remaining, veggies_collected, meat_collected, fruit_collected
            #running = False

        pygame.display.update()

    pygame.quit()
    sys.exit()