import pygame
from src.entities.entity import Entity
from src.utils.constants import *
from src.utils.assets import AssetManager

class Projectile(Entity):
    def __init__(self, groups, x, y, speed_y, damage=10, p_type='coke', target=None, speed_x=0):
        super().__init__(groups, LAYER_PROJECTILES)
        self.p_type = p_type
        self.damage = damage
        self.target = target
        self.homing_speed = 200 # Turn speed
        
        # Asset selection based on type
        assets = AssetManager()
        if p_type == 'coke':
            self.image = assets.images.get('projectile_coke', pygame.Surface((10, 20)))
        elif p_type == 'pepsi':
            self.image = assets.images.get('projectile_pepsi', pygame.Surface((12, 24)))
        elif p_type == 'snowball':
            # Snowball is just a small white circle if asset missing, but we have enemy_fast as snowball
            # Let's use a smaller version or just a white circle
            self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
            pygame.draw.circle(self.image, WHITE, (8, 8), 8)
        elif p_type == 'sprite_juice':
            self.image = assets.images.get('projectile_sprite_juice', pygame.Surface((10, 20)))
        else:
            self.image = pygame.Surface((8, 16))
            self.image.fill(NEON_BLUE)
            
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(speed_x, speed_y)
        self.rect.center = (x, y)
        
        # Trail / VFX properties
        self.emit_trail = True
        self.trail_timer = 0

    def update(self, dt):
        super().update(dt)
        
        # Homing Logic
        if self.target and self.target.alive():
            # Check if we passed the target (assuming target is below us for enemy projectiles)
            # If projectile is moving down (speed_y > 0) and is below target, stop homing
            # If projectile is moving up (speed_y < 0) and is above target, stop homing
            
            moving_down = self.velocity.y > 0
            passed = False
            if moving_down and self.position.y > self.target.rect.centery:
                passed = True
            elif not moving_down and self.position.y < self.target.rect.centery:
                passed = True
                
            if not passed:
                direction = pygame.math.Vector2(self.target.rect.center) - self.position
                if direction.length() > 0:
                    direction = direction.normalize()
                    # Steer velocity towards target
                    desired_velocity = direction * self.velocity.length()
                    steering = desired_velocity - self.velocity
                    # Limit steering
                    if steering.length() > self.homing_speed * dt:
                        steering = steering.normalize() * self.homing_speed * dt
                    self.velocity += steering
                    self.velocity = self.velocity.normalize() * self.velocity.length() # Keep speed constant

        self.position += self.velocity * dt
        self.rect.center = (int(self.position.x), int(self.position.y))
        
        # Bounds check using Virtual Resolution
        if (self.rect.bottom < -50 or 
            self.rect.top > VIRTUAL_HEIGHT + 50 or
            self.rect.right < -50 or
            self.rect.left > VIRTUAL_WIDTH + 50):
            self.kill()
