import random
import math
import pygame
from src.entities.entity import Entity
from src.utils.constants import *
from src.utils.assets import AssetManager

class DogTreat(Entity):
    def __init__(self, groups):
        super().__init__(groups, LAYER_PARTICLES)
        self.image = AssetManager().images['dog_treat']
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(random.randint(60, VIRTUAL_WIDTH - 60),
                                            random.randint(60, VIRTUAL_HEIGHT - 60))
        self.rect.center = self.position
        self.float_timer = random.uniform(0, 6.28)
        self.scale_timer = 0

    def update(self, dt):
        self.float_timer += dt * 5
        self.scale_timer += dt * 3
        offset_y = math.sin(self.float_timer) * 8
        self.rect.centery = int(self.position.y + offset_y)
