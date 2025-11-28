import pygame
import random
import math
from src.entities.entity import Entity
from src.entities.projectile import Projectile
from src.utils.constants import *
from src.utils.assets import AssetManager

class Boss(Entity):
    def __init__(self, groups, projectile_groups, player, level=1, difficulty="easy"):
        super().__init__(groups, LAYER_ENEMIES)
        self.player = player
        self.image = AssetManager().images['boss_truck']
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(VIRTUAL_WIDTH // 2, -150)
        self.rect.center = self.position
        
        self.projectile_groups = projectile_groups
        
        # Stats based on level and difficulty
        diff_mult = {"easy": 1.0, "medium": 1.5, "hard": 2.0, "extreme": 3.0}
        mult = diff_mult.get(difficulty, 1.0)
        
        self.max_health = 1000 * (1 + level * 0.2) * mult
        self.health = self.max_health
        self.speed = 100 * (1 + level * 0.05) * mult
        
        self.state = "entering" # entering, idle, attacking, moving, laser_charge
        self.state_timer = 0
        self.target_x = VIRTUAL_WIDTH // 2
        
        self.shoot_timer = 0
        self.shoot_delay = max(0.5, 2.0 - (level * 0.05)) / mult
        
        # Laser properties
        self.laser_charging = False
        self.laser_width = 0

    def update(self, dt):
        if self.state == "entering":
            self.position.y += 100 * dt
            if self.position.y >= 150:
                self.position.y = 150
                self.state = "idle"
                self.state_timer = 2.0
                
        elif self.state == "idle":
            self.state_timer -= dt
            if self.state_timer <= 0:
                self.state = random.choice(["moving", "attacking", "laser_charge"])
                self.state_timer = random.uniform(2.0, 4.0)
                if self.state == "moving":
                    self.target_x = random.randint(150, VIRTUAL_WIDTH - 150)
                elif self.state == "laser_charge":
                    self.state_timer = 2.0 # Charge time
                    self.laser_width = 2
                    
        elif self.state == "moving":
            direction = 1 if self.target_x > self.position.x else -1
            self.position.x += self.speed * direction * dt
            
            if abs(self.position.x - self.target_x) < 10:
                self.state = "idle"
                self.state_timer = 1.0
                
        elif self.state == "attacking":
            self.shoot_timer -= dt
            if self.shoot_timer <= 0:
                self.shoot()
                self.shoot_timer = self.shoot_delay
                
            self.state_timer -= dt
            if self.state_timer <= 0:
                self.state = "idle"
                self.state_timer = 2.0
                
        elif self.state == "laser_charge":
            self.state_timer -= dt
            self.laser_width += dt * 20 # Grow warning line
            if self.state_timer <= 0:
                self.state = "laser_fire"
                self.state_timer = 1.5 # Fire duration
                self.laser_width = 60 # Full beam width
                
        elif self.state == "laser_fire":
            self.state_timer -= dt
            # Damage logic handled in GameScene or here if we had reference to player group
            # For now, we just manage state. GameScene needs to check for collision with the beam rect
            if self.state_timer <= 0:
                self.state = "idle"
                self.state_timer = 2.0
                self.laser_width = 0
                
        # Enrage Phase (Health < 50%)
        if self.health < self.max_health * 0.5:
            # Simple speed up logic, careful not to compound every frame
            pass 
                
        self.rect.center = round(self.position.x), round(self.position.y)
        
    def shoot(self):
        # Shoot 3 Pepsi bottles
        offsets = [-40, 0, 40]
        
        # Enrage Pattern: 5 shots
        if self.health < self.max_health * 0.5:
            offsets = [-60, -30, 0, 30, 60]
            
        for offset in offsets:
            # 40% slower speed (400 * 0.6 = 240)
            p = Projectile(self.projectile_groups, self.rect.centerx + offset, self.rect.bottom, 240, damage=15, p_type='pepsi')
            # Make them bigger as requested
            p.image = pygame.transform.scale(p.image, (int(p.rect.width * 1.5), int(p.rect.height * 1.5)))
            p.rect = p.image.get_rect(center=p.rect.center)
