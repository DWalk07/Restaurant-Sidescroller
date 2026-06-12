import pygame
import random
import sys

#pygame.init()
def run_restaurant(screen, clock, time_remaining, volume, veggie_amount=0, meat_amount=0, fruit_amount=0, total_score = 0):
    window_size = (800,600)
    #screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption('Restaurant SS')

    #load images 
    kitchen_image = pygame.image.load('kitchen_background.png')
    kitchen_image = pygame.transform.scale(kitchen_image, window_size)
    restaurant_image = pygame.image.load('restaurant_background.jpg')
    restaurant_image = pygame.transform.scale(restaurant_image, window_size)
    pixel_smoke_image = pygame.image.load('pixel_smoke.png')
    pixel_smoke_image = pygame.transform.scale(pixel_smoke_image, (50,50))
    white_star_image = pygame.image.load("white_star.png")
    gold_star_image = pygame.image.load("gold_star.png")
    white_star_image = pygame.transform.scale(white_star_image,(150,150))
    gold_star_image = pygame.transform.scale(gold_star_image,(150,150))
    

    #customer images & lists
    customer_1_img = pygame.image.load("pixel_customer_1.png")
    customer_2_img = pygame.image.load("pixel_customer_2.png")
    customer_3_img = pygame.image.load("pixel_customer_3.png")
    customer_4_img = pygame.image.load("pixel_customer_4.png")
    customer_images = [customer_1_img,customer_2_img,customer_3_img,customer_4_img]
    customers = []
    global current_customer_target
    current_customer_target = 250

    #global variables for screen and cooking state
    global current_screen 
    current_screen = restaurant_image
    
    global cooking
    global selecting_dish
    cooking = None
    selecting_dish = False

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
    general_text = general_font.render("Rhythm Score " + str(rhythm_score), True, (255,255,255), (15,15,15))
    button_text1 = general_font.render("Go To", True, (255,255,255)) 
    button_text2 = general_font.render("Ingreedient", True, (255,255,255))
    button_text3 = general_font.render("Catcher", True, (255,255,255))
    time_remaining_text = general_font.render(f"Time Remaining: {time_remaining}", True, (255,255,255), (25,20,15))

    #global variable that tracks the dish you're making/have in hand
    global current_dish
    global dish_list
    current_dish = None
    dish_list = None
    
    global clicked_a_dish
    clicked_a_dish = False

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
        
    #menu volume functions -- same as in main menu
    def draw_button(text, x, y, width, height):
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(x, y, width, height)

        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (40, 90, 130), button_rect)
        else:
            pygame.draw.rect(screen, (70, 130, 180), button_rect)

        button_text = general_font.render(text, True, (255,255,255))
        screen.blit(
            button_text,
            (
                x + width // 2 - button_text.get_width() // 2,
                y + height // 2 - button_text.get_height() // 2
            )
        )

        return button_rect


    def draw_volume_bar(x, y, width, height, volume):
        pygame.draw.rect(screen, (180, 180, 180), (x, y, width, height))

        filled_width = int(width * volume)
        pygame.draw.rect(screen, (70, 130, 180), (x, y, filled_width, height))

        volume_text = general_font.render(f"Volume: {int(volume * 100)}%", True, (0,0,0))
        screen.blit(volume_text, (x, y - 35))

    
    
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
            self.hitbox = None
            self.created = False
        
        def create(self, rhythm_score):
            self.created = True
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
                screen.blit(self.image, (x,y))
                pixel_smoke_image.set_colorkey((255,255,255))
                screen.blit(pixel_smoke_image, (x,y-15))
            else:
                screen.blit(self.image, (x,y))
        
        def draw_dish_button(self, x, y):
            #define hitbox
            self.hitbox = pygame.Rect(x, y, 70, 70)
            #shows the dish and ingreedients in a mini-menu when you go to cook something
            screen.blit(self.image, (x,y))
            i = 1
            for ingreedient, amount in self.requirments.items():
                #green square background for the food if you have enough of it to cook, red if not
                if ingreedient.amount < amount:
                    pygame.draw.rect(screen, (245,10,10), (x, 30+y+50*i, 40, 40))
                else:
                    pygame.draw.rect(screen, (10,245,10), (x, 30+y+50*i, 40, 40))
                
                #ingreedient will be an instance of the food class
                background_color = ingreedient.image.get_at((0,0))
                ingreedient.image.set_colorkey(background_color)
                screen.blit(ingreedient.image, (x,30+y+50*i))
                i+=1
            


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

    class customer(pygame.sprite.Sprite):
        def __init__(self, x, y, order, target_x, speed = 5, state = 1):
            self.image = random.choice(customer_images)
            self.background_color = self.image.get_at((0,0))
            self.image = pygame.transform.scale(self.image, (85,225))
            self.image.set_colorkey(self.background_color)
            self.x = x
            self.y = y
            self.order = order
            self.target_x = target_x
            self.speed = speed
            self.state = state
            self.hitbox = None
            self.patience = 50*60 #50 seconds 60 fps
            self.satisfyied = True #enforcement for patience consequences
        
        def move(self):
            #state 1 is walking into the restaurant
            #state 2 is waiting to be served
            #state 3 is exiting the restaurant
            if self.state == 1:
                if self.x <= self.target_x:
                    self.state = 2
                else:
                    self.x -= self.speed
            if self.state == 3:
                self.x += self.speed
            
            if self.patience <= 0 and self.state == 2:
                self.state = 3
                self.satisfyied = False
        
        def draw(self):
            self.hitbox = pygame.Rect(self.x,self.y,85,255)
            screen.blit(self.image, (self.x, self.y))
            if self.state == 2:
                #draw a picture of the customer's order above their head in state 2
                screen.blit(self.order.image, (self.x, self.y-45))
                self.patience -= 1
                #draw patience meeter
                pygame.draw.rect(screen, (245,20,20), (self.x,self.y-75,50,25))
                pygame.draw.rect(screen, (20,245,20), (self.x,self.y-75,self.patience/60,25))

    def spawn_customer(dish):
        global current_customer_target
        print(current_customer_target)
        if len(customers) < 5:
            #logic to determine how far across the screen the customer will walk
            #loops to find an open space for customer 
            for c in customers:
                if c.target_x == current_customer_target:
                    if current_customer_target >= 750:
                        current_customer_target = 250
                    else:
                        current_customer_target += 100
            
            #loop through again to get front part of customer list now that the customer target has changed
            for c in customers:
                if c.target_x == current_customer_target:
                    if current_customer_target >= 750:
                        current_customer_target = 250
                    else:
                        current_customer_target += 100

            some_dude = customer(1000,325,dish, current_customer_target)
            current_customer_target += 100
            if current_customer_target >= 750:
                current_customer_target = 250

            customers.append(some_dude)

    def make_end_screen():
        if total_score >= 500 and total_score < 750:
            #one star 
            screen.fill((255,255,255))
            screen.blit(gold_star_image, (150,285))
            screen.blit(white_star_image, (300,285))
            screen.blit(white_star_image, (450,285))
            end_text = general_font.render(f"Good Job!  Your Final Score was: {total_score}", True, (15,15,15))
            screen.blit(end_text, (285, 185))

        elif total_score >= 750 and total_score < 1000:
            #two stars
            screen.fill((255,255,255))
            screen.blit(gold_star_image, (150,285))
            screen.blit(gold_star_image, (300,285))
            screen.blit(white_star_image, (450,285))
            end_text = general_font.render(f"Great Job!  Your Final Score was: {total_score}", True, (15,15,15))
            screen.blit(end_text, (285, 185))
        elif total_score > 1000:
            #three stars
            screen.fill((255,255,255))
            screen.blit(gold_star_image, (150,285))
            screen.blit(gold_star_image, (300,285))
            screen.blit(gold_star_image, (450,285)) 
            end_text = general_font.render(f"Fantastic Job!  Your Final Score was: {total_score}", True, (15,15,15))
            screen.blit(end_text, (285, 185)) 
        else:
            #no stars
            screen.fill((255,255,255))
            screen.blit(white_star_image, (150,285))
            screen.blit(white_star_image, (300,285))
            screen.blit(white_star_image, (450,285))
            end_text = general_font.render(f"Get em next time!  Your Final Score was: {total_score}", True, (15,15,15))
            screen.blit(end_text, (285, 185))

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
    fruit_food = food('fruit', fruit_amount, "pixel_fruit.png")
    
    meat_dish_ingreedients = {meat_food: 2}
    salad_ingreedients = {veggie_food: 3, fruit_food: 2}
    stew_ingreedients = {meat_food: 1, veggie_food: 2, fruit_food: 2}

    meat_dish = dish("Steak", "pixel_steak_dish.png", meat_dish_ingreedients)
    salad_dish = dish("Salad", "pixel_salad.png", salad_ingreedients)
    stew_dish = dish("Stew", "pixel_stew.png", stew_ingreedients)
    dish_list = [meat_dish, salad_dish, stew_dish]

    #Game Loop
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            #on click logic start
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    if on_menu == False:
                        clicked_a_dish = False
                        for appliance in appliances:
                            if appliance.hitbox.collidepoint(mouse_pos) and current_screen == kitchen_image:
                                clicked_a_dish = True
                                selecting_dish = True
                            
                            if cooking == None and selecting_dish:
                                
                                for d in dish_list:
                                    #click detection for the dish button
                                    if d.hitbox and d.hitbox.collidepoint(mouse_pos):
                                        can_make_dish = True
                                        
                                        clicked_a_dish = True
                                        for ingreedient, amnt in d.requirments.items():
                                            #ingreedient is a food obj, amnt is an int
                                            if ingreedient.amount < amnt:
                                                #checks to make sure you have enough food to cook the dish
                                                can_make_dish = False
                                                
                                        if can_make_dish:    
                                            #the cooking variable saves the item you're cooking with 
                                            cooking = appliance
                                            current_dish = d
                                            selecting_dish = False
                                            for ingreedient, amnt in d.requirments.items():
                                                #subtract cost of ingreedients
                                                ingreedient.amount -= amnt

                                        else:
                                            print("it's not enough")
                                            

                                if clicked_a_dish == False and selecting_dish:
                                    #takes you off the screen if you click something other than a dish
                                    selecting_dish = False

                        if current_dish != None and current_screen == restaurant_image:
                            for c in customers:
                                if c.hitbox != None and c.hitbox.collidepoint(mouse_pos):
                                    if current_dish == c.order:
                                        print("should give dish")
                                        #turns the customer around and walks them out the store
                                        c.state = 3
                                        c.image = pygame.transform.flip(c.image, True, False)
                                        c.image.set_colorkey(c.background_color)
                                        if current_dish.quality == "great":
                                            total_score += 150
                                        elif current_dish.quality == "good":
                                            total_score += 75
                                        else:
                                            total_score -= 10  
                                        current_dish = None


                        #changes the screen when the rectangle in the top right is clicked on
                        if catcher_button.collidepoint(mouse_pos) and cooking == None:
                            #returning this string signals to the game handler that you want to switch gamemodes
                            return "food_catcher", time_remaining, volume, total_score

                    if on_menu:
                        global volume_up_button
                        global volume_down_button
                        if volume_up_button.collidepoint(event.pos):
                            volume += 0.1
                            if volume > 1:
                                volume = 1
                            pygame.mixer.music.set_volume(volume)    
                        elif volume_down_button.collidepoint(event.pos):
                            volume -= 0.1
                            if volume < 0:
                                volume = 0
                            pygame.mixer.music.set_volume(volume)

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
                time_remaining_text = general_font.render(f"Time Remaining: {time_remaining}", True, (255,255,255),(25,20,15))
                game_time = pygame.time.get_ticks()
                #has a chance to spawn a customer with a random order every second
                #lower chance to get more customers the more you have
                if random.randint(1,100) < 100/(len(customers)+1):
                    spawn_customer(random.choice(dish_list))

            screen.blit(current_screen, (0,0))
            #player and customer movement
            plr.move()
            for c in customers:
                c.move()
                if c.satisfyied == False:
                    #reduce score for leaving a customer unattended
                    total_score -= 25
                    c.satisfyied = True
                if c.x > 1000 and c.state == 3:
                    customers.remove(c)

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
            fruit_food.draw(100, 150)
            
            #draw player sprite
            plr.draw()

            if selecting_dish:
                #drawing the dish selection menu
                meat_dish.draw_dish_button(300, 360)
                salad_dish.draw_dish_button(380, 360)
                stew_dish.draw_dish_button(460, 360)

            #this if statement is repeated to allow the player to be in front of the oven but behind the rhythm blocks
            #this is necessary since both the rhythm blocks and oven only spawn when in the kitchen, but the player needs to be between them
            if current_screen == kitchen_image:
                #cooking logic, cooking global variable used to turn the entire system on/off
                if cooking != None:
                        screen.blit(general_text, (300, 170))
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
                                    current_dish.create(rhythm_score)
                                    rhythm_score = 0
                                    
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
                                    if current_dish:
                                        current_dish.create(rhythm_score)
                                    rhythm_score = 0      
                
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
                            general_text = general_font.render("Rhythm Score " + str(rhythm_score), True, (255,255,255), (15,15,15)) 
                    elif block.lifetime/60 > block.time_window[1]/1000 and block.solved == False: 
                        block.delete_block(False)      
            
            elif current_screen == restaurant_image:
                for dude in customers:
                    dude.draw()

            #draw the dish you've made in a box at the bottom of the screen
            if current_dish != None:
                inventory_text = general_font.render("Inventory", True, (255,255,255), (15,15,15))
                screen.blit(inventory_text, (335, 470))
                current_dish.draw(350,510)
            
            #draw score at the top of the screen
            score_text = general_font.render(f"Score: {total_score}", True, (255,255,255), (15,15,15))
            screen.blit(score_text, (275,100))

        elif on_menu:
            show_menu(screen)

            #draw volume control
            #global volume_down_button
            #global volume_up_button
            volume_down_button = draw_button("-", 250, 370, 60, 50)
            volume_up_button = draw_button("+", 490, 370, 60, 50)

            draw_volume_bar(320, 385, 160, 20, volume)

        screen.blit(time_remaining_text, (340, 40))

        #end screen
        if time_remaining <= 0:
            make_end_screen()

        pygame.display.update()
        clock.tick(60)