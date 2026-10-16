"""Prosedyrisk lydgenerering — ingen .wav-filer nødvendig."""
import array
import math
import pygame


class Audio:
    def __init__(self):
        self.enabled = False
        self.sounds = {}
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.enabled = True
            self._build()
        except Exception:
            self.enabled = False

    def _tone(self, freq, duration, volume=0.25):
        sr = 44100
        n = int(sr * duration)
        buf = array.array("h")
        for i in range(n):
            env = max(0.0, 1.0 - i / n)
            v = int(volume * 32767 * env * math.sin(2 * math.pi * freq * i / sr))
            buf.append(v)
            buf.append(v)
        return pygame.mixer.Sound(buffer=buf.tobytes())

    def _sweep(self, f1, f2, duration, volume=0.25):
        sr = 44100
        n = int(sr * duration)
        buf = array.array("h")
        phase = 0.0
        for i in range(n):
            t = i / n
            f = f1 + (f2 - f1) * t
            phase += 2 * math.pi * f / sr
            env = max(0.0, 1.0 - t)
            v = int(volume * 32767 * env * math.sin(phase))
            buf.append(v)
            buf.append(v)
        return pygame.mixer.Sound(buffer=buf.tobytes())

    def _build(self):
        self.sounds = {
            "pickup":   self._tone(880, 0.08, 0.18),
            "hit":      self._sweep(280, 80, 0.25, 0.35),
            "levelup":  self._sweep(440, 880, 0.35, 0.22),
            "gameover": self._sweep(330, 110, 0.8, 0.30),
            "powerup":  self._tone(660, 0.12, 0.22),
            "shield":   self._tone(520, 0.10, 0.20),
            "start":    self._sweep(220, 660, 0.25, 0.22),
        }

    def play(self, name):
        if not self.enabled:
            return
        s = self.sounds.get(name)
        if s:
            try:
                s.play()
            except Exception:
                pass