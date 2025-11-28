import pygame
from src.utils.constants import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups=None, layer=LAYER_BACKGROUND):
        super().__init__()
        self.render_layer = layer
        self.image = pygame.Surface((32, 32))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(0, 0)
        self.velocity = pygame.math.Vector2(0, 0)
        self.active = True

        if groups:
            self.add_to_groups(groups)

    def add_to_groups(self, groups):
        if not isinstance(groups, (list, tuple, set)):
            groups = [groups]

        for group in groups:
            if isinstance(group, pygame.sprite.LayeredUpdates):
                group.add(self, layer=self.render_layer)
            else:
                group.add(self)

    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.center = round(self.position.x), round(self.position.y)
