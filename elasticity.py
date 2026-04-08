import pygame
import math
import sys
import random

pygame.init()

screen = pygame.display.set_mode((900, 900))
clock = pygame.time.Clock()
spring = 250
k = 5000
damping = 1
max_connections = 50
ygravity = 0
xgravity = 0
bounce = 0.6

class Bullet(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, mass):
        super().__init__()
        self.image = pygame.image.load("bullet.png")
        self.mass = mass/2
        self.image = pygame.transform.scale(self.image, (self.mass, self.mass))
        self.rect = self.image.get_rect()
        self.rect.center = (xpos, ypos)
        self.tick = 0
    def update(self, x, y):
        self.rect.x = x - (self.mass/2)
        self.rect.y = y - (self.mass/2)
        if self.rect.y >= 900 - self.mass:
            self.rect.y -= 10

row = 5
col = 5
solid = []

# solid[i][0] m
# solid[i][1] ax
# solid[i][2] ay
# solid[i][3] vx
# solid[i][4] vy
# solid[i][5] sx
# solid[i][6] sy

bullet_sprites = pygame.sprite.Group()

cdr = 0
delete_list = []
close_objects = []



while True:
    bullet_list = []
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if keys[pygame.K_f] and cdr == 0:
        body = [50, 0, 0, 0, 0, mouse_pos[0], mouse_pos[1]]
        solid.append(body)
        bullet_sprites.add(Bullet(body[5], body[6], body[0]))
        cdr = 10

    cdr -= 1
    if cdr <= 0:
        cdr = 0


    screen.fill((23, 33, 51))
    for i in range(len(solid)):
        # close_objects = []
        for j in range(len(solid)):
            if not i == j and i + max_connections > j and i - max_connections < j:
                # close_objects.append([math.sqrt(((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2)), j])
                # close_objects.sort(key=lambda x: x[0])
                # if len(close_objects) >= max_connections:
                #     close_count = max_connections
                # else:
                #     close_count = len(close_objects)
                if solid[i][5] == solid[j][5]:
                    if solid[i][6] >= solid[j][6]:
                        solid[i][2] += (math.sin(-math.pi / 2) * k * (math.sqrt(((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2))-spring) / solid[i][0])
                        solid[i][1] += (math.cos(-math.pi / 2) * k * (math.sqrt(((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2))-spring) / solid[i][0])
                    else:
                        solid[i][2] += (math.sin(math.pi / 2) * k * (math.sqrt(
                            ((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2)) - spring) /
                                        solid[i][0])
                        solid[i][1] += (math.cos(math.pi / 2) * k * (math.sqrt(
                            ((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2)) - spring) /
                                        solid[i][0])

                elif solid[i][5] <= solid[j][5]:
                    solid[i][2] += (math.sin(math.atan((solid[i][6] - solid[j][6]) / (solid[i][5] - solid[j][5]))) * k * (math.sqrt(
                        ((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2)) - spring) / solid[i][
                                        0])
                    solid[i][1] += (math.cos(math.atan((solid[i][6] - solid[j][6]) / (solid[i][5] - solid[j][5]))) * k * (math.sqrt(
                        ((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2)) - spring) / solid[i][
                                        0])
                else:
                    solid[i][2] += (math.sin(math.atan((solid[i][6] - solid[j][6]) / (solid[i][5] - solid[j][5])) + math.pi) * k * (math.sqrt(
                        ((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2)) - spring) / solid[i][
                                        0])
                    solid[i][1] += (math.cos(math.atan((solid[i][6] - solid[j][6]) / (solid[i][5] - solid[j][5])) + math.pi) * k * (math.sqrt(
                        ((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2)) - spring) / solid[i][
                                        0])

                pygame.draw.line(screen, (255, 255, 255), [solid[i][5], solid[i][6]], [solid[j][5], solid[j][6]])
            solid[i][2] -= (damping * solid[i][4])
            solid[i][1] -= (damping * solid[i][3])
        push = 20000
        if keys[pygame.K_RIGHT]:
            solid[i][1] += push
        if keys[pygame.K_LEFT]:
            solid[i][1] -= push
        if keys[pygame.K_UP]:
            solid[i][2] -= push
        if keys[pygame.K_DOWN]:
            solid[i][2] += push
        if keys[pygame.K_a]:
            spring += 0.2
        if keys[pygame.K_s]:
            spring -= 0.2
        solid[i][2] += ygravity
        solid[i][1] -= xgravity



    for i in range(len(solid)):
        solid[i][3] += solid[i][1]/60
        solid[i][4] += solid[i][2]/60

        solid[i][5] += solid[i][3]/60
        solid[i][6] += solid[i][4]/60

    for i in range(len(solid)):
        solid[i][1] = 0
        solid[i][2] = 0

    for i in range(len(solid) - 1, -1, -1):
        if solid[i][5] >= 900 + solid[i][0] or solid[i][5] <= -solid[i][0] or solid[i][6] <= -solid[i][0]:
            # remove physics object
            solid.pop(i)

            # remove corresponding sprite
            sprite = bullet_sprites.sprites()[i]
            sprite.kill()
        if solid[i][6] >= 900 - solid[i][0]:
            solid[i][6] = 900 - solid[i][0]
            solid[i][4] *= -bounce
        elif solid[i][6] <= solid[i][0]:
            solid[i][6] = solid[i][0]
            solid[i][4] *= -bounce
        if solid[i][5] >= 900 - solid[i][0]:
            solid[i][5] = 900 - solid[i][0]
            solid[i][3] *= -bounce
        elif solid[i][5] <= solid[i][0]:
            solid[i][5] = solid[i][0]
            solid[i][3] *= -bounce

    for i, sprite in enumerate(bullet_sprites.sprites()):
        sprite.update(solid[i][5], solid[i][6])
    bullet_sprites.draw(screen)
    grey = (92, 106, 120)
    pygame.draw.rect(screen, grey, [0, 0, 38, 900])
    pygame.draw.rect(screen, grey, [0, 0, 900, 38])
    pygame.draw.rect(screen, grey, [900-38, 0, 38, 900])
    pygame.draw.rect(screen, grey, [0, 900-38, 900, 38])
    pygame.display.update()
    clock.tick(60)
