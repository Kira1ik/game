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
        r = self.radius + math.sin(self.phase) * 1.5
        cx = cy = int(r * 4)
        size = int(r * 8)
        glow = pygame.Surface((size, size), pygame.SRCALPHA)
        for i in range(5, 0, -1):
            pygame.draw.circle(glow, (*self.color, 16), (cx, cy), int(r + i * 3))
        screen.blit(glow, (self.x - cx, self.y - cy))

        for i in range(4):
            ang = math.radians(self.rotation + i * 90)
            px = self.x + math.cos(ang) * (r + 6)
            py = self.y + math.sin(ang) * (r + 6)
            pygame.draw.circle(screen, WHITE, (int(px), int(py)), 1)

        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(r))
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), int(r * 0.5))


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
        cx = cy = self.size * 3
        glow = pygame.Surface((self.size * 6, self.size * 6), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*ICE_BLUE, 30), (cx, cy), self.size + 6)
        screen.blit(glow, (self.x - cx, self.y - cy))

        pts = []
        for i in range(6):
            ang = math.radians(self.rotation + i * 60)
            r = self.size if i % 2 == 0 else self.size * 0.6
            pts.append((int(self.x + math.cos(ang) * r),
                        int(self.y + math.sin(ang) * r)))
        pygame.draw.polygon(screen, ICE_BLUE, pts)
        pygame.draw.polygon(screen, ICE_WHITE, pts, 2)
        pygame.draw.circle(screen, WHITE,
                           (int(self.x), int(self.y)), max(2, self.size // 5))

        for i in range(3):
            ang = math.radians(self.rotation + i * 60)
            x1 = self.x + math.cos(ang) * self.size
            y1 = self.y + math.sin(ang) * self.size
            x2 = self.x - math.cos(ang) * self.size
            y2 = self.y - math.sin(ang) * self.size
            pygame.draw.line(screen, ICE_WHITE, (x1, y1), (x2, y2), 1)