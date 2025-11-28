import pygame
from src.entities.entity import Entity
from src.entities.projectile import Projectile
from src.utils.constants import *
from src.utils.assets import AssetManager

class Companion(Entity):
    def __init__(self, groups, projectile_groups, player, c_type="sprite"):
        super().__init__(groups, LAYER_PLAYER) # Same layer as player
        self.player = player
        self.c_type = c_type
        self.projectile_groups = projectile_groups
        
        assets = AssetManager()
        if c_type == "sprite":
            self.image = assets.images.get('companion_sprite', pygame.Surface((20, 40)))
        else:
            self.image = pygame.Surface((20, 20))
            self.image.fill(GREEN)
            
        self.rect = self.image.get_rect()
        self.offset = pygame.math.Vector2(-40, 20) # Relative to player
        self.position = pygame.math.Vector2(player.rect.center) + self.offset
        self.rect.center = self.position
        
        self.shoot_timer = 0
        self.shoot_delay = 1.5 # Slower than player

    def update(self, dt):
        # Follow player with slight lag or direct lock
        target_pos = pygame.math.Vector2(self.player.rect.center) + self.offset
        
        # Smooth follow
        self.position += (target_pos - self.position) * 10 * dt
        self.rect.center = (int(self.position.x), int(self.position.y))
        
        # Auto shoot
        self.shoot_timer -= dt
        if self.shoot_timer <= 0:
            self.shoot()
            self.shoot_timer = self.shoot_delay
            
    def shoot(self):
        # Sprite shoots "Lemon Lime" lasers (Green/Yellow)
        p = Projectile(self.projectile_groups, self.rect.centerx, self.rect.top, -300, damage=15, p_type='sprite_juice')
        # Custom color for sprite juice if not defined in assets
        if not hasattr(p, 'image') or p.image.get_height() < 5:
            p.image = pygame.Surface((6, 16))
            p.image.fill((50, 255, 50)) # Neon Green
            p.rect = p.image.get_rect(center=p.rect.center)
