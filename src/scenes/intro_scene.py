import pygame
from src.scenes.base_scene import Scene
from src.utils.constants import *
from src.utils.assets import AssetManager

class IntroScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.font_title = AssetManager().fonts['title']
        self.font_text = AssetManager().fonts['menu']
        
        self.story_lines = [
            "In the vast expanse of the Polar Nebula,",
            "a shadow has fallen upon the galaxy.",
            "",
            "The Galactic Grinch Federation, fueled by",
            "the industrial might of the Soda Empire,",
            "has declared war on the Spirit of Giving.",
            "",
            "They have erected a blockade around Earth,",
            "weaponizing joy and turning reindeer",
            "into cybernetic thralls.",
            "",
            "Santa Claus, the last Guardian of the North Star,",
            "must pilot the Sleigh-X1 through the blockade.",
            "",
            "This is not just a delivery...",
            "It is a crusade for the soul of the galaxy.",
            "",
            "SPACE SHOOTER SANTA"
        ]
        
        self.scroll_y = VIRTUAL_HEIGHT
        self.scroll_speed = 25
        self.skip_text = self.font_text.render("Press SPACE to Skip", True, (100, 100, 100))
        
        # Stars for background
        self.stars = []
        import random
        for _ in range(100):
            self.stars.append([
                random.randint(0, VIRTUAL_WIDTH),
                random.randint(0, VIRTUAL_HEIGHT),
                random.randint(1, 3)
            ])
            
        self.anim_timer = 0

    def process_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    self.manager.change_scene("menu")

    def update(self, dt):
        self.scroll_y -= self.scroll_speed * dt
        self.anim_timer += dt
        
        # End of scroll
        if self.scroll_y < -len(self.story_lines) * 50 - 100:
            self.manager.change_scene("menu")

    def draw(self, screen):
        screen.fill(BLACK)
        
        # Draw stars
        for star in self.stars:
            pygame.draw.circle(screen, (200, 200, 200), (star[0], star[1]), star[2])
            
        # Draw scrolling text
        for i, line in enumerate(self.story_lines):
            y = self.scroll_y + i * 50
            
            # Fade in/out effect based on position
            if -50 <= y <= VIRTUAL_HEIGHT + 50:
                # Center text
                if i == len(self.story_lines) - 1: # Title
                    surf = self.font_title.render(line, True, RED)
                else:
                    surf = self.font_text.render(line, True, GOLD)
                
                rect = surf.get_rect(center=(VIRTUAL_WIDTH // 2, y))
                screen.blit(surf, rect)
        
        # Skip hint
        screen.blit(self.skip_text, (VIRTUAL_WIDTH - 250, VIRTUAL_HEIGHT - 40))
