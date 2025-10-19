import pygame
from game_object import GameObject
from constants import *


class Tentacle(GameObject):
    """A tentacle that extends from the octopus to follow the mouse.

    Uses smoothing/lerp to create realistic movement and draws a Bezier curve.
    """

    def __init__(self, octopus):
        # Initialize at octopus position
        super().__init__(octopus.position.x, octopus.position.y)
        self.octopus = octopus
        self.target_position = pygame.Vector2(octopus.position.x, octopus.position.y)
        self.tip_radius = TENTACLE_TIP_RADIUS
        self.is_grabbing = False
        self.grabbed_object = None

    def update(self, dt):
        """Update tentacle position with smoothing toward target."""
        # Lerp (linear interpolation) toward target position
        # Formula: current + (target - current) * factor * dt
        smoothing_factor = TENTACLE_SMOOTHING * dt
        smoothing_factor = min(smoothing_factor, 1.0)  # Clamp to max 1.0

        self.position += (self.target_position - self.position) * smoothing_factor

    def set_target(self, target_pos):
        """Set the target position for the tentacle tip to move toward."""
        self.target_position = pygame.Vector2(target_pos)

    def set_grabbing(self, is_grabbing):
        """Set whether the tentacle is in grabbing mode."""
        self.is_grabbing = is_grabbing

    def grab_object(self, obj):
        """Attach an object to the tentacle."""
        self.grabbed_object = obj

    def release_object(self):
        """Release the currently grabbed object."""
        obj = self.grabbed_object
        self.grabbed_object = None
        return obj

    def draw(self, screen):
        """Draw the tentacle as a quadratic Bezier curve."""
        # Calculate control point for Bezier curve (midpoint, slightly offset)
        start = self.octopus.position
        end = self.position

        # Control point is between start and end, offset perpendicular to create curve
        mid = (start + end) / 2
        # Offset perpendicular to the line
        direction = end - start
        if direction.length() > 0:
            perpendicular = pygame.Vector2(-direction.y, direction.x).normalize()
            # Offset by 20% of the distance for a nice curve
            offset = direction.length() * 0.2
            control = mid + perpendicular * offset
        else:
            control = mid

        # Draw the Bezier curve using multiple line segments
        points = []
        segments = 20
        for i in range(segments + 1):
            t = i / segments
            # Quadratic Bezier formula: B(t) = (1-t)²P0 + 2(1-t)tP1 + t²P2
            point = (1 - t) ** 2 * start + 2 * (1 - t) * t * control + t**2 * end
            points.append((int(point.x), int(point.y)))

        # Draw the curve
        if len(points) > 1:
            pygame.draw.lines(screen, COLOR_TENTACLE, False, points, 8)

        # Draw the tip (larger circle)
        tip_color = TENTACLE_GRAB_HIGHLIGHT if self.is_grabbing else COLOR_TENTACLE
        pygame.draw.circle(
            screen,
            tip_color,
            (int(self.position.x), int(self.position.y)),
            self.tip_radius,
        )

        # Draw a smaller inner circle for detail
        pygame.draw.circle(
            screen,
            COLOR_OCTOPUS,
            (int(self.position.x), int(self.position.y)),
            self.tip_radius // 2,
        )

    def collides_with_point(self, point):
        """Check if a point collides with the tentacle tip."""
        distance = self.position.distance_to(pygame.Vector2(point))
        return distance <= self.tip_radius

    def collides_with(self, other):
        """Check if the tentacle tip collides with another object."""
        if hasattr(other, "position") and hasattr(other, "radius"):
            distance = self.position.distance_to(other.position)
            return distance <= (self.tip_radius + other.radius)
        return False
