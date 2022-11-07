import pygame as py


class Food:
    def __init__(self, size: int, color: tuple[int, int, int], x: int, y: int, life: int = 100) -> None:
        self.size = size
        self.color = color
        self.x = x
        self.y = y
        self.life = life

        self.rect = py.Rect(self.x, self.y, self.size, self.size)
        
    def create(self, screen : py.surface.Surface) -> None:
        py.draw.rect(screen, self.color, self.rect, border_radius=90)
        
    def remove_life(self, amount : int) -> None:
        self.life -= amount
        
    def is_completely_eaten(self) -> bool:
        return self.life <= 0
        
        
class Foods:
    def __init__(self) -> None:
        self.foods = []
        
    def add_food(self, food : Food) -> None:
        self.foods.append(food)
        
    def remove_food(self, food : Food) -> None:
        self.foods.remove(food)
        
    def update(self, screen : py.surface.Surface) -> None:
        for food in self.foods:
            food.create(screen)
            
            if food.is_completely_eaten():
                self.remove_food(food)