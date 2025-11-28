class SceneManager:
    def __init__(self, engine):
        self.engine = engine
        self.scenes = {}
        self.current_scene = None
        self.running = True

    def add_scene(self, name, scene_class):
        self.scenes[name] = scene_class

    def change_scene(self, name, **kwargs):
        if name in self.scenes:
            self.current_scene = self.scenes[name](self)
            if hasattr(self.current_scene, 'setup') and kwargs:
                self.current_scene.setup(**kwargs)

    def quit_game(self):
        self.running = False

    def process_input(self, events):
        if self.current_scene:
            self.current_scene.process_input(events)

    def update(self, dt):
        if self.current_scene:
            self.current_scene.update(dt)

    def draw(self, screen):
        if self.current_scene:
            self.current_scene.draw(screen)
