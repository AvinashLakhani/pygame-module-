import pygame
from pygame import mixer

pygame.init()

# screen
win = pygame.display.set_mode((800, 600))

# title
pygame.display.set_caption('Ping Pong')


# background music

mixer.music.load('background_ping.mp3')
mixer.music.play(loops=-1)


# colours
black = (0, 0, 0)
white = (255, 255, 255)
grey = (200, 200, 200)
red = (200, 0, 0)
blue = (0, 0, 200)

# paddle a
paddle_aX = 30
paddle_aY = 250
paddle_aY_change = 0


def paddle_a(x, y):
    paddle_a_ = pygame.draw.rect(win, blue, [x, y, 20, 100])
    return paddle_a_


# paddle b
paddle_bX = 745
paddle_bY = 250
paddle_bY_change = 0


def paddle_b(x, y):
    paddle_b_ = pygame.draw.rect(win, red, [x, y, 20, 100])
    return paddle_b_


# ball
ball_X = 380
ball_Y = 280
ball_X_change = 0.3
ball_Y_change = 0.3


def ball(x, y):
    pygame.draw.rect(win, white, [x, y, 20, 20])


# score
font = pygame.font.Font('freesansbold.ttf', 30)
player_1_score = 0
player_2_score = 0
scoreX = 250
scoreY = 0


def score(x, y):
    score_ = font.render(f'player A :{player_1_score}  player B :{player_2_score}', True, white)
    win.blit(score_, (x, y))


# game loop
running = True
while running:

    # background
    win.fill(black)
    # exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                paddle_aY_change = -0.5
            if event.key == pygame.K_s:
                paddle_aY_change = 0.5

            if event.key == pygame.K_UP:
                paddle_bY_change = -0.5
            if event.key == pygame.K_DOWN:
                paddle_bY_change = 0.5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                paddle_aY_change = 0

            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                paddle_bY_change = 0

    paddle_aY += paddle_aY_change
    paddle_a(paddle_aX, paddle_aY)

    paddle_bY += paddle_bY_change
    paddle_b(paddle_bX, paddle_bY)

    # boundary checking
    if paddle_aY <= 1:
        paddle_aY = 1
    if paddle_aY >= 500:
        paddle_aY = 500
    if paddle_bY <= 1:
        paddle_bY = 1
    if paddle_bY >= 500:
        paddle_bY = 500

    # ball

    ball_Y += ball_Y_change

    if ball_Y >= 580:
        ball_Y_change = -0.3
    if ball_Y <= 1:
        ball_Y_change = 0.3

    ball_X += ball_X_change
    if ball_X >= 780:
        ball_X = 380
        ball_X_change = - 0.3
        player_1_score += 1
    if ball_X <= 1:
        ball_X = 380
        ball_X_change = 0.3
        player_2_score += 1
    ball(ball_X, ball_Y)

    # score
    score(scoreX, scoreY)

    # ball and paddle collision
    if paddle_bX - 20 < ball_X < paddle_bX and (paddle_bY + 100 > ball_Y > paddle_bY):
        ball_X_change = -0.3
    if paddle_aX - 20 < ball_X < paddle_aX + 20 and (paddle_aY + 100 > ball_Y > paddle_aY):
        ball_X_change = 0.3

    pygame.display.update()
