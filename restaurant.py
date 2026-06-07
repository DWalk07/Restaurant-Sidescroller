import pygame
import random

pygame.init()

window_size = (800,600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Restaurant SS')

#load images 
kitchen_image = pygame.image.load('kitchen_background.png')
kitchen_image = pygame.transform.scale(kitchen_image, window_size)
restaurant_image = pygame.image.load('restaurant_background.jpg')
restaurant_image = pygame.transform.scale(restaurant_image, window_size)

#global variables for screen and cooking state
current_screen = restaurant_image
global cooking
cooking = None
global cooking_timer
cooking_timer = 0
global current_time
current_time = pygame.time.get_ticks()
blocks_on_screen = []
global blocks_made
blocks_made = 0
possible_rhythm_chars = ['w', 's', 'r', 't', 'f', 'g', 'h', 'j', 'k', 'l','v', 'z', 'm']

clock = pygame.time.Clock()
cook_event = pygame.USEREVENT + 1


#player class, taking in position and sprite 
class player(pygame.sprite.Sprite):
        def __init__(self, startingX=100, startingY=400):
            self.x = startingX
            self.y = startingY
            self.speed = 7
            self.image = pygame.image.load('pixel_chef.png')
            self.image = pygame.transform.scale(self.image, (50,150))
            self.image.set_colorkey((255,255,255)) #makes white background transparent

        def move(self):
            keys = pygame.key.get_pressed()
            #left and right movement on left and right keys or a and d keys
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.x -= self.speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.x += self.speed

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
            self.image = pygame.transform.scale(self.image, (50,50))#scales to the height and width of the hitbox
        elif self.type == 'oven':
            self.image = pygame.image.load('pixel_oven.png')
            self.image = pygame.transform.scale(self.image, (50,50))

    def stove_cook(self):
        print("stove cook")
        # #rhythm game for cooking on a stove
        # keys = pygame.key.get_pressed()
        
        # #spawn a rhythm block every half second
        # for i in range(10):
        #     delta_time = clock.tick(60) 
        #     if delta_time >= 500: #placeholder for timing, should be based on the quality of the stove and the dish being cooked
        #         print("block spawn start")
        #         #randomly generate a character for the rhythm block, for now just using 'a' as a placeholder
        #         char = 'a'
        #         block = rhythm_block(char,(250, 750), 100 + i*60, 200) #example of spawning a rhythm block, time window of 2 seconds and x position based on index
        #         block.draw()
        #         delta_time = 0
        #         if keys[pygame.K_a]: #placeholder for checking if the correct key is pressed, should be based on the character of the block
        #             print("correct key pressed")
        #             block.delete_block(True) #placeholder for deleting the block if the correct key is pressed, should also check if it's within the time window for scoring purposes
             
    def oven_cook(self):
        #rhythm game for cooking in an oven
        print("oven cook")

    def draw(self):
        screen.blit(self.image, self.hitbox)
        

class rhythm_block(pygame.sprite.Sprite):
    def __init__(self, character, time_window, x, y, lifetime = 0):
        #the rhythm blocks for minigame  
        #self.image = pygame.Surface((50,50), pygame.SRCALPHA) #creates a transparent surface for the block
        super().__init__()
        self.character = character
        self.time_window = time_window
        self.x = x
        self.y = y
        font = pygame.font.SysFont('Arial', 30)
        self.font = font
        self.lifetime = lifetime
    
    def draw(self):
        #blits a specific circle and ring around that circle
        #position of ring relative to circle should correspond with time in the time window
        # 3 seperate circles - 1 ring, 2 layered for the block itself
        pygame.draw.circle(screen, (185,180,175), (self.x,self.y), 20) #inner circle
        pygame.draw.circle(screen, (185 ,180,175), (self.x,self.y), 25) #outer ring
        text = self.font.render(self.character, True, (255, 255, 255))
        screen.blit(text, (self.x - 10, self.y - 10))
        self.lifetime += 1
        #print("draw")
    
    def delete_block(self, correct):
        if correct:
            print("should turn green")
        else:
            print("should turn red")
        #self deletion - supposedly the kill() method removes all refs to an instance
        self.kill()    



#printing the actual image on the screen for a room change, 
#can be used to generate all things related to that room as well
def screenChange(next_screen):
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
stove1 = cooking_appliance('stove', pygame.Rect(100, 300, 50, 50), 1)
stove2 = cooking_appliance('stove', pygame.Rect(200, 300, 50, 50), 1)
stove3 = cooking_appliance('stove', pygame.Rect(300, 300, 50, 50), 1)
stove4 = cooking_appliance('stove', pygame.Rect(400, 300, 50, 50), 1)
oven1 = cooking_appliance('oven', pygame.Rect(100, 450, 50, 50), 1)
oven2 = cooking_appliance('oven', pygame.Rect(200, 450, 50, 50), 1)
oven3 = cooking_appliance('oven', pygame.Rect(300, 450, 50, 50), 1)
oven4 = cooking_appliance('oven', pygame.Rect(400, 450, 50, 50), 1)
appliances = [stove1, stove2, stove3, stove4, oven1, oven2, oven3, oven4]
#hitboxes = [stove1.hitbox, stove2.hitbox, stove3.hitbox, stove4.hitbox, oven1.hitbox, oven2.hitbox, oven3.hitbox, oven4.hitbox]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                for appliance in appliances:
                    if appliance.hitbox.collidepoint(mouse_pos):
                        pygame.time.set_timer(cook_event, 500) #placeholder for starting the cooking process, should be based on the quality of the appliance and the dish being cooked
                        cooking = appliance


    screen.blit(current_screen, (0,0))
    plr.move()
    
    plr.draw()

    #room change logic
    if plr.x < 0 and current_screen == restaurant_image:
        #left side of the screen when in the restaurant takes you to the kitchen
        print("should go to kitchen")
        screenChange("kitchen")
        plr.x = 775
    elif plr.x > 800 and current_screen == kitchen_image:
        #right side of the screen when in the kitchen takes you to the restaurant
        print("should go to restaurant")
        screenChange("restaurant")
        plr.x = 25
     
    #drawing everything in kitchen
    if current_screen == kitchen_image:
       for appliance in appliances:
           appliance.draw()

    #cooking logic, cooking global variable used to turn the entire system on/off
    if cooking != None:
            if cooking.type == 'stove':
                if pygame.time.get_ticks() - current_time >= 500:
                    if blocks_made < 10:
                        current_time = pygame.time.get_ticks() 
                        char = random.choice(possible_rhythm_chars)
                        current_block = rhythm_block(char, (250,750), random.randint(160, 600), random.randint(200, 400)) 
                        blocks_on_screen.append(current_block)
                        blocks_made += 1
                        print("0.5 seconds should have passed")
                    else:
                        print("should stop cooking")
                        cooking = None
                        blocks_made = 0
                        blocks_on_screen = [] 
                        
            elif cooking.type == 'oven':
                cooking.oven_cook()       

    for block in blocks_on_screen:
        block.draw()
        if block.lifetime/60 >= block.time_window[0]/1000 and block.lifetime/60 <= block.time_window[1]/1000: #placeholder for checking if the block is within the time window, should be based on the quality of the appliance and the dish being cooked
            print("block is within time window")
                # keys = pygame.key.get_pressed()
                # if keys[pygame.K_a]: #placeholder for checking if the correct key is pressed, should be based on the character of the block
                #     print("correct key pressed")
                #     block.delete_block(True) #placeholder for deleting the block if the correct key is pressed, should also check if it's within the time window for scoring purposes    
    pygame.display.update()
    clock.tick(60)