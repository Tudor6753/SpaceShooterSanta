from src.scenes.game_scene import SpaceShooterScene
from src.utils.constants import *

class AndroidSpaceScene(SpaceShooterScene):
    def __init__(self, manager):
        super().__init__(manager)
        self.player.set_control_mode("pointer")
        self.player.set_auto_fire(True)
        self.exit_scene = "mode_select"
        self.mobile_bonus = 0

    def update(self, dt):
        super().update(dt)
        self.mobile_bonus += dt * 25
        if self.mobile_bonus >= 1:
            self.score += int(self.mobile_bonus)
            self.mobile_bonus = 0

    def draw(self, screen):
        super().draw(screen)
        hint = self.font_hud.render("Hold mouse like touch to steer", True, NEON_PURPLE)
        screen.blit(hint, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 70))
