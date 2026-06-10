import pygame
import random
import sys

#pygame.init()
def run_restaurant(screen, clock, time_remaining, meat_amount=0, veggie_amount=0, fruit_amount=0):
    window_size = (800,600)
    #screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption('Restaurant SS')

    #load images 
    kitchen_image = pygame.image.load('kitchen_background.png')
    kitchen_image = pygame.transform.scale(kitchen_image, window_size)
    restaurant_image = pygame.image.load('restaurant_background.jpg')
    restaurant_image = pygame.transform.scale(restaurant_image, window_size)
    pixel_smoke_image = pygame.image.load('pixel_smoke.png')

    #global variables for screen and cooking state
    global current_screen 
    current_screen = restaurant_image
    
    global cooking
    cooking = None

    global game_time
    #timer for whole game, will track every second spent not in the menu
    game_time = pygame.time.get_ticks()
    
    global current_time
    #timer for rhythm block spawning, tracks 3/4 seconds
    current_time = pygame.time.get_ticks()

    blocks_on_screen = []
    #tracks how many rhythm blocks have been made during a cooking session
    global blocks_made
    blocks_made = 0
    possible_rhythm_chars = ['w', 's', 'r', 't', 'f', 'g', 'h', 'j', 'k', 'v', 'z', 'm']

    #stores the score you get from any given rhythm minigame, resets to 0 once finished
    global rhythm_score
    rhythm_score = 0

    global general_text 
    global general_font
    global button_text
    global time_remaining_text
    general_font = pygame.font.SysFont('Arial', 22)
    #general_text gets redefined every time the score changes later in the code, it is predefined here tho
    general_text = general_font.render("Score " + str(rhythm_score), True, (255,255,255), (15,15,15))
    button_text1 = general_font.render("Go To", True, (255,255,255)) 
    button_text2 = general_font.render("Ingreedient", True, (255,255,255))
    button_text3 = general_font.render("Catcher", True, (255,255,255))
    time_remaining_text = general_font.render(f"Time Remaining: {time_remaining}", True, (255,255,255), (25,20,15))

    #global variable that tracks the dish you're making/have in hand
    global current_dish
    current_dish = None
    
    #button to switch to food catcher minigame
    catcher_button = pygame.Rect(550, 100, 100, 65)

    #global variables for menu 
    global on_menu
    on_menu = False

    menu_font = pygame.font.SysFont('Arial', 50)

    global menu_header
    menu_header = menu_font.render("MAIN MENU", True, (255,255,255), (15,15,15))
    menu_body_font = pygame.font.SysFont('Arial', 25)

    global menu_escape
    global menu_sound_text
    menu_escape = menu_body_font.render("press the esc key to exit", True, (255,255,255), (15,15,15))
    menu_sound_text = menu_body_font.render("Sound",True, (255,255,255), (15,15,15))# a slider representing volume will be there
        
    clock = pygame.time.Clock()


    #player class, taking in position and sprite 
    class player(pygame.sprite.Sprite):
            def __init__(self, startingX=100, startingY=325):
                self.x = startingX
                self.y = startingY
                self.speed = 7
                self.image = pygame.image.load('pixel_chef.png')
                self.image = pygame.transform.scale(self.image, (60,225))
                self.image.set_colorkey((255,255,255)) #makes white background transparent
                self.direction = "right"

            def move(self):
                keys = pygame.key.get_pressed()
                #left and right movement on left and right keys or a and d keys
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    if plr.x > 100 or current_screen == restaurant_image:
                        #stops player from moving left if about to go off screen when there isn't a screen to the left
                        self.x -= self.speed
                        
                        #flips the player image around if they turn
                        if self.direction == "right":
                            self.direction = "left"
                            self.image = pygame.transform.flip(self.image, True, False)
                            self.image.set_colorkey((255,255,255))
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    if plr.x < 750 or current_screen == kitchen_image:
                        #stops player from moving left if about to go off screen when there isn't a screen to the right
                        self.x += self.speed
                        
                        #flips the player image around if they turn
                        if self.direction == "left":
                            self.direction = "right"
                            self.image = pygame.transform.flip(self.image, True, False)
                            self.image.set_colorkey((255,255,255))
                

            def draw(self):
                screen.blit(self.image, (self.x,self.y))

    class menu():
        def __init__(self, items):
            self.items = items
            self.font = pygame.font.SysFont('Arial', 30)
        
        #drawing the menu
        def draw(self):
            #loop through each item in the menu array and print it
            for i, item in enumerate(self.items):
                text = self.font.render(item, True, (255, 255, 255))
                screen.blit(text, (100, 100 + i * 40))

    class food(pygame.sprite.Sprite):
        #a class for the food the player uses to cook
        def __init__(self, type, amount, image):
            self.type = type
            self.amount = amount
            self.image = pygame.image.load(image)
            self.image = pygame.transform.scale(self.image, (40,40))
            self.font = pygame.font.SysFont('Arial', 20)
        
        def draw(self, x, y):
            screen.blit(self.image, (x,y))
            text = self.font.render(f"{self.amount}", True, (0, 0, 0),(255,255,255))
            screen.blit(text, (x + 40, y+10))

    class dish(pygame.sprite.Sprite):
        #a class for the dishes the player cooks
        def __init__(self, name, image, requirements, quality = None):
            self.name = name
            self.image = pygame.image.load(image)
            self.image = pygame.transform.scale(self.image, (70,70))
            self.requirments = requirements #will be a list of ingreedients and the quantity of each
            #quality goes "burnt" --> "good" --> "great"
            self.quality = quality
        
        def create(self, rhythm_score):
            #creates the dish with a quality based on the rhythm score of the cooking minigame
            if rhythm_score < 40:
                self.quality = "burnt"
            elif rhythm_score < 75:
                self.quality = "good"
            else:
                self.quality = "great"

        def draw(self, x, y):
            #if burnt, darken the image, if great, add white smoke particles above sprite
            if self.quality == "burnt":
                burnt_img = self.image.copy()
                #creates a blended darker image of the original dish image
                burnt_img.fill((12,12,12,255), None, pygame.BLEND_RGBA_MULT)
                screen.blit(burnt_img, (x,y))
            elif self.quality == "great":
                screen.blit(pixel_smoke_image, (x,y-15))
                screen.blit(self.image, (x,y))
            else:
                screen.blit(self.image, (x,y))
            


    class cooking_appliance():
        #class for stoves, ovens, and cooking in general
        def __init__(self, type, hitbox , quality):
            #type parameter determines how the cooking functions, cooking 
            #on a stove will be different then cooking in an oven and you'll cook different things in each
            self.type = type
            
            self.hitbox = hitbox 
            
            #quality is how you can upgrade appliances (3 levels)
            #higher quality means shorter cooking times and more forgiving scoring on rythm portion 
            self.quality = quality
            if self.type == 'stove':
                self.image = pygame.image.load('pixel_stove.png')
                self.image = pygame.transform.scale(self.image, (hitbox.width,hitbox.height))#scales to the height and width of the hitbox
            elif self.type == 'oven':
                self.image = pygame.image.load('pixel_oven.png')
                self.image = pygame.transform.scale(self.image, (hitbox.width,hitbox.height))

        def draw(self):
            screen.blit(self.image, self.hitbox)
            

    class rhythm_block(pygame.sprite.Sprite):
        def __init__(self, character, time_window, x, y, lifetime = 0, solved = False):
            #the rhythm blocks for minigame  
            super().__init__()
            self.character = character
            self.time_window = time_window
            self.x = x
            self.y = y
            font = pygame.font.SysFont('Arial', 30)
            self.font = font
            self.lifetime = lifetime
            self.red = 100
            self.blue = 220
            self.green = 70
            self.solved = solved
            self.radius = 30
        def draw(self):
            #blits a specific circle and ring around that circle
            #position of ring relative to circle should correspond with time in the time window
            # 3 seperate circles - 1 ring, 2 layered for the block itself
            pygame.draw.circle(screen, (185,180,175), (self.x,self.y), self.radius) #outer circle
            pygame.draw.circle(screen, (self.red, self.green, self.blue), (self.x,self.y), 20) #inner ring
            text = self.font.render(self.character, True, (255, 255, 255))
            screen.blit(text, (self.x - 8, self.y - 18))
            self.lifetime += 1
            self.radius -= 0.15
        
        def delete_block(self, correct):
            if correct:
                self.red = 20
                self.green = 245  
                self.blue = 20
            else:
                self.red = 245
                self.green = 20
                self.blue = 20
            #self deletion - supposedly the kill() method removes all refs to an instance
            self.kill()    

    #function to show the main menu on screen
    def show_menu(screen):
        #blit menu options when on menu after pressing the escape key
        screen.fill((240,200,30))
        screen.blit(menu_header, (300,100))
        screen.blit(menu_escape, (230, 200))
        screen.blit(menu_sound_text, (230, 300))

    #printing the actual image on the screen for a room change, 
    #can be used to generate all things related to that room as well
    def screen_change(next_screen):
        global current_screen
        if next_screen == 'kitchen':
            current_screen = kitchen_image
            screen.blit(kitchen_image, (0,0))
        elif next_screen == 'restaurant':
            current_screen = restaurant_image
            screen.blit(restaurant_image, (0,0))
            

    #initializing player
    plr = player()

    #initializing stovetops
    # stove1 = cooking_appliance('stove', pygame.Rect(100, 300, 50, 50), 1)
    # stove2 = cooking_appliance('stove', pygame.Rect(200, 300, 50, 50), 1)
    # stove3 = cooking_appliance('stove', pygame.Rect(300, 300, 50, 50), 1)
    # stove4 = cooking_appliance('stove', pygame.Rect(400, 300, 50, 50), 1)
    oven1 = cooking_appliance('oven', pygame.Rect(168, 368, 130, 130), 1)
    # oven2 = cooking_appliance('oven', pygame.Rect(200, 450, 50, 50), 1)
    # oven3 = cooking_appliance('oven', pygame.Rect(300, 450, 50, 50), 1)
    # oven4 = cooking_appliance('oven', pygame.Rect(400, 450, 50, 50), 1)
    #appliances = [stove1, stove2, stove3, stove4, oven1, oven2, oven3, oven4]
    appliances = [oven1]
    #hitboxes = [stove1.hitbox, stove2.hitbox, stove3.hitbox, stove4.hitbox, oven1.hitbox, oven2.hitbox, oven3.hitbox, oven4.hitbox]

    meat_food = food('meat', meat_amount, "pixel_meat.png")
    veggie_food = food('veggie', veggie_amount, "pixel_veggie.png")
    carrot_food = food('carrot', 0, "pixel_carrot.png")
    fruit_food = food('fruit', fruit_amount, "pixel_fruit.png")
    
    #Game Loop
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
            if event.type == pygame.MOUSEBUTTONDOWN and on_menu == False:
                if event.button == 1:
                    mouse_pos = event.pos
                    for appliance in appliances:
                        if appliance.hitbox.collidepoint(mouse_pos) and current_screen == kitchen_image:
                            if cooking == None:
                                #the cooking variable saves the item you're cooking with 
                                cooking = appliance
                    #changes the screen when the rectangle in the top right is clicked on
                    if catcher_button.collidepoint(mouse_pos) and cooking == None:
                        #returning this string signals to the game handler that you want to switch gamemodes
                        return "food_catcher", time_remaining
            
            #show menu when esc is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if on_menu == False:
                        on_menu = True
                    else: 
                        on_menu = False        
        
        if not on_menu:
            #decrease time remaining every second
            if game_time + 1000 <= pygame.time.get_ticks():
                time_remaining -= 1
                #global time_remaining_text
                time_remaining_text = general_font.render(f"Time Remaining: {time_remaining}", True, (255,255,255),(25,20,15))
                game_time = pygame.time.get_ticks()

            screen.blit(current_screen, (0,0))
            plr.move()

            #room change logic
            if plr.x < 0 and current_screen == restaurant_image:
                #left side of the screen when in the restaurant takes you to the kitchen
                print("should go to kitchen")
                screen_change("kitchen")
                plr.x = 750
            elif plr.x > 800 and current_screen == kitchen_image:
                #right side of the screen when in the kitchen takes you to the restaurant
                print("should go to restaurant")
                screen_change("restaurant")
                plr.x = 25
            
            #allows you to collect ingreedients via the food catcher game if you aren't cooking
            #(click detection code is with the click detection code for the stove/oven)
            if cooking == None:
                pygame.draw.rect(screen, (240, 100, 30), catcher_button)
                screen.blit(button_text1,(catcher_button.x+5, catcher_button.y - 2))
                screen.blit(button_text2,(catcher_button.x+5, catcher_button.y+15))
                screen.blit(button_text3,(catcher_button.x+5, catcher_button.y+33))

            #drawing everything in kitchen
            if current_screen == kitchen_image:
                #had multiple appliances before but shortened it to one oven
                for appliance in appliances:
                    appliance.draw()
            
            #food display
            meat_food.draw(100, 50)
            veggie_food.draw(100, 100)
            carrot_food.draw(100, 150)
            fruit_food.draw(100, 200)
            
            #draw player sprite
            plr.draw()

            #this if statement is repeated to allow the player to be in front of the oven but behind the rhythm blocks
            #this is necessary since both the rhythm blocks and oven only spawn when in the kitchen, but the player needs to be between them
            if current_screen == kitchen_image:
                #cooking logic, cooking global variable used to turn the entire system on/off
                if cooking != None:
                        screen.blit(general_text, (300, 100))
                        if cooking.type == 'stove':
                            if pygame.time.get_ticks() - current_time >= 750:
                                #every time we go to create a block we check if less than 10 have been made rather than checking at all times
                                if blocks_made < 10:
                                    current_time = pygame.time.get_ticks() 
                                    #gives the rhythm block a random character from the possible characters list
                                    char = random.choice(possible_rhythm_chars)
                                    current_block = rhythm_block(char, (250,1000), random.randint(160, 600), random.randint(200, 400)) 
                                    #add the block that we made to this global list so it can be displayed for its lifetime
                                    blocks_on_screen.append(current_block)
                                    blocks_made += 1
                                else:
                                    cooking = None
                                    blocks_made = 0
                                    blocks_on_screen = []
                                    #make dish 
                                    #current_dish
                                    
                        elif cooking.type == 'oven':
                            if pygame.time.get_ticks() - current_time >= 750:
                                #every time we go to create a block we check if less than 10 have been made rather than checking at all times
                                if blocks_made < 10:
                                    current_time = pygame.time.get_ticks() 
                                    #gives the rhythm block a random character from the possible characters list
                                    char = random.choice(possible_rhythm_chars)
                                    current_block = rhythm_block(char, (250,1000), random.randint(160, 600), random.randint(200, 400)) 
                                    #add the block that we made to this global list so it can be displayed for its lifetime
                                    blocks_on_screen.append(current_block)
                                    blocks_made += 1
                                else:
                                    cooking = None
                                    blocks_made = 0
                                    blocks_on_screen = []
                                    #make dish       
                
                #logic for existing rhythm blocks
                for block in blocks_on_screen:
                    #draws every rhythm block that has been created since the cooking start
                    block.draw()
                    if block.lifetime/60 >= block.time_window[0]/1000 and block.lifetime/60 <= block.time_window[1]/1000: #placeholder for checking if the block is within the time window, should be based on the quality of the appliance and the dish being cooked
                        keys = pygame.key.get_pressed()
                        #making the character in the appropiate notation
                        block_char = "K_"+ block.character
                        #this if statement checks if the key the character pressed is correct by checking the specific pygame key that the block is displaying
                        if pygame.key.get_pressed()[getattr(pygame, block_char)] and block.solved == False: 
                            #when the correct key is pressed for a block it will add to the score (delete only changes the color rn)
                            block.solved = True
                            block.delete_block(True)
                            rhythm_score += 10*cooking.quality
                            #update text with new score
                            general_text = general_font.render("Score " + str(rhythm_score), True, (255,255,255), (15,15,15)) 
                    elif block.lifetime/60 > block.time_window[1]/1000 and block.solved == False: 
                        block.delete_block(False)      
        elif on_menu:
            show_menu(screen)

        screen.blit(time_remaining_text, (340, 40))

        pygame.display.update()
        clock.tick(60)