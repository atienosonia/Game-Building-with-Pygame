import pygame  
pygame.init()  
grey = (58,58,58)  

# Clock
clock = pygame.time.Clock()
  
display_surface = pygame.display.set_mode((500, 500))  
  
# set the pygame window name   
pygame.display.set_caption('My First Game Screen')  
  
image = pygame.image.load('Pokemon.jpg')  

# Set the size for the image
DEFAULT_IMAGE_SIZE = (300,300)
  
# Scale the image to your needed size
image = pygame.transform.scale(image, DEFAULT_IMAGE_SIZE)

# Set a default position
DEFAULT_IMAGE_POSITION = (100,100)

# infinite loop   
while True:  
	display_surface.fill(grey)  
	display_surface.blit(image, DEFAULT_IMAGE_POSITION)  

	for event in pygame.event.get():  
		if event.type == pygame.QUIT:  
			pygame.quit()  
			# quit the program.   
			quit()  
		
	# Part of event loop
	pygame.display.flip()
	clock.tick(30)