import pygame
import random
from src.scenes.base_scene import Scene
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.entities.boss import Boss
from src.entities.powerup import PowerUp
from src.utils.constants import *
from src.utils.assets import AssetManager
from src.core.wave_manager import WaveManager
from src.core.level_manager import LevelManager
from src.core.game_state import GameState
from src.core.vfx_manager import ParticlePool, ScreenShake
from src.ui.components import ProgressBar, Label

class SpaceShooterScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        
        self.player = Player([self.all_sprites], [self.all_sprites, self.projectiles])
        self.exit_scene = "map"
        
        self.level_manager = LevelManager()
        self.game_state = GameState()
        self.current_level = 1
        self.current_difficulty = "easy"
        self.boss = None
        self.boss_spawned = False
        self.level_complete = False
        
        self.wave_manager = WaveManager(self)
        self.score = 0
        self.coins_collected = 0
        self.combo = 0
        self.combo_timer = 0
        self.font_hud = AssetManager().fonts['hud']
        
        # VFX Systems
        self.particle_pool = ParticlePool()
        self.screen_shake = ScreenShake()
        
        # UI Components
        self.health_bar = ProgressBar(20, VIRTUAL_HEIGHT - 60, 300, 30, 100)
        self.boss_health_bar = ProgressBar(VIRTUAL_WIDTH // 2 - 200, 50, 400, 20, 1000, color=RED)
        self.score_label = Label(20, 20, "Score: 0", self.font_hud, GOLD)
        self.level_label = Label(VIRTUAL_WIDTH - 150, 20, "Level 1", self.font_hud, WHITE)
        self.zone_label = Label(VIRTUAL_WIDTH // 2 - 100, VIRTUAL_HEIGHT // 2 - 50, "", AssetManager().fonts['title'], WHITE)
        self.show_zone_timer = 0
        
        # Background
        self.stars = []
        self.bg_color = BLACK

    def setup(self, level=1, difficulty="easy"):
        self.current_level = level
        self.current_difficulty = difficulty
        self.config = self.level_manager.get_level_config(level, difficulty)
        
        # Theme Setup
        self.bg_color = self.config.get("bg_color", BLACK)
        star_color = self.config.get("star_color", WHITE)
        
        # Generate stars
        self.stars = []
        for _ in range(100):
            self.stars.append({
                'pos': [random.randint(0, VIRTUAL_WIDTH), random.randint(0, VIRTUAL_HEIGHT)],
                'speed': random.randint(20, 100),
                'size': random.randint(1, 3),
                'color': star_color
            })
            
        # Zone Name
        self.zone_label.set_text(self.config.get("name", "Unknown Sector"))
        self.show_zone_timer = 3.0
        
        # Reset state
        self.score = 0
        self.coins_collected = 0
        self.player.update_stats() # Refresh stats from GameState (XP/Level)
        self.boss = None
        self.boss_spawned = False
        self.level_complete = False
        self.level_complete_timer = 0
        
        # Clear groups
        self.enemies.empty()
        self.projectiles.empty()
        self.enemy_projectiles.empty()
        self.powerups.empty()
        # Re-add player to all_sprites if needed, but usually we just clear enemies
        for sprite in self.all_sprites:
            if sprite != self.player:
                sprite.kill()
        
        # Spawn Companions
        from src.entities.companion import Companion
        unlocked_companions = self.game_state.data.get("unlocked_companions", [])
        # For testing, let's give a companion if level > 1 or if unlocked
        if "sprite_bot" in unlocked_companions or self.current_level > 1: # Free trial at level 2
             Companion([self.all_sprites], [self.all_sprites, self.projectiles], self.player, "sprite")
                
        self.level_label.set_text(f"Level {level} - {difficulty.upper()}")
        
        # Configure wave manager (simplified for now)
        # In a real implementation, WaveManager would take the config
        
    def process_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.manager.change_scene(self.exit_scene)

    def update(self, dt):
        # Update background stars
        for star in self.stars:
            star['pos'][1] += star['speed'] * dt
            if star['pos'][1] > VIRTUAL_HEIGHT:
                star['pos'][1] = 0
                star['pos'][0] = random.randint(0, VIRTUAL_WIDTH)

        # Update zone label timer
        if self.show_zone_timer > 0:
            self.show_zone_timer -= dt

        self.all_sprites.update(dt)
        self.particle_pool.update(dt)
        self.screen_shake.update(dt)
        
        if self.level_complete:
            self.level_complete_timer -= dt
            if self.level_complete_timer <= 0:
                self.manager.change_scene("game_over", result="victory", score=self.score, coins=self.coins_collected)
            return

        # Spawn Boss Logic
        # For simplicity, spawn boss after score > 1000 or some condition
        # Let's say after killing X enemies
        if not self.boss_spawned and self.score >= 500 * self.current_level: # Simple trigger
            self.spawn_boss()
            
        if self.boss:
            self.boss_health_bar.set_value(self.boss.health)
            if self.boss.health <= 0:
                self.handle_level_complete()
        else:
            self.wave_manager.update(dt)
        
        # Update combo timer
        if self.combo_timer > 0:
            self.combo_timer -= dt
        else:
            self.combo = 0
        
        # Collisions - Projectiles hit Enemies
        hits = pygame.sprite.groupcollide(self.enemies, self.projectiles, True, True)
        for hit in hits:
            score_gain = hit.score_value * (1 + self.combo * 0.1)
            self.score += int(score_gain)
            self.combo += 1
            self.combo_timer = 2.0
            
            self.particle_pool.emit(hit.rect.centerx, hit.rect.centery, GREEN, 15, 
                                   velocity_range=(-4, 4), life_range=(15, 30))
            self.screen_shake.add_trauma(0.2)
            
            # XP & Coins
            self.game_state.add_xp(10)
            coin_amount = random.randint(1, 5)
            self.game_state.add_coins(coin_amount)
            self.coins_collected += coin_amount
            
            # Rudolph (basic enemy) drops Powerups
            if getattr(hit, 'enemy_type', '') == 'basic':
                roll = random.random()
                if roll < 0.1:
                    PowerUp([self.all_sprites, self.powerups], hit.rect.centerx, hit.rect.centery, 'cola_burst')
                elif roll < 0.2:
                    PowerUp([self.all_sprites, self.powerups], hit.rect.centerx, hit.rect.centery, 'spread_shot')
                elif roll < 0.3:
                    PowerUp([self.all_sprites, self.powerups], hit.rect.centerx, hit.rect.centery, 'rapid_fire')
                elif roll < 0.35:
                    PowerUp([self.all_sprites, self.powerups], hit.rect.centerx, hit.rect.centery, 'shield')
            elif random.random() < POWERUP_CHANCE:
                PowerUp([self.all_sprites, self.powerups], hit.rect.centerx, hit.rect.centery, 'health')
                
        # Projectiles hit Boss
        if self.boss:
            boss_hits = pygame.sprite.spritecollide(self.boss, self.projectiles, True)
            for p in boss_hits:
                damage = self.player.damage_mult * 10 # Base damage 10
                self.boss.health -= damage
                self.particle_pool.emit(p.rect.centerx, p.rect.centery, RED, 5)
                if self.boss.health <= 0:
                    self.boss.kill()
                    self.boss = None
                    
                    # Boss Explosion
                    for _ in range(100):
                        self.particle_pool.emit(p.rect.centerx, p.rect.centery, COKE_RED, 20, velocity_range=(-20, 20), life_range=(40, 80))
                        self.particle_pool.emit(p.rect.centerx, p.rect.centery, GOLD, 10, velocity_range=(-15, 15), life_range=(40, 80))
                    self.screen_shake.add_trauma(1.0)
                    
                    self.handle_level_complete()
                    break
            
        # Enemies hit Player
        hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
        if hits:
            damage = 10 * len(hits)
            self.player.health -= damage
            self.combo = 0
            self.particle_pool.emit(self.player.rect.centerx, self.player.rect.centery, 
                                   RED, 20, velocity_range=(-5, 5))
            self.screen_shake.add_trauma(0.5)
            
            if self.player.health <= 0:
                self.manager.change_scene("game_over", result="defeat", score=self.score, coins=self.coins_collected)
                
        # Enemy Projectiles hit Player (Boss Pepsi)
        p_hits = pygame.sprite.spritecollide(self.player, self.enemy_projectiles, True)
        for p in p_hits:
            damage = p.damage if hasattr(p, 'damage') else 10
            self.player.health -= damage
            self.particle_pool.emit(self.player.rect.centerx, self.player.rect.centery, BLUE, 10)
            self.screen_shake.add_trauma(0.3)
            
            if getattr(p, 'p_type', '') == 'snowball':
                self.player.freeze(1.0)
                
            if self.player.health <= 0:
                self.manager.change_scene("game_over", result="defeat", score=self.score, coins=self.coins_collected)

        # Powerup collection
        power_hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for powerup in power_hits:
            bonus = powerup.apply(self.player)
            self.score += bonus
            self.particle_pool.emit(powerup.rect.centerx, powerup.rect.centery, 
                                   NEON_BLUE, 10)
        
        # Update UI
        self.health_bar.set_value(self.player.health)
        self.health_bar.update(dt)
        self.score_label.set_text(f"Score: {self.score}")
        if self.boss:
            self.boss_health_bar.update(dt)

    def spawn_boss(self):
        self.boss_spawned = True
        # Clear existing enemies
        for e in self.enemies:
            e.kill()
        
        self.boss = Boss([self.all_sprites], [self.all_sprites, self.enemy_projectiles], 
                        self.player, self.current_level, self.current_difficulty)
        self.boss_health_bar.max_value = self.boss.max_health
        self.boss_health_bar.set_value(self.boss.health)

    def handle_level_complete(self):
        self.level_complete = True
        self.game_state.complete_level(self.current_level, self.current_difficulty)
        self.level_complete_timer = 3.0 # 3 seconds animation
        
        # Explosion Center
        center_x = self.boss.rect.centerx if self.boss else self.player.rect.centerx
        center_y = self.boss.rect.centery if self.boss else self.player.rect.centery
        
        # Snap effect (Particles) - Massive Explosion
        for _ in range(100):
            self.particle_pool.emit(center_x, center_y, RED, 15, velocity_range=(-15, 15), life_range=(40, 80))
            self.particle_pool.emit(center_x, center_y, GOLD, 10, velocity_range=(-15, 15), life_range=(40, 80))
            self.particle_pool.emit(center_x, center_y, WHITE, 8, velocity_range=(-15, 15), life_range=(40, 80))
            self.particle_pool.emit(center_x, center_y, NEON_BLUE, 12, velocity_range=(-15, 15), life_range=(40, 80))
            
        self.screen_shake.add_trauma(1.0) # Massive shake

    def draw(self, screen):
        # Apply screen shake
        shake_x, shake_y = self.screen_shake.get_offset()
        
        # Background with stars
        screen.fill(self.bg_color)
        
        # Draw stars
        for star in self.stars:
            pygame.draw.circle(screen, star['color'], (int(star['pos'][0]), int(star['pos'][1])), star['size'])
        
        # Draw sprites with shake
        for sprite in self.all_sprites:
            screen.blit(sprite.image, (sprite.rect.x + shake_x, sprite.rect.y + shake_y))
            
        # Draw Boss Laser
        if self.boss and self.boss.state in ["laser_charge", "laser_fire"]:
            laser_rect = pygame.Rect(self.boss.rect.centerx - self.boss.laser_width // 2, 
                                   self.boss.rect.bottom, 
                                   self.boss.laser_width, 
                                   VIRTUAL_HEIGHT - self.boss.rect.bottom)
            
            if self.boss.state == "laser_charge":
                # Warning line
                pygame.draw.rect(screen, (255, 0, 0, 100), laser_rect) # Transparent red not supported directly in draw.rect without surface
                # Use surface for transparency
                s = pygame.Surface((laser_rect.width, laser_rect.height), pygame.SRCALPHA)
                s.fill((255, 0, 0, 100))
                screen.blit(s, laser_rect.topleft)
            else:
                # Full beam
                pygame.draw.rect(screen, NEON_BLUE, laser_rect)
                pygame.draw.rect(screen, WHITE, laser_rect, 4)
                
                # Check collision with player
                if laser_rect.colliderect(self.player.rect):
                    self.player.health -= 1 # Rapid damage
                    self.screen_shake.add_trauma(0.1)
                    self.particle_pool.emit(self.player.rect.centerx, self.player.rect.centery, RED, 2)
                    if self.player.health <= 0:
                        self.manager.change_scene("game_over", result="defeat", score=self.score, coins=self.coins_collected)
        
        # Draw particles
        self.particle_pool.draw(screen)
        
        # UI Layer
        self.score_label.draw(screen)
        self.health_bar.draw(screen)
        self.level_label.draw(screen)
        
        # XP / Coins Display
        xp_text = self.font_hud.render(f"XP: {self.game_state.data.get('xp', 0)} | Lvl: {self.game_state.data.get('level', 1)}", True, NEON_PURPLE)
        screen.blit(xp_text, (20, 60))
        coin_text = self.font_hud.render(f"Coins: {self.game_state.data.get('coins', 0)}", True, GOLD)
        screen.blit(coin_text, (20, 90))
        
        # Draw Zone Name
        if self.show_zone_timer > 0:
            # Fade out effect could be added here, but for now just draw
            self.zone_label.draw(screen)
        
        if self.boss:
            self.boss_health_bar.draw(screen)
        
        # Wave info
        wave_surf = self.font_hud.render(f"Wave: {self.wave_manager.wave}", True, GOLD)
        screen.blit(wave_surf, (VIRTUAL_WIDTH // 2 - 70, 20))
        
        # Combo display
        if self.combo > 1:
            combo_text = self.font_hud.render(f"COMBO x{self.combo}!", True, NEON_PINK)
            combo_rect = combo_text.get_rect(center=(VIRTUAL_WIDTH // 2, 80))
            screen.blit(combo_text, combo_rect)
        
        # Controls hint
        hint = self.font_hud.render("ESC: Exit | Arrow/WASD: Move | Space/Z: Fire", True, WHITE)
        screen.blit(hint, (20, VIRTUAL_HEIGHT - 30))
