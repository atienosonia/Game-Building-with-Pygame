# import necesarry libraries
import pygame

# initialize required modules
pygame.init()

# setup window geometry 
screen = pygame.display.set_mode((400, 300))

# create a looop to run till the fane is quite by the user
done = False

while not done:

    # clear the event queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # make the changes visible
    pygame.display.flip()