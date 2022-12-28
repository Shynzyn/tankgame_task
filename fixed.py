import pygame, random

pygame.init()

enemy_tank = pygame.image.load('tank_player.png')
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

enemyX = 200
enemyY = 200
enemy_ms = 1.5
enemy_direction = random.choice(["w", "s", "d", "a"])
enemy_angle = 0
random_distance = random.randint(80, 160)
counter = 0


def enemy(x, y, angle):
    rotated = pygame.transform.rotate(enemy_tank, angle)
    screen.blit(rotated, (x, y))


running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(("white"))

    if enemy_direction == "w":
        enemy_angle = 0
        enemyY -= enemy_ms
        counter += 1
        if enemyY <= 0 or counter >= random_distance:
            enemy_direction = random.choice(["s", "d", "a"])
            counter = 0

    if enemy_direction == "s" or counter >= random_distance:
        enemy_angle = 180
        enemyY += enemy_ms
        counter += 1
        if enemyY >= 600 - 64:  # 64 is the height of the object
            enemyY = 600 - 64
            enemy_direction = random.choice(["w", "d", "a"])
            counter = 0

    if enemy_direction == "a" or counter >= random_distance:
        enemy_angle = 90
        enemyX -= enemy_ms
        counter += 1
        if enemyX <= 0:
            enemyX = 0
            enemy_direction = random.choice(["w", "s", "d"])
            counter = 0

    if enemy_direction == "d" or counter >= random_distance:
        enemy_angle = 270
        enemyX += enemy_ms
        counter += 1
        if enemyX >= 800 - 64:  # 64 is the width of the object
            enemyX = 800 - 64
            enemy_direction = random.choice(["w", "s", "a"])
            counter = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    enemy(enemyX, enemyY, enemy_angle)
    print(counter)

    pygame.display.update()

pygame.quit()
