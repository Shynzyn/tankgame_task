import pygame
import random
from pygame import mixer

# initialize
pygame.init()
clock = pygame.time.Clock()
# create screenw
screen = pygame.display.set_mode((800, 600))

# title and icon
pygame.display.set_caption("T A N K E R Z", "tank.ico")
icon = pygame.image.load('sprites/tank.ico')
pygame.display.set_icon(icon)
bg = pygame.image.load('sprites/bgfortank.jpg')

# background sound
bg_music = mixer.Sound('sounds/background.wav')
bg_music.set_volume(0.4)
bg_music.play(-1)

# player
player_img = pygame.image.load('sprites/tank_player.png')
x = 368
y = 380
move_speed = 2.5
angle = 0
movement_direction = None


# SCORE AND FUEL
fuel = 1000
score = 0
font_path = 'fonts/ARCADECLASSIC.TTF'
font = pygame.font.Font(font_path, 24)
font_game_over = pygame.font.Font(font_path, 80)
fuel_X = 10
fuel_Y = 10
score_X = 660
score_Y = 10

# enemy
enemy_tank = pygame.image.load('sprites/enemy_tank2.png')
enemyX = 200
enemyY = 200
enemy_ms = 2
enemy_direction = random.choice(["w", "s", "d", "a"])
enemy_angle = 0
enemy_delay = 2000
enemy_surface = pygame.Surface((64, 64))
enemy_rect = enemy_surface.get_rect()
enemy_health = 3
enemy_dead = False

# other stuff
counter = 0
random_distance = random.randint(200, 500)

# bullet
bulletImg = pygame.image.load('sprites/bullet.png')
bullet_surface = pygame.Surface((20, 20))
bullet_rect = bullet_surface.get_rect()
bullet_ms = 5
bullet_shooting = False
offsetX = 0
offsetY = 0
bullet_angle = angle
bullet_direction = "w"
saved_player_direction = "w"
reloaded = True
saved_x = 0
saved_y = 0
bulletX = saved_x + offsetX
bulletY = saved_y + offsetY
bullet_reload_frames = 120


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"explosion_sprites/exp{num}.png")
            img = pygame.transform.scale(img, (100, 100))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 4
        self.counter += 1
        if self.counter >= explosion_speed and self.index < len(self.images) -1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) -1 and self.counter >= explosion_speed:
            self.kill()

explosion_group = pygame.sprite.Group()


def game_over():
    global gameover
    global reloaded
    display_game_over = font_game_over.render('game    over', True, 'white')
    screen.blit(display_game_over, (205, 170))
    display_restart = font.render('press    r   to   restart', True, 'black')
    screen.blit(display_restart, (295, 240))
    reloaded = False
    gameover = True

def show_score_fuel(fx, fy, sx, sy):
    fuel_W = font.render("Fuel " + str(fuel), True, (255, 255, 255))
    score_W = font.render("Score " + str(score), True, (255, 255, 255))
    screen.blit(fuel_W, (fx, fy))
    screen.blit(score_W, (sx, sy))


# drawing player at coordinates
def player(x, y, angle):
    rotated = pygame.transform.rotate(player_img, angle)
    screen.blit(rotated, (x, y))


def enemy(x, y, angle):
    rotated = pygame.transform.rotate(enemy_tank, angle)
    screen.blit(rotated, (x, y))


def fire_bullet(x, y, angle):
    global bulletX, bulletY, offsetX, offsetY
    global bullet_shooting
    global reloaded
    bullet_shooting = True
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
    # shoot the bullet from the center of the tank\
    if reloaded:
        bulletX = saved_x + offsetX
        bulletY = saved_y + offsetY
    reloaded = False
    # rotate the bullet image
    rotated = pygame.transform.rotate(bulletImg, angle)
    # draw the bullet on the screen
    screen.blit(rotated, (bulletX, bulletY))


def check_collision(bullet_rect, enemy_rect):
    # Use the colliderect() function to check if the bullet_rect and enemy_rect are colliding
    if bullet_rect.colliderect(enemy_rect):
        # If the rectangles are colliding, return True
        return True
    else:
        # If the rectangles are not colliding, return False
        return False


