import pygame as py
import random


from . import Food


class Foods:
    def __init__(self) -> None:
        """Class used to handle the foods
        """
        self.foods : list[Food] = []
        
        
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
        (f"{food=}, {food in self.foods}")
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