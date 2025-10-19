import pygame
from game_object import GameObject
from constants import *


class Octopus(GameObject):
    """The octopus chef that stays at the center of the screen.

    The octopus is the anchor point for tentacles.
    """

    def __init__(self, x, y):
        super().__init__(x, y)
        self.radius = OCTOPUS_RADIUS

    def draw(self, screen):
        """Draw the octopus as a simple circle."""
        # Draw the main body
        pygame.draw.circle(
            screen,
            COLOR_OCTOPUS,
            (int(self.position.x), int(self.position.y)),
            self.radius,
        )

        # Draw eyes
        eye_offset_x = self.radius // 3
        eye_offset_y = self.radius // 4
        eye_radius = self.radius // 6

        # Left eye
        left_eye_pos = (
            int(self.position.x - eye_offset_x),
            int(self.position.y - eye_offset_y),
        )
        pygame.draw.circle(screen, (255, 255, 255), left_eye_pos, eye_radius)
        pygame.draw.circle(screen, (0, 0, 0), left_eye_pos, eye_radius // 2)

        # Right eye
        right_eye_pos = (
            int(self.position.x + eye_offset_x),
            int(self.position.y - eye_offset_y),
        )
        pygame.draw.circle(screen, (255, 255, 255), right_eye_pos, eye_radius)
        pygame.draw.circle(screen, (0, 0, 0), right_eye_pos, eye_radius // 2)

    def update(self, dt):
        """Octopus is stationary, so no update needed."""
        pass

    def collides_with_point(self, point):
        """Check if a point is inside the octopus."""
        distance = self.position.distance_to(pygame.Vector2(point))
        return distance <= self.radius
