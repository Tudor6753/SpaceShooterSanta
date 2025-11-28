import pygame
from src.scenes.base_scene import Scene
from src.utils.constants import *
from src.utils.assets import AssetManager

class ModeSelectScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        assets = AssetManager()
        self.font_title = assets.fonts['title']
        self.font_menu = assets.fonts['menu']
        self.options = [
            {"label": "Campaign Mode (50 Levels)", "scene": "map"},
            {"label": "Android Legacy Shooter", "scene": "android_shooter"},
            {"label": "Dog Hunt Patrol", "scene": "dog_hunt"}
        ]
        self.selected_index = 0

    def process_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.manager.change_scene("menu")
                elif event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    self.launch_mode()

    def launch_mode(self):
        target = self.options[self.selected_index]['scene']
        self.manager.change_scene(target)

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill((5, 5, 20))
        
        # Title
        title_surf = self.font_title.render("MODE SELECT", True, NEON_PURPLE)
        title_rect = title_surf.get_rect(center=(VIRTUAL_WIDTH // 2, 180))
        screen.blit(title_surf, title_rect)

        # Mode cards
        for i, option in enumerate(self.options):
            card_y = 350 + i * 150
            card_rect = pygame.Rect(VIRTUAL_WIDTH // 2 - 400, card_y, 800, 120)
            
            # Card background
            if i == self.selected_index:
                pygame.draw.rect(screen, (40, 40, 80), card_rect, border_radius=10)
                pygame.draw.rect(screen, NEON_BLUE, card_rect, 4, border_radius=10)
                color = NEON_BLUE
            else:
                pygame.draw.rect(screen, (20, 20, 40), card_rect, border_radius=10)
                pygame.draw.rect(screen, (60, 60, 80), card_rect, 2, border_radius=10)
                color = WHITE
            
            # Mode title
            text = self.font_menu.render(option['label'], True, color)
            text_rect = text.get_rect(center=(card_rect.centerx, card_rect.centery))
            screen.blit(text, text_rect)

        # Controls hint
        hint = AssetManager().fonts['hud'].render("ESC: Menu | ↑↓: Navigate | ENTER: Select", True, (200, 200, 200))
        screen.blit(hint, (VIRTUAL_WIDTH // 2 - 250, VIRTUAL_HEIGHT - 60))
