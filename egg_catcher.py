import random
from pygame import mixer
import pygame

# initialize pygame
pygame.init()

# Initial setup
screen = pygame.display.set_mode((955, 537))
background = pygame.image.load('bgimage.jpeg')
pygame.display.set_caption('Egg Catcher')

# bg sound
mixer.music.load('bgsound.mp3')
mixer.music.play(-1)

# player
playerImg = pygame.image.load('basket.png')
playerx = 100
playery = 380
playery_change = 0
playerx_change = 0


# player function
def player(x, y):
    screen.blit(playerImg, (x, y))


# eggs
crackImg = pygame.image.load('yellow crack.png')
crackImg1 = pygame.image.load('white crack.png')
crackImg2 = pygame.image.load('black crack.png')

eggImg = [
    pygame.image.load('yellow egg.png'),
    pygame.image.load('white egg.png'),
    pygame.image.load('yellow egg.png'),
    pygame.image.load('black egg.png')
]

egg_x = []
egg_y = []
eggy_y_change = []
number_of_eggs = 4

for i in range(number_of_eggs):
    egg_x.append(random.randint(0, 570))
    egg_y.append(random.randint(0, 100))
    eggy_y_change.append(4)


# Egg function
def egg(x, y, i):
    screen.blit(eggImg[i], (x, y))


def eggCollison():
    if egg_y[i] >= 450:
        return True
    else:
        return False


# score display
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textx = 10
texty = 50


# Score display function
def showscore(x, y):
    score_value = font.render('Score : ' + str(score), True, (255, 255, 255))
    screen.blit(score_value, (x, y))


# Game over text
game_font = pygame.font.Font('freesansbold.ttf', 40)
reason_font = pygame.font.Font('freesansbold.ttf', 20)


# function to display game over text
def game_over_text():
    text = game_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(text, (300, 230))
    text1 = reason_font.render('Do not catch black eggs', True, (255, 0, 0))
    screen.blit(text1, (300, 280))


# victory_font
victory_font = pygame.font.Font('freesansbold.ttf', 45)


def game_over2():
    score_value = victory_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(score_value, (300, 230))
    text1 = reason_font.render('Time limit exceeded', True, (255, 0, 0))
    screen.blit(text1, (350, 280))


def victory():
    score_value = victory_font.render('YOU WON', True, (255, 255, 255))
    screen.blit(score_value, (300, 230))


# pause text
pause_font = pygame.font.Font('freesansbold.ttf', 40)


def pause_text():
    text = pause_font.render('GAME PAUSED', True, (255, 255, 255))
    screen.blit(text, (300, 230))


# time left font
time_font = pygame.font.Font('freesansbold.ttf', 32)

# timer
sec = 30

# Time display function
def showtimer():
    score_value = time_font.render('Time Left : ' + str(int(sec)), True, (255, 255, 255))
    screen.blit(score_value, (700, 20))


def showlevel():
    score_value = font.render('Level :', True, (255, 255, 255))
    screen.blit(score_value, (700, 60))
    score_value = font.render('             Easy', True, (0, 255, 0))
    screen.blit(score_value, (700, 60))
    score_value = font.render('Target : 35', True, (255, 255, 255))
    screen.blit(score_value, (700, 100))


# Game loop
running = True
pause = False
Exit = False
target = 35

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change -= 10
            if event.key == pygame.K_RIGHT:
                playerx_change += 10

            # check when to restart
            if event.key == pygame.K_SPACE:
                Exit = False
                score = 0
                for j in range(3):
                    egg_x[j] = random.randint(0, 570)
                    egg_y[j] = random.randint(0, 100)

            # check when to pause/resume the game
            if event.key == pygame.K_UP:
                if pause:
                    pause = False
                else:
                    pause = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    # boundary restriction
    if playerx <= -30:
        playerx = -30
    elif playerx > 700:
        playerx = 700

    for i in range(number_of_eggs):
        if egg_y[i] >= 600:
            egg_x[i] = random.randint(0, 570)
            egg_y[i] = random.randint(0, 100)

        egg_y[i] += eggy_y_change[i]
        if egg_y[i] <= 450:
            egg(egg_x[i], egg_y[i], i)

        # check when to display cracked eggs
        if eggCollison():
            if egg_y[1] >= 450:
                screen.blit(crackImg1, (egg_x[1] - 10, 450))
            elif egg_y[0] >= 450:
                screen.blit(crackImg, (egg_x[0] - 10, 450))
            elif egg_y[2] >= 450:
                screen.blit(crackImg, (egg_x[2] - 10, 450))
            elif egg_y[3] >= 450:
                screen.blit(crackImg2, (egg_x[3] - 10, 450))

        # check when egg collide with basket
        egg_rect = pygame.Rect(egg_x[i], egg_y[i], 32, 50)
        rot_rect = pygame.Rect(egg_x[3], egg_y[3], 32, 52)
        basket_rect = pygame.Rect(playerx + 40, playery + 30, 80, 120)
        if egg_rect.colliderect(basket_rect):
            if rot_rect.colliderect(basket_rect) and egg_y[i] <= 450:
                Exit = True
            else:
                egg_x[i] = random.randint(0, 570)
                egg_y[i] = random.randint(0, 100)
                score += 1


        if pause:
            egg_x[i] = 2000
            pause_text()
            break

        if Exit:
            egg_x[i] = 2000
            game_over_text()
            sec = 30
            break

        if score == target:
            egg_x[i] = 2000
            victory()
            sec = 30
            break

        seconds = int(sec)
        if sec <= 0:
            egg_x[i] = 2000
            game_over2()
            break

    if not pause:
        sec -= 1 / 72  # 72 iterations per second

    showtimer()
    showscore(20, 20)
    showlevel()

    playerx += playerx_change
    player(playerx, playery)
    pygame.display.update()
