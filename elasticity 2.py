import pygame
import math
import sys
pygame.init()

screen = pygame.display.set_mode((900, 900))
clock = pygame.time.Clock()
spring = 50
k = 50000
damping = 0.2
max_connections = 50
ygravity = 5000
xgravity = 0
bounce = 1

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

# row = 5
# col = 7
# solid = []
#
# for c in range(col):
#     for r in range(row):
#         solid.append([50, 0, 0, 0, 0, c*spring+200, r*spring+200])
# bullet_sprites = pygame.sprite.Group()
# for i in range(len(solid)):
#     bullet_sprites.add(Bullet(solid[i][5], solid[i][6], solid[i][0]))

# solid[i][0] m
# solid[i][1] ax
# solid[i][2] ay
# solid[i][3] vx
# solid[i][4] vy
# solid[i][5] sx
# solid[i][6] sy
solid = []
bullet_sprites = pygame.sprite.Group()
col = 6
row = 4

cdr = 0
delete_list = []
close_objects = []
font = pygame.font.SysFont("calibri", 40, 0)



while True:
    bullet_list = []
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if keys[pygame.K_r]:
        spring += 1
    if keys[pygame.K_e]:
        spring -= 1
    if keys[pygame.K_w] and cdr == 0:
        row += 1
        solid = []
        for c in range(col):
            for r in range(row):
                solid.append([50, 0, 0, 0, 0, c * spring + 200, r * spring + 200])
        bullet_sprites = pygame.sprite.Group()
        for i in range(len(solid)):
            bullet_sprites.add(Bullet(solid[i][5], solid[i][6], solid[i][0]))
        cdr = 10
    if keys[pygame.K_s] and cdr == 0:
        row -= 1
        solid = []
        for c in range(col):
            for r in range(row):
                solid.append([50, 0, 0, 0, 0, c * spring + 200, r * spring + 200])
        bullet_sprites = pygame.sprite.Group()
        for i in range(len(solid)):
            bullet_sprites.add(Bullet(solid[i][5], solid[i][6], solid[i][0]))
        cdr = 10
    if keys[pygame.K_a] and cdr == 0:
        col -= 1
        solid = []
        for c in range(col):
            for r in range(row):
                solid.append([50, 0, 0, 0, 0, c * spring + 200, r * spring + 200])
        bullet_sprites = pygame.sprite.Group()
        for i in range(len(solid)):
            bullet_sprites.add(Bullet(solid[i][5], solid[i][6], solid[i][0]))
        cdr = 10
    if keys[pygame.K_d] and cdr == 0:
        col += 1
        solid = []
        for c in range(col):
            for r in range(row):
                solid.append([50, 0, 0, 0, 0, c * spring + 200, r * spring + 200])
        bullet_sprites = pygame.sprite.Group()
        for i in range(len(solid)):
            bullet_sprites.add(Bullet(solid[i][5], solid[i][6], solid[i][0]))
        cdr = 10


    cdr -= 1
    if cdr <= 0:
        cdr = 0


    screen.fill((23, 33, 51))
    for i in range(len(solid)):
        # close_objects = []
        for j in range(len(solid)):
            if not i == j:
                if (i - row == j and i - row >= 0) or (i + row == j and i + row <= len(solid)) or (i - 1 == j and j >= 0 and not i%row == 0) or (i + 1 == j and j <= len(solid) and not (i+1)%row == 0):
            # if not i == j and i + max_connections > j and i - max_connections < j:
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

            if (i + row + 1 == j and i + row + 1 <= len(solid) and not (i+1)%row == 0) or (i + row - 1 == j and i + row - 1 <= len(solid) and not i%row == 0) or (i - row + 1 == j and i - row + 1 >= 0 and not (i+1)%row == 0) or (i - row - 1 == j and i - row - 1 >= 0 and not i%row == 0):
                # if not i == j and i + max_connections > j and i - max_connections < j:
                # close_objects.append([math.sqrt(((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2)), j])
                # close_objects.sort(key=lambda x: x[0])
                # if len(close_objects) >= max_connections:
                #     close_count = max_connections
                # else:
                #     close_count = len(close_objects)
                if solid[i][5] == solid[j][5]:
                    if solid[i][6] >= solid[j][6]:
                        solid[i][2] += (math.sin(-math.pi / 2) * k * (math.sqrt(
                            ((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2)) - (
                                                                                  spring * math.sqrt(2))) /
                                        solid[i][0])
                        solid[i][1] += (math.cos(-math.pi / 2) * k * (math.sqrt(
                            ((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2)) - (
                                                                                  spring * math.sqrt(2))) /
                                        solid[i][0])
                    else:
                        solid[i][2] += (math.sin(math.pi / 2) * k * (math.sqrt(
                            ((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2)) - (
                                                                                 spring * math.sqrt(2))) /
                                        solid[i][0])
                        solid[i][1] += (math.cos(math.pi / 2) * k * (math.sqrt(
                            ((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2)) - (
                                                                                 spring * math.sqrt(2))) /
                                        solid[i][0])

                elif solid[i][5] <= solid[j][5]:
                    solid[i][2] += (math.sin(
                        math.atan((solid[i][6] - solid[j][6]) / (solid[i][5] - solid[j][5]))) * k * (math.sqrt(
                        ((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2)) - (spring * math.sqrt(
                        2))) /
                                    solid[i][
                                        0])
                    solid[i][1] += (math.cos(
                        math.atan((solid[i][6] - solid[j][6]) / (solid[i][5] - solid[j][5]))) * k * (math.sqrt(
                        ((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2)) - (spring * math.sqrt(
                        2))) /
                                    solid[i][
                                        0])
                else:
                    solid[i][2] += (math.sin(
                        math.atan((solid[i][6] - solid[j][6]) / (solid[i][5] - solid[j][5])) + math.pi) * k * (
                                            math.sqrt(
                                                ((solid[i][6] - solid[j][6]) ** 2) + (
                                                        (solid[i][5] - solid[j][5]) ** 2)) - (spring * math.sqrt(2))) /
                                    solid[i][
                                        0])
                    solid[i][1] += (math.cos(
                        math.atan((solid[i][6] - solid[j][6]) / (solid[i][5] - solid[j][5])) + math.pi) * k * (
                                            math.sqrt(
                                                ((solid[i][6] - solid[j][6]) ** 2) + (
                                                        (solid[i][5] - solid[j][5]) ** 2)) - (spring * math.sqrt(2))) /
                                    solid[i][
                                        0])

                pygame.draw.line(screen, (255, 255, 255), [solid[i][5], solid[i][6]], [solid[j][5], solid[j][6]])
            solid[i][2] -= (damping * solid[i][4])
            solid[i][1] -= (damping * solid[i][3])
        push = 3
        if keys[pygame.K_RIGHT]:
            solid[i][5] += push
        if keys[pygame.K_LEFT]:
            solid[i][5] -= push
        if keys[pygame.K_UP]:
            solid[i][6] -= push*3
        if keys[pygame.K_DOWN]:
            solid[i][6] += push
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
            solid.pop(i)
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
    pygame.draw.rect(screen, grey, [900 - 38, 0, 38, 900])
    pygame.draw.rect(screen, grey, [0, 900 - 38, 900, 38])
    row_text = font.render('Rows: ' + str(row), True, (255, 255, 255))
    col_text = font.render('Columns: ' + str(col), True, (255, 255, 255))
    size_text = font.render('Length: ' + str(spring), True, (255, 255, 255))
    screen.blit(row_text, (40, 40))
    screen.blit(col_text, (40, 80))
    screen.blit(size_text, (40, 120))
    pygame.display.update()
    clock.tick(60)