import pygame
import sys

# Initializing Pygame
pygame.init()

# Size of the screen
HEIGHT = 600
WIDTH = 800

# Set the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set icon
iconImg = pygame.image.load('images/ufo.png')
pygame.display.set_icon(iconImg)

# Set Caption
pygame.display.set_caption('Space Invaders')

# def default_template(defaultimg, img):
#     defaultImg = pygame.image.load(img)

# The player image, position and rate of change
playerImg = pygame.image.load('images/player.png')
playerX = 370
playerY = 480
player_change = 0



# Bullet image and position
bulletImg = pygame.image.load('images/bullet.png')
bulletY = 480
bullet_state = 'ready'


def display_player(player_x, player_y):
    screen.blit(playerImg, (player_x, player_y))


def display_bullet(player_x, bullet_y):
    global bullet_state
    screen.blit(bulletImg, (player_x + 16, bullet_y + 10))


while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # Check if any key is been pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_change = -3
            if event.key == pygame.K_RIGHT:
                player_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_state = 'fire'
                    bulletX = playerX
                    display_bullet(bulletX, bulletY)

        # Check if the pressed key has been released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_change = 0

    # Change the player's direction in the X-axis
    playerX += player_change

    # Check and prevent the player from going out of bounds
    if playerX >= 740:
        playerX = 740
    if playerX <= 0:
        playerX = 0

    #  If the state is fire, move the bullet up
    if bullet_state == 'fire':
        bulletY -= 1
        display_bullet(bulletX, bulletY)
    # If the bullet leaves the screen change the state and reset it's position
    if bulletY <= 0:
        bullet_state = 'ready'
        bulletY = 480

    display_player(playerX, playerY)

    pygame.display.update()
