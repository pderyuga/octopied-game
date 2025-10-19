import pygame
from game_object import GameObject
from constants import *


class Tentacle(GameObject):
    """A tentacle that extends from the octopus to follow the mouse.

    Uses smoothing/lerp to create realistic movement and draws a Bezier curve.
    """

    def __init__(self, octopus, tentacle_id, angle):
        """Initialize a tentacle.

        Args:
            octopus: The octopus object this tentacle is attached to
            tentacle_id: Unique ID for this tentacle (0-3)
            angle: Starting angle in degrees from top (clockwise)
        """
        # Calculate initial position based on angle
        import math

        angle_rad = math.radians(angle)
        x = octopus.position.x + TENTACLE_OFFSET * math.sin(angle_rad)
        y = octopus.position.y + TENTACLE_OFFSET * math.cos(angle_rad)

        super().__init__(x, y)
        self.octopus = octopus
        self.tentacle_id = tentacle_id
        self.target_position = pygame.Vector2(x, y)
        self.locked_position = pygame.Vector2(x, y)  # Position when inactive
        self.tip_radius = TENTACLE_TIP_RADIUS
        self.is_grabbing = False
        self.grabbed_object = None
        self.is_active = False
        self.auto_grabbing = False  # For inactive tentacles

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

    def lock_position(self):
        """Lock the tentacle at its current position when becoming inactive."""
        self.locked_position = self.position.copy()
        self.target_position = self.locked_position.copy()

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

        # Choose color based on active state
        tentacle_color = COLOR_TENTACLE if self.is_active else TENTACLE_INACTIVE_COLOR
        line_width = 8 if self.is_active else 5

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
            pygame.draw.lines(screen, tentacle_color, False, points, line_width)

        # Draw the tip (larger circle)
        if self.is_grabbing:
            tip_color = TENTACLE_GRAB_HIGHLIGHT
        else:
            tip_color = tentacle_color

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

        # Draw tentacle number
        font = pygame.font.Font(None, 20)
        number_text = font.render(str(self.tentacle_id + 1), True, (255, 255, 255))
        text_rect = number_text.get_rect(
            center=(int(self.position.x), int(self.position.y))
        )
        screen.blit(number_text, text_rect)
        
        # Draw auto-grab range indicator for inactive tentacles
        if not self.is_active and not self.is_grabbing:
            # Draw a subtle circle showing the grab range
            pygame.draw.circle(
                screen,
                (*tentacle_color[:2], tentacle_color[2], 50),  # Semi-transparent
                (int(self.position.x), int(self.position.y)),
                self.tip_radius * 2,
                1  # Line width
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
