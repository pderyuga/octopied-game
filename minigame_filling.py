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

        # Create multiple tentacles
        self.tentacles = []
        for i in range(NUM_TENTACLES):
            tentacle = Tentacle(self.octopus, i, TENTACLE_ANGLES[i])
            self.tentacles.append(tentacle)

        # Set first tentacle as active
        self.active_tentacle_index = 0
        self.tentacles[0].is_active = True

        self.pie_crust = PieCrust(PIE_CRUST_X, PIE_CRUST_Y)
        self.spawner = IngredientSpawner(self.recipe)

        # Lists to track ingredients
        self.falling_ingredients = []
        self.ingredients_in_crust = []

        # Game state
        self.mouse_pos = (OCTOPUS_X, OCTOPUS_Y)
        self.mouse_pressed = False
        
        # Phase management
        self.instructions_phase = True
        self.prep_phase = False 
        self.prep_time_remaining = PREP_PHASE_DURATION

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
        # Instructions phase - no updates needed, waiting for user to skip
        if self.instructions_phase:
            return True
        
        # Handle prep phase
        if self.prep_phase:
            self.prep_time_remaining -= dt
            if self.prep_time_remaining <= 0:
                self.prep_phase = False
                # Reset spawner timer when exiting prep phase
                self.spawner.time_since_spawn = 0
        
        # Update timer (only counts during active phase, not instructions or prep)
        if not self.prep_phase and not self.instructions_phase:
            self.elapsed_time += dt

        # Get active tentacle
        active_tentacle = self.tentacles[self.active_tentacle_index]

        # Update active tentacle position to follow mouse (only during prep and active phases)
        if not self.instructions_phase:
            active_tentacle.set_target(self.mouse_pos)

        # Update all tentacles' physics
        for tentacle in self.tentacles:
            tentacle.update(dt)

        # Update spawner and spawn new ingredients (only after prep phase)
        if not self.prep_phase:
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
                # Grabbed ingredient follows the tentacle that grabbed it
                # Find which tentacle is holding this ingredient
                for tentacle in self.tentacles:
                    if tentacle.grabbed_object == ingredient:
                        ingredient.position = tentacle.position.copy()
                        break

        # Handle grabbing logic for active tentacle only
        if self.mouse_pressed and not active_tentacle.is_grabbing:
            # Try to grab an ingredient with active tentacle
            for ingredient in self.falling_ingredients:
                if ingredient.state == "falling" and active_tentacle.collides_with(
                    ingredient
                ):
                    # Grab this ingredient
                    active_tentacle.set_grabbing(True)
                    active_tentacle.grab_object(ingredient)
                    ingredient.set_state("grabbed")
                    break

        elif not self.mouse_pressed and active_tentacle.is_grabbing:
            # Release the grabbed ingredient from active tentacle
            released = active_tentacle.release_object()
            if released:
                active_tentacle.set_grabbing(False)

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

        # Auto-grab and auto-drop logic for inactive tentacles
        for tentacle in self.tentacles:
            if not tentacle.is_active:
                if not tentacle.is_grabbing:
                    # Try to auto-grab nearby falling ingredients
                    for ingredient in self.falling_ingredients:
                        if ingredient.state == "falling" and tentacle.collides_with(ingredient):
                            tentacle.set_grabbing(True)
                            tentacle.grab_object(ingredient)
                            ingredient.set_state("grabbed")
                            break
                else:
                    # Move toward crust with grabbed ingredient
                    tentacle.set_target(self.pie_crust.position)
                    
                    # Check if over crust - auto-drop
                    if self.pie_crust.collides_with(tentacle.grabbed_object):
                        released = tentacle.release_object()
                        if released:
                            tentacle.set_grabbing(False)
                            released.set_state("in_crust")
                            self.falling_ingredients.remove(released)
                            self.pie_crust.add_ingredient(released)
                            self.ingredients_in_crust.append(released)
                            
                            # Instant loss for inedible items
                            if released.category == "inedible":
                                self.is_active = False
                            
                            # Return to locked position
                            tentacle.set_target(tentacle.locked_position)

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

        # Draw all tentacles
        for tentacle in self.tentacles:
            tentacle.draw(screen)

        # Draw falling ingredients
        for ingredient in self.falling_ingredients:
            ingredient.draw(screen)

        # Draw UI
        self._draw_ui(screen)

    def _draw_instructions_overlay(self, screen):
        """Draw the static instructions overlay."""
        # Darker overlay since no interaction needed
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Large title
        large_font = pygame.font.Font(None, 64)
        title_text = large_font.render("HOW TO PLAY", True, (255, 255, 100))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_text, title_rect)
        
        # Instructions
        instructions = [
            "Use your octopus's 4 arms to catch ingredients!",
            "",
            "Controls:",
            "  • Press 1-4 to switch between arms",
            "  • Move mouse to control active arm",
            "  • Click to grab/release ingredients",
            "",
            "Strategy:",
            "  • Position arms strategically before time starts",
            "  • Positioned arms auto-catch nearby ingredients",
            "  • Avoid wrong ingredients and rocks!",
        ]
        
        y_offset = 240
        for instruction in instructions:
            if instruction:
                inst_text = self.small_font.render(instruction, True, (255, 255, 255))
                inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                screen.blit(inst_text, inst_rect)
            y_offset += 32
        
        # Skip prompt
        skip_font = pygame.font.Font(None, 40)
        skip_text = skip_font.render("Press SPACE to start!", True, (100, 255, 100))
        skip_rect = skip_text.get_rect(center=(SCREEN_WIDTH // 2, 540))
        screen.blit(skip_text, skip_rect)
    
    def _draw_countdown_overlay(self, screen):
        """Draw the prep phase countdown (no overlay for full visibility)."""
        # Large title
        large_font = pygame.font.Font(None, 64)
        title_text = large_font.render("POSITION YOUR ARMS!", True, (255, 255, 100))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
        screen.blit(title_text, title_rect)
        
        # Quick reminder
        reminder = "Press 1-4 to switch • Move mouse to position"
        reminder_text = self.small_font.render(reminder, True, (255, 255, 255))
        reminder_rect = reminder_text.get_rect(center=(SCREEN_WIDTH // 2, 320))
        screen.blit(reminder_text, reminder_rect)
        
        # Countdown
        countdown_font = pygame.font.Font(None, 96)
        countdown = int(self.prep_time_remaining) + 1  # Shows 5,4,3,2,1
        countdown_text = countdown_font.render(
            str(countdown),
            True,
            COLOR_TIMER
        )
        countdown_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, 420))
        screen.blit(countdown_text, countdown_rect)

    def _draw_ui(self, screen):
        """Draw UI elements like timer, score, and requirements."""
        # Draw instructions overlay if in instructions phase
        if self.instructions_phase:
            self._draw_instructions_overlay(screen)
            return
        
        # Draw countdown overlay if in prep phase
        if self.prep_phase:
            self._draw_countdown_overlay(screen)
            return  # Don't draw normal UI during prep
        
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

    def handle_key_press(self, key):
        """Handle keyboard events for tentacle switching and skipping instructions.

        Args:
            key: The pygame key constant (e.g., pygame.K_1, pygame.K_SPACE)
        """
        # Handle SPACE to skip instructions phase
        if key == pygame.K_SPACE and self.instructions_phase:
            self.instructions_phase = False
            self.prep_phase = True
            return
        
        # Switch tentacle based on number key (1-4)
        if key == pygame.K_1:
            self._switch_tentacle(0)
        elif key == pygame.K_2:
            self._switch_tentacle(1)
        elif key == pygame.K_3:
            self._switch_tentacle(2)
        elif key == pygame.K_4:
            self._switch_tentacle(3)

    def _switch_tentacle(self, index):
        """Switch to the specified tentacle.

        Args:
            index: The index of the tentacle to switch to (0-3)
        """
        if 0 <= index < NUM_TENTACLES and index != self.active_tentacle_index:
            # Lock current tentacle's position
            current_tentacle = self.tentacles[self.active_tentacle_index]
            current_tentacle.is_active = False
            current_tentacle.lock_position()

            # Activate new tentacle
            self.active_tentacle_index = index
            self.tentacles[index].is_active = True
