import pygame
import random 

# initialize pygame
pygame.init()

# custom event IDs for color change events
SPRITE1_COLOR_CHANGE_EVENT = pygame.USEREVENT + 1
SPRITE2_COLOR_CHANGE_EVENT = pygame.USEREVENT + 2
BACKGROUND_COLOR_CHANGE_EVENT = pygame.USEREVENT + 3
BOTH_SPRITES_COLOR_CHANGE_EVENT = pygame.USEREVENT + 4

# define basic colors using pygame.Color
# background colors
BLUE = pygame.Color("blue")
LIGHT_BLUE = pygame.Color("lightblue")
DARKBLUE = pygame.Color("darkblue")
GREEN = pygame.Color("green")
PURPLE = pygame.Color("purple")
GRAY = pygame.Color("gray")

# sprite colors
YELLOW = pygame.Color("yellow")
MAGENTA  = pygame.Color("magenta")
ORANGE = pygame.Color("orange")
WHITE = pygame.Color("white")
CYAN = pygame.Color("cyan")
RED = pygame.Color("red")
LIME = pygame.Color("lime")
PINK = pygame.Color("pink")

# sprite class representing the moving object 
class Sprite(pygame.sprite.Sprite):

    # constructor method
    def __init__(self, color, height, width, sprite_id):
        # call to the parent class (sprite) constructor
        super().__init__()

        # create the sprite surface with dimensions and color
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # get the sprite's rect defining its position and size
        self.rect = self.image.get_rect()

        # set initial velocity with random direction
        self.velocity = [random.choice([-2, -1, 1, 2]), random.choice([-2, -1, 1, 2])]
        
        # store sprite ID to identify which sprite this is
        self.sprite_id = sprite_id

    # method to update the sprite's position
    def update(self):
        # move the sprite by its velocity 
        self.rect.move_ip(self.velocity)

        # flag to track if the sprite hits a boundary 
        boundary_hit = False

        # check for collision with left or right boundaries and reverse direction
        if self.rect.left <= 0 or self.rect.right >= 500:
            self.velocity[0] = -self.velocity[0]
            boundary_hit = True

        # check for collision with top or bottom boundaries and reverse direction
        if self.rect.top <= 0 or self.rect.bottom >= 400:
            self.velocity[1] = -self.velocity[1]
            boundary_hit = True

        # if a boundary was hit, post events to change colors
        if boundary_hit:
            # Post individual sprite color change event based on sprite ID
            if self.sprite_id == 1:
                pygame.event.post(pygame.event.Event(SPRITE1_COLOR_CHANGE_EVENT))
            elif self.sprite_id == 2:
                pygame.event.post(pygame.event.Event(SPRITE2_COLOR_CHANGE_EVENT))
            
            # Also post background color change event
            pygame.event.post(pygame.event.Event(BACKGROUND_COLOR_CHANGE_EVENT))
            
            # Occasionally post event to change both sprites
            if random.random() < 0.3:  # 30% chance
                pygame.event.post(pygame.event.Event(BOTH_SPRITES_COLOR_CHANGE_EVENT))

    # method to change the sprite's color
    def change_color(self):
        if self.sprite_id == 1:
            # Color palette for sprite 1
            self.image.fill(random.choice([YELLOW, MAGENTA, ORANGE, WHITE, CYAN]))
        else:
            # Color palette for sprite 2
            self.image.fill(random.choice([RED, LIME, PINK, CYAN, ORANGE]))

# function to change the background color
def change_background_color():
    global bg_color
    bg_color = random.choice([BLUE, LIGHT_BLUE, DARKBLUE, GREEN, PURPLE, GRAY])

# create a group to hold the sprites
all_sprites_list = pygame.sprite.Group()
    
# instantiate the first sprite
sp1 = Sprite(WHITE, 20, 30, 1)
# randomly position the sprite
sp1.rect.x = random.randint(50, 200)
sp1.rect.y = random.randint(50, 200)

# instantiate the second sprite  
sp2 = Sprite(RED, 25, 25, 2)
# randomly position the second sprite
sp2.rect.x = random.randint(250, 400)
sp2.rect.y = random.randint(150, 300)

# add the sprites to the group
all_sprites_list.add(sp1)   
all_sprites_list.add(sp2)

# create the game window
screen = pygame.display.set_mode((500, 400))

# set the window title
pygame.display.set_caption("Two Sprites with Custom Color Events")

# set the initial background color
bg_color = BLUE
screen.fill(bg_color)

# game loop control flag
exit_game = False

# create a clock object to control the frame rate
clock = pygame.time.Clock()

# main game loop
while not exit_game:
    # event handling loop
    for event in pygame.event.get():
        # if the window's close button is clicked, exit the game
        if event.type == pygame.QUIT:
            exit_game = True

        # Handle sprite 1 color change event
        elif event.type == SPRITE1_COLOR_CHANGE_EVENT:
            sp1.change_color()
            print("Sprite 1 changed color!")

        # Handle sprite 2 color change event  
        elif event.type == SPRITE2_COLOR_CHANGE_EVENT:
            sp2.change_color()
            print("Sprite 2 changed color!")

        # Handle background color change event
        elif event.type == BACKGROUND_COLOR_CHANGE_EVENT:
            change_background_color()
            print("Background changed color!")

        # Handle both sprites color change event
        elif event.type == BOTH_SPRITES_COLOR_CHANGE_EVENT:
            sp1.change_color()
            sp2.change_color()
            print("Both sprites changed colors!")

    # update all sprites in the group
    all_sprites_list.update()

    # fill the screen with the current background color
    screen.fill(bg_color)

    # draw all sprites onto the screen
    all_sprites_list.draw(screen)

    # refresh the display
    pygame.display.flip()
    
    # limit the frame rate to 60 frames per second
    clock.tick(60)

# quit pygame
pygame.quit()