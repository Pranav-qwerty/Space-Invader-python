import pygame
import random
import math
from pygame import mixer
from time import sleep

# initiation the pygame
pygame.init()

# creates a screen using pygame
screen = pygame.display.set_mode((800, 700))  # first argument is for width and second for height

# Title, Icon and Background
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('icon.jpg')
icon = pygame.transform.scale(icon, (64, 64))
pygame.display.set_icon(icon)
background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (900, 700))
mixer.music.load('backgroundsou.wav')
mixer.music.play(-1)

# Player
player_img = pygame.image.load('spaceship.png')
playerX = 370
playerY = 610
playerX_change = 0

# Space Invaders
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemy = 6
for i in range(num_enemy):
    enemy_img.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyY_change.append(40)
    enemyX_change.append(0.25)

# Bullet
bullet_img = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = 'ready'
# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score :"+str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Game Over function
gameo = pygame.font.Font('freesansbold.ttf', 64)


def game_over():
    score = gameo.render("GAME OVER", True, (255, 0, 0))
    screen.blit(score, (200, 250))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, t):
    screen.blit(enemy_img[1], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img, (x + 16, y + 10))


def collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:
    # fill the screen with colour
    screen.fill((0, 0, 0))
    # Background
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        # Making a exit function
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed then check whether it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.25
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.25
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bulletsou = mixer.Sound("lasersou.wav")
                    bulletsou.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    # Player Movement
    playerX += playerX_change
    # boundaries for the spaceship
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Enemy Movement
    for i in range(num_enemy):
        # Game over
        if enemyY[i] > 440:
            for j in range(num_enemy):
                enemyY[j] = 2000
            game_over()
            sleep(1)
            break
        enemyX[i] += enemyX_change[i]
        # boundaries for the invader
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # check for collision
        collisio = collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collisio:
            explosou = mixer.Sound("explosionsou.wav")
            explosou.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value = score_value + 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        # setting up the enemy position
        enemy(enemyX[i], enemyY[i], i)

    # setting up player position
    player(playerX, playerY)
    # show the score_value in the screen
    show_score(textX, textY)
    # reload the screen
    pygame.display.update()
