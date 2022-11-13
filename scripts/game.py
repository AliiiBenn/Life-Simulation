import random
import pygame as py

from animals import Animals, Animal
from foods import Foods
from water import Water

from foods.food_placer import FoodPlacer

FOOD_COLOR = (7, 97, 34)
BACKGROUND_COLOR = (13, 181, 63)


class Screen:
    """Class use to handle the game screen
    """
    def __init__(self, screen_witdh : int, screen_height : int) -> None:
        """Initialize the screen

        Args:
            screen_witdh (int): The screen width
            screen_height (int): The screen height
        """
        self.screen_witdh = screen_witdh
        self.screen_height = screen_height
        self.screen = py.display.set_mode((self.screen_witdh, self.screen_height))
        
    def change_background_color(self, color : tuple) -> None:
        """Change the background color of the screen

        Args:
            color (tuple): The color to set (RGB)
        """
        self.screen.fill(color)

class Game:
    def __init__(self, screen : Screen) -> None:
        """Class use to handle the game

        Args:
            screen (Screen): The game screen
        """
        self.screen = screen
        self.clock = py.time.Clock()
        self.running = True
        
        self.animals = Animals()
        # self.animals.add_animal(Animal(20, (255, 0, 0), 100, 100))
        for _ in range(1):
            self.animals.add_animal(Animal(30, (255, 0, 0), random.randint(0, self.screen.screen_witdh - 50), random.randint(0, self.screen.screen_height - 50)))
        
        self.foods = Foods()
        self.foods.add_foods(self.screen.screen, 25, 6, FOOD_COLOR)
        self.water = Water(100, 100, 100, 100)
        
    def is_quitting(self, event : py.event.Event) -> bool:
        """Check if the user is quitting the game

        Args:
            event (py.event.Event): The event to check

        Returns:
            bool: Whether the user is quitting the game or not
        """
        return event.type == py.QUIT    
        
    def run(self) -> None:
        """The main game loop.
        """
        while self.running:
            self.clock.tick(60)
            self.screen.change_background_color(BACKGROUND_COLOR)
            
            self.water.update(self.screen.screen)
            
            self.animals.update(self.screen.screen, self.foods)
            self.foods.update(self.screen.screen)
            
            py.display.flip()
            
            for event in py.event.get():
                self.running = not self.is_quitting(event)
                FoodPlacer.is_left_click(event, self.foods, 1, 6, FOOD_COLOR)
        py.quit()
         