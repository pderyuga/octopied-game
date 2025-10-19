# Game constants for Octopied

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Colors (RGB)
COLOR_BACKGROUND = (230, 240, 255)  # Light blue background
COLOR_OCTOPUS = (255, 100, 150)  # Pink octopus
COLOR_TENTACLE = (255, 130, 170)  # Lighter pink tentacle
COLOR_CRUST = (210, 180, 140)  # Tan pie crust
COLOR_APPLE = (200, 50, 50)  # Red apple
COLOR_BERRY = (100, 50, 150)  # Purple berry
COLOR_CINNAMON = (139, 69, 19)  # Brown cinnamon
COLOR_ROCK = (100, 100, 100)  # Gray rock
COLOR_UI_TEXT = (50, 50, 50)  # Dark gray text
COLOR_TIMER = (255, 100, 100)  # Red timer
COLOR_SCORE = (50, 200, 50)  # Green score

# Octopus settings
OCTOPUS_X = SCREEN_WIDTH // 2  # Center horizontally
OCTOPUS_Y = SCREEN_HEIGHT // 2  # Center vertically
OCTOPUS_RADIUS = 40

# Tentacle settings
TENTACLE_TIP_RADIUS = 15
TENTACLE_SMOOTHING = 8.0  # Lower = faster, higher = smoother
TENTACLE_GRAB_HIGHLIGHT = (255, 200, 220)  # Color when grabbing

# Pie crust settings
PIE_CRUST_X = SCREEN_WIDTH // 2  # Center horizontally
PIE_CRUST_Y = 600  # Below octopus
PIE_CRUST_WIDTH = 200
PIE_CRUST_HEIGHT = 60

# Ingredient settings
INGREDIENT_RADIUS = 20
INGREDIENT_FALL_SPEED = 150  # Pixels per second
INGREDIENT_SPAWN_Y = -INGREDIENT_RADIUS  # Spawn above screen
INGREDIENT_SPAWN_INTERVAL = 1.5  # Seconds between spawns

# Minigame settings
MINIGAME_DURATION = 20  # Seconds
MINIGAME_MAX_SCORE = 100

# Physics
GRAVITY = 0  # Not using gravity, constant fall speed

# UI settings
UI_MARGIN = 20
UI_FONT_SIZE = 32
UI_SMALL_FONT_SIZE = 24
