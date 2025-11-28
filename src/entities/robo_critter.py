import random
import pygame
from src.entities.entity import Entity
from src.utils.constants import *
from src.utils.assets import AssetManager

class RoboCritter(Entity):
    def __init__(self, groups):
        super().__init__(groups, LAYER_ENEMIES)
        self.image = AssetManager().images['robo_critter']
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(random.randint(60, VIRTUAL_WIDTH - 60),
                                            random.randint(60, VIRTUAL_HEIGHT // 2))
        self.rect.center = self.position
        self.velocity = pygame.math.Vector2(random.choice([-240, 240]), random.uniform(-60, 60))
        self.health = 1

    def update(self, dt):
        self.position += self.velocity * dt
        if self.position.x <= 40 or self.position.x >= VIRTUAL_WIDTH - 40:
            self.velocity.x *= -1
        if self.position.y <= 40 or self.position.y >= VIRTUAL_HEIGHT - 40:
            self.velocity.y *= -1
        self.rect.center = (int(self.position.x), int(self.position.y))