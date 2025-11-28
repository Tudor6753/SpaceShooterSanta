import pygame
import random
from src.entities.entity import Entity
from src.utils.constants import *
from src.utils.assets import AssetManager

class Enemy(Entity):
    def __init__(self, groups, enemy_type='basic'):
        super().__init__(groups, LAYER_ENEMIES)
        self.enemy_type = enemy_type
        
        if enemy_type == 'basic':
            self.image = AssetManager().images['enemy_basic']
            self.speed = random.uniform(120, 250)
            self.health = 1
            self.score_value = 100
        elif enemy_type == 'fast':
            self.image = AssetManager().images['enemy_fast']
            self.speed = random.uniform(300, 450)
            self.health = 1
            self.score_value = 150
            
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(
            random.randint(40, VIRTUAL_WIDTH - 40),
            random.randint(-200, -80)
        )
        self.velocity = pygame.math.Vector2(random.uniform(-60, 60), self.speed)
        self.rect.center = self.position

    def update(self, dt):
        super().update(dt)
        
        # Wrap around or kill
        if self.rect.top > VIRTUAL_HEIGHT + 20:
            self.kill()
