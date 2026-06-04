import pygame
pygame.init()

window_size = (800,600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Restaurant SS')

#load images 
kitchen_image = pygame.image.load('kitchen_background.png')
kitchen_image = pygame.transform.scale(kitchen_image, window_size)
restaurant_image = pygame.image.load('restaurant_background.jpg')
restaurant_image = pygame.transform.scale(restaurant_image, window_size)

current_screen = restaurant_image
clock = pygame.time.Clock()

#player class, taking in position and sprite 
class player(pygame.sprite.Sprite):
        def __init__(self, startingX=100, startingY=400):
            self.x = startingX
            self.y = startingY
            self.speed = 7
            self.image = pygame.image.load('pixel_chef.png')
            self.image = pygame.transform.scale(self.image, (50,150))
        
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
            self.image = pygame.transform.scale(self.image, (50,150))
        elif self.type == 'oven':
            self.image = pygame.image.load('pixel_oven.png')
            self.image = pygame.transform.scale(self.image, (50,150))

    def stove_cook(self):
        #rhythm game for cooking on a stove
        print("stove cook")
         
    def oven_cook(self):
        #rhythm game for cooking in an oven
        print("oven cook")

    def draw(self):
        screen.blit(self.image, self.hitbox)
        

class rhythm_block():
    def __init__(self, character, time_window, x, y):
        #the rhythm blocks for minigame  
        self.character = character
        self.time_window = time_window
        self.x = x
        self.y = y
    
    def draw(self):
        #blits a specific circle and ring around that circle
        #position of ring relative to circle should correspond with time in the time window
        # 3 seperate circles - 1 ring, 2 layered for the block itself
        print("draw")
    
    def delete_block(self):
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
hitboxes = [stove1.hitbox, stove2.hitbox, stove3.hitbox, stove4.hitbox]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                for hitbox in hitboxes:
                    if hitbox.collidepoint(mouse_pos):
                        print("clicked on stove")
                        
                        

    screen.blit(current_screen, (0,0))
    #screenChange('restaurant')
    #screenChange('kitchen')
    plr.move()
    
    plr.draw()

    #room change logic
    print(plr.x)
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
       
        stove1.draw()
        stove2.draw()
        stove3.draw()
        stove4.draw()

    pygame.display.update()
    clock.tick(60)