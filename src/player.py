import math
import pygame
from .settings import *
from .particles import Particle


class Player:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.radius = PLAYER_RADIUS
        self.speed = PLAYER_SPEED
        self.rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        self.rect.center = (int(self.x), int(self.y))
        self.rotation = 0.0
        self.pulse = 0.0
        self.trail_timer = 0
        self.trail = []
        self.magnet_timer = 0
        self.shield_timer = 0

    def update(self, keys):
        dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - \
             (keys[pygame.K_LEFT] or keys[pygame.K_a])
        dy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - \
             (keys[pygame.K_UP] or keys[pygame.K_w])
        if dx and dy:
            dx *= 0.7071
            dy *= 0.7071

        self.x += dx * self.speed
        self.y += dy * self.speed
        self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        self.y = max(self.radius + 60, min(HEIGHT - self.radius, self.y))
        self.rect.center = (int(self.x), int(self.y))

        self.rotation += 2.5
        self.pulse += 0.1

        if self.shield_timer > 0:
            self.shield_timer -= 1
        if self.magnet_timer > 0:
            self.magnet_timer -= 1

        self.trail_timer += 1
        if self.trail_timer >= 2:
            self.trail_timer = 0
            col = AURORA_GREEN if self.shield_timer == 0 else AURORA_BLUE
            self.trail.append(Particle(self.x, self.y, 0, 0.5, col, 18, 5))
        for p in self.trail:
            p.update()
        self.trail = [p for p in self.trail if not p.dead()]

    def has_shield(self):
        return self.shield_timer > 0

    def has_magnet(self):
        return self.magnet_timer > 0

    def draw(self, screen):
        # Tegn halen først, slik at den ligger bak spilleren.
        for particle in self.trail:
            particle.draw(screen)

        x, y = int(self.x), int(self.y)
        radius = int(self.radius + math.sin(self.pulse) * 2)

        # Enkle ringer gjør spilleren synlig mot den mørke bakgrunnen.
        pygame.draw.circle(screen, AURORA_PURPLE, (x, y), radius + 5, 2)
        pygame.draw.circle(screen, AURORA_GREEN, (x, y), radius)
        pygame.draw.circle(screen, WHITE, (x, y), max(2, radius - 6))

        if self.has_shield():
            pygame.draw.circle(screen, AURORA_BLUE, (x, y), radius + 12, 2)

        if self.has_magnet():
            pygame.draw.circle(screen, GOLD, (x, y), 90, 1)
