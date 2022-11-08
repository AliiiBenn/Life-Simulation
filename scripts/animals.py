import math
import pygame as py
from enum import Enum
import random

from food import Food

class Direction(Enum):
    """Enum use to handle the direction of the animal
    """
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
        """Class used to create animals

        Args:
            size (int): The size of the animal (width = height)
            color (tuple[int, int, int]): The RGB color of the animal
            x (int): The x position of the animal
            y (int): The y position of the animal
            speed (int, optional): The speed of the animal. Defaults to 1.
            life (int, optional): The life of the animal. Defaults to 100.
        """
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
        """Method used to update the animal

        Args:
            screen (py.surface.Surface): The game screen
            foods (list[Food]): All the foods in the game
        """
        self.create(screen)
        self.check_screen_collision(screen)
        
        self.update_vision()
        self.check_foods_in_vision(foods, screen)
        self.move()
            
    def update_vision(self) -> None:
        """Update the animal vision based on his rect
        """
        self.vision.x = self.rect.centerx - self.vision.width // 2
        self.vision.y = self.rect.centery - self.vision.height // 2
        
    def check_screen_collision(self, screen : py.surface.Surface) -> None:
        """Check if the animal is colliding with the screen borders

        Args:
            screen (py.surface.Surface): The screen to check the collision
        """
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > screen.get_width() - self.size:
            self.rect.x = screen.get_width() - self.size
        elif self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > screen.get_height() - self.size:
            self.rect.y = screen.get_height() - self.size
        
    def choose_direction(self) -> tuple[int, int]:
        """Choose a random direction based on the `Direction` enum

        Returns:
            tuple[int, int]: The direction tuple (x, y)
        """
        return random.choice(list(Direction)).value
    
    def is_dead(self) -> bool:
        """Check if the animal is dead (life <= 0)

        Returns:
            bool: Whether the animal is dead or not
        """
        return self.life <= 0
    
    def is_starving(self) -> bool:
        """Check if the animal is starving (hunger <= 0)

        Returns:
            bool: Whether the animal is starving or not
        """
        return self.hunger <= 0
    
    def increase_hunger(self, amount : int) -> None:
        """Increase the hunger of the animal, so the variable will be decreased

        Args:
            amount (int): The amount to increase the hunger
        """
        self.hunger -= amount
        
    def decrease_hunger(self, amount : int) -> None:
        """Decrease the hunger of the animal, so the variable will be increased

        Args:
            amount (int): The amount to decrease the hunger
        """
        self.hunger += amount
        
    def remove_life_from_starvation(self, amount : int) -> None:
        """Remove life from the animal when he is starving, so it check if the animal is starving before removing life
        """
        if self.is_starving():
            self.life -= amount
        
    def create(self, screen : py.surface.Surface) -> None:
        """Create the animal on the screen and his vision

        Args:
            screen (py.surface.Surface): The screen to create the animal
        """
        py.draw.rect(screen, self.color, self.rect)
        py.draw.rect(screen, (255, 0, 0), self.vision, 1)
        
    def move(self):
        """Move the animal based on his direction, every 100 frames the animal will choose a new direction
        """        
        self.direction_count += 1
        
        if self.direction_count >= 100:
            self.direction = self.choose_direction()
            self.direction_count = 0
            
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        
    def is_food_in_vision(self, food : Food) -> bool:
        """Check if there is a food in the animal vision

        Args:
            food (Food): The food to check

        Returns:
            bool: Whether the food is in the vision or not
        """
        return self.vision.colliderect(food.rect)
    
    def check_foods_in_vision(self, foods : list[Food], screen : py.surface.Surface) -> None:
        """Check for all foods in the screen if they are any in the animal vision

        Args:
            foods (list[Food]): The list of foods to check
            screen (py.surface.Surface): _description_
        """
        for food in foods:
            if self.is_food_in_vision(food):
                self.draw_food_line(screen, food)
                
    def is_colliding_with_food(self, food : Food) -> bool:
        """Check if the animal is colliding with a food

        Args:
            food (Food): The food to check

        Returns:
            bool: Whether the animal is colliding with the food or not
        """
        return self.rect.colliderect(food.rect)
                
    def eat(self, food : Food) -> None:
        """Eat a food

        Args:
            food (Food): The food to eat, (remove it from the screen)
        """
        self.decrease_hunger(10)
        food.remove_life(10)
        
    def draw_food_line(self, screen : py.surface.Surface, food : Food) -> None:
        """Method to draw a line from the animal to the food

        Args:
            screen (py.surface.Surface): The screen to draw the line
            food (Food): The food to draw the line to
        """
        py.draw.line(screen, (0, 255, 0), self.rect.center, food.rect.center)
        
    def move_to_food(self, food : Food):
        """Method to move the animal to the food based on the hypotenuse

        Args:
            food (Food): The food to move to
        """
        dx, dy = food.rect.centerx - self.rect.centerx, food.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        
        
class Animals:
    def __init__(self, animals : list[Animal] = []) -> None:
        """Class used to manage all animals

        Args:
            animals (list[Animal], optional): In case there is already a list of animals somewhere in the game. Defaults to [].
        """
        self.animals = animals
        
    def add_animal(self, animal : Animal) -> None:
        """Add an animal to the list of animals

        Args:
            animal (Animal): The animal to add
        """     
        self.animals.append(animal)
        
    def remove_animal(self, animal : Animal) -> None:
        """Remove an animal from the list of animals

        Args:
            animal (Animal): The animal to remove
        """
        self.animals.remove(animal)
        
    def update(self, screen : py.surface.Surface, foods : list[Food]) -> None:
        """Main update method for all animals

        Args:
            screen (py.surface.Surface): The game screen
            foods (list[Food]): List of all foods in the game
        """
        for animal in self.animals:
            animal.update(screen, foods)
            if animal.is_dead():
                self.remove_animal(animal)
        
        
if __name__ == '__main__':
    print(list(Direction))
    print(random.choice(list(Direction)).value)