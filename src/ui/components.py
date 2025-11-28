import pygame
from src.utils.constants import *

class Button:
    """Production-quality UI button"""
    def __init__(self, x, y, width, height, text, font, callback=None, bg_color=(60, 60, 80)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.callback = callback
        self.hovered = False
        self.pressed = False
        self.enabled = True
        self.color = bg_color
        self.hover_color = (min(255, bg_color[0] + 20), min(255, bg_color[1] + 20), min(255, bg_color[2] + 40))
        self.text_color = WHITE
        self.border_color = NEON_BLUE
    
    def handle_event(self, event):
        """Handle input events"""
        if not self.enabled:
            return
            
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.hovered:
                self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.pressed and self.hovered:
                    if self.callback:
                        self.callback()
                self.pressed = False

    def update(self, dt):
        """Update button state (animations etc)"""
        pass
    
    def draw(self, surface):
        """Render the button"""
        color = self.hover_color if self.hovered else self.color
        if not self.enabled:
            color = (40, 40, 40)
        
        # Button body with gradient effect
        rect = self.rect
        if self.hovered and self.enabled:
            # Glow effect
            for i in range(3):
                pygame.draw.rect(surface, (self.border_color[0]//2, self.border_color[1]//2, self.border_color[2]//2), 
                               rect.inflate(i*2, i*2), border_radius=10)
        
        pygame.draw.rect(surface, color, rect, border_radius=8)
        
        # Shine effect (top half lighter)
        shine_rect = pygame.Rect(rect.x, rect.y, rect.width, rect.height // 2)
        s = pygame.Surface((rect.width, rect.height // 2), pygame.SRCALPHA)
        s.fill((255, 255, 255, 30))
        surface.blit(s, shine_rect.topleft)
        
        # Border
        border_color = self.border_color if self.hovered else (40, 40, 60)
        pygame.draw.rect(surface, border_color, rect, 3, border_radius=8)
        
        # Text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        
        # Text shadow
        if self.enabled:
            shadow_surf = self.font.render(self.text, True, (0, 0, 0))
            surface.blit(shadow_surf, (text_rect.x + 2, text_rect.y + 2))
            
        surface.blit(text_surf, text_rect)


class ProgressBar:
    """Animated progress bar"""
    def __init__(self, x, y, width, height, max_value=100, color=NEON_GREEN):
        self.rect = pygame.Rect(x, y, width, height)
        self.value = 0
        self.max_value = max_value
        self.target_value = 0
        self.lerp_speed = 5.0
        self.color = color
        self.bg_color = (30, 30, 40)
    
    def set_value(self, value):
        """Set target value"""
        self.target_value = max(0, min(self.max_value, value))
    
    def update(self, dt):
        """Smoothly interpolate to target value"""
        if abs(self.value - self.target_value) > 0.1:
            self.value += (self.target_value - self.value) * self.lerp_speed * dt
        else:
            self.value = self.target_value
    
    def draw(self, surface):
        """Render the progress bar"""
        # Background
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=4)
        
        # Fill
        fill_width = int((self.value / self.max_value) * self.rect.width)
        if fill_width > 0:
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
            pygame.draw.rect(surface, self.color, fill_rect, border_radius=4)
        
        # Border
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=4)


class Label:
    """Simple text label with optional background"""
    def __init__(self, x, y, text, font, color=WHITE, bg_color=None):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.color = color
        self.bg_color = bg_color
        self.padding = 10
    
    def set_text(self, text):
        """Update label text"""
        self.text = text
    
    def draw(self, surface):
        """Render the label"""
        text_surf = self.font.render(str(self.text), True, self.color)
        text_rect = text_surf.get_rect(topleft=(self.x, self.y))
        
        if self.bg_color:
            bg_rect = text_rect.inflate(self.padding * 2, self.padding * 2)
            pygame.draw.rect(surface, self.bg_color, bg_rect, border_radius=4)
        
        surface.blit(text_surf, text_rect)
