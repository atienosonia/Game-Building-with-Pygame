import math
import random
import pygame 

# constants 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
PLAYER_START_X = 370
PLAYER_START_Y = 380
ENEMY_START_Y_MIN = 50
ENEMY_START_Y_MAX = 150
ENEMY_SPEED_X = 4
ENEMY_SPEED_Y = 40 
BULLET_SPEED_Y = 10

# Resize-related constants
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 80
ENEMY_WIDTH = 98
ENEMY_HEIGHT = 98
COLLISION_DISTANCE = 25

# initialize pygame and mixer for sound
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound

# create the screen 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# caption and icon
pygame.display.set_caption("Space Invader - With Background Sound")
icon = pygame.image.load("ufo-clean.png")
pygame.display.set_icon(icon)

# Add clock for frame rate control
clock = pygame.time.Clock()

# Load background sound as MP3
try:
    background_sound = pygame.mixer.Sound("audio-new.mp3")  # MP3 background sound
    background_sound.set_volume(0.3)  # Set volume (0.0 to 1.0)
    print("MP3 audio file loaded successfully!")
except pygame.error as e:
    print(f"Sound loading error: {e}")
    print("Make sure you have the sound file: audio-new.mp3")
    # Create dummy sound object to avoid crashes
    background_sound = pygame.mixer.Sound(buffer=bytearray())

# background image
background = pygame.image.load("test-space-new3.jpg")

# player
playerImg = pygame.image.load("test-player-new1-clean.png")
# scale player down so it appears smaller
playerImg = pygame.transform.scale(playerImg, (PLAYER_WIDTH, PLAYER_HEIGHT))
playerX = PLAYER_START_X
playerY = PLAYER_START_Y
playerX_change = 0

# enemy and bullet setup 
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 7  # Changed to 7 enemies as requested

# creating 7 enemies
for i in range(num_of_enemies):
    img = pygame.image.load("new-thanos-clean.png")
    img = pygame.transform.scale(img, (ENEMY_WIDTH, ENEMY_HEIGHT))
    enemyImg.append(img)
    enemyX.append(random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH))
    enemyY.append(random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX))
    enemyX_change.append(ENEMY_SPEED_X)
    enemyY_change.append(ENEMY_SPEED_Y)

# bullet variables - CHANGED: Now using multiple bullets
bulletImg = pygame.image.load("bullet-clean.png")
bulletImg = pygame.transform.scale(bulletImg, (12, 24))

# CHANGED: Using list for multiple bullets
bullets = []  # List to store active bullets: each bullet is [x, y]
bullet_speed = BULLET_SPEED_Y

# score and rendering
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX  = 10
textY = 10 

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Game state variables
game_over = False
sound_playing = False

# Spacebar state tracking
space_pressed = False

# function to show score
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# function to display game over text 
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# function to draw the player
def player(x, y):
    screen.blit(playerImg, (x, y))

# function to draw the enemy 
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# CHANGED: Function to fire a bullet (adds new bullet to list)
def fire_bullet(x, y):
    bullets.append([x + PLAYER_WIDTH // 2 - 6, y])  # Center the bullet on player

# function to check for collision between enemy and bullet
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    return distance < COLLISION_DISTANCE

# function to check for collision between player and enemy
def isPlayerCollision(playerX, playerY, enemyX, enemyY):
    distance = math.sqrt((playerX - enemyX) ** 2 + (playerY - enemyY) ** 2)
    return distance < COLLISION_DISTANCE

# Start background sound
try:
    # Play background sound in loop (-1 means infinite loop)
    background_sound.play(-1)
    sound_playing = True
    print("Background MP3 sound started - playing throughout game")
except:
    print("Could not play background MP3 sound")

# game loop 
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # CHANGED: Track spacebar state for continuous firing
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                space_pressed = True  # Spacebar is being pressed
        
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                playerX_change = 0
            if event.key == pygame.K_SPACE:
                space_pressed = False  # Spacebar is released
            
            # Restart game with R key when game over
            if event.key == pygame.K_r and game_over:
                # Reset game state
                game_over = False
                score_value = 0
                playerX = PLAYER_START_X
                playerY = PLAYER_START_Y
                bullets.clear()  # Clear all bullets
                # Reset enemies
                for i in range(num_of_enemies):
                    enemyX[i] = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
                    enemyY[i] = random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX)
                    enemyX_change[i] = ENEMY_SPEED_X
                # Restart background sound if it stopped
                if not sound_playing:
                    background_sound.play(-1)
                    sound_playing = True

    if not game_over:
        # CHANGED: Continuous bullet firing when spacebar is held down
        if space_pressed:
            fire_bullet(playerX, playerY)

        # player movement 
        playerX += playerX_change
        playerX = max(0, min(playerX, SCREEN_WIDTH - PLAYER_WIDTH))

        # CHANGED: Bullet movement and collision (using list of bullets)
        bullets_to_remove = []
        enemies_to_respawn = []
        
        for bullet in bullets[:]:  # Iterate over a copy of the list
            bullet[1] -= bullet_speed  # Move bullet upward
            
            # Remove bullet if it goes off screen
            if bullet[1] <= 0:
                bullets_to_remove.append(bullet)
                continue
            
            # Check collision with each enemy for this bullet
            for i in range(num_of_enemies):
                if isCollision(enemyX[i], enemyY[i], bullet[0], bullet[1]):
                    score_value += 1
                    bullets_to_remove.append(bullet)
                    enemies_to_respawn.append(i)
                    break
        
        # Remove bullets that hit enemies or went off screen
        for bullet in bullets_to_remove:
            if bullet in bullets:
                bullets.remove(bullet)
        
        # Respawn enemies that were hit
        for i in enemies_to_respawn:
            enemyX[i] = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
            enemyY[i] = random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX)

        # enemy movement
        for i in range(num_of_enemies):
            # Game over condition - if enemy reaches bottom
            if enemyY[i] > 340:
                game_over = True
                # Stop background sound when game over
                background_sound.stop()
                sound_playing = False
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0 or enemyX[i] >= SCREEN_WIDTH - ENEMY_WIDTH:
                enemyX_change[i] *= -1
                enemyY[i] += enemyY_change[i]

            # Collision detection between player and enemy
            if isPlayerCollision(playerX, playerY, enemyX[i], enemyY[i]):
                score_value += 1  # Increase score by 1 when player collides with enemy
                # Respawn enemy at random position
                enemyX[i] = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
                enemyY[i] = random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX)

            enemy(enemyX[i], enemyY[i], i)

        # CHANGED: Draw all active bullets
        for bullet in bullets:
            screen.blit(bulletImg, (bullet[0], bullet[1]))

        player(playerX, playerY)
        show_score(textX, textY)
    else:
        # Game over state
        game_over_text()
        restart_font = pygame.font.Font('freesansbold.ttf', 24)
        restart_text = restart_font.render("Press R to Restart", True, (255, 255, 255))
        screen.blit(restart_text, (300, 350))

    pygame.display.update()

    # control the frame rate
    clock.tick(60)

# Stop sound before quitting
pygame.mixer.stop()
pygame.mixer.quit()
pygame.quit()