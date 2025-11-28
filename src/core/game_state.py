import json
import os

SAVE_FILE = "save_data.json"

class GameState:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameState, cls).__new__(cls)
            cls._instance.load_data()
        return cls._instance
    
    def load_data(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, 'r') as f:
                    self.data = json.load(f)
            except:
                self.create_default_data()
        else:
            self.create_default_data()
            
    def create_default_data(self):
        self.data = {
            "unlocked_level": 1,
            "level_difficulties": {
                "1": ["easy"] # Level 1 starts with easy unlocked
            },
            "high_scores": {},
            "coins": 0,
            "xp": 0,
            "level": 1,
            "unlocked_skins": ["default"],
            "current_skin": "default",
            "unlocked_companions": [],
            "current_companion": None,
            "ammo_design": "default"
        }
        self.save_data()
        
    def add_coins(self, amount):
        self.data["coins"] = self.data.get("coins", 0) + amount
        self.save_data()
        
    def add_xp(self, amount):
        self.data["xp"] = self.data.get("xp", 0) + amount
        # Simple level up logic: Level * 1000 XP needed
        needed = self.data.get("level", 1) * 1000
        if self.data["xp"] >= needed:
            self.data["xp"] -= needed
            self.data["level"] = self.data.get("level", 1) + 1
        self.save_data()
        
    def get_player_stats(self):
        lvl = self.data.get("level", 1)
        return {
            "damage_mult": 1.0 + (lvl - 1) * 0.1,
            "health_bonus": (lvl - 1) * 10
        }

    def save_data(self):
        with open(SAVE_FILE, 'w') as f:
            json.dump(self.data, f)
            
    def is_level_unlocked(self, level):
        return level <= self.data["unlocked_level"]
        
    def is_difficulty_unlocked(self, level, difficulty):
        # Logic: 
        # Level 1: Easy unlocked.
        # To unlock Medium, beat Easy.
        # To unlock Hard, beat Medium.
        # To unlock Extreme, beat Hard.
        
        # If level is not in dict, it's locked (unless it's level 1 easy which is default)
        if str(level) not in self.data["level_difficulties"]:
            return False
            
        return difficulty in self.data["level_difficulties"][str(level)]
        
    def complete_level(self, level, difficulty):
        # Unlock next difficulty for this level
        diff_order = ["easy", "medium", "hard", "extreme"]
        try:
            idx = diff_order.index(difficulty)
            if idx < len(diff_order) - 1:
                next_diff = diff_order[idx + 1]
                if str(level) not in self.data["level_difficulties"]:
                    self.data["level_difficulties"][str(level)] = []
                if next_diff not in self.data["level_difficulties"][str(level)]:
                    self.data["level_difficulties"][str(level)].append(next_diff)
        except ValueError:
            pass
            
        # Unlock next level (easy) if we beat any difficulty of current level? 
        # Or maybe require beating at least Easy to unlock next level?
        # Let's say beating Easy unlocks next level Easy.
        if difficulty == "easy":
            if level == self.data["unlocked_level"]:
                self.data["unlocked_level"] += 1
                next_level_str = str(level + 1)
                if next_level_str not in self.data["level_difficulties"]:
                    self.data["level_difficulties"][next_level_str] = ["easy"]
                    
        self.save_data()
