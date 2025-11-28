import pygame
import random
from src.entities.enemy import Enemy
from src.utils.constants import *

class WaveManager:
    def __init__(self, game_scene):
        self.game_scene = game_scene
        self.wave = 1
        self.enemies_spawned = 0
        self.enemies_to_spawn = 10
        self.spawn_timer = 0
        self.wave_in_progress = True
        self.wave_cooldown = 0

    def update(self, dt):
        if not self.wave_in_progress:
            self.wave_cooldown -= dt
            if self.wave_cooldown <= 0:
                self.start_next_wave()
            return

        self.spawn_timer += dt * 1000
        if self.spawn_timer >= ENEMY_SPAWN_RATE / (1 + (self.wave * 0.1)): # Spawn faster each wave
            self.spawn_timer = 0
            if self.enemies_spawned < self.enemies_to_spawn:
                self.spawn_enemy()
            elif len(self.game_scene.enemies) == 0:
                self.wave_complete()

    def spawn_enemy(self):
        # Difficulty scaling
        fast_chance = min(0.1 * self.wave, 0.8)
        enemy_type = 'fast' if random.random() < fast_chance else 'basic'
        
        Enemy([self.game_scene.all_sprites, self.game_scene.enemies], enemy_type)
        self.enemies_spawned += 1

    def wave_complete(self):
        self.wave_in_progress = False
        self.wave_cooldown = 3.0 # 3 seconds between waves
        print(f"Wave {self.wave} Complete!")

    def start_next_wave(self):
        self.wave += 1
        self.enemies_spawned = 0
        self.enemies_to_spawn = int(10 * (1.2 ** (self.wave - 1)))
        self.wave_in_progress = True
        print(f"Starting Wave {self.wave}")
