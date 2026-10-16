import math
import random
import sys
import pygame

from .settings import *
from .player import Player
from .objects import AuroraParticle, IceShard
from .powerups import PowerUp
from .particles import Burst, FloatingText
from .audio import Audio


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Nordlysjeger")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.font_big = pygame.font.SysFont("arial", 68, bold=True)
        self.font_mid = pygame.font.SysFont("arial", 30, bold=True)
        self.font_small = pygame.font.SysFont("arial", 20)
        self.font_huge = pygame.font.SysFont("arial", 88, bold=True)

        self.audio = Audio()
        self.state = "menu"
        self.high_score = self.load_high_score()

        self.shake = 0.0
        self.flash = None
        self.flash_timer = 0
        self.menu_time = 0.0
        self.aurora_phase = 0.0

        self._build_starfield()
        self._build_background()
        self._init_game_objects()

    # ---------- Setup ----------
    def _build_starfield(self):
        self.star_layers = []
        for n, spd, rad in ((80, 0.2, 1), (60, 0.5, 2), (40, 0.9, 2)):
            self.star_layers.append([
                [random.randint(0, WIDTH), random.randint(0, HEIGHT),
                 spd, rad, random.randint(80, 220)]
                for _ in range(n)
            ])

    def _build_background(self):
        self.bg = pygame.Surface((WIDTH, HEIGHT))
        for y in range(HEIGHT):
            t = y / HEIGHT
            r = int(NIGHT_TOP[0] * (1 - t) + NIGHT_BOTTOM[0] * t)
            g = int(NIGHT_TOP[1] * (1 - t) + NIGHT_BOTTOM[1] * t)
            b = int(NIGHT_TOP[2] * (1 - t) + NIGHT_BOTTOM[2] * t)
            pygame.draw.line(self.bg, (r, g, b), (0, y), (WIDTH, y))

        self.mountain = pygame.Surface((WIDTH, 180), pygame.SRCALPHA)
        pts = [(0, 180)]
        for x in range(0, WIDTH + 40, 40):
            h = 100 + math.sin(x * 0.01) * 40 + math.sin(x * 0.03 + 1) * 20
            pts.append((x, 180 - h))
        pts.append((WIDTH, 180))
        pygame.draw.polygon(self.mountain, (5, 5, 20, 255), pts)

    def _init_game_objects(self):
        self.player = Player(WIDTH // 2, HEIGHT - 120)
        self.particles = []
        self.shards = []
        self.powerups = []
        self.bursts = []
        self.texts = []
        self.score = 0
        self.display_score = 0
        self.lives = START_LIVES
        self.level = 1
        self.level_timer = 0
        self.level_banner_timer = 0
        self.spawn_timer = 0
        self.shard_spawn_timer = 0
        self.powerup_spawn_timer = 0
        self.combo = 0
        self.combo_timer = 0
        self.slow_timer = 0

    # ---------- Persistence ----------
    def load_high_score(self):
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read().strip())
        except Exception:
            return 0

    def save_high_score(self):
        try:
            with open("highscore.txt", "w") as f:
                f.write(str(self.high_score))
        except Exception:
            pass

    # ---------- Effects ----------
    def trigger_shake(self, amount):
        self.shake = max(self.shake, amount)

    def trigger_flash(self, color, duration=12, alpha=100):
        self.flash = (color, alpha)
        self.flash_timer = duration

    # ---------- State transitions ----------
    def start_new_game(self):
        self._init_game_objects()
        self.state = "playing"
        self.audio.play("start")

    def game_over(self):
        self.state = "gameover"
        self.audio.play("gameover")
        self.trigger_shake(25)
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

    # ---------- Events ----------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type != pygame.KEYDOWN:
                continue

            if self.state == "menu":
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.start_new_game()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif self.state == "playing":
                if event.key in (pygame.K_ESCAPE, pygame.K_p):
                    self.state = "paused"
            elif self.state == "paused":
                if event.key in (pygame.K_ESCAPE, pygame.K_p):
                    self.state = "playing"
                elif event.key == pygame.K_q:
                    self.state = "menu"
            elif self.state == "gameover":
                if event.key == pygame.K_RETURN:
                    self.start_new_game()
                elif event.key == pygame.K_ESCAPE:
                    self.state = "menu"

    # ---------- Update ----------
    def _update_background(self):
        for layer in self.star_layers:
            for s in layer:
                s[1] += s[2]
                if s[1] > HEIGHT:
                    s[1] = 0
                    s[0] = random.randint(0, WIDTH)
        self.aurora_phase += 0.01

    def update(self):
        self.menu_time += 0.03
        self._update_background()

        if self.shake > 0:
            self.shake *= 0.85
            if self.shake < 0.3:
                self.shake = 0
        if self.flash_timer > 0:
            self.flash_timer -= 1
        else:
            self.flash = None

        if self.state != "playing":
            for b in self.bursts:
                b.update()
            self.bursts = [b for b in self.bursts if not b.dead()]
            for t in self.texts:
                t.update()
            self.texts = [t for t in self.texts if not t.dead()]
            return

        keys = pygame.key.get_pressed()
        self.player.update(keys)

        # Combo decay
        if self.combo_timer > 0:
            self.combo_timer -= 1
            if self.combo_timer <= 0:
                self.combo = 0

        # Level-up
        self.level_timer += 1
        if self.level_timer >= FPS * 20:
            self.level += 1
            self.level_timer = 0
            self.level_banner_timer = 120
            self.audio.play("levelup")
            self.trigger_flash(AURORA_PURPLE, 20, 80)

        if self.level_banner_timer > 0:
            self.level_banner_timer -= 1

        if self.slow_timer > 0:
            self.slow_timer -= 1
            time_scale = 0.45
        else:
            time_scale = 1.0

        speed_mult = (1 + (self.level - 1) * 0.1) * time_scale

        # Spawning
        self.spawn_timer += 1
        if self.spawn_timer >= max(18, 48 - self.level * 3):
            self.spawn_timer = 0
            self.particles.append(AuroraParticle(speed_mult))

        self.shard_spawn_timer += 1
        if self.shard_spawn_timer >= max(30, 75 - self.level * 4):
            self.shard_spawn_timer = 0
            self.shards.append(IceShard(speed_mult))

        self.powerup_spawn_timer += 1
        if self.powerup_spawn_timer >= FPS * 15 and random.random() < 0.35:
            self.powerup_spawn_timer = 0
            self.powerups.append(PowerUp(speed_mult))

        # Magnet effect
        if self.player.has_magnet():
            for p in self.particles:
                dx = self.player.x - p.x
                dy = self.player.y - p.y
                d = math.hypot(dx, dy)
                if 0 < d < 200:
                    p.x += (dx / d) * 3
                    p.y += (dy / d) * 3

        # Particles pickups
        for p in self.particles[:]:
            p.update()
            if p.off_screen():
                self.particles.remove(p)
            elif p.rect.colliderect(self.player.rect):
                self.particles.remove(p)
                self.combo += 1
                self.combo_timer = int(COMBO_TIMEOUT)
                mult = 1 + (self.combo // COMBO_STEP) * 0.5
                gain = int(10 * mult)
                self.score += gain
                self.bursts.append(Burst(p.x, p.y, p.color, 14, 4, 28, 3))
                self.texts.append(
                    FloatingText(p.x, p.y - 10, f"+{gain}", p.color))
                self.audio.play("pickup")
                self.trigger_flash(p.color, 6, 30)

        # Shards collisions
        for s in self.shards[:]:
            s.update()
            if s.off_screen():
                self.shards.remove(s)
            elif s.rect.colliderect(self.player.rect):
                if self.player.has_shield():
                    self.shards.remove(s)
                    self.bursts.append(
                        Burst(s.x, s.y, AURORA_BLUE, 16, 5, 30, 3))
                    self.audio.play("shield")
                else:
                    self.shards.remove(s)
                    self.lives -= 1
                    self.combo = 0
                    self.bursts.append(Burst(s.x, s.y, RED, 24, 6, 40, 4))
                    self.texts.append(
                        FloatingText(self.player.x, self.player.y - 30,
                                     "-1", RED, 60))
                    self.trigger_shake(18)
                    self.trigger_flash(RED, 15, 120)
                    self.audio.play("hit")
                    if self.lives <= 0:
                        self.game_over()
                        return

        # Powerups
        for pu in self.powerups[:]:
            pu.update()
            if pu.off_screen():
                self.powerups.remove(pu)
            elif pu.rect.colliderect(self.player.rect):
                self.powerups.remove(pu)
                self._apply_powerup(pu)
                self.bursts.append(Burst(pu.x, pu.y, pu.color, 18, 5, 32, 3))
                self.audio.play("powerup")

        # Update effects
        for b in self.bursts:
            b.update()
        self.bursts = [b for b in self.bursts if not b.dead()]
        for t in self.texts:
            t.update()
        self.texts = [t for t in self.texts if not t.dead()]

        # Smooth score
        if self.display_score < self.score:
            self.display_score = min(
                self.score,
                self.display_score + max(1, (self.score - self.display_score) // 5 + 1))

    def _apply_powerup(self, pu):
        if pu.kind == "shield":
            self.player.shield_timer = SHIELD_DURATION
            label, col = "SKJOLD!", AURORA_BLUE
        elif pu.kind == "magnet":
            self.player.magnet_timer = MAGNET_DURATION
            label, col = "MAGNET!", GOLD
        else:
            self.slow_timer = SLOWMO_DURATION
            label, col = "SAKTE!", AURORA_PURPLE
        self.texts.append(FloatingText(self.player.x, self.player.y - 40,
                                       label, col, 60))

    # ---------- Drawing ----------
    def _draw_background(self, surf):
        surf.blit(self.bg, (0, 0))

        aurora = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for i, color in enumerate((AURORA_GREEN, AURORA_PURPLE, AURORA_TEAL)):
            y_base = 120 + i * 80
            amp = 40 + i * 15
            phase = self.aurora_phase * (1.0 + i * 0.3) + i * 2
            pts = [(0, y_base)]
            for x in range(0, WIDTH + 20, 20):
                y = y_base + math.sin(x * 0.008 + phase) * amp \
                    + math.sin(x * 0.003 + phase * 1.7) * 20
                pts.append((x, y))
            pts += [(WIDTH, HEIGHT), (0, HEIGHT)]
            pygame.draw.polygon(aurora, (*color, 24), pts)
        surf.blit(aurora, (0, 0))

        for layer in self.star_layers:
            for s in layer:
                col = (s[4], s[4], min(255, s[4] + 30))
                pygame.draw.circle(surf, col, (int(s[0]), int(s[1])), s[3])

        surf.blit(self.mountain, (0, HEIGHT - 180))

    def _draw_heart(self, surf, x, y, size, color):
        pts = []
        for i in range(24):
            t = i / 24 * math.tau
            hx = 16 * math.sin(t) ** 3
            hy = -(13 * math.cos(t) - 5 * math.cos(2 * t)
                   - 2 * math.cos(3 * t) - math.cos(4 * t))
            pts.append((x + hx * size / 16, y + hy * size / 16))
        pygame.draw.polygon(surf, color, pts)

    def _draw_timer_icon(self, surf, x, y, color, letter, timer, max_timer):
        pygame.draw.circle(surf, (0, 0, 0, 120), (x, y), 20)
        ratio = max(0.001, min(0.999, timer / max_timer))
        pygame.draw.arc(surf, color,
                        pygame.Rect(x - 20, y - 20, 40, 40),
                        -math.pi / 2,
                        -math.pi / 2 + math.tau * ratio, 3)
        s = self.font_small.render(letter, True, color)
        surf.blit(s, (x - s.get_width() // 2, y - s.get_height() // 2))

    def _draw_hud(self, surf):
        panel = pygame.Surface((WIDTH, 60), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 90))
        surf.blit(panel, (0, 0))

        # Score
        score_surf = self.font_mid.render(str(self.display_score), True, WHITE)
        surf.blit(score_surf, (24, 14))
        surf.blit(self.font_small.render("POENG", True, DIM), (24, 44))

        # Level
        lvl = self.font_mid.render(f"NIVÅ {self.level}", True, AURORA_PURPLE)
        surf.blit(lvl, (WIDTH // 2 - lvl.get_width() // 2, 14))

        # Combo
        if self.combo >= COMBO_STEP:
            mult = 1 + (self.combo // COMBO_STEP) * 0.5
            cs = self.font_small.render(
                f"COMBO x{mult:.1f}  ({self.combo})", True, GOLD)
            surf.blit(cs, (WIDTH // 2 - cs.get_width() // 2, 44))

        # Lives
        for i in range(self.lives):
            self._draw_heart(surf, WIDTH - 40 - i * 34, 30, 12, RED)

        # High score
        hs = self.font_small.render(f"REKORD {self.high_score}", True, GOLD)
        surf.blit(hs, (WIDTH - hs.get_width() - 20, 46))

        # Power-up timers
        px, py = 20, HEIGHT - 40
        if self.player.has_shield():
            self._draw_timer_icon(surf, px, py, AURORA_BLUE, "S",
                                  self.player.shield_timer, SHIELD_DURATION)
            px += 70
        if self.player.has_magnet():
            self._draw_timer_icon(surf, px, py, GOLD, "M",
                                  self.player.magnet_timer, MAGNET_DURATION)
            px += 70
        if self.slow_timer > 0:
            self._draw_timer_icon(surf, px, py, AURORA_PURPLE, "T",
                                  self.slow_timer, SLOWMO_DURATION)

        # Level banner
        if self.level_banner_timer > 0:
            t = self.level_banner_timer / 120
            alpha = int(255 * min(1, t * 2) * min(1, (1 - t) * 4))
            b = self.font_big.render(f"NIVÅ {self.level}", True, AURORA_PURPLE)
            b.set_alpha(alpha)
            surf.blit(b, b.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))

    def _draw_flash(self, surf):
        if self.flash:
            color, alpha = self.flash
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((*color, alpha))
            surf.blit(overlay, (0, 0))

    # ---------- Screens ----------
    def _draw_menu(self, surf):
        self._draw_background(surf)

        scale = 1 + math.sin(self.menu_time * 2) * 0.03
        title = self.font_huge.render("NORDLYSJEGER", True, AURORA_GREEN)
        glow = self.font_huge.render("NORDLYSJEGER", True, AURORA_PURPLE)
        rot = math.sin(self.menu_time) * 1.5
        title = pygame.transform.rotozoom(title, rot, scale)
        glow = pygame.transform.rotozoom(glow, rot, scale)
        rect = title.get_rect(center=(WIDTH // 2, 160))
        surf.blit(glow, (rect.x + 3, rect.y + 3))
        surf.blit(title, rect)

        sub = self.font_mid.render("Jakt på nordlyset", True, TEXT)
        surf.blit(sub, (WIDTH // 2 - sub.get_width() // 2, 230))

        # Floating demo-particles
        for i in range(3):
            x = WIDTH // 2 + math.sin(self.menu_time + i * 2) * 200
            y = 320 + math.sin(self.menu_time * 1.5 + i) * 30 + i * 20
            col = (AURORA_GREEN, AURORA_PURPLE, AURORA_BLUE)[i]
            pygame.draw.circle(surf, col, (int(x), int(y)), 10)
            pygame.draw.circle(surf, WHITE, (int(x), int(y)), 5)

        info = [
            ("BEVEGELSE", "Piltaster eller WASD"),
            ("MÅL",       "Samle nordlys  •  Unngå is"),
            ("POWER-UPS", "Skjold  •  Magnet  •  Slow-motion"),
            ("START",     "Trykk ENTER eller SPACE"),
        ]
        y = 420
        for label, text in info:
            surf.blit(self.font_small.render(label, True, AURORA_TEAL),
                      (WIDTH // 2 - 220, y))
            surf.blit(self.font_small.render(text, True, TEXT),
                      (WIDTH // 2 - 80, y))
            y += 34

        hs = self.font_mid.render(f"REKORD: {self.high_score}", True, GOLD)
        surf.blit(hs, (WIDTH // 2 - hs.get_width() // 2, y + 20))

    def _draw_paused(self, surf):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        surf.blit(overlay, (0, 0))
        t = self.font_huge.render("PAUSE", True, WHITE)
        surf.blit(t, (WIDTH // 2 - t.get_width() // 2, HEIGHT // 2 - 120))
        for i, line in enumerate(("P / ESC  =  fortsett",
                                  "Q  =  tilbake til meny")):
            s = self.font_mid.render(line, True, TEXT)
            surf.blit(s, (WIDTH // 2 - s.get_width() // 2,
                          HEIGHT // 2 + 10 + i * 50))

    def _draw_gameover(self, surf):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 0, 20, 200))
        surf.blit(overlay, (0, 0))

        t = self.font_big.render("SPILLET ER SLUTT", True, RED)
        surf.blit(t, (WIDTH // 2 - t.get_width() // 2, 160))

        s1 = self.font_mid.render(f"Poeng: {self.score}", True, WHITE)
        surf.blit(s1, (WIDTH // 2 - s1.get_width() // 2, 270))

        s2 = self.font_mid.render(f"Rekord: {self.high_score}", True, GOLD)
        surf.blit(s2, (WIDTH // 2 - s2.get_width() // 2, 320))

        if self.score >= self.high_score and self.score > 0:
            nb = self.font_small.render("★ NY REKORD! ★", True, GOLD)
            surf.blit(nb, (WIDTH // 2 - nb.get_width() // 2, 370))

        info = self.font_small.render(
            "ENTER = spill igjen     ESC = meny", True, TEXT)
        surf.blit(info, (WIDTH // 2 - info.get_width() // 2, 470))

    # ---------- Main draw ----------
    def draw(self):
        if self.state == "menu":
            self._draw_menu(self.screen)
            self._draw_flash(self.screen)
            pygame.display.flip()
            return

        scene = pygame.Surface((WIDTH, HEIGHT))
        self._draw_background(scene)

        for pu in self.powerups:
            pu.draw(scene)
        for p in self.particles:
            p.draw(scene)
        for s in self.shards:
            s.draw(scene)
        self.player.draw(scene)
        for b in self.bursts:
            b.draw(scene)
        for t in self.texts:
            t.draw(scene)

        self._draw_hud(scene)

        sx = sy = 0
        if self.shake > 0:
            sx = random.uniform(-self.shake, self.shake)
            sy = random.uniform(-self.shake, self.shake)
        self.screen.blit(scene, (sx, sy))

        if self.state == "paused":
            self._draw_paused(self.screen)
        elif self.state == "gameover":
            self._draw_gameover(self.screen)

        self._draw_flash(self.screen)
        pygame.display.flip()

    # ---------- Loop ----------
    def run(self):
        while True:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()