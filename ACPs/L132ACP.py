import math
import random
import pygame # pygame is a library for creating video games

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

# Resize-related constants (reduced sizes)
PLAYER_WIDTH = 48
PLAYER_HEIGHT = 48
ENEMY_WIDTH = 48
ENEMY_HEIGHT = 48
COLLISION_DISTANCE = 25

# initialize pygame
pygame.init()

# create the screen 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# caption and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("ufo-clean.png")
pygame.display.set_icon(icon)

# Add clock for frame rate control
clock = pygame.time.Clock()

# background image
background = pygame.image.load("space.jpg")

# player
playerImg = pygame.image.load("player-clean.png")
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
num_of_enemies = 6

# creating enemies
for i in range(num_of_enemies):
    img = pygame.image.load("enemy-clean.png")
    img = pygame.transform.scale(img, (ENEMY_WIDTH, ENEMY_HEIGHT))  # scale enemy down
    enemyImg.append(img)
    enemyX.append(random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH))
    enemyY.append(random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX))
    enemyX_change.append(ENEMY_SPEED_X)
    enemyY_change.append(ENEMY_SPEED_Y)

# initializing bulltet variables
# bullet

bulletImg = pygame.image.load("bullet-clean.png")
# optional: scale bullet so it matches new sizes (uncomment / adjust if desired)
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
    # display the current score on the screen
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# function to display game over text 
def game_over_text():
    # display the game over text
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# function to draw the player
def player(x, y):
    # draw the player
    screen.blit(playerImg, (x, y))

# function to draw the enemy 
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# function to fire a bullet
def fire_bullet(x, y):
    # fire a bullet from the player's position
    global bullet_state 
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# function to check for collision
def isCollision(enemyX, enemyY, bulletX, bulletY):
    # check if there is a collision between the enemy and a bullet
    distance = math.sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
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
    # use PLAYER_WIDTH for boundary clamp instead of hard-coded 64
    playerX = max(0, min(playerX, SCREEN_WIDTH - PLAYER_WIDTH))

    # enemy movement
    for i in range(num_of_enemies):
        if enemyY[i] > 340:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        # use ENEMY_WIDTH for edge checks
        if enemyX[i] <= 0 or enemyX[i] >= SCREEN_WIDTH - ENEMY_WIDTH:
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change[i]

        # collision detection
        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            score_value += 1                      # <- increment score
            bulletY = PLAYER_START_Y
            bullet_state = "ready"
            # respawn enemy using ENEMY_WIDTH constant
            enemyX[i] = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
            enemyY[i] = random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX)

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