import pygame
from src.entities.entity import Entity
from src.entities.projectile import Projectile
from src.utils.constants import *
from src.utils.assets import AssetManager

class Player(Entity):
    def __init__(self, groups, projectile_groups):
        super().__init__(groups, LAYER_PLAYER)
        self.image = AssetManager().images['santa']
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT - 100)
        self.rect.center = self.position
        self.speed = PLAYER_SPEED
        self.projectile_groups = projectile_groups
        self.shoot_cooldown = 0
        self.health = 100
        self.max_health = 100
        self.control_mode = "keyboard"
        self.auto_fire = False
        self.frozen_timer = 0
        
        # Powerup Timers
        self.powerups = {
            "cola_burst": 0,
            "spread_shot": 0,
            "rapid_fire": 0,
            "shield": 0
        }
        
        # Load stats from GameState
        from src.core.game_state import GameState
        stats = GameState().get_player_stats()
        self.max_health += stats["health_bonus"]
        self.health = self.max_health
        self.damage_mult = stats["damage_mult"]
        
        # Load Skin
        skin = GameState().data.get("current_skin", "default")
        if skin != "default":
            # In a real app, load different asset. For now, tint or change
            pass

    def freeze(self, duration):
        if self.powerups["shield"] > 0:
            return # Immune
        self.frozen_timer = duration
        
    def activate_powerup(self, p_type, duration):
        self.powerups[p_type] = duration
        
    # Deprecated but kept for compatibility if called elsewhere
    def activate_cola_burst(self, duration):
        self.activate_powerup("cola_burst", duration)

    def set_control_mode(self, mode):
        self.control_mode = mode

    def set_auto_fire(self, enabled):
        self.auto_fire = enabled

    def _handle_keyboard(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -self.speed
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = self.speed
        else:
            self.velocity.x = 0
            
        # Vertical movement
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity.y = -self.speed
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity.y = self.speed
        else:
            self.velocity.y = 0

        return keys[pygame.K_SPACE] or keys[pygame.K_z] or pygame.mouse.get_pressed()[0]

    def _handle_pointer(self):
        from src.core.resolution_manager import ResolutionManager
        res_mgr = ResolutionManager()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        virtual_x, virtual_y = res_mgr.to_virtual(mouse_x, mouse_y)
        
        self.velocity.x = 0
        if virtual_x < self.position.x - 10:
            self.velocity.x = -self.speed
        elif virtual_x > self.position.x + 10:
            self.velocity.x = self.speed

        return pygame.mouse.get_pressed()[0]
        
    def update(self, dt):
        # Update powerup timers
        for p in self.powerups:
            if self.powerups[p] > 0:
                self.powerups[p] -= dt
                
        if self.frozen_timer > 0:
            self.frozen_timer -= dt
            return # Can't move or shoot
            
        super().update(dt)
        self.input()
        
        # Clamp position
        self.position.x = max(20, min(VIRTUAL_WIDTH - 20, self.position.x))
        self.position.y = max(20, min(VIRTUAL_HEIGHT - 20, self.position.y))
        self.rect.center = (int(self.position.x), int(self.position.y))
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt

    def input(self):
        if self.control_mode == "pointer":
            firing = self._handle_pointer()
        else:
            firing = self._handle_keyboard()

        # Fire rate logic
        base_cooldown = 0.33
        if self.powerups["rapid_fire"] > 0:
            base_cooldown = 0.15
            
        if (firing or self.auto_fire) and self.shoot_cooldown <= 0:
            self.shoot()
            self.shoot_cooldown = base_cooldown

    def shoot(self):
        # Determine shot pattern
        if self.powerups["cola_burst"] > 0:
            # Triple parallel
            Projectile(self.projectile_groups, self.rect.centerx, self.rect.top, -BULLET_SPEED)
            Projectile(self.projectile_groups, self.rect.centerx - 20, self.rect.top + 10, -BULLET_SPEED)
            Projectile(self.projectile_groups, self.rect.centerx + 20, self.rect.top + 10, -BULLET_SPEED)
        elif self.powerups["spread_shot"] > 0:
            # 5-way spread
            Projectile(self.projectile_groups, self.rect.centerx, self.rect.top, -BULLET_SPEED)
            Projectile(self.projectile_groups, self.rect.centerx, self.rect.top, -BULLET_SPEED * 0.9, speed_x=-100)
            Projectile(self.projectile_groups, self.rect.centerx, self.rect.top, -BULLET_SPEED * 0.9, speed_x=100)
            Projectile(self.projectile_groups, self.rect.centerx, self.rect.top, -BULLET_SPEED * 0.8, speed_x=-200)
            Projectile(self.projectile_groups, self.rect.centerx, self.rect.top, -BULLET_SPEED * 0.8, speed_x=200)
        else:
            Projectile(self.projectile_groups, self.rect.centerx, self.rect.top, -BULLET_SPEED)

    def update_stats(self):
        from src.core.game_state import GameState
        stats = GameState().get_player_stats()
        # Reset base max health then add bonus
        self.max_health = 100 + stats["health_bonus"]
        self.health = self.max_health
        self.damage_mult = stats["damage_mult"]
