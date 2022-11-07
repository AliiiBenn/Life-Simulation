import random
import pygame as py

from animals import Animals, Animal
from food import Foods, Food

class Screen:
    def __init__(self, screen_witdh : int, screen_height : int) -> None:
        self.screen_witdh = screen_witdh
        self.screen_height = screen_height
        self.screen = py.display.set_mode((self.screen_witdh, self.screen_height))
        
    def change_background_color(self, color : tuple) -> None:
        self.screen.fill(color)

class Game:
    def __init__(self, screen : Screen) -> None:
        self.screen = screen
        self.clock = py.time.Clock()
        self.running = True
        
        self.animals = Animals()
        self.animals.add_animal(Animal(50, (255, 0, 0), 100, 100))
        
        self.foods = Foods()
        for _ in range(25):
            self.foods.add_food(Food(10, (0, 0, 255), random.randint(0, self.screen.screen_witdh - 50), random.randint(0, self.screen.screen_height - 50)))
        
    def is_quitting(self, event : py.event.Event) -> bool:
        return event.type == py.QUIT    
        
    def run(self) -> None:
        
        while self.running:
            self.clock.tick(60)
            self.screen.change_background_color((0, 180, 0))
            
            self.animals.update(self.screen.screen, self.foods.foods)
            self.foods.update(self.screen.screen)
            
            py.display.flip()
            
            for event in py.event.get():
                self.running = not self.is_quitting(event)
        py.quit()
         