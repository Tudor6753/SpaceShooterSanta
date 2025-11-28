import pygame
from src.utils.constants import *

class ResolutionManager:
    """Handles dynamic resolution scaling and virtual coordinate mapping"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ResolutionManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def __init__(self):
        if self.initialized:
            return
        self.virtual_width = VIRTUAL_WIDTH
        self.virtual_height = VIRTUAL_HEIGHT
        self.screen_width = 1920
        self.screen_height = 1080
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.virtual_surface = None
        self.initialized = True
    
    def set_resolution(self, width, height):
        """Set the actual screen resolution and calculate scaling"""
        self.screen_width = width
        self.screen_height = height
        
        # Calculate aspect ratio preserving scale
        scale_x = width / self.virtual_width
        scale_y = height / self.virtual_height
        
        # Use uniform scaling to preserve aspect ratio
        self.scale = min(scale_x, scale_y)
        
        # Calculate scaled dimensions
        scaled_width = int(self.virtual_width * self.scale)
        scaled_height = int(self.virtual_height * self.scale)
        
        # Center the viewport
        self.offset_x = (width - scaled_width) // 2
        self.offset_y = (height - scaled_height) // 2
        
        # Create virtual surface for rendering
        self.virtual_surface = pygame.Surface((self.virtual_width, self.virtual_height))
        
        self.scale_x = self.scale
        self.scale_y = self.scale
    
    def to_virtual(self, screen_x, screen_y):
        """Convert screen coordinates to virtual coordinates"""
        virtual_x = (screen_x - self.offset_x) / self.scale
        virtual_y = (screen_y - self.offset_y) / self.scale
        return int(virtual_x), int(virtual_y)
    
    def to_screen(self, virtual_x, virtual_y):
        """Convert virtual coordinates to screen coordinates"""
        screen_x = virtual_x * self.scale + self.offset_x
        screen_y = virtual_y * self.scale + self.offset_y
        return int(screen_x), int(screen_y)
    
    def scale_value(self, value):
        """Scale a single value from virtual to screen space"""
        return value * self.scale
    
    def get_virtual_surface(self):
        """Get the virtual rendering surface"""
        return self.virtual_surface
    
    def present(self, screen):
        """Blit the virtual surface to the actual screen with scaling"""
        if self.virtual_surface:
            scaled_surf = pygame.transform.scale(
                self.virtual_surface,
                (int(self.virtual_width * self.scale), int(self.virtual_height * self.scale))
            )
            # Fill letterbox bars
            screen.fill(BLACK)
            screen.blit(scaled_surf, (self.offset_x, self.offset_y))
