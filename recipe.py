import json
from constants import *


class Recipe:
    """Loads and manages recipe data from JSON configuration files."""

    def __init__(self, recipe_path):
        """Load recipe from a JSON file.

        Args:
            recipe_path: Path to the recipe JSON file
        """
        with open(recipe_path, "r") as f:
            data = json.load(f)

        self.name = data.get("name", "Unknown Pie")
        self.duration = data.get("duration", MINIGAME_DURATION)
        self.required_ingredients = data.get("required_ingredients", {})
        self.allowed_ingredients = data.get("allowed_ingredients", {})
        self.spawn_rates = data.get("spawn_rates", {})

        # Map ingredient types to colors
        self.ingredient_colors = {
            "apple": COLOR_APPLE,
            "berry": COLOR_BERRY,
            "cinnamon": COLOR_CINNAMON,
            "rock": COLOR_ROCK,
        }

    def get_ingredient_data(self, ingredient_type):
        """Get data for a specific ingredient type.

        Returns:
            dict with 'points', 'category', 'color' keys
        """
        if ingredient_type in self.allowed_ingredients:
            data = self.allowed_ingredients[ingredient_type]
            return {
                "points": data.get("points", 0),
                "category": data.get("category", "good"),
                "color": self.ingredient_colors.get(ingredient_type, (200, 200, 200)),
            }
        return None

    def get_spawn_probability(self, ingredient_type):
        """Get the spawn probability for an ingredient type."""
        return self.spawn_rates.get(ingredient_type, 0)

    def get_all_ingredient_types(self):
        """Get list of all ingredient types in this recipe."""
        return list(self.allowed_ingredients.keys())

    def is_required(self, ingredient_type):
        """Check if an ingredient is required for the recipe."""
        return ingredient_type in self.required_ingredients

    def get_required_count(self, ingredient_type):
        """Get how many of this ingredient are required."""
        return self.required_ingredients.get(ingredient_type, 0)

    def calculate_score(self, collected_ingredients):
        """Calculate score based on collected ingredients.

        Args:
            collected_ingredients: List of Ingredient objects

        Returns:
            Score from 0-100
        """
        score = 0
        required_counts = dict(self.required_ingredients)

        # Count each ingredient type
        for ingredient in collected_ingredients:
            ing_type = ingredient.ingredient_type

            # Add/subtract points based on ingredient
            score += ingredient.points

            # Track if we're meeting requirements
            if ing_type in required_counts and required_counts[ing_type] > 0:
                required_counts[ing_type] -= 1

        # Bonus for meeting requirements
        requirements_met = sum(1 for count in required_counts.values() if count <= 0)
        total_requirements = len(self.required_ingredients)
        if total_requirements > 0:
            completion_bonus = (requirements_met / total_requirements) * 50
            score += completion_bonus

        # Normalize to 0-100 range
        score = max(0, min(MINIGAME_MAX_SCORE, score))
        return int(score)
