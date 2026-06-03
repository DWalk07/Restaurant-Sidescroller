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

current_screen = "restaurant"
clock = pygame.time.Clock()

#player class, taking in position and sprite 
class player(pygame.sprite.Sprite):
        def __init__(self, startingX=100, startingY=500):
            self.x = startingX
            self.y = startingY
            self.speed = 3
            self.image = pygame.image.load('pixel_chef.png')
            self.image = pygame.transform.scale(self.image, (50,50))
        
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

    def stove_cook():
        #rythm game for cooking on a stove
        print("stove cook")
         
    def oven_cook():
        #rythm game for cooking in an oven
        print("oven cook")


#screen change logic
def screenChange(nextScreen):
    if nextScreen == 'kitchen':
        screen.blit(kitchen_image, (0,0))
    elif nextScreen == 'restaurant':
        screen.blit(restaurant_image, (0,0))

#initializing player
plr = player()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                print(mouse_pos)
                #if         

    screen.blit(restaurant_image, (0,0))
    #screenChange('restaurant')
    #screenChange('kitchen')
    plr.move()
    
    plr.draw()
    pygame.display.update()
    clock.tick(60)