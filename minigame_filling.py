import pygame
from minigame_base import MinigameBase
from octopus import Octopus
from tentacle import Tentacle
from pie_crust import PieCrust
from ingredient_spawner import IngredientSpawner
from recipe import Recipe
from constants import *


class MinigameFilling(MinigameBase):
    """Pie filling minigame where player catches falling ingredients.

    Player uses tentacle to catch ingredients and drop them into the pie crust.
    Score is based on collecting the right ingredients and avoiding bad ones.
    """

    def __init__(self, recipe_path):
        """Initialize the filling minigame.

        Args:
            recipe_path: Path to the recipe JSON file
        """
        # Load recipe first to get duration
        self.recipe = Recipe(recipe_path)
        super().__init__(self.recipe.duration)

        # Initialize game objects
        self.octopus = Octopus(OCTOPUS_X, OCTOPUS_Y)
        self.tentacle = Tentacle(self.octopus)
        self.pie_crust = PieCrust(PIE_CRUST_X, PIE_CRUST_Y)
        self.spawner = IngredientSpawner(self.recipe)

        # Lists to track ingredients
        self.falling_ingredients = []
        self.ingredients_in_crust = []

        # Game state
        self.mouse_pos = (OCTOPUS_X, OCTOPUS_Y)
        self.mouse_pressed = False

        # Initialize font for UI
        pygame.font.init()
        self.font = pygame.font.Font(None, UI_FONT_SIZE)
        self.small_font = pygame.font.Font(None, UI_SMALL_FONT_SIZE)

    def start(self):
        """Initialize the minigame state."""
        self.elapsed_time = 0
        self.is_active = True
        self.score = 0

    def update(self, dt):
        """Update game logic.

        Returns:
            True if minigame should continue, False if complete
        """
        # Update timer
        self.elapsed_time += dt

        # Update tentacle position to follow mouse
        self.tentacle.set_target(self.mouse_pos)
        self.tentacle.update(dt)

        # Update spawner and spawn new ingredients
        self.spawner.update(dt)
        if self.spawner.should_spawn():
            new_ingredient = self.spawner.spawn()
            if new_ingredient:
                self.falling_ingredients.append(new_ingredient)

        # Update all falling ingredients
        for ingredient in self.falling_ingredients[:]:
            if ingredient.state == "falling":
                ingredient.update(dt)

                # Check if ingredient fell off screen
                if ingredient.is_off_screen():
                    self.falling_ingredients.remove(ingredient)
                    ingredient.set_state("missed")

            elif ingredient.state == "grabbed":
                # Grabbed ingredient follows tentacle
                ingredient.position = self.tentacle.position.copy()

        # Handle grabbing logic
        if self.mouse_pressed and not self.tentacle.is_grabbing:
            # Try to grab an ingredient
            for ingredient in self.falling_ingredients:
                if ingredient.state == "falling" and self.tentacle.collides_with(
                    ingredient
                ):
                    # Grab this ingredient
                    self.tentacle.set_grabbing(True)
                    self.tentacle.grab_object(ingredient)
                    ingredient.set_state("grabbed")
                    break

        elif not self.mouse_pressed and self.tentacle.is_grabbing:
            # Release the grabbed ingredient
            released = self.tentacle.release_object()
            if released:
                self.tentacle.set_grabbing(False)

                # Check if ingredient lands in crust
                if self.pie_crust.collides_with(released):
                    # Successfully dropped in crust
                    released.set_state("in_crust")
                    self.falling_ingredients.remove(released)
                    self.pie_crust.add_ingredient(released)
                    self.ingredients_in_crust.append(released)

                    # Instant loss for inedible items
                    if released.category == "inedible":
                        self.is_active = False
                else:
                    # Dropped outside crust, let it continue falling
                    released.set_state("falling")

        # Check if time is up
        if self.is_complete():
            return False

        return True

    def draw(self, screen):
        """Render the minigame."""
        # Draw background
        screen.fill(COLOR_BACKGROUND)

        # Draw pie crust first (background layer)
        self.pie_crust.draw(screen)

        # Draw octopus
        self.octopus.draw(screen)

        # Draw tentacle
        self.tentacle.draw(screen)

        # Draw falling ingredients
        for ingredient in self.falling_ingredients:
            ingredient.draw(screen)

        # Draw UI
        self._draw_ui(screen)

    def _draw_ui(self, screen):
        """Draw UI elements like timer, score, and requirements."""
        # Draw timer
        remaining_time = self.get_remaining_time()
        timer_text = self.font.render(
            f"Time: {int(remaining_time)}s", True, COLOR_TIMER
        )
        screen.blit(timer_text, (UI_MARGIN, UI_MARGIN))

        # Draw recipe name
        name_text = self.small_font.render(self.recipe.name, True, COLOR_UI_TEXT)
        screen.blit(name_text, (UI_MARGIN, UI_MARGIN + 40))

        # Draw required ingredients
        y_offset = UI_MARGIN + 80
        requirements_text = self.small_font.render("Required:", True, COLOR_UI_TEXT)
        screen.blit(requirements_text, (UI_MARGIN, y_offset))
        y_offset += 30

        for ing_type, required_count in self.recipe.required_ingredients.items():
            # Count how many we have
            collected_count = sum(
                1
                for ing in self.ingredients_in_crust
                if ing.ingredient_type == ing_type
            )
            text = self.small_font.render(
                f"{ing_type}: {collected_count}/{required_count}",
                True,
                COLOR_SCORE if collected_count >= required_count else COLOR_UI_TEXT,
            )
            screen.blit(text, (UI_MARGIN + 20, y_offset))
            y_offset += 25

        # Draw current score (live calculation)
        current_score = self.recipe.calculate_score(self.ingredients_in_crust)
        score_text = self.font.render(f"Score: {current_score}", True, COLOR_SCORE)
        screen.blit(score_text, (SCREEN_WIDTH - 200, UI_MARGIN))

    def calculate_score(self):
        """Calculate final score (0-100)."""
        self.score = self.recipe.calculate_score(self.ingredients_in_crust)
        return self.score

    def get_summary(self):
        """Return a dictionary with result summary."""
        # Calculate final score
        final_score = self.calculate_score()

        # Count ingredients by type
        ingredient_counts = {}
        for ingredient in self.ingredients_in_crust:
            ing_type = ingredient.ingredient_type
            ingredient_counts[ing_type] = ingredient_counts.get(ing_type, 0) + 1

        # Check which requirements were met
        requirements_met = {}
        for ing_type, required in self.recipe.required_ingredients.items():
            collected = ingredient_counts.get(ing_type, 0)
            requirements_met[ing_type] = {
                "required": required,
                "collected": collected,
                "met": collected >= required,
            }

        return {
            "score": final_score,
            "recipe_name": self.recipe.name,
            "ingredients_collected": ingredient_counts,
            "requirements_met": requirements_met,
            "total_ingredients": len(self.ingredients_in_crust),
        }

    def handle_mouse_motion(self, pos):
        """Handle mouse motion events."""
        self.mouse_pos = pos

    def handle_mouse_button(self, pressed):
        """Handle mouse button events."""
        self.mouse_pressed = pressed
