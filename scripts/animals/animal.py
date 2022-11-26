import pygame as py
import random, math

from .food_handler import AnimalFoodHandler
from foods import Foods, Food
from water import Water
from .direction import Direction
from .vision import Vision

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
        
        self.food_handler = AnimalFoodHandler()
        self.vision_scale = 6
        self.vision = Vision(self.rect.centerx, self.rect.centery, self.size * self.vision_scale, self.size * self.vision_scale)
        
        self.targeted_food = None
        self.stop_moving = False
        
        self.age = 0
        self.death_age = random.randint(50, 100)
        
    def __str__(self) -> str:
        return f"Animal: x={self.x}, y={self.y}, size={self.size}, color={self.color}, speed={self.speed}, life={self.life}"
        
    def update(self, screen : py.surface.Surface, foods : Foods) -> None:
        """Method used to update the animal

        Args:
            screen (py.surface.Surface): The game screen
            foods (list[Food]): All the foods in the game
        """
        
        self.create(screen)
        self.vision.update(screen)
        self.check_screen_collision(screen)
        
        self.vision.update_rect(self.rect)
        self.food_in_vision = self.vision.check_visible_foods(foods.foods)
        
        print(self.food_handler.food_storage)
        if self.targeted_food is not None and self.targeted_food.is_completely_eaten():
            self.remove_eaten_targeted_food(foods)
            
        if self.targeted_food is not None:
            if self.food_handler.is_hungry():
                self.stop_moving = True
                if self.is_colliding_with_food(self.targeted_food):
                    self.food_handler.eat_food(self.targeted_food)
                self.move_to_food(self.targeted_food)
            else:
                self.stop_moving = False
                self.targeted_food = None
            
        if len(self.food_in_vision) > 0:
            if self.targeted_food is None and self.food_handler.is_hungry():
                self.targeted_food = self.get_closest_food(self.food_in_vision)
        
        
        if not self.stop_moving:
            self.move()
            
        self.food_handler.food_removing_timer()
        self.life = self.food_handler.remove_life_from_starvation(self.life, 1)
        
    def remove_eaten_targeted_food(self, foods : Foods) -> None:
        (f"targerted food is completely eaten: {self.targeted_food}")
        if self.targeted_food in foods.foods:
            foods.remove_food(self.targeted_food)
        self.targeted_food = None
        self.stop_moving = False
        
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
        
    def create(self, screen : py.surface.Surface) -> None:
        """Create the animal on the screen and his vision

        Args:
            screen (py.surface.Surface): The screen to create the animal
        """
        py.draw.rect(screen, self.color, self.rect)
        
    def move(self):
        """Move the animal based on his direction, every 100 frames the animal will choose a new direction
        """        
        self.direction_count += 1
        
        if self.direction_count >= 100:
            self.direction = self.choose_direction()
            self.direction_count = 0
            
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
           
    def is_colliding_with_food(self, food : Food) -> bool:
        """Check if the animal is colliding with a food

        Args:
            food (Food): The food to check

        Returns:
            bool: Whether the animal is colliding with the food or not
        """
        return self.rect.colliderect(food.rect)
        
    def move_to_food(self, food : Food):
        """Method to move the animal to the food based on the hypotenuse

        Args:
            food (Food): The food to move to
        """
        
        dx, dy = food.rect.centerx - self.rect.centerx, food.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        try:
            dx, dy = dx / dist, dy / dist
        except ZeroDivisionError:
            dx = dy = 0
            
        if round(dx * self.speed) >= 1:
            self.rect.x += round(dx * self.speed)
        else:
            self.rect.x -= 1
            
        if round(dy * self.speed) >= 1:
            self.rect.y += round(dy * self.speed)
        else:
            self.rect.y -= 1
        # self.rect.x += dx * self.speed
        # self.rect.y += dy * self.speed
        
    def get_distance_from_food(self, food : Food) -> float:
        """Get the distance from the animal to the food

        Args:
            food (Food): The food to get the distance from

        Returns:
            float: The distance from the animal to the food
        """
        return math.hypot(food.rect.centerx - self.rect.centerx, food.rect.centery - self.rect.centery)
    
    def get_closest_food(self, foods : list[Food]) -> Food:
        """Get the closest food from the animal

        Args:
            foods (list[Food]): The list of foods to check

        Returns:
            Food: The closest food from the animal
        """
        closest_food = None
        closest_distance : float = 0
        for food in foods:
            distance = self.get_distance_from_food(food)
            if closest_food is None or distance < closest_distance:
                closest_food = food
                closest_distance = distance
        return closest_food # type: ignore
        