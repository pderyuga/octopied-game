import pygame
from game_object import GameObject
from constants import *


class Ingredient(GameObject):
    """A falling ingredient that can be caught by the tentacle.

    Attributes:
        ingredient_type: String ID like "apple", "berry", "rock"
        category: "good", "bad", or "inedible"
        points: Score value (positive or negative)
        color: RGB color for rendering
    """

    def __init__(self, x, y, ingredient_type, category, points, color):
        super().__init__(x, y)
        self.ingredient_type = ingredient_type
        self.category = category
        self.points = points
        self.color = color
        self.radius = INGREDIENT_RADIUS
        self.state = "falling"  # falling, grabbed, in_crust, missed
        self.velocity = pygame.Vector2(0, INGREDIENT_FALL_SPEED)

    def update(self, dt):
        """Update ingredient position based on state."""
        if self.state == "falling":
            # Fall downward at constant speed
            self.position += self.velocity * dt
        elif self.state == "grabbed":
            # Ingredients don't update position when grabbed
            # They'll be positioned by the tentacle
            pass

    def draw(self, screen):
        """Draw the ingredient as a colored circle with a label."""
        # Draw the main ingredient circle
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.position.x), int(self.position.y)),
            self.radius,
        )

        # Draw a darker outline
        pygame.draw.circle(
            screen,
            tuple(max(0, c - 50) for c in self.color),
            (int(self.position.x), int(self.position.y)),
            self.radius,
            2,
        )

    def is_off_screen(self):
        """Check if the ingredient has fallen off the bottom of the screen."""
        return self.position.y > SCREEN_HEIGHT + self.radius

    def set_state(self, state):
        """Change the ingredient's state."""
        self.state = state

    def collides_with_point(self, point):
        """Check if a point collides with this ingredient."""
        distance = self.position.distance_to(pygame.Vector2(point))
        return distance <= self.radius

    def collides_with(self, other):
        """Check if this ingredient collides with another object."""
        if hasattr(other, "position") and hasattr(other, "radius"):
            distance = self.position.distance_to(other.position)
            return distance <= (self.radius + other.radius)
        return False
