import pygame
import math
import sys
import random

pygame.init()
G = 5
tweak = 20
screen = pygame.display.set_mode((1300, 600))
clock = pygame.time.Clock()
size = 10
class Bullet(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, mass):
        super().__init__()
        self.image = pygame.image.load("box.png")
        self.mass = mass/size
        self.image = pygame.transform.scale(self.image, (self.mass, self.mass))
        self.rect = self.image.get_rect()
        self.rect.center = (xpos, ypos)
    def update(self, x, y):
        self.rect.x = x - self.mass/2
        self.rect.y = y - self.mass/2
        # if self.rect.x >= WIDTH + self.mass or self.rect.x <= -self.mass:
        #     self.kill()
        # if self.rect.y >= HEIGHT + self.mass or self.rect.y <= -self.mass:
        #     self.kill()

solid = []

# solid[i][0] m
# solid[i][1] ax
# solid[i][2] ay
# solid[i][3] vx
# solid[i][4] vyf
# solid[i][5] sx
# solid[i][6] sy

bullet_sprites = pygame.sprite.Group()

cdr = 0
delete_list = []

m1 = 1300
body = [m1, 0, 0, -5, 0, 500, 600-(m1/(size*2))-38]
solid.append(body)
bullet_sprites.add(Bullet(body[5], body[6], body[0]))

m2 = 500
body = [m2, 0, 0, 0, 0, 200, 600-(m2/(size*2))-38]
solid.append(body)
bullet_sprites.add(Bullet(body[5], body[6], body[0]))

collision = False
wall_collision = False
hit = 0


while True:
    bullet_list = []
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    mass = solid[0][0]
    ax = solid[0][1]
    ay = solid[0][2]
    vx = solid[0][3]
    vy = solid[0][4]
    sx = solid[0][5]
    sy = solid[0][6]
    jmass = solid[1][0]
    jax = solid[1][1]
    jay = solid[1][2]
    jvx = solid[1][3]
    jvy = solid[1][4]
    jsx = solid[1][5]
    jsy = solid[1][6]
    pi = mass * vx
    pj = jmass * jvx

    if sx-mass/(size*2) < 38:
        wall_collision = True

    if wall_collision == True:
        solid[0][3] = -vx
        print("hit")
        wall_collision = False

    if jsx-jmass/(size*2) < 38:
        wall_collision = True

    if wall_collision == True:
        solid[1][3] = -jvx
        print("hit")
        wall_collision = False



    if sx-mass/(size*2) <= jsx+jmass/(size*2) and sx+mass/(size*2) >= jsx+jmass/(size*2):
        solid[0][3] = ((solid[0][0] - solid[1][0]) / (solid[0][0] + solid[1][0])) * vx
        solid[1][3] = ((2 * solid[0][0]) / (solid[0][0] + solid[1][0])) *  vx

            # solid[i][3] = ((solid[i][0] - solid[j][0])/(solid[i][0] + solid[j][0])) * jvx
            # solid[j][3] = ((2*solid[i][0])/(solid[i][0] + solid[j][0])) * jvx

    for i in range(len(solid)):
        solid[i][3] += solid[i][1]
        solid[i][4] += solid[i][2]

        solid[i][5] += solid[i][3]
        solid[i][6] += solid[i][4]

    for i in range(len(solid)):
        solid[i][1] = 0
        solid[i][2] = 0

    for i in range(len(solid) - 1, -1, -1):
        if solid[i][5] >= 900 + solid[i][0]/2 or solid[i][5] <= -solid[i][0]/2 or solid[i][6] >= 900 + solid[i][0]/2 or solid[i][6] <= -solid[i][0]/2:
            # remove physics object
            solid.pop(i)

            # remove corresponding sprite
            sprite = bullet_sprites.sprites()[i]
            sprite.kill()

    screen.fill((23, 33, 51))
    grey = (92, 106, 120)
    pygame.draw.rect(screen, grey, [0, 300, 38, 300])
    pygame.draw.rect(screen, grey, [0, 600 - 38, 1300, 38])
    for i in range(len(bullet_sprites.sprites())):
        bullet_sprites.sprites()[i].update(solid[i][5], solid[i][6])
    bullet_sprites.draw(screen)
    pygame.display.update()
    clock.tick(60)