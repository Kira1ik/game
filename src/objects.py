import math
import random
import pygame
from .settings import *


class AuroraParticle:
    def __init__(self, speed_mult=1.0):
        self.radius = 10
        self.x = random.randint(self.radius + 20, WIDTH - self.radius - 20)
        self.y = -self.radius
        self.vy = random.uniform(1.8, 3.0) * speed_mult
        self.vx = random.uniform(-0.4, 0.4)
        self.color = random.choice(
            [AURORA_GREEN, AURORA_PURPLE, AURORA_BLUE,
             AURORA_TEAL, AURORA_PINK])
        self.phase = random.uniform(0, math.tau)
        self.rotation = 0
        self.rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        self.rect.center = (int(self.x), int(self.y))

    def update(self):
        self.phase += 0.14
        self.rotation += 4
        self.x += self.vx + math.sin(self.phase) * 0.8
        self.y += self.vy
        self.rect.center = (int(self.x), int(self.y))

    def off_screen(self):
        return self.y > HEIGHT + self.radius

    def draw(self, screen):
        r = int(self.radius + math.sin(self.phase) * 1.5)
        x, y = int(self.x), int(self.y)
        pygame.draw.circle(screen, self.color, (x, y), r)
        pygame.draw.circle(screen, WHITE, (x, y), max(2, r // 2))



class IceShard:
    def __init__(self, speed_mult=1.0):
        self.size = random.randint(11, 17)
        self.x = random.randint(self.size + 20, WIDTH - self.size - 20)
        self.y = -self.size
        self.vy = random.uniform(2.8, 4.5) * speed_mult
        self.vx = random.uniform(-0.6, 0.6)
        self.rotation = random.uniform(0, 360)
        self.rot_speed = random.uniform(-5, 5)
        self.phase = random.uniform(0, math.tau)
        self.rect = pygame.Rect(0, 0, self.size * 2, self.size * 2)
        self.rect.center = (int(self.x), int(self.y))

    def update(self):
        self.phase += 0.15
        self.x += self.vx + math.sin(self.phase) * 0.3
        self.y += self.vy
        self.rotation += self.rot_speed
        self.rect.center = (int(self.x), int(self.y))

    def off_screen(self):
        return self.y > HEIGHT + self.size

    def draw(self, screen):
        # Iskrystallen er en roterende sekskant med spisse hjørner.
        points = []
        for i in range(6):
            angle = math.radians(self.rotation + i * 60)
            radius = self.size if i % 2 == 0 else self.size * 0.6
            px = int(self.x + math.cos(angle) * radius)
            py = int(self.y + math.sin(angle) * radius)
            points.append((px, py))

        pygame.draw.polygon(screen, ICE_BLUE, points)
        pygame.draw.polygon(screen, ICE_WHITE, points, 2)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)),
                           max(2, self.size // 5))
