import pygame
import random
import sys
import math

# Initializing Pygame
pygame.init()

# Size of the screen
HEIGHT = 600
WIDTH = 800

# Keeps tally of the score
score_value = 0

# COLORS
WHITE =(255,255,255)
BLACK =(0,0,0)

# Set the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set icon
iconImg = pygame.image.load('images/ufo.png')
pygame.display.set_icon(iconImg)

# Set Caption
pygame.display.set_caption('Space Invaders')

# Background Image
backgroundImg = pygame.image.load('images/background.png')

# The player image, position and rate of change
playerImg = pygame.image.load('images/player.png')
playerX = 370
playerY = 480
player_change = 0

# The enemy image, position and rate of change
enemyImg = pygame.image.load('images/enemy.png')
enemyX = random.randint(0, 750)
enemyY = random.randint(70, 100)
enemyX_change = 5
enemyY_change = 40

# Player Bullet image and position
player_bulletImg = pygame.image.load('images/bullet.png')
player_bulletY = 480
player_bulletX = 0
player_bullet_state = 'ready'

# Enemy Bullet image and position
enemy_bulletImg = pygame.image.load('images/minus.png')
enemy_bulletY = 0
enemy_bulletX = 0
enemy_bullet_state = 'ready'


score_font = pygame.font.Font('freesansbold.ttf', 32)


def display_player(player_x, player_y):
    screen.blit(playerImg, (player_x, player_y))


def display_enemy(enemy_x, enemy_y):
    screen.blit(enemyImg, (enemy_x, enemy_y))


def display_player_bullet(player_x, bullet_y):
    global player_bullet_state
    screen.blit(player_bulletImg, (player_x + 16, bullet_y + 10))


def display_enemy_bullet(ebullet_x, ebullet_y):
    global enemy_bullet_state
    screen.blit(enemy_bulletImg, (ebullet_x + 16, ebullet_y + 16))


def bullet_and_enemy_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:
        return True


def show_score():
    score_text = score_font.render(f'Score : {str(score_value)}', True, WHITE)
    screen.blit(score_text, dest=(10, 10))


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
                enemy_bullet_state = 'fire'
                enemy_bulletY = enemyY
                enemy_bulletX = enemyX
                display_enemy_bullet(enemy_bulletX, enemy_bulletY)

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

    # Move the enemy spaceship in the X/horizontal direction
    enemyX += enemyX_change

    # If the enemy ship gets to the left boundary change it's X and Y direction
    if enemyX <= 0:
        enemyX_change = 7
        enemyY += enemyY_change
    if enemyX >= 748:
        enemyX_change = -7
        enemyY += enemyY_change
    display_enemy(enemyX, enemyY)

    # If the the bullet from the player hits the enemy reset the bullet and respawn the enemy
    collision = bullet_and_enemy_collision(enemyX, enemyY, player_bulletX, player_bulletY)
    if collision:
        player_bullet_state = 'ready'
        player_bulletY = 480
        enemyX = random.randint(0, 750)
        enemyY = random.randint(70, 100)
        score_value += 1

    #  If the state is fire, move the bullet up
    if enemy_bullet_state == 'fire':
        enemy_bulletY += 6
        display_enemy_bullet(enemy_bulletX, enemy_bulletY)

    # If the bullet leaves the screen change the state and reset it's position
    if enemy_bulletY >= 600:
        enemy_bullet_state = 'ready'

    show_score()
    pygame.display.update()
