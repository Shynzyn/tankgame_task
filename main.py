import pygame
import random

# initialize
pygame.init()
clock = pygame.time.Clock()
# create screen
screen = pygame.display.set_mode((800, 600))

# title and icon
pygame.display.set_caption("T A N K E R Z", "tank.ico")
icon = pygame.image.load('tank.ico')
enemy_tank = pygame.image.load('enemy_tank2.png')
pygame.display.set_icon(icon)

# player
player_img = pygame.image.load('tank_player.png')
x = 368
y = 380
move_speed = 2.5
angle = 0
movement_direction = None
fuel = 1000

# enemy
enemyX = 200
enemyY = 200
enemy_ms = 2
enemy_direction = random.choice(["w", "s", "d", "a"])
enemy_angle = 0
enemy_delay = 2000

# other stuff
counter = 0
random_distance = random.randint(200, 500)

# bullet
bulletImg = pygame.image.load('bullet.png')
bullet_ms = 5
bullet_shooting = False
offsetX = 0
offsetY = 0
bulletX = x + offsetX
bulletY = y + offsetY
bullet_angle = angle
bullet_direction = "w"
reloaded = True

# drawing player at coordinates
def player(x, y, angle):
    rotated = pygame.transform.rotate(player_img, angle)
    screen.blit(rotated, (x, y))


def enemy(x, y, angle):
    rotated = pygame.transform.rotate(enemy_tank, angle)
    screen.blit(rotated, (x, y))


def fire_bullet(x, y, angle):
    global bullet_shooting
    global reloaded
    bullet_shooting = True
    reloaded = False
    # determine the direction the tank is facing
    if bullet_direction == "w":  # facing north
        offsetX = 16
        offsetY = 0
    elif bullet_direction == "a":  # facing west
        offsetX = -22
        offsetY = 16
    elif bullet_direction == "s":  # facing south
        offsetX = 16
        offsetY = 20
    elif bullet_direction == "d":  # facing east
        offsetX = 60
        offsetY = 16
    # shoot the bullet from the center of the tank
    bulletX = x + offsetX
    bulletY = y + offsetY
    # rotate the bullet image
    rotated = pygame.transform.rotate(bulletImg, angle)
    # draw the bullet on the screen
    screen.blit(rotated, (bulletX, bulletY))



running = True
while running:
    clock.tick(60)  # limiting fps
    screen.fill((0, 160, 160))
    keys = pygame.key.get_pressed()
    # BULLET MOVEMENT
    if bullet_shooting is True:
        fire_bullet(bulletX, bulletY, bullet_angle)
        # move the bullet in the direction it is facing
        if bullet_direction == "w":
            bullet_angle = 0
            bulletY -= bullet_ms
        elif bullet_direction == "s":
            bullet_angle = 180
            bulletY += bullet_ms
        elif bullet_direction == "a":
            bullet_angle = 90
            bulletX -= bullet_ms
        elif bullet_direction == "d":
            bullet_angle = 270
            bulletX += bullet_ms
        reloaded = False
        # if the bullet goes off screen, stop shooting
        if bulletX < 0 or bulletX > 800 or bulletY < 0 or bulletY > 600:
            bulletX = x
            bulletY = y
            bullet_shooting = False
            reloaded = True

    # ENEMY MOVEMENT
    if enemy_direction == "w":
        enemy_angle = 0
        enemyY -= enemy_ms
        counter += 1
        if enemyY <= 0:
            enemy_direction = random.choice(["s", "d", "a"])
        if counter > random_distance:
            enemy_direction = random.choice(["s", "d", "a"])
            counter = 0

    if enemy_direction == "s":
        enemy_angle = 180
        enemyY += enemy_ms
        counter += 1
        if enemyY >= 600 - 64:  # 64 is the height of the object
            enemy_direction = random.choice(["w", "d", "a"])
        if counter > random_distance:
            enemy_direction = random.choice(["w", "d", "a"])
            counter = 0

    if enemy_direction == "a":
        enemy_angle = 90
        enemyX -= enemy_ms
        counter += 1
        if enemyX <= 0:
            enemy_direction = random.choice(["w", "s", "d"])
        if counter > random_distance:
            enemy_direction = random.choice(["w", "s", "d"])
            counter = 0

    if enemy_direction == "d":
        enemy_angle = 270
        enemyX += enemy_ms
        counter += 1
        if enemyX >= 800 - 64:  # 64 is the width of the object
            enemy_direction = random.choice(["w", "s", "a"])
        if counter > random_distance:
            enemy_direction = random.choice(["s", "w", "a"])
            counter = 0

    # PLAYER MOVEMENT

    if movement_direction == "w":
        bullet_direction = "w"
        angle = 0
        y -= move_speed
        fuel -= 1
        print(fuel)
    if movement_direction == "s":
        bullet_direction = "s"
        angle = 180
        y += move_speed
        fuel -= 1
        print(fuel)
    if movement_direction == "a":
        bullet_direction = "a"
        angle = 90
        x -= move_speed
        fuel -= 1
        print(fuel)
    if movement_direction == "d":
        bullet_direction = "d"
        angle = 270
        x += move_speed
        fuel -= 1
        print(fuel)

    if keys[pygame.K_a] and fuel > 0 and x > 0:
        movement_direction = "a"
    elif keys[pygame.K_d] and fuel > 0 and x < 740:
        movement_direction = "d"
    elif keys[pygame.K_w] and fuel > 0 and y > 0:
        movement_direction = "w"
    elif keys[pygame.K_s] and fuel > 0 and y < 540:
        movement_direction = "s"
    else:
        # Clear the movement direction if no keys are being pressed
        movement_direction = None
    if keys[pygame.K_SPACE] and reloaded:
        bullet_shooting = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player(x, y, angle)
    enemy(enemyX, enemyY, enemy_angle)
    pygame.display.update()