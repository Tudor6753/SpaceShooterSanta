import pygame
from src.entities.entity import Entity
from src.utils.constants import *
from src.utils.assets import AssetManager

class DogHunter(Entity):
    def __init__(self, groups):
        super().__init__(groups, LAYER_PLAYER)
        self.image = AssetManager().images['dog_hunter']
        self.rect = self.image.get_rect(center=(VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT // 2))
        self.position = pygame.math.Vector2(self.rect.center)
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 420
        self.energy = 100
        self.max_energy = 100

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.velocity.xy = (0, 0)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity.y = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity.y = self.speed

        # Normalize diagonal movement
        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize() * self.speed

        self.position += self.velocity * dt
        self.position.x = max(30, min(VIRTUAL_WIDTH - 30, self.position.x))
        self.position.y = max(30, min(VIRTUAL_HEIGHT - 30, self.position.y))
        self.rect.center = (int(self.position.x), int(self.position.y))
        self.energy = max(0, self.energy - 5 * dt)
