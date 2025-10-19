import pygame
from game_object import GameObject
from constants import *


class PieCrust(GameObject):
    """The pie crust where ingredients are dropped.

    Positioned below the octopus to create the appearance of a workbench.
    """

    def __init__(self, x, y):
        super().__init__(x, y)
        self.width = PIE_CRUST_WIDTH
        self.height = PIE_CRUST_HEIGHT
        self.contents = []  # List of ingredients that landed in the crust

    def draw(self, screen):
        """Draw the pie crust as a rectangle."""
        # Draw the main crust (outer rectangle)
        crust_rect = pygame.Rect(
            int(self.position.x - self.width // 2),
            int(self.position.y - self.height // 2),
            self.width,
            self.height,
        )
        pygame.draw.rect(screen, COLOR_CRUST, crust_rect)
        pygame.draw.rect(
            screen, tuple(max(0, c - 40) for c in COLOR_CRUST), crust_rect, 3
        )

        # Draw the inner area (lighter)
        inner_rect = pygame.Rect(
            int(self.position.x - self.width // 2 + 10),
            int(self.position.y - self.height // 2 + 10),
            self.width - 20,
            self.height - 20,
        )
        pygame.draw.rect(
            screen, tuple(min(255, c + 20) for c in COLOR_CRUST), inner_rect
        )

    def update(self, dt):
        """Pie crust is stationary."""
        pass

    def add_ingredient(self, ingredient):
        """Add an ingredient to the crust contents."""
        self.contents.append(ingredient)

    def get_contents(self):
        """Get the list of ingredients in the crust."""
        return self.contents

    def collides_with_point(self, point):
        """Check if a point is inside the crust area."""
        px, py = point
        left = self.position.x - self.width // 2
        right = self.position.x + self.width // 2
        top = self.position.y - self.height // 2
        bottom = self.position.y + self.height // 2
        return left <= px <= right and top <= py <= bottom

    def collides_with(self, other):
        """Check if an object collides with the crust."""
        if hasattr(other, "position"):
            # For circular objects, check if center is in rectangle
            return self.collides_with_point((other.position.x, other.position.y))
        return False
