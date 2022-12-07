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
