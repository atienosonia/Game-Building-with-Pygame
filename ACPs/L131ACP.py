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

# initialize pygame
pygame.init()

# create the screen 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# caption and icon
pygame.display.set_caption("Space Invader - 7 Enemies")
icon = pygame.image.load("ufo-clean.png")
pygame.display.set_icon(icon)

# Add clock for frame rate control
clock = pygame.time.Clock()

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

# bullet variables
bulletImg = pygame.image.load("bullet-clean.png")
bulletImg = pygame.transform.scale(bulletImg, (12, 24))

bulletX = 0
bulletY = PLAYER_START_Y
bulletX_change = 0
bulletY_change = BULLET_SPEED_Y
bullet_state = "ready"

# score and rendering
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX  = 10
textY = 10 

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

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

# function to fire a bullet
def fire_bullet(x, y):
    global bullet_state 
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# function to check for collision between enemy and bullet
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    return distance < COLLISION_DISTANCE

# function to check for collision between player and enemy
def isPlayerCollision(playerX, playerY, enemyX, enemyY):
    distance = math.sqrt((playerX - enemyX) ** 2 + (playerY - enemyY) ** 2)
    return distance < COLLISION_DISTANCE

# game loop 
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bulletX = playerX
                bulletY = PLAYER_START_Y
                fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP and event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
            playerX_change = 0

    # player movement 
    playerX += playerX_change
    playerX = max(0, min(playerX, SCREEN_WIDTH - PLAYER_WIDTH))

    # enemy movement
    for i in range(num_of_enemies):
        # Game over condition - if enemy reaches bottom
        if enemyY[i] > 340:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0 or enemyX[i] >= SCREEN_WIDTH - ENEMY_WIDTH:
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change[i]

        # Collision detection between bullet and enemy
        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            score_value += 1  # Increase score by 1 when collision occurs
            bulletY = PLAYER_START_Y
            bullet_state = "ready"
            # Respawn enemy at random position
            enemyX[i] = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
            enemyY[i] = random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX)

        # Collision detection between player and enemy
        if isPlayerCollision(playerX, playerY, enemyX[i], enemyY[i]):
            score_value += 1  # Increase score by 1 when player collides with enemy
            # Respawn enemy at random position
            enemyX[i] = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
            enemyY[i] = random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX)
            # Optional: Add player penalty or effect here

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = PLAYER_START_Y
        bullet_state = "ready"
    elif bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()

    # control the frame rate
    clock.tick(60)

pygame.quit()