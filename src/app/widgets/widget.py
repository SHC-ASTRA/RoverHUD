from abc import ABC, abstractmethod
from app import app
from typing import NamedTuple


class Size(NamedTuple):
    width: int
    height: int


class Position(NamedTuple):
    x: int = 0
    y: int = 0


class Widget(ABC):
    def __init__(self, size: Size, position: Position = Position()):
        self.width = size.width
        self.height = size.height
        self.x = position.x
        self.y = position.y

    def register_widget(self, app: app.App):
        self.register(app)

    def on_resize(self, app: app.App):
        return

    def update_widget(self, app: app.App):
        self.update(app)

    @abstractmethod
    def register(self, app: app.App):
        return NotImplementedError()

    def calculate_resize(self):
        self.size.calculate()

    @abstractmethod
    def update(self, app: app.App):
        return NotImplementedError()
