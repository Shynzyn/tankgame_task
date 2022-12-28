import pygame, random

pygame.init()

object = pygame.image.load('tank_player.png')
screen = pygame.display.set_mode((800, 600))

x = 200
y = 200
move_speed = 0.1
enemy_direction = random.choice(["w", "s", "d", "a"])
angle = 0


def player(x, y, angle):
    rotated = pygame.transform.rotate(object, angle)
    screen.blit(rotated, (x, y))


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(("white"))

    if enemy_direction == "w":
        angle = 0
        y -= move_speed
        if y < 0:
            enemy_direction = random.choice(["s", "d", "a"])
    if enemy_direction == "s":
        angle = 180
        y += move_speed
        if y < 600:
            enemy_direction = random.choice(["w", "d", "a"])
    if enemy_direction == "a":
        angle = 90
        x -= move_speed
        if x < 0:
            enemy_direction = random.choice(["w", "s", "d"])
    if enemy_direction == "d":
        angle = 270
        x += move_speed
        if x > 760:
            enemy_direction = random.choice(["w", "s", "a"])


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player(x, y, angle)

    pygame.display.update()

pygame.quit()
