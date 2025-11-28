import pygame
from src.scenes.base_scene import Scene
from src.utils.constants import *
from src.utils.assets import AssetManager
from src.ui.components import Button, Label
from src.core.game_state import GameState

class ShopScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.game_state = GameState()
        self.assets = AssetManager()
        self.font = self.assets.fonts['menu']
        self.title_font = self.assets.fonts['title']
        
        self.items = [
            {"id": "skin_robo", "type": "skin", "name": "Robo-Santa", "cost": 100, "desc": "Beep Boop Ho Ho Ho"},
            {"id": "skin_ninja", "type": "skin", "name": "Ninja Santa", "cost": 200, "desc": "Silent Night, Deadly Night"},
            {"id": "companion_sprite", "type": "companion", "name": "Sprite Bot", "cost": 150, "desc": "Shoots Lemon-Lime Lasers"},
            {"id": "upgrade_damage", "type": "upgrade", "name": "Damage Up", "cost": 50, "desc": "+10% Damage (Stackable)"},
            {"id": "upgrade_health", "type": "upgrade", "name": "Health Up", "cost": 50, "desc": "+10 Max Health (Stackable)"}
        ]
        
        self.buttons = []
        self.labels = []
        self.create_ui()
        
    def create_ui(self):
        self.buttons = []
        self.labels = []
        
        # Title
        self.labels.append(Label(VIRTUAL_WIDTH // 2 - 100, 30, "GALACTIC SHOP", self.title_font, GOLD))
        
        # Coins Display
        self.coin_label = Label(VIRTUAL_WIDTH - 200, 40, f"Coins: {self.game_state.data.get('coins', 0)}", self.assets.fonts['hud'], GOLD)
        
        # Back Button
        self.buttons.append(Button(50, 40, 100, 40, "BACK", self.font, lambda: self.manager.change_scene("menu")))
        
        # Item Grid
        start_x = 100
        start_y = 150
        padding = 20
        w = 250
        h = 120
        
        for i, item in enumerate(self.items):
            row = i // 2
            col = i % 2
            x = start_x + col * (w + padding + 50)
            y = start_y + row * (h + padding)
            
            self.create_item_card(x, y, w, h, item)

    def create_item_card(self, x, y, w, h, item):
        # Buy/Equip Button
        btn_text = "BUY"
        btn_color = GREEN
        action = lambda i=item: self.buy_item(i)
        
        is_owned = False
        is_equipped = False
        
        if item['type'] == 'skin':
            if item['id'] in self.game_state.data.get('unlocked_skins', []):
                is_owned = True
                if self.game_state.data.get('current_skin') == item['id']:
                    is_equipped = True
        elif item['type'] == 'companion':
            if item['id'] in self.game_state.data.get('unlocked_companions', []):
                is_owned = True
                if self.game_state.data.get('current_companion') == item['id']:
                    is_equipped = True
                    
        if is_equipped:
            btn_text = "ACTIVE"
            btn_color = (100, 100, 100)
            action = lambda: None
        elif is_owned:
            btn_text = "EQUIP"
            btn_color = NEON_BLUE
            action = lambda i=item: self.equip_item(i)
        elif item['type'] == 'upgrade':
            # Upgrades are always buyable
            pass
            
        btn = Button(x + w - 110, y + h - 50, 100, 40, btn_text, self.assets.fonts['hud'], action, bg_color=btn_color)
        self.buttons.append(btn)
        
        # Store item data for drawing
        item['rect'] = pygame.Rect(x, y, w, h)
        item['btn'] = btn

    def buy_item(self, item):
        cost = item['cost']
        coins = self.game_state.data.get('coins', 0)
        
        if coins >= cost:
            self.game_state.add_coins(-cost)
            
            if item['type'] == 'skin':
                skins = self.game_state.data.get('unlocked_skins', [])
                skins.append(item['id'])
                self.game_state.data['unlocked_skins'] = skins
                self.game_state.save_data()
            elif item['type'] == 'companion':
                comps = self.game_state.data.get('unlocked_companions', [])
                comps.append(item['id'])
                self.game_state.data['unlocked_companions'] = comps
                self.game_state.save_data()
            elif item['type'] == 'upgrade':
                upgrades = self.game_state.data.get('upgrades', {})
                if item['id'] == 'upgrade_damage':
                    upgrades['damage'] = upgrades.get('damage', 0) + 1
                elif item['id'] == 'upgrade_health':
                    upgrades['health'] = upgrades.get('health', 0) + 1
                self.game_state.data['upgrades'] = upgrades
                self.game_state.save_data()
                
            self.create_ui() # Refresh UI

    def equip_item(self, item):
        if item['type'] == 'skin':
            self.game_state.data['current_skin'] = item['id']
        elif item['type'] == 'companion':
            self.game_state.data['current_companion'] = item['id']
        self.game_state.save_data()
        self.create_ui()

    def update(self, dt):
        for btn in self.buttons:
            btn.update(dt)
        self.coin_label.set_text(f"Coins: {self.game_state.data.get('coins', 0)}")

    def draw(self, screen):
        screen.fill((20, 20, 40))
        
        for label in self.labels:
            label.draw(screen)
        self.coin_label.draw(screen)
            
        # Draw Item Cards
        for item in self.items:
            if 'rect' in item:
                rect = item['rect']
                pygame.draw.rect(screen, (40, 40, 60), rect, border_radius=10)
                pygame.draw.rect(screen, (100, 100, 120), rect, 2, border_radius=10)
                
                # Name
                name_surf = self.assets.fonts['hud'].render(item['name'], True, WHITE)
                screen.blit(name_surf, (rect.x + 10, rect.y + 10))
                
                # Desc
                desc_surf = pygame.font.SysFont("Arial", 16).render(item['desc'], True, (200, 200, 200))
                screen.blit(desc_surf, (rect.x + 10, rect.y + 40))
                
                # Cost
                cost_text = f"${item['cost']}"
                if item['type'] == 'upgrade':
                    upgrades = self.game_state.data.get('upgrades', {})
                    lvl = 0
                    if item['id'] == 'upgrade_damage': lvl = upgrades.get('damage', 0)
                    elif item['id'] == 'upgrade_health': lvl = upgrades.get('health', 0)
                    cost_text += f" (Lvl {lvl})"
                
                cost_surf = self.assets.fonts['hud'].render(cost_text, True, GOLD)
                screen.blit(cost_surf, (rect.x + 10, rect.y + 80))

        for btn in self.buttons:
            btn.draw(screen)

    def process_input(self, events):
        for event in events:
            for btn in self.buttons:
                btn.handle_event(event)
