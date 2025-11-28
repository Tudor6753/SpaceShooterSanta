import pygame
from src.utils.constants import *

class AudioManager:
    """Centralized audio management system"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AudioManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def __init__(self):
        if self.initialized:
            return
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self.sounds = {}
        self.music_volume = 0.8
        self.sound_volume = 1.0
        self.current_music = None
        self.initialized = True
    
    def load_sound(self, name, filename=None):
        """Load a sound effect (or generate procedurally)"""
        # For now, generate placeholder sounds
        # In production, you'd load actual audio files
        try:
            sound = pygame.mixer.Sound(buffer=self.generate_tone(440, 0.1))
            self.sounds[name] = sound
        except:
            pass
    
    def play_sound(self, name, volume=1.0):
        """Play a sound effect"""
        if name in self.sounds:
            sound = self.sounds[name]
            sound.set_volume(self.sound_volume * volume)
            sound.play()
    
    def play_music(self, name, loops=-1):
        """Play background music"""
        # In production, load and play actual music files
        pass
    
    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def set_sound_volume(self, volume):
        """Set sound effect volume (0.0 to 1.0)"""
        self.sound_volume = max(0.0, min(1.0, volume))
    
    def generate_tone(self, frequency, duration):
        """Generate a simple tone for placeholder audio"""
        sample_rate = 44100
        samples = int(sample_rate * duration)
        wave = []
        for i in range(samples):
            value = int(32767 * 0.3 * pygame.math.sin(2.0 * 3.14159 * frequency * i / sample_rate))
            wave.append([value, value])
        return bytes(wave)
    
    def stop_all(self):
        """Stop all sounds"""
        pygame.mixer.stop()
        pygame.mixer.music.stop()
