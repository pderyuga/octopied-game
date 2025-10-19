from abc import ABC, abstractmethod


class MinigameBase(ABC):
    """Abstract base class for all minigames in Octopied.

    Each minigame should:
    - Run for a specified duration
    - Track and return a score (0-100)
    - Provide a summary of results
    """

    def __init__(self, duration):
        self.duration = duration
        self.elapsed_time = 0
        self.is_active = True
        self.score = 0

    @abstractmethod
    def start(self):
        """Initialize the minigame state."""
        pass

    @abstractmethod
    def update(self, dt):
        """Update game logic. Returns True if minigame should continue."""
        pass

    @abstractmethod
    def draw(self, screen):
        """Render the minigame."""
        pass

    @abstractmethod
    def calculate_score(self):
        """Calculate final score (0-100)."""
        pass

    @abstractmethod
    def get_summary(self):
        """Return a dictionary with result summary."""
        pass

    def is_complete(self):
        """Check if the minigame has finished."""
        return self.elapsed_time >= self.duration or not self.is_active

    def get_remaining_time(self):
        """Get remaining time in seconds."""
        return max(0, self.duration - self.elapsed_time)

    def get_score(self):
        """Get the current score."""
        return self.score
