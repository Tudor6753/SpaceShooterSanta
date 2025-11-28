class LevelManager:
    def __init__(self):
        self.total_levels = 50
        
    def get_level_config(self, level, difficulty):
        diff_mult = {"easy": 1.0, "medium": 1.5, "hard": 2.0, "extreme": 3.0}
        mult = diff_mult.get(difficulty, 1.0)
        
        # Procedural generation of level data
        enemy_count = int((10 + level * 2) * mult)
        wave_count = 3 + (level // 5)
        
        config = {
            "level": level,
            "difficulty": difficulty,
            "enemy_count": enemy_count,
            "wave_count": wave_count,
            "enemy_hp_mult": (1 + level * 0.1) * mult,
            "enemy_speed_mult": (1 + level * 0.05) * mult,
            "boss_hp": 1000 * (1 + level * 0.2) * mult,
            "spawn_rate": max(0.5, 2.0 - (level * 0.02)) / mult
        }
        # Theme generation
        theme = self.get_theme(level)
        config.update(theme)
        
        return config

    def get_theme(self, level):
        if level <= 10:
            return {
                "name": "Frosty Frontier",
                "bg_color": (5, 10, 30), # Dark Blue
                "star_color": (200, 200, 255),
                "nebula_color": (0, 0, 50)
            }
        elif level <= 20:
            return {
                "name": "Candy Cane Nebula",
                "bg_color": (30, 5, 5), # Dark Red
                "star_color": (255, 200, 200),
                "nebula_color": (50, 0, 0)
            }
        elif level <= 30:
            return {
                "name": "Aurora Borealis",
                "bg_color": (5, 20, 10), # Dark Green
                "star_color": (200, 255, 200),
                "nebula_color": (0, 50, 20)
            }
        elif level <= 40:
            return {
                "name": "Deep Space Void",
                "bg_color": (0, 0, 0), # Black
                "star_color": (150, 150, 150),
                "nebula_color": (10, 10, 10)
            }
        else:
            return {
                "name": "The North Pole Core",
                "bg_color": (20, 20, 0), # Dark Gold
                "star_color": (255, 255, 200),
                "nebula_color": (50, 50, 0)
            }
