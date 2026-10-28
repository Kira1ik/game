import math
import random
import pygame
from .settings import *


class PowerUp:
    TYPES = ("shield", "magnet", "slow")
    COLORS = {"shield": AURORA_BLUE, "magnet": GOLD, "slow": AURORA_PURPLE}

    def __init__(self, speed_mult=1.0):
        self.kind = random.choice(self.TYPES)
        self.color = self.COLORS[self.kind]
        self.size = 14
        self.x = random.randint(40, WIDTH - 40)
        self.y = -self.size
        self.vy = random.uniform(1.6, 2.4) * speed_mult
        self.phase = random.uniform(0, math.tau)
        self.rotation = 0
        self.rect = pygame.Rect(0, 0, self.size * 2, self.size * 2)
        self.rect.center = (int(self.x), int(self.y))

    def update(self):
        self.phase += 0.15
        self.rotation += 3
        self.y += self.vy
        self.x += math.sin(self.phase) * 0.7
        self.rect.center = (int(self.x), int(self.y))

    def off_screen(self):
        return self.y > HEIGHT + self.size

    def draw(self, screen):
        # Power-ups vises som roterende firkanter med ulikt symbol.
        points = []
        for i in range(4):
            angle = math.radians(self.rotation + i * 90)
            px = int(self.x + math.cos(angle) * self.size)
            py = int(self.y + math.sin(angle) * self.size)
            points.append((px, py))

        pygame.draw.polygon(screen, self.color, points)
        pygame.draw.polygon(screen, WHITE, points, 2)

        x, y = int(self.x), int(self.y)
        if self.kind == "shield":
            pygame.draw.circle(screen, WHITE, (x, y), self.size // 2, 2)
        elif self.kind == "magnet":
            pygame.draw.line(screen, WHITE, (x - 4, y), (x + 4, y), 2)
            pygame.draw.line(screen, WHITE, (x, y - 4), (x, y + 4), 2)
        else:
            pygame.draw.polygon(screen, WHITE, [(x, y - 5), (x + 4, y + 3),
                                                (x - 4, y + 3)])
