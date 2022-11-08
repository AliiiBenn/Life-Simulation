import random
import pygame as py


class Food:
    def __init__(self, size: int, color: tuple[int, int, int], x: int, y: int, life: int = 10) -> None:
        """Class used to create foods

        Args:
            size (int): The size of the food (width = height)
            color (tuple[int, int, int]): The RGB color of the food
            x (int): The x position of the food
            y (int): The y position of the food
            life (int, optional): The life of the food. Defaults to 100.
        """
        self.size = size
        self.color = color
        self.x = x
        self.y = y
        self.life = life

        self.rect = py.Rect(self.x, self.y, self.size, self.size)
        
    def create(self, screen : py.surface.Surface) -> None:
        """Draw the food on the screen

        Args:
            screen (py.surface.Surface): The screen where the food will be drawn
        """
        py.draw.rect(screen, self.color, self.rect, border_radius=90)
        
    def remove_life(self, amount : int) -> None:
        """Remove life to the food

        Args:
            amount (int): The amount of life to remove
        """
        self.life -= amount
        
    def is_completely_eaten(self) -> bool:
        """Check if the food is completely eaten (life <= 0)

        Returns:
            bool: Whether the food is completely eaten or not
        """
        return self.life <= 0
        
        
class Foods:
    def __init__(self) -> None:
        """Class used to handle the foods
        """
        self.foods = []
        
        
    def add_food(self, food : Food) -> None:
        """Add a food to the list of foods

        Args:
            food (Food): The food to add
        """
        self.foods.append(food)
        
    def add_foods(self, screen : py.surface.Surface, amount : int, size : int, color : tuple[int, int, int]) -> None:
        """Add foods to the list of foods

        Args:
            amount (int): The amount of foods to add
            size (int): The size of the foods
            color (tuple[int, int, int]): The color of the foods
        """
        for _ in range(amount):
            self.foods.append(Food(size, color, random.randint(0, screen.get_width() - 50), random.randint(0, screen.get_height() - 50)))
        
    def remove_food(self, food : Food) -> None:
        """Remove a food from the list of foods

        Args:
            food (Food): The food to remove
        """
        self.foods.remove(food)
        
    def update(self, screen : py.surface.Surface) -> None:
        """The main update function of the foods

        Args:
            screen (py.surface.Surface): The game screen
        """
        for food in self.foods:
            food.create(screen)
            
            # if food.is_completely_eaten():
            #     self.remove_food(food)