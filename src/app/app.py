"""GUI Application Code."""

import pyglet
from pyglet.math import Mat4
from app import graphics

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.widgets import widget


class App(pyglet.window.Window):
    """Application window class."""

    def __init__(self, width: int, height: int, widgets: "List[widget.Widget]"):
        """
        Initialize App class.

        Args:
            width (int): default width of application window
            height (int): default height of application window
            widgets (List[widget.Widget]): list of widgets to include in the app

        """
        super().__init__(width, height, fullscreen=False, vsync=True, resizable=True)
        self.projection = Mat4.perspective_projection(
            self.aspect_ratio, z_near=0.1, z_far=255
        )

        self.fov = 60

        self.Background2D = graphics.Background2D(
            width=width, height=height, fov=self.fov
        )
        self.Background3D = graphics.Background3D(
            width=width, height=height, fov=self.fov
        )
        self.Foreground2D = graphics.Foreground2D(
            width=width, height=height, fov=self.fov
        )

        self.alive = True

        self.widgets = widgets
        for w in self.widgets:
            w.register_widget(self)

    def on_close(self):
        """
        Event handler for on_close.

        ---
        Behavior: Marks self.alive flag False
        """
        self.alive = False

    def render(self):
        """
        Render method.

        ---
        Behavior: Clears the window. Draws all render layers in order. Flips the window to update.
        """
        self.clear()

        # Render 2D Background
        self.Background2D.render(self)

        # Render 3D Background
        self.Background3D.render(self)

        # Render 2D Foreground
        self.Foreground2D.render(self)

        # Render 3D Foreground

        self.flip()

    def update(self):
        """
        Update method.

        ---
        Behavior: Loops through self.widgets and updates each widget.
        """
        for w in self.widgets:
            w.update(self)

    def run(self):
        """
        Run method.

        ---
        Behavior: While self.alive flag is True, call update method and render method.
        Then dispatch event handlers.
        """
        while self.alive:
            self.update()
            self.render()

            _ = self.dispatch_events()