running = True
while running:
    # print(movement_direction)
    clock.tick(60)  # limiting fps
    screen.blit(bg, (0,0))
    explosion_group.draw(screen)
    explosion_group.update()
    keys = pygame.key.get_pressed()
    bullet_reload_frames += 1
    if fuel <= 0:
        game_over()
    # BULLET MOVEMENT
    if bullet_shooting is True:
        fire_bullet(bulletX, bulletY, bullet_angle)
        # move the bullet in the direction it is facing
        if bullet_direction == "w":
            bullet_angle = 0
            bulletY -= bullet_ms
            bullet_rect.x = bulletX
            bullet_rect.y = bulletY
        elif bullet_direction == "s":
            bullet_angle = 180
            bulletY += bullet_ms
            bullet_rect.x = bulletX
            bullet_rect.y = bulletY
        elif bullet_direction == "a":
            bullet_angle = 90
            bulletX -= bullet_ms
            bullet_rect.x = bulletX
            bullet_rect.y = bulletY
        elif bullet_direction == "d":
            bullet_angle = 270
            bulletX += bullet_ms
            bullet_rect.x = bulletX
            bullet_rect.y = bulletY
        reloaded = False

        # if the bullet goes off-screen, stop shooting
        if bulletX < 0 or bulletX > 800 or bulletY < 0 or bulletY > 600:
            bullet_shooting = False
            reloaded = True

        if check_collision(bullet_rect, enemy_rect):
            saved_enemyX = enemyX
            saved_enemyY = enemyY
            hit_sound = mixer.Sound('sounds/explosion.wav')
            hit_sound.play()
            enemy_health -= 1
            bulletX = -100
            bulletY = -100
            # Update the bullet rect to match the new position
            bullet_rect.x = bulletX
            bullet_rect.y = bulletY
            print(enemy_health)
            print("HIT!")
            bullet_shooting = False
            reloaded = True

    # ENEMY MOVEMENT
    if enemy_direction == "w":
        enemy_angle = 0
        enemyY -= enemy_ms
        enemy_rect.y = enemyY
        enemy_rect.x = enemyX
        counter += 1
        if enemyY <= 0:
            enemy_direction = random.choice(["s", "d", "a"])
        if counter > random_distance:
            enemy_direction = random.choice(["s", "d", "a"])
            counter = 0

    if enemy_direction == "s":
        enemy_angle = 180
        enemyY += enemy_ms
        enemy_rect.y = enemyY
        enemy_rect.x = enemyX
        counter += 1
        if enemyY >= 600 - 64:  # 64 is the height of the object
            enemy_direction = random.choice(["w", "d", "a"])
        if counter > random_distance:
            enemy_direction = random.choice(["w", "d", "a"])
            counter = 0

    if enemy_direction == "a":
        enemy_angle = 90
        enemyX -= enemy_ms
        enemy_rect.y = enemyY
        enemy_rect.x = enemyX
        counter += 1
        if enemyX <= 0:
            enemy_direction = random.choice(["w", "s", "d"])
        if counter > random_distance:
            enemy_direction = random.choice(["w", "s", "d"])
            counter = 0

    if enemy_direction == "d":
        enemy_angle = 270
        enemyX += enemy_ms
        enemy_rect.y = enemyY
        enemy_rect.x = enemyX
        counter += 1
        if enemyX >= 800 - 64:  # 64 is the width of the object
            enemy_direction = random.choice(["w", "s", "a"])
        if counter > random_distance:
            enemy_direction = random.choice(["s", "w", "a"])
            counter = 0

    # COLLISION DETECTION

    # PLAYER MOVEMENT

    if movement_direction == "w":
        saved_player_direction = "w"
        angle = 0
        y -= move_speed
        fuel -= 1
    if movement_direction == "s":
        saved_player_direction = "s"
        angle = 180
        y += move_speed
        fuel -= 1
    if movement_direction == "a":
        saved_player_direction = "a"
        angle = 90
        x -= move_speed
        fuel -= 1
    if movement_direction == "d":
        saved_player_direction = "d"
        angle = 270
        x += move_speed
        fuel -= 1

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
    if keys[pygame.K_SPACE] and reloaded and bullet_reload_frames >= 60:
        bullet_sound = mixer.Sound('sounds/laser.wav')
        bullet_sound.play()
        bullet_reload_frames = 0
        saved_x = x
        saved_y = y
        bullet_angle = angle
        bullet_shooting = True
        bullet_direction = saved_player_direction

    if keys[pygame.K_r]:
        fuel = 1000
        score = 0
        #reset enemy
        enemy_health = 3
        enemyX = 200
        enemyY = 200
        enemy_ms = 2
        enemy_direction = random.choice(["w", "s", "d", "a"])
        enemy_angle = 0
        enemy_delay = 2000
        #reset player
        x = 368
        y = 380
        move_speed = 2.5
        angle = 0
        movement_direction = None
        #reset bullet
        bullet_shooting = False
        offsetX = 0
        offsetY = 0
        bullet_angle = angle
        bullet_direction = "w"
        saved_player_direction = "w"
        reloaded = True
        saved_x = 0
        saved_y = 0
        bulletX = saved_x + offsetX
        bulletY = saved_y + offsetY
        gameover = False



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player(x, y, angle)
    enemy(enemyX, enemyY, enemy_angle)
    show_score_fuel(fuel_X, fuel_Y, score_X,score_Y)
    if enemy_health <= 0:
        enemy_dead = True
        if enemy_dead:
            explosion = Explosion(enemyX, enemyY)
            explosion_group.add(explosion)
            enemy_dead = False
        enemyX = random.randint(10, 740)
        enemyY = random.randint(10, 540)
        enemy_health = 3
        score += 100
        fuel += 150
    pygame.display.update()
