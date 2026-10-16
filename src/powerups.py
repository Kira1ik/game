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
        cx = cy = self.size * 3
        glow = pygame.Surface((self.size * 6, self.size * 6), pygame.SRCALPHA)
        for i in range(4, 0, -1):
            pygame.draw.circle(glow, (*self.color, 22), (cx, cy),
                               self.size + i * 3)
        screen.blit(glow, (self.x - cx, self.y - cy))

        pts = []
        for i in range(4):
            ang = math.radians(self.rotation + i * 90)
            pts.append((int(self.x + math.cos(ang) * self.size),
                        int(self.y + math.sin(ang) * self.size)))
        pygame.draw.polygon(screen, self.color, pts)
        pygame.draw.polygon(screen, WHITE, pts, 2)

        if self.kind == "shield":
            pygame.draw.circle(screen, WHITE,
                               (int(self.x), int(self.y)), self.size // 2, 2)
        elif self.kind == "magnet":
            pygame.draw.line(screen, WHITE, (self.x - 4, self.y),
                             (self.x + 4, self.y), 2)
            pygame.draw.line(screen, WHITE, (self.x, self.y - 4),
                             (self.x, self.y + 4), 2)
        else:  # slow
            pygame.draw.polygon(screen, WHITE, [
                (int(self.x), int(self.y) - 5),
                (int(self.x + 4), int(self.y + 3)),
                (int(self.x - 4), int(self.y + 3)),
            ])