import pygame as py
import random, math

from .food_handler import AnimalFoodHandler
from foods import Foods, Food
from .direction import Direction

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
        self.vision = py.Rect(self.rect.centerx, self.rect.centery, self.size * self.vision_scale, self.size * self.vision_scale)
        
        self.food_in_vision : list[Food] = []
        self.targeted_food : Food | None = None
        
        self.stop_moving = False
        
    def __str__(self) -> str:
        return f"Animal: x={self.x}, y={self.y}, size={self.size}, color={self.color}, speed={self.speed}, life={self.life}"
    
    def handle_input(self) -> None:
        key = py.key.get_pressed()
        if key[py.K_SPACE]:
            self.stop_moving = not self.stop_moving
        
    def update(self, screen : py.surface.Surface, foods : Foods) -> None:
        """Method used to update the animal

        Args:
            screen (py.surface.Surface): The game screen
            foods (list[Food]): All the foods in the game
        """
        self.create(screen)
        self.check_screen_collision(screen)
        self.handle_input()
        
        self.update_vision()
        self.food_in_vision = self.check_foods_in_vision(foods.foods, screen)
        
        if len(self.food_in_vision) > 0:
            if self.targeted_food is None:
                self.targeted_food = self.get_closest_food(self.food_in_vision)
            if self.targeted_food.is_completely_eaten():
                foods.remove_food(self.targeted_food)
                self.targeted_food = None
                self.stop_moving = False
                
            else:
                self.stop_moving = True
                if self.is_colliding_with_food(self.targeted_food):
                    self.food_handler.eat_food(self.targeted_food)
                self.move_to_food(self.targeted_food)
                
        
        if not self.stop_moving:
            self.move()
            
        self.food_handler.decrease_hunger(1)
        self.life = self.food_handler.remove_life_from_starvation(self.life, 1)
        print(self.food_handler.food_storage, self.life)
        
            
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
        return self.vision.collidepoint(food.rect.centerx, food.rect.centery)
    
    def check_foods_in_vision(self, foods : list[Food], screen : py.surface.Surface) -> list[Food]:
        """Check for all foods in the screen if they are any in the animal vision

        Args:
            foods (list[Food]): The list of foods to check
            screen (py.surface.Surface): _description_
            
        Returns:
            list[Food]: The list of foods in the vision
        """
        food_in_vision : list[Food] = []
        for food in foods:
            if self.is_food_in_vision(food):
                self.draw_food_line(screen, food)
                food_in_vision.append(food)
        return food_in_vision
                
    def is_colliding_with_food(self, food : Food) -> bool:
        """Check if the animal is colliding with a food

        Args:
            food (Food): The food to check

        Returns:
            bool: Whether the animal is colliding with the food or not
        """
        return self.rect.colliderect(food.rect)
        
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
        