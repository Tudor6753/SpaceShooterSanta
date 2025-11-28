import pygame
from src.scenes.base_scene import Scene
from src.utils.constants import *
from src.utils.assets import AssetManager
from src.ui.components import Button, Label
from src.core.game_state import GameState

class MapScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.game_state = GameState()
        self.assets = AssetManager()
        self.font = self.assets.fonts['menu']
        self.title_font = self.assets.fonts['title']
        
        self.buttons = []
        self.labels = []
        
        self.create_ui()
        
        self.selected_level = None
        self.difficulty_buttons = []
        self.show_difficulty_select = False
        
        # Keyboard Navigation
        self.selected_index = 0 # Index in self.buttons (0 is Back, 1-50 are levels)
        
    def create_ui(self):
        self.labels.append(Label(VIRTUAL_WIDTH // 2 - 150, 30, "GALACTIC MAP", self.title_font, GOLD))
        
        # Back Button
        self.buttons.append(Button(50, 30, 120, 40, "BACK", self.font, 
                                 lambda: self.manager.change_scene("menu")))
        
        # Level Grid (Snake Pattern)
        start_x = 100
        start_y = 150
        padding_x = 40
        padding_y = 60
        btn_w = 80
        btn_h = 60
        cols = 10
        
        for i in range(50):
            level = i + 1
            row = i // cols
            col = i % cols
            
            # Snake pattern: Reverse column order on odd rows
            if row % 2 == 1:
                col = cols - 1 - col
            
            x = start_x + col * (btn_w + padding_x)
            y = start_y + row * (btn_h + padding_y)
            
            is_unlocked = self.game_state.is_level_unlocked(level)
            color = NEON_BLUE if is_unlocked else (50, 50, 50)
            text = f"{level}"
            
            # Capture level in lambda default arg
            btn = Button(x, y, btn_w, btn_h, text, self.assets.fonts['hud'], 
                       lambda l=level: self.select_level(l), 
                       bg_color=color)
            
            if not is_unlocked:
                btn.enabled = False
                
            self.buttons.append(btn)
            
    def select_level(self, level):
        self.selected_level = level
        self.show_difficulty_select = True
        self.create_difficulty_ui()
        
    def create_difficulty_ui(self):
        self.difficulty_buttons = []
        
        # Overlay background (handled in draw)
        
        # Difficulty Buttons
        diffs = ["easy", "medium", "hard", "extreme"]
        colors = [GREEN, GOLD, RED, NEON_PURPLE]
        
        center_x = VIRTUAL_WIDTH // 2
        center_y = VIRTUAL_HEIGHT // 2
        
        for i, diff in enumerate(diffs):
            is_unlocked = self.game_state.is_difficulty_unlocked(self.selected_level, diff)
            color = colors[i] if is_unlocked else (100, 100, 100)
            
            btn = Button(center_x - 150, center_y - 100 + i * 70, 300, 60, diff.upper(), self.font,
                       lambda d=diff: self.start_game(d),
                       bg_color=color)
            
            if not is_unlocked:
                btn.enabled = False
                
            self.difficulty_buttons.append(btn)
            
        # Close button
        self.difficulty_buttons.append(Button(center_x - 150, center_y + 200, 300, 60, "CANCEL", self.font,
                                            self.close_difficulty_select, bg_color=RED))

    def close_difficulty_select(self):
        self.show_difficulty_select = False
        self.difficulty_buttons = []

    def start_game(self, difficulty):
        # Pass level config to game scene
        self.manager.change_scene("game", level=self.selected_level, difficulty=difficulty)

    def update(self, dt):
        if self.show_difficulty_select:
            for btn in self.difficulty_buttons:
                btn.update(dt)
        else:
            for btn in self.buttons:
                btn.update(dt)

    def draw(self, screen):
        # Background - Galaxy Map Style
        screen.fill((5, 5, 20))
        
        # Draw stars (static for map)
        import random
        random.seed(42) # Consistent stars
        for _ in range(100):
            sx = random.randint(0, VIRTUAL_WIDTH)
            sy = random.randint(0, VIRTUAL_HEIGHT)
            pygame.draw.circle(screen, (200, 200, 255), (sx, sy), random.randint(1, 2))
        random.seed() # Reset seed
            
        # Draw connecting lines (Paths)
        if not self.show_difficulty_select:
            # We need to draw lines based on logical order (1->2->3), not button list order if we sorted them differently
            # But self.buttons is appended in order 1..50
            for i in range(len(self.buttons) - 1):
                btn1 = self.buttons[i]
                btn2 = self.buttons[i+1]
                
                # Draw path
                color = (100, 200, 255) if btn1.enabled and btn2.enabled else (50, 50, 80)
                pygame.draw.line(screen, color, btn1.rect.center, btn2.rect.center, 4)

        for label in self.labels:
            label.draw(screen)
            
        for btn in self.buttons:
            # Custom draw for circular nodes
            center = btn.rect.center
            radius = 30
            color = btn.color if btn.enabled else (50, 50, 50)
            
            # Highlight if hovered OR selected via keyboard
            is_selected = (btn == self.buttons[self.selected_index]) if not self.show_difficulty_select else False
            
            if (btn.hovered or is_selected) and btn.enabled:
                color = WHITE
                pygame.draw.circle(screen, GOLD, center, radius + 4) # Glow
                
            pygame.draw.circle(screen, color, center, radius)
            pygame.draw.circle(screen, WHITE, center, radius, 2) # Border
            
            # Text
            text_surf = btn.font.render(btn.text, True, BLACK if btn.enabled else (100, 100, 100))
            text_rect = text_surf.get_rect(center=center)
            screen.blit(text_surf, text_rect)
            
        # Stats Display
        stats_text = f"Coins: {self.game_state.data.get('coins', 0)} | XP: {self.game_state.data.get('xp', 0)}"
        stats_surf = self.assets.fonts['hud'].render(stats_text, True, GOLD)
        screen.blit(stats_surf, (VIRTUAL_WIDTH - 300, 40))
            
        if self.show_difficulty_select:
            # Dim background
            overlay = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))
            
            # Draw popup box
            pygame.draw.rect(screen, (50, 50, 80), (VIRTUAL_WIDTH//2 - 200, VIRTUAL_HEIGHT//2 - 200, 400, 500), border_radius=20)
            pygame.draw.rect(screen, WHITE, (VIRTUAL_WIDTH//2 - 200, VIRTUAL_HEIGHT//2 - 200, 400, 500), 2, border_radius=20)
            
            title = self.font.render(f"LEVEL {self.selected_level}", True, WHITE)
            screen.blit(title, (VIRTUAL_WIDTH//2 - title.get_width()//2, VIRTUAL_HEIGHT//2 - 180))
            
            for btn in self.difficulty_buttons:
                btn.draw(screen)
                
    def process_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.show_difficulty_select:
                        self.close_difficulty_select()
                    else:
                        self.manager.change_scene("menu")
                
                if not self.show_difficulty_select:
                    # Navigation for Level Grid
                    if event.key == pygame.K_RIGHT:
                        self.selected_index = min(len(self.buttons) - 1, self.selected_index + 1)
                    elif event.key == pygame.K_LEFT:
                        self.selected_index = max(0, self.selected_index - 1)
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = min(len(self.buttons) - 1, self.selected_index + 10)
                    elif event.key == pygame.K_UP:
                        self.selected_index = max(0, self.selected_index - 10)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if self.buttons[self.selected_index].enabled:
                            if self.buttons[self.selected_index].callback:
                                self.buttons[self.selected_index].callback()
            
            if self.show_difficulty_select:
                for btn in self.difficulty_buttons:
                    btn.handle_event(event)
            else:
                for i, btn in enumerate(self.buttons):
                    btn.handle_event(event)
                    if btn.hovered:
                        self.selected_index = i
