# import neccesary libraries
import pygame
pygame.init()
white = (128, 128, 128)


clock = pygame.time.Clock()

# create the display surface object of specific dimension..(x,y)
display_surface = pygame.display.set_mode((500,500))

# set the pygame window name
pygame.display.set_caption("Image")

# create a surface object, image is drawn on it.
# YOU NEED TO HAVE THE IMAGE FILE INSIDE THE GAME BUILDING WITH PYGAME FOLDER
image = pygame.image.load("buglife1.jpg")

# set the size for the size for the image
DEFAULT_IMAGE_SIZE = (200, 200)

# select the image to your needed size
image = pygame.transform.scale(image, DEFAULT_IMAGE_SIZE)

# set a default position
DEFAULT_IMAGE_POSITION = (150, 150)

# infinite loop
while True:
    display_surface.fill(white)
    display_surface.blit(image, DEFAULT_IMAGE_POSITION)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            # quite the program
            quit()
     
     # part of the event loop
    pygame.display.flip()
    clock.tick(30)