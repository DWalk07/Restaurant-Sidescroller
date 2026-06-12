#determines when to run the restaurant code or the food-catcher code
#allows for the restaurant and food catchers to share variables(mainly amount of food you have and money)
import pygame
from restaurant import run_restaurant
from food_catcher import run_food_catcher

def run_game_handler(screen, clock, volume=0.5):
    pygame.mixer.music.set_volume(volume)
    time_remaining = 300
    total_score = 0
    #these variables track the amount of each type of food gathered in the catcher and pass it into the restaurant
    veg = 0
    meat = 0
    fruit = 0

    current = "restaurant"
    while current != "quit":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_ESCAPE:
            #         if on_menu == False:
            #             on_menu = True
            #         else:
            #             on_menu = False

        if current == "restaurant":
            current, time_remaining, volume, score = run_restaurant(screen,clock, time_remaining, volume, veg, meat, fruit, total_score)
            total_score = score
            score = 0
        elif current == "food_catcher":
            current, time_remaining, veggie, meats, fruits, score = run_food_catcher(screen,clock, time_remaining)
            veg += veggie
            meat += meats
            fruit += fruits
            print("total score", total_score)
            total_score += score
            print("total score", total_score)
            score = 0
    return "menu"

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    run_game_handler(screen, clock)