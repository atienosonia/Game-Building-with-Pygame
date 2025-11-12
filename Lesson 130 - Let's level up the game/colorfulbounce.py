import  pygame
import random 

# initialize pygame
pygame.init()

# custom event IDs for color change events
SPRITE_COLOR_CHANGE_EVENT = pygame.USEREVENT + 1
BACKGROUND_COLOR_CHANGE_EVENT = pygame.USEREVENT + 2

# define basic colors using pygame.Color
# background colors
BLUE = pygame.Color("blue")
LIGHT_BLUE = pygame.Color("lightblue")
DARKBLUE = pygame.Color("darkblue")

# sprite colors
YELLOW = pygame.Color("yellow")
MAGENTA  = pygame.Color("magenta")
ORANGE = pygame.Color("orange")
WHITE = pygame.Color("white")
CYAN = pygame.Color("cyan")

# sprite class representing the moving object 
class Sprite(pygame.sprite.Sprite):

    # constructor method
    def __init__(self, color, height, width):

        # call to the parent class (sprite) constructor
        super().__init__()

        # create the sprite surface with dimensions and color
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # get the sprite's rect defining its position and size
        self.rect = self.image.get_rect()

        # set initial velocity with random direction
        self.velocity = [random.choice([-1, 1]), random.choice([-1, 1])]

    # method to update the sprite's position
    def update(self):
        # move the sprite by its velocity 
        self.rect.move_ip(self.velocity)

        # flag to track if the sprite hits a boundary 
        boundary_hit = False

        # check for collision with left or right boundaries and reverse direction
        if self.rect.left <= 0 or self.rect.right >=500:
            self.velocity[0] = -self.velocity[0]
            boundary_hit = True

        # check for collision with top or bottom boundaries and reverse direction
        if self.rect.top <= 0 or self.rect.bottom >=400:
            self.velocity[1] = -self.velocity[1]
            boundary_hit = True

        # if a boundary was hit, post events to change colors
        if boundary_hit:
            pygame.event.post(pygame.event.Event(SPRITE_COLOR_CHANGE_EVENT))

            pygame.event.post(pygame.event.Event(BACKGROUND_COLOR_CHANGE_EVENT))

    # method to change the sprite's color
    def change_color(self):
        self.image.fill(random.choice([YELLOW, MAGENTA, ORANGE, WHITE, CYAN]))

    # function to change the background color
    @staticmethod
    def change_background_color():
        global bg_color
        bg_color = random.choice([BLUE, LIGHT_BLUE, DARKBLUE])

# create a group to hold the sprite
all_sprites_list = pygame.sprite.Group()
    
# instantiate the sprite
sp1 = Sprite(WHITE, 20, 30)

# randomly position the sprite
sp1.rect.x = random.randint(0, 480)
sp1.rect.y = random.randint(0, 370)

# add the sprite to the group
all_sprites_list.add(sp1)   

# create the game window
screen = pygame.display.set_mode((500, 400))

# set the window title
pygame.display.set_caption("Colorful Bounce")

# set the initial background color
bg_color = BLUE
screen.fill(bg_color)
# game loop control flag
running = False
exit = False

# create a clock object to control the frame rate
clock = pygame.time.Clock()
# main game loop
while not running:
    # event handling loop
    for event in pygame.event.get():
        # if the window's close button is clicked, exit the game
        if event.type == pygame.QUIT:
            running = True
            exit = True

        # if the sprite color change event is triggered, change the background color
        elif event.type == SPRITE_COLOR_CHANGE_EVENT:
            sp1.change_color()

        # if the background color change event is triggered, change the background color
        elif event.type == BACKGROUND_COLOR_CHANGE_EVENT:
            Sprite.change_background_color()

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
    clock.tick(240)
# quit pygame
pygame.quit()

