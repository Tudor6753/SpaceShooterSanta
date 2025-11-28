import random
import pygame
from src.scenes.base_scene import Scene
from src.entities.dog_hunter import DogHunter
from src.entities.dog_treat import DogTreat
from src.entities.robo_critter import RoboCritter
from src.utils.constants import *
from src.utils.assets import AssetManager

class DogHuntScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.all_sprites = pygame.sprite.Group()
        self.treats = pygame.sprite.Group()
        self.critters = pygame.sprite.Group()
        self.dog = DogHunter([self.all_sprites])
        self.score = 0
        self.timer = 60.0
        self.exit_scene = "mode_select"
        self.font = AssetManager().fonts['hud']
        self.treat_timer = 0
        self.critter_timer = 0

    def process_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.manager.change_scene(self.exit_scene)

    def update(self, dt):
        self.all_sprites.update(dt)
        self.treats.update(dt)
        self.critters.update(dt)

        self.timer -= dt
        if self.timer <= 0 or self.dog.energy <= 0:
            self.manager.change_scene(self.exit_scene)
            return

        self.treat_timer += dt
        self.critter_timer += dt
        if self.treat_timer >= 1.5:
            self.treat_timer = 0
            DogTreat([self.all_sprites, self.treats])
        if self.critter_timer >= 3.0:
            self.critter_timer = 0
            RoboCritter([self.all_sprites, self.critters])

        treat_hits = pygame.sprite.spritecollide(self.dog, self.treats, True)
        for _ in treat_hits:
            self.score += 150
            self.dog.energy = min(100, self.dog.energy + 15)

        critter_hits = pygame.sprite.spritecollide(self.dog, self.critters, False)
        if critter_hits:
            self.dog.energy = max(0, self.dog.energy - 25 * dt * len(critter_hits))

    def draw(self, screen):
        screen.fill((15, 40, 30))
        
        # Draw grid pattern
        for x in range(0, VIRTUAL_WIDTH, 100):
            pygame.draw.line(screen, (25, 50, 40), (x, 0), (x, VIRTUAL_HEIGHT), 1)
        for y in range(0, VIRTUAL_HEIGHT, 100):
            pygame.draw.line(screen, (25, 50, 40), (0, y), (VIRTUAL_WIDTH, y), 1)
        
        self.all_sprites.draw(screen)
        self.treats.draw(screen)
        self.critters.draw(screen)

        # HUD
        score = self.font.render(f"Treats Collected: {self.score}", True, GOLD)
        timer = self.font.render(f"Time: {int(self.timer)}s", True, WHITE)
        energy = self.font.render(f"Energy: {int(self.dog.energy)}%", True, NEON_GREEN if self.dog.energy > 30 else RED)
        screen.blit(score, (30, 30))
        screen.blit(timer, (30, 70))
        screen.blit(energy, (30, 110))
        
        # Progress bar for energy
        from src.ui.components import ProgressBar
        energy_bar = ProgressBar(30, 150, 300, 25, self.dog.max_energy)
        energy_bar.set_value(self.dog.energy)
        energy_bar.color = NEON_GREEN if self.dog.energy > 30 else RED
        energy_bar.draw(screen)
        
        hint = self.font.render("ESC: Exit | Arrow/WASD: Move", True, WHITE)
        screen.blit(hint, (30, VIRTUAL_HEIGHT - 50))
