import pygame
import sys
from constants import *
from minigame_filling import MinigameFilling


def main():
    # Initialize pygame
    pygame.init()
    clock = pygame.time.Clock()

    print("Starting Octopied!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Octopied - Pie Filling Minigame")

    # Create the minigame
    minigame = MinigameFilling("recipes/apple_pie.json")
    minigame.start()

    # Game state
    game_complete = False
    dt = 0

    # Main game loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                # Update tentacle target position
                minigame.handle_mouse_motion(event.pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    minigame.handle_mouse_button(True)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    minigame.handle_mouse_button(False)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE and game_complete:
                    # Restart game
                    minigame = MinigameFilling("recipes/apple_pie.json")
                    minigame.start()
                    game_complete = False

        if not game_complete:
            # Update game
            continue_game = minigame.update(dt)

            # Draw game
            minigame.draw(screen)

            # Check if game is complete
            if not continue_game or minigame.is_complete():
                game_complete = True
                print("\nGame Complete!")
                summary = minigame.get_summary()
                print(f"Recipe: {summary['recipe_name']}")
                print(f"Final Score: {summary['score']}/100")
                print(f"Total ingredients collected: {summary['total_ingredients']}")
                print("\nIngredients collected:")
                for ing_type, count in summary["ingredients_collected"].items():
                    print(f"  {ing_type}: {count}")
                print("\nRequirements:")
                for ing_type, data in summary["requirements_met"].items():
                    status = "✓" if data["met"] else "✗"
                    print(
                        f"  {status} {ing_type}: {data['collected']}/{data['required']}"
                    )
        else:
            # Show game over screen
            minigame.draw(screen)

            # Draw game over overlay
            font = pygame.font.Font(None, 64)
            small_font = pygame.font.Font(None, 32)

            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            # Game Over text
            game_over_text = font.render("Pie Complete!", True, (255, 255, 255))
            game_over_rect = game_over_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
            )
            screen.blit(game_over_text, game_over_rect)

            # Score
            summary = minigame.get_summary()
            score_text = font.render(
                f"Score: {summary['score']}/100", True, COLOR_SCORE
            )
            score_rect = score_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            )
            screen.blit(score_text, score_rect)

            # Requirements summary
            y_offset = SCREEN_HEIGHT // 2 + 60
            for ing_type, data in summary["requirements_met"].items():
                color = COLOR_SCORE if data["met"] else COLOR_TIMER
                status = "✓" if data["met"] else "✗"
                req_text = small_font.render(
                    f"{status} {ing_type}: {data['collected']}/{data['required']}",
                    True,
                    color,
                )
                req_rect = req_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                screen.blit(req_text, req_rect)
                y_offset += 35

            # Instructions
            restart_text = small_font.render(
                "Press SPACE to play again", True, (200, 200, 200)
            )
            restart_rect = restart_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
            )
            screen.blit(restart_text, restart_rect)

            quit_text = small_font.render("Press ESC to quit", True, (200, 200, 200))
            quit_rect = quit_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)
            )
            screen.blit(quit_text, quit_rect)

        # Update display
        pygame.display.flip()

        # Limit to 60 FPS and get delta time
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
