
#Elizabeth Fatade

import pygame
from pygame import mixer
import random
import math
import fileinput

#Function to draw the player
def player(x, y):
    screen.blit(player_image, (x, y))

#Function to draw the Enemy 
def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))

#Function to draw the bullet and fire it
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x + 16, y + 10))

#Function to check whther the bullet has hit an enemy
def collide(enemyx, enemyy, bulletx, bullety):
    d = math.sqrt((enemyx - bulletx)**2 + (enemyy - bullety)**2) 
    if d < 27:
        return True
    else:
        return False

#Function to show the score of the player
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

#Function to show high score
def show_high_score(x, y, high_score):
    highscore = high_font.render("High Score: " + str(high_score), True, (255, 255, 255))
    screen.blit(highscore, (x, y))

#Function to show game over
def game_over_text():
    over_text = game_over_font.render("GAME OVER! ", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

#Initialize the pygame 
pygame.init()

#Create the sccreen
screen = pygame.display.set_mode((800, 600))

#Create background image
background = pygame.image.load('background.png').convert_alpha()

#Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png').convert_alpha()
pygame.display.set_icon(icon)

#Score 
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

#High score
infile = open("highscore.txt", "r")
high_score = infile.readline()
infile.close()
high_font = pygame.font.Font('freesansbold.ttf', 32)
hightext_x = 10
hightext_y = 38

#Game over text
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

#Player
player_image = pygame.image.load('player.png').convert_alpha()
player_x = 370
player_y = 480
playerx_change = 0

#Enemy
enemy_image = []
enemy_x = []
enemy_y = []
enemyx_change = []
enemyy_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_image.append(pygame.image.load('enemy.png').convert_alpha())
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemyx_change.append(20)
    enemyy_change.append(40) 

#Bullet
bullet_image = pygame.image.load('bullet.png').convert_alpha()
bullet_x = 0
bullet_y = 480
bulletx_change = 4 
bullety_change = 40

#'ready' state means you cannot see bullet and 'fire' state means when bullet is moving
bullet_state = "ready"

#GAME LOOP
screen_running = True
while screen_running:

    #RGB - Red, Green, Blue       
    screen.fill((0, 0, 0))

    #Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            screen_running = False

        #if keystroke is presssed
        if event.type == pygame.KEYDOWN:
            #check whther left
            if event.key == pygame.K_LEFT:
                 playerx_change = -15

            #check whther right
            if event.key == pygame.K_RIGHT:
                 playerx_change = 15
                       
            #check whther space
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    #Play bullet sound
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()

                    #Gets the current x coordinate of the spaceship
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    #setting up boundary for player, so it does not go out of bounds
    player_x += playerx_change

    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    #setting up movement for enemy
    #Put everything in a for loop so that it makes sure the event happens for each enemy and it counts it
    for i in range(num_of_enemies):
        #Game over
        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[i] = 2000
            game_over_text()
            break

        #Enemy movement
        enemy_x[i] += enemyx_change[i]
        
        if enemy_x[i] <= 0:
            enemyx_change[i] = 20
            enemy_y[i] += enemyy_change[i]
        elif enemy_x[i] >= 736:
            enemyx_change[i] = -20
            enemy_y[i] += enemyy_change[i]
        
        #Collision
        collision =  collide(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            #Play explosion sound
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()

            bullet_y = 480
            bullet_state = "ready"
            score_value += 1 
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)

        #Update the high score and keep a record of it
        for line in fileinput.FileInput("highscore.txt", inplace=1):
            line = int(line)
            if score_value > line:
                high_score = score_value 
                line = str(line)
                line = line.replace(line, str(high_score))
            print(line)
        
        #Call the enemy function
        enemy(enemy_x[i], enemy_y[i], i)


    #Bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullety_change

    #call the functions    
    player(player_x, player_y)  
    show_score(textX, textY)
    show_high_score(hightext_x, hightext_y, high_score)

    #update the window each time
    pygame.display.update()