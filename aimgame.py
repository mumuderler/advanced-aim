import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mirror Shooting Game")
clock = pygame.time.Clock()

# Counters and flags
successful_clicks = 0
failed_clicks = 0
attempts = 0
game_start_time = None
game_over = False
game_started = False
difficulty_level = None  # Difficulty level: 'easy', 'medium', 'hard'

# Function to generate a new target based on difficulty level
def generate_new_target(difficulty_level):
    if difficulty_level == 'easy':
        return [random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH - 25),
                random.randint(25, SCREEN_HEIGHT - 25)]
    elif difficulty_level == 'medium':
        return [random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH - 20),
                random.randint(20, SCREEN_HEIGHT - 20)]
    elif difficulty_level == 'hard':
        return [random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH - 10),
                random.randint(10, SCREEN_HEIGHT - 10)]

# Function to draw the opening page
def draw_opening_page():
    screen.fill(WHITE)

    # Draw "Mumuderler" text in the right bottom corner
    font_mumuderler = pygame.font.Font(None, 12)
    text_mumuderler = font_mumuderler.render("Mumuderler", True, BLACK)
    text_rect_mumuderler = text_mumuderler.get_rect(bottomright=(SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(text_mumuderler, text_rect_mumuderler)

    # Draw difficulty level buttons
    font_difficulty = pygame.font.Font(None, 24)
    text_easy = font_difficulty.render("Easy", True, BLACK)
    text_medium = font_difficulty.render("Medium", True, BLACK)
    text_hard = font_difficulty.render("Hard", True, BLACK)

    text_rect_easy = text_easy.get_rect(center=(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 100))
    text_rect_medium = text_medium.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    text_rect_hard = text_hard.get_rect(center=(3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 100))

    pygame.draw.rect(screen, WHITE, text_rect_easy)
    pygame.draw.rect(screen, WHITE, text_rect_medium)
    pygame.draw.rect(screen, WHITE, text_rect_hard)

    screen.blit(text_easy, text_rect_easy)
    screen.blit(text_medium, text_rect_medium)
    screen.blit(text_hard, text_rect_hard)

    return text_rect_easy, text_rect_medium, text_rect_hard

# Function to draw the start button
def draw_start_button():
    start_button_radius = 30
    start_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - start_button_radius,
                                     SCREEN_HEIGHT // 2 - start_button_radius,
                                     start_button_radius * 2,
                                     start_button_radius * 2))
    pygame.draw.circle(screen, BLUE, start_button_rect.center, start_button_radius)
    font_start = pygame.font.Font(None, 36)
    text_start = font_start.render("Start", True, WHITE)
    text_rect_start = text_start.get_rect(center=start_button_rect.center)
    screen.blit(text_start, text_rect_start)

    return start_button_rect

# Function to draw the end screen with results and restart button
def draw_end_screen():
    font = pygame.font.Font(None, 36)
    text_clicks = font.render(f"Total Clicks: {attempts}", True, BLACK)
    text_successful_clicks = font.render(f"Successful Clicks: {successful_clicks}", True, BLACK)
    text_failed_clicks = font.render(f"Failed Clicks: {failed_clicks}", True, BLACK)
    text_time = font.render(f"Time: {time_spent} seconds", True, BLACK)

    text_rect_clicks = text_clicks.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    text_rect_successful_clicks = text_successful_clicks.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    text_rect_failed_clicks = text_failed_clicks.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    text_rect_time = text_time.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    screen.blit(text_clicks, text_rect_clicks)
    screen.blit(text_successful_clicks, text_rect_successful_clicks)
    screen.blit(text_failed_clicks, text_rect_failed_clicks)
    screen.blit(text_time, text_rect_time)

    restart_button = pygame.Rect(300, 400, 200, 50)
    pygame.draw.rect(screen, RED, restart_button)
    text_restart = font.render("Restart", True, WHITE)
    text_rect_restart = text_restart.get_rect(center=restart_button.center)
    screen.blit(text_restart, text_rect_restart)

    return restart_button

# Main game loop
text_easy_rect, text_medium_rect, text_hard_rect = draw_opening_page()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if not game_started:
                # Check if the mouse click is within the difficulty level buttons on the opening page
                if text_easy_rect.collidepoint(mouse_x, mouse_y):
                    difficulty_level = 'easy'
                elif text_medium_rect.collidepoint(mouse_x, mouse_y):
                    difficulty_level = 'medium'
                elif text_hard_rect.collidepoint(mouse_x, mouse_y):
                    difficulty_level = 'hard'

                # Check if the mouse click is within the start button on the opening page
                if text_easy_rect.collidepoint(mouse_x, mouse_y) or \
                   text_medium_rect.collidepoint(mouse_x, mouse_y) or \
                   text_hard_rect.collidepoint(mouse_x, mouse_y):
                    game_started = True
                    target_pos = generate_new_target(difficulty_level)
                    target_radius = 25 if difficulty_level == 'easy' else (20 if difficulty_level == 'medium' else 10)
                    start_button_rect = draw_start_button()
            else:
                # Check if the mouse click is within the left side of the screen
                if mouse_x < SCREEN_WIDTH // 2:
                    # Mirror the click to (600, 100) on the right side
                    mirrored_x = SCREEN_WIDTH // 2 + mouse_x
                    mirrored_y = mouse_y
                    # Check if the mirrored click is within the target on the right side
                    if SCREEN_WIDTH // 2 <= mirrored_x <= target_pos[0] + target_radius and \
                            target_pos[1] - target_radius <= mirrored_y <= target_pos[1] + target_radius:
                        target_pos = generate_new_target(difficulty_level)
                        successful_clicks += 1
                        attempts += 1
                        # Start the timer on the first successful click
                        if successful_clicks == 1:
                            game_start_time = time.time()
                        # Check if the game is finished
                        if successful_clicks == 5:
                            game_over = True
                            # Stop the timer when the game is over
                            game_end_time = time.time()
                            time_spent = round(game_end_time - game_start_time, 2)
                    else:
                        # Increment failed clicks when the click is outside the target
                        failed_clicks += 1
                        attempts += 1

    if not game_started:
        text_easy_rect, text_medium_rect, text_hard_rect = draw_opening_page()
    else:
        # Draw everything
        screen.fill(WHITE)

        # Draw target on the right side
        pygame.draw.circle(screen, RED, (target_pos[0], target_pos[1]), target_radius)

        # Draw mirror line
        pygame.draw.line(screen, RED, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 2)

        if game_over:
            # Display end screen with table and restart button
            restart_button = draw_end_screen()

            # Check for restart button click
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if restart_button.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0]:
                # Reset game variables
                successful_clicks = 0
                failed_clicks = 0
                attempts = 0
                game_start_time = None
                game_over = False
                game_started = False
                difficulty_level = None
                text_easy_rect, text_medium_rect, text_hard_rect = draw_opening_page()
        else:
            # Draw "Mumuderler" text in the right bottom corner
            font_mumuderler = pygame.font.Font(None, 12)
            text_mumuderler = font_mumuderler.render("Mumuderler", True, BLACK)
            text_rect_mumuderler = text_mumuderler.get_rect(bottomright=(SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(text_mumuderler, text_rect_mumuderler)

    pygame.display.flip()
    clock.tick(FPS)
