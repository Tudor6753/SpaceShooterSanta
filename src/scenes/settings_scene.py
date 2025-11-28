import pygame
from src.scenes.base_scene import Scene
from src.core.settings import Settings
from src.utils.assets import AssetManager
from src.utils.constants import *

class SettingsScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.settings = Settings()
        assets = AssetManager()
        self.font_menu = assets.fonts['menu']
        self.font_hud = assets.fonts['hud']
        self.resolutions = [(1280, 720), (1920, 1080), (2560, 1440), (3840, 2160)]
        self.particle_qualities = ['low', 'medium', 'high', 'ultra']
        self.options = [
            {"label": "Resolution", "type": "resolution"},
            {"label": "Fullscreen", "type": "toggle", "attr": "fullscreen"},
            {"label": "VSync", "type": "toggle", "attr": "vsync"},
            {"label": "Music Volume", "type": "range", "attr": "music_volume", "step": 0.1, "min": 0.0, "max": 1.0},
            {"label": "Sound Volume", "type": "range", "attr": "sound_volume", "step": 0.1, "min": 0.0, "max": 1.0},
            {"label": "Particle Quality", "type": "quality"},
            {"label": "Show FPS", "type": "toggle", "attr": "show_fps"},
            {"label": "Save & Back", "type": "action"}
        ]
        self.selected_index = 0

    def process_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.leave()
                elif event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    direction = -1 if event.key == pygame.K_LEFT else 1
                    self.adjust_option(direction)
                elif event.key == pygame.K_RETURN:
                    self.select_option()

    def adjust_option(self, direction):
        option = self.options[self.selected_index]
        
        if option['type'] == 'resolution':
            current_res = (self.settings.resolution_width, self.settings.resolution_height)
            try:
                idx = self.resolutions.index(current_res)
            except ValueError:
                idx = 1
            idx = (idx + direction) % len(self.resolutions)
            self.settings.resolution_width, self.settings.resolution_height = self.resolutions[idx]
            self.manager.engine.apply_display_settings()
        elif option['type'] == 'quality':
            try:
                idx = self.particle_qualities.index(self.settings.particle_quality)
            except ValueError:
                idx = 2
            idx = (idx + direction) % len(self.particle_qualities)
            self.settings.particle_quality = self.particle_qualities[idx]
        elif option['type'] == 'toggle' and direction != 0:
            current = getattr(self.settings, option['attr'])
            setattr(self.settings, option['attr'], not current)
            if option['attr'] in ('fullscreen', 'vsync'):
                self.manager.engine.apply_display_settings()
        elif option['type'] == 'range':
            value = getattr(self.settings, option['attr'])
            value += option['step'] * direction
            value = max(option['min'], min(option['max'], value))
            setattr(self.settings, option['attr'], round(value, 2))

    def select_option(self):
        option = self.options[self.selected_index]
        if option['type'] == 'action':
            self.leave()
        elif option['type'] == 'toggle':
            self.adjust_option(1)

    def leave(self):
        self.settings.save()
        self.manager.change_scene('menu')

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill((20, 20, 30))
        title = self.font_menu.render("SETTINGS", True, NEON_PURPLE)
        screen.blit(title, (VIRTUAL_WIDTH // 2 - title.get_width() // 2, 120))

        for idx, option in enumerate(self.options):
            color = NEON_BLUE if idx == self.selected_index else WHITE
            label = option['label']
            value = ""
            
            if option['type'] == 'resolution':
                value = f"{self.settings.resolution_width}x{self.settings.resolution_height}"
            elif option['type'] == 'quality':
                value = self.settings.particle_quality.upper()
            elif option['type'] == 'range':
                value = f"{getattr(self.settings, option['attr']):.1f}"
            elif option['type'] == 'toggle':
                value = "ON" if getattr(self.settings, option['attr']) else "OFF"
            
            text = self.font_menu.render(f"{label}: {value}", True, color)
            screen.blit(text, (VIRTUAL_WIDTH // 2 - text.get_width() // 2, 250 + idx * 70))

        hint = self.font_hud.render("←→: Adjust | ↑↓: Navigate | ENTER: Toggle | ESC: Back", True, WHITE)
        screen.blit(hint, (VIRTUAL_WIDTH // 2 - hint.get_width() // 2, VIRTUAL_HEIGHT - 60))
