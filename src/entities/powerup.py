import pygame
from src.entities.entity import Entity
from src.utils.constants import *
from src.utils.assets import AssetManager

class PowerUp(Entity):
    def __init__(self, groups, x, y, power_type='health'):
        super().__init__(groups, LAYER_PROJECTILES)
        self.power_type = power_type
        assets = AssetManager()
        if power_type == 'health':
            self.image = assets.images.get('powerup_health', pygame.Surface((20, 20)))
        elif power_type == 'cola_burst':
            self.image = assets.images.get('powerup_cola', pygame.Surface((20, 20)))
            if 'powerup_cola' not in assets.images:
                self.image.fill(RED)
        elif power_type == 'spread_shot':
            self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
            pygame.draw.circle(self.image, NEON_PURPLE, (12, 12), 12)
            pygame.draw.circle(self.image, WHITE, (12, 12), 8, 2)
            # 3 dots in triangle
            pygame.draw.circle(self.image, WHITE, (12, 6), 2)
            pygame.draw.circle(self.image, WHITE, (6, 16), 2)
            pygame.draw.circle(self.image, WHITE, (18, 16), 2)
        elif power_type == 'rapid_fire':
            self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
            pygame.draw.rect(self.image, GOLD, (4, 4, 16, 16), border_radius=4)
            pygame.draw.polygon(self.image, WHITE, [(8, 8), (16, 12), (8, 16)]) # Play icon
        elif power_type == 'shield':
            self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
            pygame.draw.circle(self.image, NEON_BLUE, (12, 12), 12)
            pygame.draw.circle(self.image, WHITE, (12, 12), 10, 2)
            pygame.draw.line(self.image, WHITE, (6, 12), (18, 12), 2)
            pygame.draw.line(self.image, WHITE, (12, 6), (12, 18), 2)
        else:
            self.image = pygame.Surface((20, 20))
            self.image.fill(NEON_BLUE)
        self.rect = self.image.get_rect(center=(x, y))
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 120)

    def update(self, dt):
        self.position.y += self.velocity.y * dt
        self.rect.center = (int(self.position.x), int(self.position.y))
        if self.rect.top > VIRTUAL_HEIGHT:
            self.kill()

    def apply(self, player):
        if self.power_type == 'health':
            player.health = min(player.max_health, player.health + 25)
            return 50
        elif self.power_type == 'cola_burst':
            player.activate_powerup('cola_burst', 10.0)
            return 100
        elif self.power_type == 'spread_shot':
            player.activate_powerup('spread_shot', 10.0)
            return 100
        elif self.power_type == 'rapid_fire':
            player.activate_powerup('rapid_fire', 8.0)
            return 100
        elif self.power_type == 'shield':
            player.activate_powerup('shield', 5.0)
            return 150
        return 0
