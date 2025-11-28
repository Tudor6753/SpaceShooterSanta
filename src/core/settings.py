import json
import os

class Settings:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance.load()
        return cls._instance

    def load(self):
        self.sound_volume = 1.0
        self.music_volume = 0.8
        self.fullscreen = False
        self.vsync = True
        self.resolution_width = 1920
        self.resolution_height = 1080
        self.high_score = 0
        self.achievements = {}
        self.particle_quality = 'high'  # low, medium, high, ultra
        self.show_fps = False
        
        # Try to load from file
        try:
            if os.path.exists('config/settings.json'):
                with open('config/settings.json', 'r') as f:
                    data = json.load(f)
                    self.sound_volume = data.get('sound_volume', 1.0)
                    self.music_volume = data.get('music_volume', 0.8)
                    self.fullscreen = data.get('fullscreen', False)
                    self.vsync = data.get('vsync', True)
                    self.resolution_width = data.get('resolution_width', 1920)
                    self.resolution_height = data.get('resolution_height', 1080)
                    self.high_score = data.get('high_score', 0)
                    self.achievements = data.get('achievements', {})
                    self.particle_quality = data.get('particle_quality', 'high')
                    self.show_fps = data.get('show_fps', False)
        except:
            pass

    def save(self):
        data = {
            'sound_volume': self.sound_volume,
            'music_volume': self.music_volume,
            'fullscreen': self.fullscreen,
            'vsync': self.vsync,
            'resolution_width': self.resolution_width,
            'resolution_height': self.resolution_height,
            'high_score': self.high_score,
            'achievements': self.achievements,
            'particle_quality': self.particle_quality,
            'show_fps': self.show_fps
        }
        try:
            os.makedirs('config', exist_ok=True)
            with open('config/settings.json', 'w') as f:
                json.dump(data, f, indent=2)
        except:
            pass
