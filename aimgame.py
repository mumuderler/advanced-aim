import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 200)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)
TURQUOISE = (64, 224, 208)
EMERALD = (46, 204, 113)
TRANSPARENT_BLACK = (0, 0, 0, 128)  # Transparent black color


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
aim_color = RED  # Default aim color

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
    screen.fill(YELLOW)

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

    button_radius = 50
    circle_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    #Game title
    font_title = pygame.font.Font(None, 48)
    text_title = font_title.render('Mirrored Aim', True, RED)
    pygame.draw.rect(screen, ORANGE, pygame.Rect(circle_center[0]-125, circle_center[1]/2-50, 250, 100))
    text_rect_title = text_title.get_rect(center=(circle_center[0], circle_center[1]/2))
    screen.blit(text_title, text_rect_title)

    # Easy button
    easy_button_rect = pygame.Rect((circle_center[0] - button_radius-120, circle_center[1] - button_radius - 100),
                                   (button_radius * 2, button_radius * 2))
    pygame.draw.circle(screen, WHITE, (circle_center[0]-120, circle_center[1]-100), button_radius)
    pygame.draw.rect(screen, BLACK, easy_button_rect, 3)
    text_rect_easy = text_easy.get_rect(center=(circle_center[0]-120, circle_center[1]-100))
    screen.blit(text_easy, text_rect_easy)

    # Medium button
    medium_button_rect = pygame.Rect((circle_center[0] - button_radius, circle_center[1] - button_radius - 100),
                                     (button_radius * 2, button_radius * 2))
    pygame.draw.circle(screen, WHITE, (circle_center[0], circle_center[1]-100), button_radius)
    pygame.draw.rect(screen, BLACK, medium_button_rect, 3)
    text_rect_medium = text_medium.get_rect(center=(circle_center[0], circle_center[1]-100))
    screen.blit(text_medium, text_rect_medium)

    # Hard button
    hard_button_rect = pygame.Rect((circle_center[0] - button_radius+120, circle_center[1] - button_radius - 100),
                                   (button_radius * 2, button_radius * 2))
    pygame.draw.circle(screen, WHITE, (circle_center[0]+120, circle_center[1]-100), button_radius)
    pygame.draw.rect(screen, BLACK, hard_button_rect, 3)
    text_rect_hard = text_hard.get_rect(center=(circle_center[0]+120, circle_center[1]-100))
    screen.blit(text_hard, text_rect_hard)



    # Draw aim color selection buttons
    font_color = pygame.font.Font(None, 24)
    text_red = font_color.render("Red", True, BLACK)
    text_blue = font_color.render("Blue", True, BLACK)
    text_yellow = font_color.render("Yellow", True, BLACK)
    text_orange = font_color.render("Orange", True, BLACK)
    text_black = font_color.render("Black", True, WHITE)
    text_emerald = font_color.render("Emerald", True, WHITE)

    color_button_width = 80
    color_button_height = 50
    color_button_spacing = 20

    # Red button
    red_button_rect = pygame.Rect((SCREEN_WIDTH // 4 - color_button_width // 2,
                                   SCREEN_HEIGHT // 2 + color_button_spacing),
                                  (color_button_width, color_button_height))
    pygame.draw.rect(screen, RED, red_button_rect)
    pygame.draw.rect(screen, BLACK, red_button_rect, 2)
    text_rect_red = text_red.get_rect(center=red_button_rect.center)
    screen.blit(text_red, text_rect_red)

    # Blue button
    blue_button_rect = pygame.Rect((SCREEN_WIDTH // 4 * 2 - color_button_width // 2,
                                    SCREEN_HEIGHT // 2 + color_button_spacing),
                                   (color_button_width, color_button_height))
    pygame.draw.rect(screen, BLUE, blue_button_rect)
    pygame.draw.rect(screen, BLACK, blue_button_rect, 2)
    text_rect_blue = text_blue.get_rect(center=blue_button_rect.center)
    screen.blit(text_blue, text_rect_blue)

    # Yellow button
    yellow_button_rect = pygame.Rect((SCREEN_WIDTH // 4 * 3 - color_button_width // 2,
                                      SCREEN_HEIGHT // 2 + color_button_spacing),
                                     (color_button_width, color_button_height))
    pygame.draw.rect(screen, YELLOW, yellow_button_rect)
    pygame.draw.rect(screen, BLACK, yellow_button_rect, 2)
    text_rect_yellow = text_yellow.get_rect(center=yellow_button_rect.center)
    screen.blit(text_yellow, text_rect_yellow)

    # Orange button
    orange_button_rect = pygame.Rect((SCREEN_WIDTH // 4 - color_button_width // 2,
                                      SCREEN_HEIGHT // 2 + color_button_spacing * 2 + color_button_height),
                                     (color_button_width, color_button_height))
    pygame.draw.rect(screen, ORANGE, orange_button_rect)
    pygame.draw.rect(screen, BLACK, orange_button_rect, 2)
    text_rect_orange = text_orange.get_rect(center=orange_button_rect.center)
    screen.blit(text_orange, text_rect_orange)

    # Black button
    black_button_rect = pygame.Rect((SCREEN_WIDTH // 4 * 2 - color_button_width // 2,
                                     SCREEN_HEIGHT // 2 + color_button_spacing * 2 + color_button_height),
                                    (color_button_width, color_button_height))
    pygame.draw.rect(screen, BLACK, black_button_rect)
    pygame.draw.rect(screen, BLACK, black_button_rect, 2)
    text_rect_black = text_black.get_rect(center=black_button_rect.center)
    screen.blit(text_black, text_rect_black)

    # Emerald button
    emerald_button_rect = pygame.Rect((SCREEN_WIDTH // 4 * 3 - color_button_width // 2,
                                     SCREEN_HEIGHT // 2 + color_button_spacing * 2 + color_button_height),
                                    (color_button_width, color_button_height))
    pygame.draw.rect(screen, EMERALD, emerald_button_rect)
    pygame.draw.rect(screen, EMERALD, emerald_button_rect, 2)
    text_rect_emerald = text_emerald.get_rect(center=emerald_button_rect.center)
    screen.blit(text_emerald, text_rect_emerald)

    # Function to draw the start button
    start_button_radius = 60
    start_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - start_button_radius,
                                     SCREEN_HEIGHT * 3 // 4  - start_button_radius,
                                     start_button_radius * 2,
                                     start_button_radius * 2))
    pygame.draw.circle(screen, EMERALD, start_button_rect.center, start_button_radius)
    font_start = pygame.font.Font(None, 36)
    text_start = font_start.render("Start", True, WHITE)
    text_rect_start = text_start.get_rect(center=start_button_rect.center)
    screen.blit(text_start, text_rect_start)

    return easy_button_rect, medium_button_rect, hard_button_rect, \
           red_button_rect, blue_button_rect, yellow_button_rect, \
            orange_button_rect, black_button_rect, start_button_rect, emerald_button_rect

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

    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT * 3 // 4, 200, 50)
    pygame.draw.rect(screen, RED, restart_button)
    text_restart = font.render("Restart", True, WHITE)
    text_rect_restart = text_restart.get_rect(center=restart_button.center)
    screen.blit(text_restart, text_rect_restart)

    return restart_button

def draw_pause(screen):
    # Draw "GAME PAUSED" text in the middle of the screen when game is paused
    font = pygame.font.Font(None, 36)
    paused_surface = pygame.Surface((SCREEN_WIDTH // 2, SCREEN_HEIGHT//2), pygame.SRCALPHA)  # Create transparent surface
    paused_surface.fill(TRANSPARENT_BLACK)  # Fill surface with transparent black
    paused_text = font.render("GAME PAUSED", True, WHITE)
    paused_text_rect = paused_text.get_rect(center=(SCREEN_WIDTH //4, SCREEN_HEIGHT//4))
    paused_surface.blit(paused_text, paused_text_rect)  # Blit text onto surface
    screen.blit(paused_surface, (SCREEN_WIDTH //4, SCREEN_HEIGHT//4))  # Blit surface onto main screen
    pygame.display.flip()  # Update the display


    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
                    screen.fill(WHITE)  # Clear the screen
                    pygame.display.flip()  # Update the display

# Main game loop
easy_button_rect, medium_button_rect, hard_button_rect, \
red_button_rect, blue_button_rect, yellow_button_rect, \
orange_button_rect, black_button_rect, start_button_rect, emerald_button_rect = draw_opening_page()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if not game_started and event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click is within the difficulty level buttons on the opening page
                if easy_button_rect.collidepoint(mouse_x, mouse_y):
                    difficulty_level = 'easy'
                elif medium_button_rect.collidepoint(mouse_x, mouse_y):
                    difficulty_level = 'medium'
                elif hard_button_rect.collidepoint(mouse_x, mouse_y):
                    difficulty_level = 'hard'

                # Check if the mouse click is within the aim color selection buttons on the opening page
                if red_button_rect.collidepoint(mouse_x, mouse_y):
                    aim_color = RED
                elif blue_button_rect.collidepoint(mouse_x, mouse_y):
                    aim_color = BLUE
                elif yellow_button_rect.collidepoint(mouse_x, mouse_y):
                    aim_color = YELLOW
                elif orange_button_rect.collidepoint(mouse_x, mouse_y):
                    aim_color = ORANGE
                elif black_button_rect.collidepoint(mouse_x, mouse_y):
                    aim_color = BLACK
                elif emerald_button_rect.collidepoint(mouse_x, mouse_y):
                    aim_color = EMERALD    

                # Check if both difficulty level and color have been chosen before activating the start button
                if difficulty_level and aim_color and start_button_rect.collidepoint(mouse_x, mouse_y):
                    game_started = True
                    target_pos = generate_new_target(difficulty_level)
                    target_radius = 25 if difficulty_level == 'easy' else (20 if difficulty_level == 'medium' else 10)
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
        elif event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_ESCAPE:  # Pause the game when "escape" key is pressed
                draw_pause(screen)
    
            if event.key == pygame.K_SPACE:  # Resume the game when "space" key is pressed
                game_started = True
                # No need to reset game variables, just resume the game    

    if not game_started:
        easy_button_rect, medium_button_rect, hard_button_rect, \
        red_button_rect, blue_button_rect, yellow_button_rect, \
        orange_button_rect, black_button_rect, start_button_rect, emerald_button_rect = draw_opening_page()

    else:
        # Draw everything
        screen.fill(TURQUOISE)

        # Draw target on the right side
        pygame.draw.circle(screen, aim_color, (target_pos[0], target_pos[1]), target_radius)

        # Draw mirror line
        pygame.draw.line(screen, aim_color, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 2)

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
                easy_button_rect, medium_button_rect, hard_button_rect, \
                red_button_rect, blue_button_rect, yellow_button_rect, orange_button_rect, \
                black_button_rect, start_button_rect, emerald_button_rect = draw_opening_page()

        else:
            # Draw "Mumuderler" text in the right bottom corner
            font_mumuderler = pygame.font.Font(None, 12)
            text_mumuderler = font_mumuderler.render("Mumuderler", True, BLACK)
            text_rect_mumuderler = text_mumuderler.get_rect(bottomright=(SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(text_mumuderler, text_rect_mumuderler)

    pygame.display.flip()
    clock.tick(FPS)
    
# Quit Pygame
pygame.quit()
sys.exit()
