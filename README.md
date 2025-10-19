# 🐙 Octopied

A cozy Cooking Mama-style game where you play as an octopus chef baking pies through interactive minigames!

## About

Use the octopus's flexible tentacles to complete a series of fun, interactive minigames that simulate the pie-making process. Each successful pie earns you points based on how well you follow the recipe!

The game is built with Python and Pygame, featuring smooth physics-based tentacle controls and a recipe system that makes it easy to create new challenges.

### Current Status

✅ **Pie Filling Minigame** - Fully functional with geometric shapes (sprite graphics coming soon!)  
🚧 Coming Soon: Mixing, Rolling, Oven, and Decorating minigames

## Getting Started

### Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd octopied-game
   ```

2. **Create a virtual environment**

   ```bash
   uv venv
   ```

3. **Activate the virtual environment**

   ```bash
   source .venv/bin/activate  # On macOS/Linux
   # or
   .venv\Scripts\activate     # On Windows
   ```

4. **Install dependencies**

   ```bash
   uv add pygame==2.6.1
   ```

5. **Run the game**
   ```bash
   uv run python main.py
   ```

## How to Play

### Objective

Help the octopus chef collect the right ingredients to make a delicious pie! Each recipe has specific requirements - gather the correct ingredients while avoiding unwanted items.

### Controls

- **Mouse Movement**: Control the octopus tentacle - it will smoothly follow your cursor
- **Left Click (Hold)**: Grab an ingredient when the tentacle touches it
- **Left Click (Release)**: Drop the ingredient into the pie crust below
- **ESC**: Quit the game
- **SPACE** (on game over screen): Play again

### Gameplay & Scoring

You have **20 seconds** to catch ingredients and earn **0-100 points**:

- ✅ **Correct ingredients**: +10-15 points each
- 🎯 **Complete recipe requirements**: +50 bonus points
- ⚠️ **Wrong ingredients** (e.g., berries in apple pie): -5 points
- 💀 **Inedible items** (rocks): Instant game over!

**Tips**: Watch the requirements on the left side of the screen, and drop ingredients carefully into the pie crust to avoid missing them.

## Creating Custom Recipes

You can create new recipes by adding JSON files to the `recipes/` directory. Here's the format:

```json
{
  "name": "Your Pie Name",
  "duration": 20,
  "required_ingredients": {
    "ingredient1": 5,
    "ingredient2": 2
  },
  "allowed_ingredients": {
    "ingredient1": {
      "points": 10,
      "category": "good"
    },
    "ingredient2": {
      "points": 15,
      "category": "good"
    },
    "bad_item": {
      "points": -5,
      "category": "bad"
    },
    "dangerous_item": {
      "points": -20,
      "category": "inedible"
    }
  },
  "spawn_rates": {
    "ingredient1": 0.4,
    "ingredient2": 0.2,
    "bad_item": 0.2,
    "dangerous_item": 0.2
  }
}
```

**Note**: You'll also need to add color mappings in `recipe.py` for new ingredient types.

## Technologies

Python 3.13 • Pygame 2.6.1 • uv

## Future Features

The complete Octopied experience will include five minigames:

1. 🚧 **Mixing** - Rotate mouse around bowl to mix ingredients
2. 🚧 **Rolling** - Drag horizontally to roll dough evenly
3. ✅ **Filling** - Catch falling ingredients (Current)
4. 🚧 **Oven** - Adjust temperature dial to bake perfectly
5. 🚧 **Decorating** - Draw frosting patterns on the finished pie

Each minigame will last 15-25 seconds and contribute to your final pie score!

## Contributing

This is a learning project, but suggestions and feedback are welcome! Feel free to:

- Report bugs
- Suggest new recipes
- Propose new minigame ideas
- Share your high scores

## License

This project is open source and available for educational purposes.

---

**Enjoy baking with your octopus friend! 🐙🥧**
