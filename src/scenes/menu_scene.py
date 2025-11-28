import pygame
import math
import random
from src.scenes.base_scene import Scene
from src.utils.constants import *
from src.utils.assets import AssetManager

class MenuScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.font_title = AssetManager().fonts['title']
        self.font_menu = AssetManager().fonts['menu']
        self.options = [
            {"label": "Arcade Launchpad", "action": "scene", "target": "mode_select"},
            {"label": "Galactic Shop", "action": "scene", "target": "shop"},
            {"label": "Settings", "action": "scene", "target": "settings"},
            {"label": "Exit", "action": "exit"}
        ]
        self.selected_index = 0
        
        # Persistent stars
        self.stars = []
        import random
        for _ in range(100):
            self.stars.append({
                'pos': [random.randint(0, VIRTUAL_WIDTH), random.randint(0, VIRTUAL_HEIGHT)],
                'speed': random.randint(10, 50),
                'size': random.randint(1, 3),
                'brightness': random.randint(100, 255)
            })
        self.pulse_timer = 0

    def process_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    self.select_option()
                elif event.key == pygame.K_ESCAPE:
                    self.manager.quit_game()
            
            # Mouse Support
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for i in range(len(self.options)):
                    # Calculate rect for each option
                    rect = pygame.Rect(VIRTUAL_WIDTH // 2 - 200, 400 + i * 80 - 25, 400, 50)
                    if rect.collidepoint(mouse_pos):
                        self.selected_index = i
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    for i in range(len(self.options)):
                        rect = pygame.Rect(VIRTUAL_WIDTH // 2 - 200, 400 + i * 80 - 25, 400, 50)
                        if rect.collidepoint(mouse_pos):
                            self.selected_index = i
                            self.select_option()

    def select_option(self):
        option = self.options[self.selected_index]
        if option["action"] == "scene":
            self.manager.change_scene(option["target"])
        elif option["action"] == "exit":
            self.manager.quit_game()

    def update(self, dt):
        self.pulse_timer += dt * 5
        # Update stars
        for star in self.stars:
            star['pos'][1] += star['speed'] * dt
            if star['pos'][1] > VIRTUAL_HEIGHT:
                star['pos'][1] = 0
                star['pos'][0] = random.randint(0, VIRTUAL_WIDTH)

    def draw(self, screen):
        # Animated background
        screen.fill((5, 5, 15))
        for star in self.stars:
            pygame.draw.circle(screen, (star['brightness'], star['brightness'], star['brightness']), 
                             (int(star['pos'][0]), int(star['pos'][1])), star['size'])
        
        # Title with glow effect
        title_surf = self.font_title.render(TITLE, True, NEON_BLUE)
        title_rect = title_surf.get_rect(center=(VIRTUAL_WIDTH // 2, 200))
        # Glow
        for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
            glow = self.font_title.render(TITLE, True, (0, 100, 150))
            screen.blit(glow, (title_rect.x + offset[0], title_rect.y + offset[1]))
        screen.blit(title_surf, title_rect)
        
        # Menu Options
        for i, option in enumerate(self.options):
            if i == self.selected_index:
                # Pulsing color
                pulse = (math.sin(self.pulse_timer) + 1) * 0.5 # 0 to 1
                r = int(NEON_BLUE[0] * (0.5 + 0.5 * pulse))
                g = int(NEON_BLUE[1] * (0.5 + 0.5 * pulse))
                b = int(NEON_BLUE[2])
                color = (r, g, b)
                
                # Selection indicator
                indicator_y = 400 + i * 80
                pygame.draw.polygon(screen, color, 
                                  [(VIRTUAL_WIDTH // 2 - 250, indicator_y + 10),
                                   (VIRTUAL_WIDTH // 2 - 230, indicator_y),
                                   (VIRTUAL_WIDTH // 2 - 230, indicator_y + 20)])
            else:
                color = (140, 140, 160)
            
            text_surf = self.font_menu.render(option["label"], True, color)
            text_rect = text_surf.get_rect(center=(VIRTUAL_WIDTH // 2, 400 + i * 80))
            screen.blit(text_surf, text_rect)
        
        # Version/Credits
        version = AssetManager().fonts['hud'].render("v2.1 Enhanced Edition", True, (100, 100, 120))
        screen.blit(version, (VIRTUAL_WIDTH - 250, VIRTUAL_HEIGHT - 40))
