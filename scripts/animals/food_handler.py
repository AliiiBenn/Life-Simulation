import random
import pygame as py

from foods import Food

from typing import Union


class AnimalFoodHandler:
    def __init__(self, 
                 max_food_storage : Union[int, float] = 100,
                 food_removing_quantity : Union[int, float] = 2) -> None:
        self.max_food_storage = max_food_storage
        self.food_storage = max_food_storage
        self.food_removing_quantity = food_removing_quantity
        
        self.last = py.time.get_ticks()
        self.food_removing_cooldown = 1000
        
    def food_removing_timer(self):
        now = py.time.get_ticks()
        if now - self.last >= self.food_removing_cooldown:
            self.last = now
            self.decrease_hunger(self.food_removing_quantity)
            (self.food_storage)
            
    def is_hungry(self) -> bool:
        """Check if the animal is hungry

        Returns:
            bool: True if the animal is hungry, False otherwise
        """
        return self.food_storage <= 70
    
    def is_full(self) -> bool:
        """Check if the animal is full

        Returns:
            bool: True if the animal is full, False otherwise
        """
        return self.food_storage >= self.max_food_storage
        
    def is_starving(self) -> bool:
        return self.food_storage <= 0
    
    def increase_hunger(self, amount : Union[int, float]) -> None:
        """Increase the food_storage of the animal

        Args:
            amount (int): The amount to increase the food_storage
        """
        if self.food_storage + amount > self.max_food_storage:
            difference = self.max_food_storage - self.food_storage
            self.food_storage += difference
            return
        self.food_storage += amount
        return
        
    def decrease_hunger(self, amount : Union[int, float]) -> None:
        """Decrease the food_storage of the animal

        Args:
            amount (int): The amount to decrease the food_storage
        """
        if self.food_storage > 0 and self.food_storage - amount >= 0:
            self.food_storage -= amount
    
    def remove_life_from_starvation(self, life : int, amount : int) -> int:
        """Remove life from the animal when he is starving, so it check if the animal is starving before removing life
        """
        if self.is_starving():
            life -= amount
        return life
    
    def eat_food(self, food : Food) -> None:
        """Eat the food given in parameter, will increase the amount of food and remove quantity of food from the food

        Args:
            food (Food): _description_
        """
        self.increase_hunger(random.randint(1, food.quantity))
        food.remove_quantity(random.randint(1, food.quantity))