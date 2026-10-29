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

    def _make_sound(self, freq_start, freq_end, duration, volume):

        sample_rate = 44100
        n = int(sample_rate * duration)
        data = array.array("h")
        phase = 0.0
        for i in range(n):
            t = i / n                                        
            freq = freq_start + (freq_end - freq_start) * t   
            phase += 2 * math.pi * freq / sample_rate
            fade = 1.0 - t                                   
            value = int(volume * 32767 * fade * math.sin(phase))
            data.append(value)  
            data.append(value)  
        return pygame.mixer.Sound(buffer=data.tobytes())

    def _build(self):
        self.sounds = {
            "pickup":   self._make_sound(880, 880, 0.08, 0.18),
            "hit":      self._make_sound(280, 80, 0.25, 0.35),
            "levelup":  self._make_sound(440, 880, 0.35, 0.22),
            "gameover": self._make_sound(330, 110, 0.8, 0.30),
            "powerup":  self._make_sound(660, 660, 0.12, 0.22),
            "shield":   self._make_sound(520, 520, 0.10, 0.20),
            "start":    self._make_sound(220, 660, 0.25, 0.22),
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