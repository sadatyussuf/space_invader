import pygame
import random
import sys
import math
from pygame import mixer

# Initializing Pygame
pygame.init()

# Size of the screen
HEIGHT = 600
WIDTH = 800

# Keeps tally of the score
score_value = 0

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set icon
iconImg = pygame.image.load('images/ufo.png')
pygame.display.set_icon(iconImg)

# Set Caption
pygame.display.set_caption('Space Invaders')

# Background Image
backgroundImg = pygame.image.load('images/background.png')

# Background Sound
mixer.music.load('misc/background.wav')
mixer.music.play(-1)

# The player image, position and rate of change
playerImg = pygame.image.load('images/player.png')
playerX = 370
playerY = 480
player_change = 0

# The enemy image, position and rate of change
# enemyImg = pygame.image.load('images/enemy.png')
# enemyX = random.randint(0, 750)
# enemyY = random.randint(70, 100)
# enemyX_change = 5
# enemyY_change = 40
num_of_enemies = 6
enemyX_change = []
enemyY_change = []
enemyImg = []
enemyX = []
enemyY = []
# Enemy Bullet image and position
enemy_bulletImg = []
enemy_bulletY = []
enemy_bulletX = []
enemy_bullet_state = 'ready'

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('images/enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

    # Enemy Bullet image and position
# for i in range(int(num_of_enemies/2)):
    enemy_bulletImg.append(pygame.image.load('images/minus.png'))
    enemy_bulletX.append(0)
    enemy_bulletY.append(0)

# # Enemy Bullet image and position
# enemy_bulletImg = pygame.image.load('images/minus.png')
# enemy_bulletY = 0
# enemy_bulletX = 0
# enemy_bullet_state = 'ready'

# Player Bullet image and position
player_bulletImg = pygame.image.load('images/bullet.png')
player_bulletY = 480
player_bulletX = 0
player_bullet_state = 'ready'

# The heart image representing the life of the player
num_of_heartImg = 3
heartImg = []
heartX = [705, 725, 745]
heartY = 10
for i in range(num_of_heartImg):
    # creating the heart image
    heartImg.append(pygame.image.load('images/life.png'))

# Score text
score_font = pygame.font.Font('freesansbold.ttf', 32)

# Game Over text
game_over_font = pygame.font.Font('freesansbold.ttf', 64)


def life_bar(x, y, i):
    screen.blit(heartImg[i], (x, y))


def display_player(player_x, player_y):
    screen.blit(playerImg, (player_x, player_y))


# def display_enemy(enemy_x, enemy_y):
#     screen.blit(enemyImg, (enemy_x, enemy_y))
def display_enemy(enemy_x, enemy_y, i):
    screen.blit(enemyImg[i], (enemy_x, enemy_y))


def display_player_bullet(player_x, bullet_y):
    global player_bullet_state
    screen.blit(player_bulletImg, (player_x + 16, bullet_y + 10))


# def display_enemy_bullet(ebullet_x, ebullet_y):
#     global enemy_bullet_state
#     screen.blit(enemy_bulletImg, (ebullet_x + 16, ebullet_y + 16))
def display_enemy_bullet(x, y, i):
    global enemy_bullet_state
    screen.blit(enemy_bulletImg[i], (x + 16, y + 16))


def bullet_and_enemy_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:
        return True


def show_score():
    score_text = score_font.render(f'Score : {str(score_value)}', True, WHITE)
    screen.blit(score_text, dest=(10, 10))


def game_over_text():
    game_over_texts = game_over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(game_over_texts, (200, 250))


def collision_sound():
    coll_sound = mixer.Sound('misc/shoot.wav')
    coll_sound.play()


# Creating pygame custom USER event for enemy shooting
enemyShoot = pygame.USEREVENT + 1

# Calls the enemyShoot event for a specified amount of time
pygame.time.set_timer(enemyShoot, 500)

while True:
    screen.fill((0, 0, 0))

    # background image
    screen.blit(backgroundImg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # Check if any key is been pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_change = -5
            if event.key == pygame.K_RIGHT:
                player_change = 5
            if event.key == pygame.K_SPACE:
                # laser Sound
                bullet_sound = mixer.Sound('misc/laser.wav')
                bullet_sound.play()
                if player_bullet_state == 'ready':
                    player_bullet_state = 'fire'
                    player_bulletX = playerX
                    display_player_bullet(player_bulletX, player_bulletY)

        # Check if the pressed key has been released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_change = 0
        # Checks if the enemyShoot event has been called
        if event.type == enemyShoot:

            if enemy_bullet_state == 'ready':
                for i in range(int(num_of_enemies)):
                    enemy_bullet_state = 'fire'
                    enemy_bulletY[i] = enemyY[i]
                    enemy_bulletX[i] = enemyX[i]
                    display_enemy_bullet(enemy_bulletX[i], enemy_bulletY[i], i)


    # check if player has more lives left
    if num_of_heartImg == 0:
        for i in range(num_of_enemies):
            enemyY[i] = 2000
    #   explosion sound
        explosion_sound = mixer.Sound('misc/explosion.wav')
        explosion_sound.play()

        game_over_text()
        # break
    else:
        # Show the heartImg on screen
        for i in range(num_of_heartImg):
            life_bar(heartX[i], heartY, i)

    # Change the player's direction in the X-axis
    playerX += player_change

    # Check and prevent the player from going out of bounds
    if playerX >= 740:
        playerX = 740
    if playerX <= 0:
        playerX = 0

    #  If the state is fire, move the bullet up
    if player_bullet_state == 'fire':
        player_bulletY -= 6
        display_player_bullet(player_bulletX, player_bulletY)
    # If the bullet leaves the screen change the state and reset it's position
    if player_bulletY <= 0:
        player_bullet_state = 'ready'
        player_bulletY = 480

    display_player(playerX, playerY)

    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 480:
            for j in range(num_of_enemies):
                enemyY[j] = 2000

            game_over_text()
            break
        # Move the enemy spaceship in the X/horizontal direction
        enemyX[i] += enemyX_change[i]

        # If the enemy ship gets to the left boundary change it's X and Y direction
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 748:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        display_enemy(enemyX[i], enemyY[i],i)

        # If the the bullet from the player hits the enemy reset the bullet and respawn the enemy
        collision = bullet_and_enemy_collision(enemyX[i], enemyY[i], player_bulletX, player_bulletY)
        if collision:
            player_bullet_state = 'ready'
            player_bulletY = 480
            enemyX[i] = random.randint(0, 750)
            enemyY[i] = random.randint(70, 100)
            score_value += 1
            # Collision Sound
            collision_sound()

        #  If the state is fire, move the bullet up
        if enemy_bullet_state == 'fire':
            enemy_bulletY[i] += 6
            display_enemy_bullet(enemy_bulletX[i], enemy_bulletY[i],i)

        # If the bullet leaves the screen change the state and reset it's position
        if enemy_bulletY[i] >= 600:
            enemy_bullet_state = 'ready'

        # If the the bullet from the player hits the enemy reset the bullet and respawn the enemy
        collision = bullet_and_enemy_collision(playerX, playerY, enemy_bulletX[i], enemy_bulletY[i])
        if collision:
            enemy_bullet_state = 'ready'
            enemy_bulletY[i] = enemyY[i]
            playerX = 370
            playerY = 480
            num_of_heartImg -= 1
            # Collision Sound
            collision_sound()

    show_score()
    pygame.display.update()
