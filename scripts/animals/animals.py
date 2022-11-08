import pygame as py

from .animal import Animal
from foods import Foods

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
        
    def update(self, screen : py.surface.Surface, foods : Foods) -> None:
        """Main update method for all animals

        Args:
            screen (py.surface.Surface): The game screen
            foods (list[Food]): List of all foods in the game
        """
        for animal in self.animals:
            animal.update(screen, foods)
            if animal.is_dead():
                self.remove_animal(animal)
        