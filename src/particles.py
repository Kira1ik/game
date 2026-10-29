"""Partikler, burst-effekter og flytende poeng-tekst."""
import math
import random
import pygame


class Particle:
    def __init__(self, x, y, vx, vy, color, life, size,
                 gravity=0.0, fade=True):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.color = color
        self.life = life
        self.max_life = life
        self.size = size
        self.gravity = gravity
        self.fade = fade

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.vx *= 0.98
        self.vy *= 0.98
        self.life -= 1

    def dead(self):
        return self.life <= 0

    def draw(self, surf):
        ratio = self.life / self.max_life
        radius = max(1, int(self.size * ratio))
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), radius)



class Burst:
    def __init__(self, x, y, color, count=12, speed=4, life=30, size=3):
        self.particles = []
        for _ in range(count):
            ang = random.uniform(0, math.tau)
            spd = random.uniform(speed * 0.4, speed)
            self.particles.append(Particle(
                x, y,
                math.cos(ang) * spd, math.sin(ang) * spd,
                color, life, size,
            ))

    def update(self):
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if not p.dead()]

    def dead(self):
        return not self.particles

    def draw(self, surf):
        for p in self.particles:
            p.draw(surf)


class FloatingText:
    def __init__(self, x, y, text, color, life=45):
        self.x, self.y = x, y
        self.text = text
        self.color = color
        self.life = life
        self.max_life = life
        self.font = pygame.font.SysFont("arial", 20, bold=True)

    def update(self):
        self.y -= 1.2
        self.life -= 1

    def dead(self):
        return self.life <= 0

    def draw(self, surf):
        t = self.life / self.max_life
        s = self.font.render(self.text, True, self.color)
        s.set_alpha(int(255 * t))
        surf.blit(s, s.get_rect(center=(self.x, self.y)))