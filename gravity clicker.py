import pygame
import math
import sys
import random

pygame.init()

screen = pygame.display.set_mode((900, 900))
clock = pygame.time.Clock()
G = 3
tweak = 10
def draw_arrow(
        surface: pygame.Surface,
        start: pygame.Vector2,
        end: pygame.Vector2,
        color: pygame.Color,
        body_width: int = 2,
        head_width: int = 4,
        head_height: int = 2,
    ):
    """Draw an arrow between start and end with the arrow head at the end.

    Args:
        surface (pygame.Surface): The surface to draw on
        start (pygame.Vector2): Start position
        end (pygame.Vector2): End position
        color (pygame.Color): Color of the arrow
        body_width (int, optional): Defaults to 2.
        head_width (int, optional): Defaults to 4.
        head_height (float, optional): Defaults to 2.
    """
    arrow = start - end
    angle = arrow.angle_to(pygame.Vector2(0, -1))
    body_length = arrow.length() - head_height

    # Create the triangle head around the origin
    head_verts = [
        pygame.Vector2(0, head_height / 2),  # Center
        pygame.Vector2(head_width / 2, -head_height / 2),  # Bottomright
        pygame.Vector2(-head_width / 2, -head_height / 2),  # Bottomleft
    ]
    # Rotate and translate the head into place
    translation = pygame.Vector2(0, arrow.length() - (head_height /
2)).rotate(-angle)
    for i in range(len(head_verts)):
        head_verts[i].rotate_ip(-angle)
        head_verts[i] += translation
        head_verts[i] += start

    pygame.draw.polygon(surface, color, head_verts)

    # Stop weird shapes when the arrow is shorter than arrow head
    if arrow.length() >= head_height:
        # Calculate the body rect, rotate and translate into place
        body_verts = [
            pygame.Vector2(-body_width / 2, body_length / 2),  # Topleft
            pygame.Vector2(body_width / 2, body_length / 2),  # Topright
            pygame.Vector2(body_width / 2, -body_length / 2),  # Bottomright
            pygame.Vector2(-body_width / 2, -body_length / 2),  # Bottomleft
        ]
        translation = pygame.Vector2(0, body_length / 2).rotate(-angle)
        for i in range(len(body_verts)):
            body_verts[i].rotate_ip(-angle)
            body_verts[i] += translation
            body_verts[i] += start

        pygame.draw.polygon(surface, color, body_verts)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, mass, stationary):
        super().__init__()
        self.image = pygame.image.load("bullet.png")
        self.mass = mass
        self.stationary = stationary
        self.image = pygame.transform.scale(self.image, (self.mass/5,
self.mass/5))
        self.rect = self.image.get_rect()
        self.rect.center = (xpos, ypos)
    def update(self, x, y):
        if self.stationary == False:
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
    #screen.fill((23, 33, 51))
    bullet_list = []
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if keys[pygame.K_f] and cdr == 0:
        body = [100, 0, 0, 2, 0, mouse_pos[0], mouse_pos[1]]
        solid.append(body)
        bullet_sprites.add(Bullet(body[5], body[6], body[0], False))
        cdr = 20
    if keys[pygame.K_r] and cdr == 0:
        body = [500, 0, 0, 0, 0, 450, 450]
        solid.append(body)
        bullet_sprites.add(Bullet(body[5], body[6], body[0], True))
        cdr = 20

    cdr -= 1
    if cdr <= 0:
        cdr = 0

    for i in range(len(solid)):
        for j in range(len(solid)):
            if not i == j and not i == 0:
                if solid[i][5] == solid[j][5]:
                    if solid[i][6] >= solid[j][6]:
                        solid[i][2] += collision * (math.sin(-math.pi / 2) * (G * solid[j][0]) / ((math.sqrt(
                            ((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2))) ** 2))
                        solid[i][1] += collision * (math.cos(-math.pi / 2) * (G * solid[j][0]) / ((math.sqrt(
                            ((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2))) ** 2))
                    else:
                        solid[i][2] += collision * (math.sin(math.pi / 2) * (G * solid[j][0]) / ((math.sqrt(
                            ((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2)) + tweak) ** 2))
                        solid[i][1] += collision * (math.cos(math.pi / 2) * (G * solid[j][0]) / ((math.sqrt(
                            ((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2)) + tweak) ** 2))

                elif solid[i][5] <= solid[j][5]:
                    solid[i][2] += collision * (
                                math.sin(math.atan((solid[i][6] - solid[j][6]) / (solid[i][5] - solid[j][5]))) * (
                                    G * solid[j][0]) / ((math.sqrt(
                            ((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2)) + tweak) ** 2))
                    solid[i][1] += collision * (
                                math.cos(math.atan((solid[i][6] - solid[j][6]) / (solid[i][5] - solid[j][5]))) * (
                                    G * solid[j][0]) / ((math.sqrt(
                            ((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2)) + tweak) ** 2))
                else:
                    solid[i][2] += collision * (math.sin(
                        math.atan((solid[i][6] - solid[j][6]) / (solid[i][5] - solid[j][5])) + math.pi) * (
                                                            G * solid[j][0]) / ((math.sqrt(
                        ((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2)) + tweak) ** 2))
                    solid[i][1] += collision * (math.cos(
                        math.atan((solid[i][6] - solid[j][6]) / (solid[i][5] - solid[j][5])) + math.pi) * (
                                                            G * solid[j][0]) / ((math.sqrt(
                        ((solid[i][6] - solid[j][6]) ** 2) + ((solid[i][5] - solid[j][5]) ** 2)) + tweak) ** 2))

    for i in range(len(solid)):
        solid[i][3] += solid[i][1]
        solid[i][4] += solid[i][2]

        solid[i][5] += solid[i][3]
        solid[i][6] += solid[i][4]
        acc_length = 200
        vel_length = 20
        #draw_arrow(screen, pygame.Vector2(solid[i][5], solid[i][6]),
                   #pygame.Vector2(solid[i][5] + (solid[i][3] *
#el_length), solid[i][6] + (solid[i][4] * vel_length)),
                   #(255, 255, 255), 3, 10, 10)
        #draw_arrow(screen, pygame.Vector2(solid[i][5], solid[i][6]),
                   #pygame.Vector2(solid[i][5] + (solid[i][1] *
#acc_length), solid[i][6] + (solid[i][2] * acc_length)),
                   #(248, 142, 30), 3, 10, 10)

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


    for i in range(len(bullet_sprites.sprites())):
        bullet_sprites.sprites()[i].update(solid[i][5], solid[i][6])
    bullet_sprites.draw(screen)
    pygame.display.update()
    clock.tick(120)