import math
import pygame as py
from enum import Enum
import random

from food import Food

class Direction(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)
    UP_LEFT = (-1, -1)
    UP_RIGHT = (1, -1)
    DOWN_LEFT = (-1, 1)
    DOWN_RIGHT = (1, 1)


class Animal:
    def __init__(self, 
                 size : int,
                 color : tuple[int, int, int],
                 x : int,
                 y : int,
                 speed : int = 1,
                 life : int = 100) -> None:
        self.size = size
        self.color = color
        self.x = x
        self.y = y
        self.speed = speed
        self.life = life
        
        self.rect = py.Rect(self.x, self.y, self.size, self.size)
        
        self.direction = self.choose_direction()
        self.direction_count = 0
        self.hunger = 200
        
        self.vision_scale = 6
        self.vision = py.Rect(self.rect.centerx, self.rect.centery, self.size * self.vision_scale, self.size * self.vision_scale)
        
        self.foods : list[Food] = []
        
    def __str__(self) -> str:
        return f"Animal: x={self.x}, y={self.y}, size={self.size}, color={self.color}, speed={self.speed}, life={self.life}"
        
    def update(self, screen : py.surface.Surface, foods : list[Food]) -> None:
        self.create(screen)
        self.check_screen_collision(screen)
        
        self.update_vision()
        self.check_foods_in_vision(foods, screen)
        print(f"{self.foods = }\n")
        if not self.foods:
            print("No foods in vision")
            self.move()
        else:
            if not self.is_colliding_with_food(self.foods[0]):
                print("Moving to food", self.foods[0])
                self.move_to_food(self.foods[0])
            else:
                self.eat(self.foods[0])
                if self.foods[0].is_completely_eaten():
                    print("Food is completely eaten")
                    self.foods.pop(0)
            
        
        
        # print(self.hunger)
        
        # if self.hunger > 0:
        #     self.increase_hunger(1)
        # if self.is_starving():
        #     self.remove_life_from_starvation(1)
        
    def update_vision(self):
        self.vision.x = self.rect.centerx - self.vision.width // 2
        self.vision.y = self.rect.centery - self.vision.height // 2
        
    def check_screen_collision(self, screen : py.surface.Surface) -> None:
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > screen.get_width() - self.size:
            self.rect.x = screen.get_width() - self.size
        elif self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > screen.get_height() - self.size:
            self.rect.y = screen.get_height() - self.size
        
    def choose_direction(self) -> tuple[int, int]:
        return random.choice(list(Direction)).value
    
    def is_dead(self) -> bool:
        return self.life <= 0
    
    def is_starving(self) -> bool:
        return self.hunger <= 0
    
    def increase_hunger(self, amount : int) -> None:
        self.hunger -= amount
        
    def decrease_hunger(self, amount : int) -> None:
        self.hunger += amount
        
    def remove_life_from_starvation(self, amount : int) -> None:
        self.life -= amount
        
    def create(self, screen : py.surface.Surface) -> None:
        py.draw.rect(screen, self.color, self.rect)
        py.draw.rect(screen, (255, 0, 0), self.vision, 1)
        
    def move(self):
        # print(f"Moving {self.direction = }")
        self.direction_count += 1
        
        if self.direction_count >= 100:
            self.direction = self.choose_direction()
            self.direction_count = 0
            
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        
        
        
    def is_food_in_vision(self, food : Food) -> bool:
        return self.vision.colliderect(food.rect)
    
    def check_foods_in_vision(self, foods : list[Food], screen : py.surface.Surface) -> None:
        for food in foods:
            if self.is_food_in_vision(food):
                self.draw_food_line(screen, food)
                if not food in self.foods:
                    self.foods.append(food)
                
    def is_colliding_with_food(self, food : Food) -> bool:
        return self.rect.colliderect(food.rect)
                
    def eat(self, food : Food) -> None:
        self.decrease_hunger(10)
        food.remove_life(10)
        
    def draw_food_line(self, screen : py.surface.Surface, food : Food) -> None:
        py.draw.line(screen, (0, 255, 0), self.rect.center, food.rect.center)
        
    def move_to_food(self, food : Food):
        
        dx, dy = food.rect.centerx - self.rect.centerx, food.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        
        
class Animals:
    def __init__(self, animals : list[Animal] = []) -> None:
        self.animals = animals
        
    def add_animal(self, animal : Animal) -> None:
        self.animals.append(animal)
        
    def remove_animal(self, animal : Animal) -> None:
        self.animals.remove(animal)
        
    def update(self, screen : py.surface.Surface, foods : list[Food]) -> None:
        for animal in self.animals:
            animal.update(screen, foods)
            if animal.is_dead():
                self.remove_animal(animal)
        
        
if __name__ == '__main__':
    print(list(Direction))
    print(random.choice(list(Direction)).value)