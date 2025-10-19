import pygame


# Base class for game objects
class GameObject(pygame.sprite.Sprite):
    """Base class for all game objects in Octopied.

    Similar to CircleShape from asteroids, but more flexible for different shapes.
    """

    def __init__(self, x, y):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)

    def update(self, dt):
        """Update the object's state. Override in subclasses."""
        pass

    def draw(self, screen):
        """Draw the object. Override in subclasses."""
        pass

    def collides_with_point(self, point):
        """Check if a point collides with this object. Override in subclasses."""
        return False

    def collides_with(self, other):
        """Check if this object collides with another. Override in subclasses."""
        return False
