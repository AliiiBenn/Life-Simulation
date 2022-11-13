from typing import Any
import pygame as py

from foods import Food

class Vision:
    def __init__(self, x : int, y : int, width : int, height : int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.rect = py.Rect(self.x, self.y, self.width, self.height)
        
        self.visible_foods : list[Food] = []
        
    def update(self, screen : py.surface.Surface) -> None:
        self.create(screen)
        self.update_rect(self.rect)
        self.draw_visible_foods_lines(screen)
        
    def create(self, screen : py.surface.Surface) -> py.rect.Rect:
        return py.draw.rect(screen, (255, 0, 0), self.rect, 1)
        
    def update_rect(self, animal_rect : py.rect.Rect) -> None:
        self.rect.x = animal_rect.centerx - self.width // 2
        self.rect.y = animal_rect.centery - self.height // 2
        
    def is_food_visible(self, food : Food) -> bool:
        return self.rect.collidepoint(food.rect.center)
        
    def check_visible_foods(self, foods : list[Food]) -> list[Food] | list[Any]:
        visible_foods : list[Food] | list[Any] = []
        for food in foods:
            if self.is_food_visible(food):
                visible_foods.append(food)
        return visible_foods

    def draw_visible_foods_lines(self, screen : py.surface.Surface) -> None:
        for food in self.visible_foods:
            py.draw.line(screen, (255, 255, 255), self.rect.center, food.rect.center, 1)