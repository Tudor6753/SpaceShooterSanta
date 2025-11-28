import pygame
import sys
from src.utils.constants import *
from src.core.scene_manager import SceneManager
from src.core.settings import Settings
from src.core.resolution_manager import ResolutionManager
from src.core.audio_manager import AudioManager
from src.utils.assets import AssetManager
from src.scenes.menu_scene import MenuScene
from src.scenes.mode_select_scene import ModeSelectScene
from src.scenes.game_scene import SpaceShooterScene
from src.scenes.android_space_scene import AndroidSpaceScene
from src.scenes.dog_hunt_scene import DogHuntScene
from src.scenes.settings_scene import SettingsScene
from src.scenes.map_scene import MapScene
from src.scenes.intro_scene import IntroScene
from src.scenes.shop_scene import ShopScene
from src.scenes.game_over_scene import GameOverScene

class Engine:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.resolution_manager = ResolutionManager()
        self.audio_manager = AudioManager()
        
        self.screen = None
        self.apply_display_settings()
        
        self.clock = pygame.time.Clock()
        self.asset_manager = AssetManager()
        self.asset_manager.load_assets()
        
        # Performance tracking
        self.fps_history = []
        self.frame_time = 0
        
        self.scene_manager = SceneManager(self)
        self.scene_manager.add_scene("menu", MenuScene)
        self.scene_manager.add_scene("mode_select", ModeSelectScene)
        self.scene_manager.add_scene("space_shooter", SpaceShooterScene)
        self.scene_manager.add_scene("android_shooter", AndroidSpaceScene)
        self.scene_manager.add_scene("dog_hunt", DogHuntScene)
        self.scene_manager.add_scene("settings", SettingsScene)
        self.scene_manager.add_scene("map", MapScene)
        self.scene_manager.add_scene("game", SpaceShooterScene) # Alias for map scene to use
        self.scene_manager.add_scene("intro", IntroScene)
        self.scene_manager.add_scene("shop", ShopScene)
        self.scene_manager.add_scene("game_over", GameOverScene)
        self.scene_manager.change_scene("intro")

    def apply_display_settings(self):
        """Apply display settings with proper resolution handling"""
        flags = 0
        if self.settings.fullscreen:
            flags |= pygame.FULLSCREEN
        if self.settings.vsync:
            flags |= pygame.SCALED
        
        width = self.settings.resolution_width
        height = self.settings.resolution_height
        
        # Ensure minimum resolution
        width = max(MIN_WIDTH, width)
        height = max(MIN_HEIGHT, height)
        
        self.screen = pygame.display.set_mode((width, height), flags)
        pygame.display.set_caption(TITLE)
        
        # Configure resolution manager
        self.resolution_manager.set_resolution(width, height)
        
        # Update audio settings
        self.audio_manager.set_music_volume(self.settings.music_volume)
        self.audio_manager.set_sound_volume(self.settings.sound_volume)

    def run(self):
        while self.scene_manager.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            self.frame_time = dt
            
            # Track FPS
            if self.settings.show_fps:
                current_fps = self.clock.get_fps()
                self.fps_history.append(current_fps)
                if len(self.fps_history) > 60:
                    self.fps_history.pop(0)
            
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.scene_manager.quit_game()
                elif event.type == pygame.VIDEORESIZE:
                    self.settings.resolution_width = event.w
                    self.settings.resolution_height = event.h
                    self.resolution_manager.set_resolution(event.w, event.h)
            
            # Get virtual surface for rendering
            virtual_surface = self.resolution_manager.get_virtual_surface()
            
            self.scene_manager.process_input(events)
            self.scene_manager.update(dt)
            self.scene_manager.draw(virtual_surface)
            
            # Draw FPS if enabled
            if self.settings.show_fps and self.fps_history:
                avg_fps = sum(self.fps_history) / len(self.fps_history)
                font = self.asset_manager.fonts['hud']
                fps_text = font.render(f"FPS: {int(avg_fps)}", True, NEON_GREEN)
                virtual_surface.blit(fps_text, (VIRTUAL_WIDTH - 120, 10))
            
            # Present to actual screen with scaling
            self.resolution_manager.present(self.screen)
            pygame.display.flip()
            
        self.settings.save()
        pygame.quit()
        sys.exit()
