import pygame
import random
from src.utils.constants import *

class AssetManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AssetManager, cls).__new__(cls)
            cls._instance.images = {}
            cls._instance.fonts = {}
            cls._instance.sounds = {}
        return cls._instance

    def load_assets(self):
        # In a real production app, we would load files here.
        # For this "Extreme Design" procedural app, we generate them.
        self.generate_santa()
        self.generate_enemies()
        self.generate_boss()
        self.generate_projectiles()
        self.generate_powerups()
        self.generate_companions()
        
        # Fonts
        self.fonts['title'] = pygame.font.SysFont("Arial", 64, bold=True)
        self.fonts['hud'] = pygame.font.SysFont("Arial", 24, bold=True)
        self.fonts['menu'] = pygame.font.SysFont("Arial", 36)

    def generate_santa(self):
        # Detailed Santa Sleigh
        surf = pygame.Surface((80, 80), pygame.SRCALPHA)
        
        # Runners (Silver)
        pygame.draw.lines(surf, (192, 192, 192), False, [(5, 60), (75, 60)], 4)
        pygame.draw.arc(surf, (192, 192, 192), (5, 45, 70, 30), 3.14, 6.28, 3)
        
        # Sleigh Body (Red with Gold Trim)
        pygame.draw.polygon(surf, (200, 0, 0), [(10, 45), (70, 45), (60, 65), (20, 65)])
        pygame.draw.polygon(surf, GOLD, [(10, 45), (70, 45), (60, 65), (20, 65)], 3)
        
        # Santa
        # Body
        pygame.draw.ellipse(surf, RED, (30, 25, 30, 30))
        # Head
        pygame.draw.circle(surf, (255, 220, 200), (45, 20), 12)
        # Beard
        pygame.draw.circle(surf, WHITE, (45, 28), 10)
        # Hat
        pygame.draw.polygon(surf, RED, [(35, 15), (55, 15), (45, 0)])
        pygame.draw.circle(surf, WHITE, (45, 0), 5) # Pompom
        
        # Bag of Toys (Brown)
        pygame.draw.circle(surf, (139, 69, 19), (65, 35), 15)
        pygame.draw.circle(surf, (160, 82, 45), (65, 35), 12) # Highlight
        
        self.images['santa'] = surf

    def generate_enemies(self):
        # Basic Enemy -> Reindeer (Rudolf)
        surf = pygame.Surface((64, 64), pygame.SRCALPHA)
        
        # Head
        pygame.draw.ellipse(surf, (139, 69, 19), (17, 20, 30, 35)) # Brown face
        
        # Ears
        pygame.draw.ellipse(surf, (100, 50, 10), (5, 25, 15, 10))
        pygame.draw.ellipse(surf, (100, 50, 10), (44, 25, 15, 10))
        
        # Antlers
        pygame.draw.line(surf, (210, 180, 140), (22, 20), (10, 5), 4)
        pygame.draw.line(surf, (210, 180, 140), (42, 20), (54, 5), 4)
        pygame.draw.line(surf, (210, 180, 140), (10, 5), (15, 0), 3)
        pygame.draw.line(surf, (210, 180, 140), (54, 5), (49, 0), 3)
        
        # Eyes
        pygame.draw.circle(surf, WHITE, (24, 30), 5)
        pygame.draw.circle(surf, WHITE, (40, 30), 5)
        pygame.draw.circle(surf, BLACK, (24, 30), 2)
        pygame.draw.circle(surf, BLACK, (40, 30), 2)
        
        # Red Nose (Glowing)
        pygame.draw.circle(surf, (255, 0, 0), (32, 45), 7)
        pygame.draw.circle(surf, (255, 150, 150), (30, 43), 3) # Shine
        
        self.images['enemy_basic'] = surf
        
        # Fast Enemy -> Snowball
        surf = pygame.Surface((48, 48), pygame.SRCALPHA)
        pygame.draw.circle(surf, (240, 248, 255), (24, 24), 20) # Alice Blue / White
        # Shading (Blue-ish tint at bottom right)
        pygame.draw.arc(surf, (200, 200, 230), (8, 8, 32, 32), 3.14, 6.28, 3)
        # Texture dots
        pygame.draw.circle(surf, (200, 200, 230), (18, 18), 2)
        pygame.draw.circle(surf, (200, 200, 230), (30, 30), 3)
        pygame.draw.circle(surf, (200, 200, 230), (14, 30), 2)
        
        self.images['enemy_fast'] = surf

        # Robo Critter (Dog Hunt adversary)
        surf = pygame.Surface((40, 25), pygame.SRCALPHA)
        pygame.draw.rect(surf, NEON_BLUE, (2, 5, 36, 15), border_radius=8)
        pygame.draw.circle(surf, WHITE, (10, 12), 4)
        pygame.draw.circle(surf, WHITE, (30, 12), 4)
        pygame.draw.circle(surf, BLACK, (10, 12), 2)
        pygame.draw.circle(surf, BLACK, (30, 12), 2)
        pygame.draw.circle(surf, NEON_PURPLE, (20, 20), 5)
        self.images['robo_critter'] = surf

    def generate_projectiles(self):
        # Detailed Coke Bottle
        surf = pygame.Surface((20, 48), pygame.SRCALPHA)
        
        # Glass Body (Dark Brown/Black with transparency)
        pygame.draw.rect(surf, (60, 20, 10), (5, 12, 10, 30), border_radius=4)
        
        # Neck
        pygame.draw.rect(surf, (60, 20, 10), (7, 2, 6, 10))
        
        # Cap (Red)
        pygame.draw.rect(surf, COKE_RED, (6, 0, 8, 3))
        
        # Label (Red with White Wave)
        pygame.draw.rect(surf, COKE_RED, (4, 22, 12, 12))
        pygame.draw.arc(surf, WHITE, (4, 22, 12, 12), 0, 3.14, 2) # Wave
        
        self.images['projectile_coke'] = surf
        
        # Pepsi Bottle (Boss Projectile)
        surf = pygame.Surface((24, 56), pygame.SRCALPHA)
        # Glass Body
        pygame.draw.rect(surf, (60, 20, 10), (6, 14, 12, 36), border_radius=4)
        pygame.draw.rect(surf, (60, 20, 10), (8, 2, 8, 12))
        # Cap (Blue)
        pygame.draw.rect(surf, BLUE, (7, 0, 10, 4))
        # Label (Blue/Red/White Circle)
        pygame.draw.circle(surf, WHITE, (12, 32), 8)
        pygame.draw.arc(surf, RED, (4, 24, 16, 16), 0, 3.14, 8)
        pygame.draw.arc(surf, BLUE, (4, 24, 16, 16), 3.14, 6.28, 8)
        self.images['projectile_pepsi'] = surf

        # Sprite Juice (Companion Projectile)
        surf = pygame.Surface((10, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, (50, 255, 50), (0, 0, 10, 20)) # Neon Green Blob
        pygame.draw.circle(surf, (200, 255, 200), (3, 5), 2) # Highlight
        self.images['projectile_sprite_juice'] = surf

    def generate_boss(self):
        # Coca Cola Truck - Ultra Enhanced Design
        surf = pygame.Surface((260, 150), pygame.SRCALPHA)
        
        # Shadow
        pygame.draw.ellipse(surf, (0, 0, 0, 100), (10, 120, 240, 30))
        
        # Trailer (Red with gradient effect simulated by lines)
        pygame.draw.rect(surf, (140, 0, 0), (60, 10, 190, 110), border_radius=8) # Darker base
        pygame.draw.rect(surf, COKE_RED, (65, 15, 180, 100), border_radius=6) # Main body
        
        # Trailer Details (Chrome strips)
        pygame.draw.rect(surf, (220, 220, 220), (65, 105, 180, 10)) # Bottom chrome
        pygame.draw.rect(surf, (220, 220, 220), (65, 15, 180, 5)) # Top chrome
        
        # Cab (Red)
        pygame.draw.rect(surf, (140, 0, 0), (0, 50, 60, 80), border_radius=8)
        pygame.draw.rect(surf, COKE_RED, (5, 55, 50, 70), border_radius=6)
        
        # Windshield (Gradient Blue)
        pygame.draw.rect(surf, (100, 150, 255), (5, 60, 45, 30))
        pygame.draw.line(surf, WHITE, (5, 60), (50, 90), 2) # Reflection
        
        # Driver (Santa Silhouette)
        pygame.draw.circle(surf, (255, 200, 200), (25, 75), 8) # Face
        pygame.draw.polygon(surf, RED, [(15, 75), (35, 75), (25, 55)]) # Hat
        pygame.draw.circle(surf, WHITE, (25, 80), 6) # Beard
        
        # Grille (Chrome)
        pygame.draw.rect(surf, (200, 200, 200), (5, 95, 50, 25))
        for i in range(6):
            pygame.draw.line(surf, (100, 100, 100), (5, 95 + i*4), (55, 95 + i*4), 2)
            
        # Headlights (Glowing)
        pygame.draw.circle(surf, (255, 255, 200), (10, 125), 8)
        pygame.draw.circle(surf, (255, 255, 255), (10, 125), 4)
        pygame.draw.circle(surf, (255, 255, 200), (50, 125), 8)
        pygame.draw.circle(surf, (255, 255, 255), (50, 125), 4)
            
        # Wheels (More detailed - 18 wheeler style)
        for x in [30, 80, 95, 200, 215, 230]:
            pygame.draw.circle(surf, (20, 20, 20), (x, 135), 14) # Tire
            pygame.draw.circle(surf, (180, 180, 180), (x, 135), 8) # Rim
            pygame.draw.circle(surf, (50, 50, 50), (x, 135), 2) # Nut
            
        # Logo on side (Santa with Coke)
        pygame.draw.rect(surf, WHITE, (80, 45, 140, 40), border_radius=20)
        # Stylized Wave
        pygame.draw.arc(surf, COKE_RED, (80, 45, 140, 40), 0, 3.14, 4)
        font = pygame.font.SysFont("Arial", 20, bold=True)
        text = font.render("SANTA", True, COKE_RED)
        surf.blit(text, (110, 55))
        
        # Exhaust Pipes (Chrome stacks)
        pygame.draw.rect(surf, (180, 180, 180), (52, 20, 6, 80))
        pygame.draw.ellipse(surf, (100, 100, 100), (50, 15, 10, 5)) # Top smoke hole
        
        self.images['boss_truck'] = surf

    def generate_powerups(self):
        # Health Crate
        surf = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.rect(surf, (200, 200, 200), (0, 0, 24, 24), border_radius=4)
        pygame.draw.rect(surf, RED, (8, 2, 8, 20))
        pygame.draw.rect(surf, RED, (2, 8, 20, 8))
        pygame.draw.rect(surf, WHITE, (8, 2, 8, 20), 1) # Outline
        self.images['powerup_health'] = surf
        
        # Cola Burst (Triple Shot)
        surf = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(surf, COKE_RED, (12, 12), 12)
        pygame.draw.circle(surf, WHITE, (12, 12), 10, 2)
        # 3 dots
        pygame.draw.circle(surf, WHITE, (12, 6), 2)
        pygame.draw.circle(surf, WHITE, (7, 15), 2)
        pygame.draw.circle(surf, WHITE, (17, 15), 2)
        self.images['powerup_cola'] = surf
        
        # Coin (New)
        surf = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(surf, GOLD, (10, 10), 10)
        pygame.draw.circle(surf, (255, 255, 200), (10, 10), 8, 1)
        font = pygame.font.SysFont("Arial", 12, bold=True)
        text = font.render("$", True, (180, 140, 0))
        surf.blit(text, (7, 3))
        self.images['coin'] = surf

        # Dog Treat
        treat = pygame.Surface((32, 18), pygame.SRCALPHA)
        pygame.draw.ellipse(treat, GOLD, (0, 0, 32, 18))
        pygame.draw.circle(treat, (255, 170, 0), (5, 9), 5)
        pygame.draw.circle(treat, (255, 170, 0), (27, 9), 5)
        self.images['dog_treat'] = treat

    def generate_companions(self):
        # Sprite Bottle Companion
        surf = pygame.Surface((24, 48), pygame.SRCALPHA)
        # Green Glass
        pygame.draw.rect(surf, (0, 180, 60), (6, 14, 12, 30), border_radius=4)
        pygame.draw.rect(surf, (0, 180, 60), (8, 2, 8, 12))
        # Cap (Silver/Green)
        pygame.draw.rect(surf, (200, 255, 200), (7, 0, 10, 4))
        # Label (Blue/Yellow)
        pygame.draw.rect(surf, (0, 100, 200), (4, 24, 16, 10))
        pygame.draw.circle(surf, (255, 255, 0), (18, 24), 4) # Lemon
        
        self.images['companion_sprite'] = surf
        
        # Dog Hunter (Existing)
        surf = pygame.Surface((50, 30), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, (180, 120, 80), (0, 5, 40, 20))
        pygame.draw.circle(surf, (200, 150, 110), (35, 15), 10)
        pygame.draw.circle(surf, BLACK, (40, 12), 2)
        pygame.draw.circle(surf, BLACK, (40, 18), 2)
        pygame.draw.polygon(surf, (180, 120, 80), [(5, 5), (10, 0), (15, 5)])
        pygame.draw.polygon(surf, (180, 120, 80), [(5, 25), (10, 30), (15, 25)])
        pygame.draw.rect(surf, WHITE, (10, 20, 12, 6))
        self.images['dog_hunter'] = surf
