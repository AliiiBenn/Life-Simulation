import pygame as py

from foods import Foods, Food

class FoodPlacer:
    @staticmethod
    def place_food(foods : Foods, food_count : int, food_size : int, food_color : tuple) -> None:
        """Place food on the screen

        Args:
            foods (Foods): The foods object
            screen (py.Surface): The screen
            food_count (int): The number of food to place
            food_size (int): The size of the food
            food_color (tuple): The color of the food
        """
        for _ in range(food_count):
            foods.add_food(Food(food_size, food_color, py.mouse.get_pos()[0], py.mouse.get_pos()[1]))
            
    @classmethod
    def is_left_click(cls, event : py.event.Event, foods : Foods, food_count : int, food_size : int, food_color : tuple) -> None:
        """Check if the user is left clicking

        Args:
            event (py.event.Event): The event to check
            foods (Foods): The foods object
            screen (py.Surface): The screen
            food_count (int): The number of food to place
            food_size (int): The size of the food
            food_color (tuple): The color of the food
        """
        if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
            cls.place_food(foods, food_count, food_size, food_color)