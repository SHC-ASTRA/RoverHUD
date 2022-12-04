"""GUI Application Code."""

import pyglet


class App(pyglet.window.Window):
    """Application window class."""

    def __init__(self):
        super().__init__(800, 600, fullscreen=False, vsync=True)

        self.widgets = []
        self.batches = {}
        self.subgroups = {}

        self.alive = True

    def on_draw(self):
        pass

    def on_close(self):
        self.alive = False

    def render(self):
        self.clear()

        self.flip()

    def run(self):
        while self.alive:
            self.render()

            _ = self.dispatch_events()
