import pygame
import math
import sys
import random

pygame.init()

screen = pygame.display.set_mode((900, 900))
clock = pygame.time.Clock()
G = 5
tweak = 20
class Bullet(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, mass):
        super().__init__()
        self.image = pygame.image.load("bullet.png")
        self.mass = mass
        self.image = pygame.transform.scale(self.image, (self.mass/5, self.mass/5))
        self.rect = self.image.get_rect()
        self.rect.center = (xpos, ypos)
    def update(self, x, y):
        self.rect.x = x - self.mass/10
        self.rect.y = y - self.mass/10
        # if self.rect.x >= WIDTH + self.mass or self.rect.x <= -self.mass:
        #     self.kill()
        # if self.rect.y >= HEIGHT + self.mass or self.rect.y <= -self.mass:
        #     self.kill()

row = 5
col = 5
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
collision = 1



while True:
    bullet_list = []
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if keys[pygame.K_f] and cdr == 0:
        body = [100, 0, 0, 0, 0, mouse_pos[0], mouse_pos[1]]
        solid.append(body)
        bullet_sprites.add(Bullet(body[5], body[6], body[0]))
        cdr = 10
    if keys[pygame.K_r] and cdr == 0:
        body = [1000, 0, 0, 0, 0, mouse_pos[0], mouse_pos[1]]
        solid.append(body)
        bullet_sprites.add(Bullet(body[5], body[6], body[0]))
        cdr = 10

    cdr -= 1
    if cdr <= 0:
        cdr = 0


    for i in range(len(solid)):
        for j in range(len(solid)):
            if not i == j:
                if solid[i][5] == solid[j][5]:
                    if solid[i][6] >= solid[j][6]:
                        solid[i][2] += collision * (math.sin(-math.pi / 2) * (G * solid[j][0]) / ((math.sqrt(((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2))) ** 2))
                        solid[i][1] += collision * (math.cos(-math.pi / 2) * (G * solid[j][0]) / ((math.sqrt(((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2))) ** 2))
                    else:
                        solid[i][2] += collision * (math.sin(math.pi / 2) * (G * solid[j][0]) / ((math.sqrt(((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2)) + tweak) ** 2))
                        solid[i][1] += collision * (math.cos(math.pi / 2) * (G * solid[j][0]) / ((math.sqrt(((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2)) + tweak) ** 2))

                elif solid[i][5] <= solid[j][5]:
                    solid[i][2] += collision * (math.sin(math.atan((solid[i][6] - solid[j][6]) / (solid[i][5] - solid[j][5]))) * (G * solid[j][0]) / ((math.sqrt(
                        ((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2)) + tweak) ** 2))
                    solid[i][1] += collision * (math.cos(math.atan((solid[i][6] - solid[j][6]) / (solid[i][5] - solid[j][5]))) * (G * solid[j][0]) / ((math.sqrt(
                        ((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2)) + tweak) ** 2))
                else:
                    solid[i][2] += collision * (math.sin(math.atan((solid[i][6] - solid[j][6]) / (solid[i][5] - solid[j][5])) + math.pi) * (G * solid[j][0]) / ((math.sqrt(
                        ((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2)) + tweak) ** 2))
                    solid[i][1] += collision * (math.cos(math.atan((solid[i][6] - solid[j][6]) / (solid[i][5] - solid[j][5])) + math.pi) * (G * solid[j][0]) / ((math.sqrt(
                        ((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2)) + tweak) ** 2))

                #my attempt at collision
                #solid[i][0]/10 is the diameter of the planet
                # if math.sqrt(abs(((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5])))) < solid[i][0]/10:
                #     collision = -1
                # else:
                #     collision = 1

    for i in range(len(solid)):
        solid[i][3] += solid[i][1]
        solid[i][4] += solid[i][2]

        solid[i][5] += solid[i][3]
        solid[i][6] += solid[i][4]

    for i in range(len(solid)):
        solid[i][1] = 0
        solid[i][2] = 0

    for i in range(len(solid) - 1, -1, -1):
        if solid[i][5] >= 900 + solid[i][0]/5 or solid[i][5] <= -solid[i][0]/5 or solid[i][6] >= 900 + solid[i][0]/5 or solid[i][6] <= -solid[i][0]/5:
            # remove physics object
            solid.pop(i)

            # remove corresponding sprite
            sprite = bullet_sprites.sprites()[i]
            sprite.kill()

    screen.fill((23, 33, 51))
    for i in range(len(bullet_sprites.sprites())):
        bullet_sprites.sprites()[i].update(solid[i][5], solid[i][6])
    bullet_sprites.draw(screen)
    pygame.display.update()
    clock.tick(60)