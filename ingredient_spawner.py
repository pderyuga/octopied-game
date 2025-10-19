import pygame
import random
from ingredient import Ingredient
from constants import *


class IngredientSpawner:
    """Spawns ingredients from the top of the screen based on recipe data."""

    def __init__(self, recipe):
        """Initialize the spawner with a recipe.

        Args:
            recipe: Recipe object containing spawn rates and ingredient data
        """
        self.recipe = recipe
        self.spawn_timer = 0
        self.spawn_interval = INGREDIENT_SPAWN_INTERVAL

        # Build a weighted list of ingredient types for random selection
        self.ingredient_types = []
        self.weights = []
        for ing_type in recipe.get_all_ingredient_types():
            probability = recipe.get_spawn_probability(ing_type)
            if probability > 0:
                self.ingredient_types.append(ing_type)
                self.weights.append(probability)

    def update(self, dt):
        """Update the spawn timer."""
        self.spawn_timer += dt

    def should_spawn(self):
        """Check if it's time to spawn a new ingredient."""
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            return True
        return False

    def spawn(self):
        """Spawn a random ingredient based on recipe spawn rates.

        Returns:
            Ingredient object or None if no types available
        """
        if not self.ingredient_types:
            return None

        # Choose a random ingredient type based on weights
        ingredient_type = random.choices(self.ingredient_types, weights=self.weights)[0]

        # Get ingredient data from recipe
        data = self.recipe.get_ingredient_data(ingredient_type)
        if not data:
            return None

        # Random X position across the screen
        x = random.randint(INGREDIENT_RADIUS, SCREEN_WIDTH - INGREDIENT_RADIUS)
        y = INGREDIENT_SPAWN_Y

        # Create and return the ingredient
        return Ingredient(
            x, y, ingredient_type, data["category"], data["points"], data["color"]
        )
