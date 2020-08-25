import pygame
import random
import math
from pygame import mixer

# intialize the pygame
pygame.init()

# screen
screen = pygame.display.set_mode((900, 601))

# title
pygame.display.set_caption('Space invaders')

# icon
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# background image
background = pygame.image.load('background.jpg')

# background music
mixer.music.load('background.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(loops=-1)

# colour
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 200, 0)
white = (255, 255, 255)

# player
playerimg = pygame.image.load('spaceship.png')
playerX = 420
playerY = 480
playerX_change = 0


def player(x, y):
    screen.blit(playerimg, (x, y))


# enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 836))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


# Bullet
bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bullet_state = "ready"


def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 8))


# score
score_value = 0
score_font = pygame.font.Font('font.ttf', 32)
scoreX = 10
scoreY = 10


def score(x, y):
    score = score_font.render('Score = ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# collisison
def IsCollision(enemyx, enemyy, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyx - bulletX, 2)) + (math.pow(enemyy - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# game over
game_over_font = pygame.font.Font('font.ttf', 60)


def game_over():
    game_over = game_over_font.render('GAME OVER', True, (255, 0, 0))
    screen.blit(game_over, (200, 200))


# restart
re_font = pygame.font.Font('freesansbold.ttf', 32)


def restart_text():
    restart = re_font.render('wanna play again?', True, (255, 255, 255))
    screen.blit(restart, (280, 280))


# game loop
running = True
while running:

    screen.fill((0, 0, 0))
    # background

    screen.blit(background, (0, 0))
    player(playerX, playerY)

    for event in pygame.event.get():
        # exit
        if event.type == pygame.QUIT:
            running = False

        # controls

        # keyboard
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('bullet.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # borderline for player
    if playerX <= 1:
        playerX = 1
    if playerX >= 836:
        playerX = 836
    if playerY <= 1:
        playerY = 1
    if playerY >= 536:
        playerY = 536

    # enemy movement
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        enemy(enemyX[i], enemyY[i], i)
        if enemyX[i] <= 1:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 836:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # collision
        collision = IsCollision(enemyX[i], enemyY[i], bulletX, bulletY)

        if collision:
            explosive_sound = mixer.Sound('Explosion.wav')
            explosive_sound.play()
            bullet_state = "ready"
            bulletY = 480
            enemyX[i] = random.randint(0, 836)
            enemyY[i] = random.randint(0, 150)
            score_value += 1

        # game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 1000
                game_over()

    # score
    score(scoreX, scoreY)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        bullet(bulletX, bulletY)
        bulletY_change = 7
        bulletY -= bulletY_change

    pygame.display.update()
