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
        for p in self.trail:
            p.draw(screen)

        base_r = self.radius + math.sin(self.pulse) * 2
        cx = cy = int(base_r * 4)
        size = int(base_r * 8)
        glow = pygame.Surface((size, size), pygame.SRCALPHA)
        for i in range(8, 0, -1):
            pygame.draw.circle(glow, (*AURORA_GREEN, 10), (cx, cy),
                               int(base_r + i * 4))
        screen.blit(glow, (self.x - cx, self.y - cy))

        # Roterende partikler rundt spilleren
        for i in range(6):
            ang = math.radians(self.rotation + i * 60)
            px = self.x + math.cos(ang) * (base_r + 10)
            py = self.y + math.sin(ang) * (base_r + 10)
            pygame.draw.circle(screen, AURORA_PURPLE, (int(px), int(py)), 2)

        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), int(base_r))
        pygame.draw.circle(screen, AURORA_GREEN, (int(self.x), int(self.y)),
                           int(base_r - 3))
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)),
                           int(base_r - 7))

        if self.shield_timer > 0:
            alpha = 100 + int(80 * math.sin(self.pulse * 2))
            s = pygame.Surface((self.radius * 6, self.radius * 6), pygame.SRCALPHA)
            pygame.draw.circle(s, (*AURORA_BLUE, alpha),
                               (self.radius * 3, self.radius * 3),
                               int(self.radius + 14), 3)
            screen.blit(s, (self.x - self.radius * 3, self.y - self.radius * 3))

        if self.magnet_timer > 0:
            alpha = 60 + int(40 * math.sin(self.pulse * 3))
            s = pygame.Surface((200, 200), pygame.SRCALPHA)
            pygame.draw.circle(s, (*GOLD, alpha), (100, 100), 90, 2)
            pygame.draw.circle(s, (*GOLD, alpha // 2), (100, 100), 70, 1)
            screen.blit(s, (self.x - 100, self.y - 100))