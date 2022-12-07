"""Application graphics helper."""
from abc import ABCMeta, abstractmethod
import pyglet
from pyglet.gl import glEnable, glDisable, GL_DEPTH_TEST, GL_CULL_FACE
from pyglet.math import Mat4, Vec3

NEAR = 0.1
FAR = 3000


class AppRenderLayer(pyglet.graphics.Batch, metaclass=ABCMeta):
    """Abstract class for render layers."""

    def __init__(self, height: int, width: int, fov: float):
        """
        Create a render layer.

        Args:
            height (int): canvas height
            width (int): canvas width
            fov (float): camera field of view

        """
        super().__init__()
        self.resize(width, height)
        self.fov = fov

    @abstractmethod
    def resize(self, width: int, height: int):
        """
        Resize render layer canvas.

        Args:
            width (int): width of new canvas
            height (int): height of new canvas

        """
        return NotImplementedError()

    @abstractmethod
    def render(self, window: pyglet.window.Window):
        """
        Render layer.

        Args:
            window (pyglet.window.Window): window doing the rendering

        """
        return NotImplementedError()


class Background2D(AppRenderLayer):
    """Render layer for 2D background layer."""

    def resize(self, width, height):
        """
        Resize render layer canvas.

        Args:
            width (int): width of new canvas
            height (int): height of new canvas

        """
        self.height = height
        self.width = width
        self.projection = Mat4.orthogonal_projection(0, width, 0, height, NEAR, FAR)
        self.view = Mat4.look_at(
            position=Vec3(0, 0, 5), target=Vec3(0, 0, 0), up=Vec3(0, 1, 0)
        )

    def render(self, window: pyglet.window.Window):
        """
        Draw the render layer.

        Args:
            window (pyglet.window.Window): window being used to render

        """
        # Set 2D Render Options
        glDisable(GL_DEPTH_TEST)
        window.projection = self.projection
        window.view = self.view

        # Dispatch draw call
        super().draw()


class Background3D(AppRenderLayer):
    """Render layer for 3D background layer."""

    def resize(self, width, height):
        """
        Resize render layer canvas.

        Args:
            width (int): width of new canvas
            height (int): height of new canvas

        """
        self.width = width
        self.height = height

        self.projection = Mat4.perspective_projection(
            (width / height), z_near=NEAR, z_far=FAR, fov=self.fov
        )
        self.view = Mat4.look_at(
            position=Vec3(0, 0, 5), target=Vec3(0, 0, 0), up=Vec3(0, 1, 0)
        )

    def render(self, window: pyglet.window.Window):
        """
        Draw the render layer.

        Args:
            window (pyglet.window.Window): window being used to render

        """
        # Set 3D Render Options
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        window.projection = self.projection
        window.view = self.view

        # Dispatch draw call
        super().draw()


class Foreground2D(AppRenderLayer):
    """Render layer for 2D foreground layer."""

    def resize(self, width, height):
        """
        Resize render layer canvas.

        Args:
            width (int): width of new canvas
            height (int): height of new canvas

        """
        self.height = height
        self.width = width
        self.projection = Mat4.orthogonal_projection(0, width, 0, height, NEAR, FAR)
        self.view = Mat4.look_at(
            position=Vec3(0, 0, 5), target=Vec3(0, 0, 0), up=Vec3(0, 1, 0)
        )

    def render(self, window: pyglet.window.Window):
        """
        Draw the render layer.

        Args:
            window (pyglet.window.Window): window being used to render

        """
        # Set 2D Render Options
        window.projection = self.projection
        window.view = self.view

        # Dispatch draw call
        super().draw()
