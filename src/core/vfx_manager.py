import random
import pygame
from src.utils.constants import *

class ParticlePool:
    """Object pool for efficient particle management"""
    def __init__(self, max_particles=PARTICLE_POOL_SIZE):
        self.particles = []
        self.max_particles = max_particles
    
    def emit(self, x, y, color, count=10, velocity_range=(-3, 3), life_range=(20, 40), size_range=(2, 5)):
        """Emit particles at a position"""
        for _ in range(count):
            if len(self.particles) >= self.max_particles:
                break
            particle = {
                'pos': [float(x), float(y)],
                'vel': [random.uniform(*velocity_range), random.uniform(*velocity_range)],
                'life': random.randint(*life_range),
                'max_life': random.randint(*life_range),
                'color': color,
                'size': random.uniform(*size_range)
            }
            self.particles.append(particle)
    
    def update(self, dt):
        """Update all active particles"""
        for particle in self.particles[:]:
            particle['pos'][0] += particle['vel'][0]
            particle['pos'][1] += particle['vel'][1]
            particle['life'] -= 1
            particle['size'] = max(0, particle['size'] - 0.05)
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw(self, surface):
        """Render all particles"""
        for particle in self.particles:
            alpha_factor = max(0.0, min(1.0, particle['life'] / particle['max_life']))
            
            # Ensure color values are valid (0-255)
            try:
                color = tuple(max(0, min(255, int(c * alpha_factor))) for c in particle['color'])
                size = max(1, int(particle['size']))
                pygame.draw.circle(surface, color, (int(particle['pos'][0]), int(particle['pos'][1])), size)
            except (ValueError, TypeError):
                continue
    
    def clear(self):
        """Clear all particles"""
        self.particles.clear()


class ScreenShake:
    """Camera shake effect system"""
    def __init__(self):
        self.trauma = 0.0
        self.trauma_decay = 1.5
        self.max_offset = 15
    
    def add_trauma(self, amount):
        """Add screen shake (0.0 to 1.0)"""
        self.trauma = min(1.0, self.trauma + amount)
    
    def update(self, dt):
        """Update shake intensity"""
        self.trauma = max(0, self.trauma - self.trauma_decay * dt)
    
    def get_offset(self):
        """Get current shake offset"""
        if self.trauma <= 0:
            return (0, 0)
        shake = self.trauma ** 2
        offset_x = random.uniform(-1, 1) * self.max_offset * shake
        offset_y = random.uniform(-1, 1) * self.max_offset * shake
        return (int(offset_x), int(offset_y))


class TrailEffect:
    """Motion trail effect for fast-moving objects"""
    def __init__(self, max_length=8):
        self.positions = []
        self.max_length = max_length
    
    def add_position(self, pos):
        """Add a position to the trail"""
        self.positions.append(pos)
        if len(self.positions) > self.max_length:
            self.positions.pop(0)
    
    def draw(self, surface, color):
        """Draw the trail with fading effect"""
        if len(self.positions) < 2:
            return
        for i, pos in enumerate(self.positions[:-1]):
            alpha = int(255 * (i / len(self.positions)))
            fade_color = (*color[:3], alpha)
            next_pos = self.positions[i + 1]
            pygame.draw.line(surface, fade_color, pos, next_pos, 2)
    
    def clear(self):
        """Clear the trail"""
        self.positions.clear()
