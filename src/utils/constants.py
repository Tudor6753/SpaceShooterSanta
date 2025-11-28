import pygame

# Virtual Resolution (16:9 aspect ratio base)
VIRTUAL_WIDTH = 1920
VIRTUAL_HEIGHT = 1080
ASPECT_RATIO = 16 / 9

# Display
FPS = 144  # Unlocked frame rate for smooth gameplay
TITLE = "Space Shooter Santa: Galactic Justice"
MIN_WIDTH = 1280
MIN_HEIGHT = 720

# Colors
BLACK = (10, 10, 20)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
COKE_RED = (244, 0, 9)
GOLD = (255, 215, 0)
NEON_BLUE = (0, 255, 255)
NEON_PURPLE = (255, 0, 255)
NEON_GREEN = (0, 255, 100)
NEON_PINK = (255, 20, 147)

# Layers
LAYER_BACKGROUND = 0
LAYER_PARTICLES = 1
LAYER_ENEMIES = 2
LAYER_PLAYER = 3
LAYER_PROJECTILES = 4
LAYER_EFFECTS = 5
LAYER_UI = 6

# Gameplay Balance
PLAYER_SPEED = 480  # pixels per second at virtual res
BULLET_SPEED = 720
ENEMY_SPAWN_RATE = 1000  # ms
POWERUP_CHANCE = 0.20

# Performance
PARTICLE_POOL_SIZE = 500
MAX_ENEMIES = 50
MAX_PROJECTILES = 100
