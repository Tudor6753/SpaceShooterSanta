import pygame
from src.scenes.base_scene import Scene
from src.utils.constants import *
from src.utils.assets import AssetManager
from src.ui.components import Button, Label

class GameOverScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.assets = AssetManager()
        self.font_title = self.assets.fonts['title']
        self.font_menu = self.assets.fonts['menu']
        
        self.result = "defeat" # or "victory"
        self.score = 0
        self.coins = 0
        
        self.buttons = []
        self.labels = []
        
    def setup(self, result="defeat", score=0, coins=0):
        self.result = result
        self.score = score
        self.coins = coins
        self.create_ui()
        
    def create_ui(self):
        self.buttons = []
        self.labels = []
        
        title_text = "GAME OVER" if self.result == "defeat" else "VICTORY!"
        title_color = RED if self.result == "defeat" else GREEN
        
        # Center text properly
        title_surf = self.font_title.render(title_text, True, title_color)
        self.labels.append(Label(VIRTUAL_WIDTH // 2 - title_surf.get_width() // 2, 100, title_text, self.font_title, title_color))
        
        score_text = f"Score: {self.score}"
        score_surf = self.font_menu.render(score_text, True, WHITE)
        self.labels.append(Label(VIRTUAL_WIDTH // 2 - score_surf.get_width() // 2, 200, score_text, self.font_menu, WHITE))
        
        coins_text = f"Coins Earned: {self.coins}"
        coins_surf = self.font_menu.render(coins_text, True, GOLD)
        self.labels.append(Label(VIRTUAL_WIDTH // 2 - coins_surf.get_width() // 2, 250, coins_text, self.font_menu, GOLD))
        
        # Buttons
        # Retry only if defeat or just always? Always is fine.
        self.buttons.append(Button(VIRTUAL_WIDTH // 2 - 100, 350, 200, 50, "RETRY", self.font_menu, 
                                 lambda: self.manager.change_scene("game", level=self.manager.scenes['game'].current_level, difficulty=self.manager.scenes['game'].current_difficulty)))
        
        self.buttons.append(Button(VIRTUAL_WIDTH // 2 - 100, 420, 200, 50, "MAP", self.font_menu, 
                                 lambda: self.manager.change_scene("map")))
                                 
        self.buttons.append(Button(VIRTUAL_WIDTH // 2 - 100, 490, 200, 50, "SHOP", self.font_menu, 
                                 lambda: self.manager.change_scene("shop")))

    def update(self, dt):
        for btn in self.buttons:
            btn.update(dt)

    def draw(self, screen):
        # Dark overlay
        overlay = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        screen.blit(overlay, (0, 0))
        
        for label in self.labels:
            label.draw(screen)
            
        for btn in self.buttons:
            btn.draw(screen)

    def process_input(self, events):
        for event in events:
            for btn in self.buttons:
                btn.handle_event(event)
