import pygame as py


class Water:
    def __init__(self, x : int, y : int, size : int, quantity : int) -> None:
        self.x = x
        self.y = y
        self.size = size
        self.quantity = quantity
        
        self.COLOR = (16, 27, 194)
        
        self.rect = py.Rect(self.x, self.y, self.size * (self.quantity // 100), self.size * (self.quantity // 100))
        
    def update(self, screen : py.surface.Surface) -> None:
        self.create(screen)
        
    def create(self, screen : py.surface.Surface) -> None:
        py.draw.rect(screen, self.COLOR, self.rect, border_radius=90)
        
    def decrease_quantity(self, quantity : int) -> None:
        self.quantity -= quantity
        
    def is_empty(self) -> bool:
        return self.quantity <= 0