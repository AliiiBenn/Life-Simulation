import pygame as py



class Food:
    def __init__(self, size: int, color: tuple[int, int, int], x: int, y: int, quantity: int = 30) -> None:
        """Class used to create foods

        Args:
            size (int): The size of the food (width = height)
            color (tuple[int, int, int]): The RGB color of the food
            x (int): The x position of the food
            y (int): The y position of the food
            quantity (int, optional): The quantity of the food. Defaults to 100.
        """
        self.size = size
        self.color = color
        self.x = x
        self.y = y
        self.quantity = quantity

        self.rect = py.Rect(self.x, self.y, self.size, self.size)
        self.size_limit = 2
        
    def set_size(self) -> int:
        """Return the size of the food based on its quantity

        Returns:
            int: The size of the food
        """
        if self.size * (self.quantity // 10) <= self.size_limit:
            return self.size_limit
        return self.size * (self.quantity // 10)
    
    def create(self, screen : py.surface.Surface) -> None:
        """Draw the food on the screen

        Args:
            screen (py.surface.Surface): The screen where the food will be drawn
        """
        size = self.set_size()
        self.rect = py.Rect(self.x, self.y, size, size)
        py.draw.rect(screen, self.color, self.rect, border_radius=90)
        
    def remove_quantity(self, amount : int) -> None:
        """Remove quantity to the food

        Args:
            amount (int): The amount of quantity to remove
        """
        self.quantity -= amount
        
    def is_completely_eaten(self) -> bool:
        """Check if the food is completely eaten (quantity <= 0)

        Returns:
            bool: Whether the food is completely eaten or not
        """
        return self.quantity <= 0
        
        
