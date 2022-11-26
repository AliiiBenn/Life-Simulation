import random
import pygame as py

from foods import Food

from typing import Callable, Literal, Union

class FoodConsumptionTimer:
    def __init__(self, cooldown : int, callback : Callable):
        self.cooldown = cooldown
        self.callback = callback
        self.last = py.time.get_ticks()
        
    def update(self):
        now = py.time.get_ticks()
        if now - self.last >= self.cooldown:
            self.callback
            self.last = py.time.get_ticks()    
            
class FoodQuantityChecker:
    @staticmethod
    def is_hungry(current_food : int, required_food : int) -> bool:
        """Check if the animal is hungry

        Args:
            current_food (int): The current amount of food
            required_food (int): The required amount of food

        Returns:
            bool: True if the animal is hungry, False otherwise
        """
        return current_food <= required_food
    
    @staticmethod
    def is_full(current_food : int, max_food : int) -> bool:
        """Check if the animal is full

        Args:
            current_food (int): The current amount of food
            max_food (int): The maximum amount of food

        Returns:
            bool: True if the animal is full, False otherwise
        """
        return current_food >= max_food
    
    @staticmethod
    def is_starving(current_food : int) -> bool:
        """Check if the animal is starving

        Args:
            current_food (int): The current amount of food
            required_food (int): The required amount of food

        Returns:
            bool: True if the animal is starving, False otherwise
        """
        return current_food <= 0
    
class FoodIncreaser:
    @staticmethod
    def increase(current_food : int, amount : int) -> int:
        """Increase the amount of food

        Args:
            current_food (int): The current amount of food
            amount (int): The amount of food to increase

        Returns:
            int: The new amount of food
        """
        return current_food + amount
    
    @staticmethod
    def reset_food_storage(max_food_storage : int) -> int:
        """Reset the food_storage to the max_food_storage

        Args:
            food_storage (int): The current food_storage
            max_food_storage (int): The maximum food_storage

        Returns:
            int: The new food_storage
        """
        return max_food_storage
    
class FoodRemover:
    @staticmethod
    def decrease(current_food : int, amount : int) -> int:
        """Decrease the amount of food

        Args:
            current_food (int): The current amount of food
            amount (int): The amount of food to decrease

        Returns:
            int: The new amount of food
        """
        return current_food - amount
    
    @staticmethod
    async def remove_all_food() -> Literal[0]:
        return 0
    
class FoodEater:
    @staticmethod
    def eat_food(current_food : int, food : Food) -> None:
        """Eat the food given in parameter, will increase the amount of food and remove quantity of food from the food

        Args:
            food (Food): _description_
        """
        quantity_to_eat = random.randint(1, food.quantity)
        FoodIncreaser.increase(current_food, quantity_to_eat)
        food.remove_quantity(quantity_to_eat)
        
class StarvingHandler:
    def remove_life_from_starvation(self, current_food : int, life : int, amount : int) -> int:
        """Remove life from the animal when he is starving, so it check if the animal is starving before removing life
        """
        if FoodQuantityChecker.is_starving(current_food):
            life -= amount
        return life

class AnimalFoodHandler:
    def __init__(self, 
                 max_food_storage : int = 100,
                 food_removing_quantity : int = 1) -> None:
        self.max_food_storage = max_food_storage
        self.food_storage = max_food_storage
        self.food_removing_quantity = food_removing_quantity
         

        

    
    
    
    