import pygame
import sys
import random

# Initialize constants
CELL_SIZE = 20   # Size of each grid cell in pixels
CELL_COUNT = 20  # Number of cells horizontally and vertically (so 400x400 window)
SCREEN_WIDTH = CELL_SIZE * CELL_COUNT
SCREEN_HEIGHT = CELL_SIZE * CELL_COUNT

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0) # Default snake color

# Load background images
backgrounds = [
    pygame.image.load("images/forest.png"),
    pygame.image.load("images/desert2.jpg"),
    pygame.image.load("images/ocean.jpg"),
    pygame.image.load("images/mountain.jpg"),
    pygame.image.load("images/space.jpg")
]
current_background = 0  # Index for current background

# 1. Initialize Pygame & setup display
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# 2. Set up clock for controlling the frame rate
clock = pygame.time.Clock()

# Initialize sound
pygame.mixer.init()
pygame.mixer.music.load("Sound.mp3")  # Load background music
pygame.mixer.music.play(-1)  # Loop the music indefinitely
volume = 0.5
pygame.mixer.music.set_volume(volume)

# Game state
paused = False

def get_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# 3. Define a helper function to get a random position for the food
def get_random_food_position():
    # Randomly place food within the grid (0 <= x < CELL_COUNT, 0 <= y < CELL_COUNT)
    x = random.randint(0, CELL_COUNT - 1)
    y = random.randint(0, CELL_COUNT - 1)
    color = get_random_color()
    return (x, y, color)

def main():
    global current_background, paused, volume
    # 4. Initialize the snake
    # Snake is a list of (x, y) positions; start in the middle with length 3
    snake = [(CELL_COUNT // 2, CELL_COUNT // 2),
             (CELL_COUNT // 2 - 1, CELL_COUNT // 2),
             (CELL_COUNT // 2 - 2, CELL_COUNT // 2)]
    
    # The snake's direction (dx, dy). Start moving right.
    dx, dy = 1, 0

    # 5. Place initial food and snake color
    snake_color = GREEN
    food = get_random_food_position()

    # 6. Game loop

    # define next directions, AVOID BUG OF SNAKE GOING INTO ITSELF
    next_dx, next_dy = dx, dy
    
    #Set the mouse cursor to invisible
    #pygame.mouse.set_visible(False)

    running = True
    while running:
        clock.tick(10)  # Limit to 10 frames per second (adjust for difficulty)

        # --- EVENT HANDLING ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Prevent snake from going directly backward
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and dx != 1:
                    next_dx, next_dy = -1, 0
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and dx != -1:
                    next_dx, next_dy = 1, 0
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and dy != 1:
                    next_dx, next_dy = 0, -1
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and dy != -1:
                    next_dx, next_dy = 0, 1
                elif event.key == pygame.K_p:  # Pause toggle
                    paused = not paused
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:  # Increase volume
                    volume = min(1.0, volume + 0.1)
                    pygame.mixer.music.set_volume(volume)
                elif event.key == pygame.K_MINUS:  # Decrease volume
                    volume = max(0.0, volume - 0.1)
                    pygame.mixer.music.set_volume(volume)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 10 <= event.pos[0] <= 110 and 10 <= event.pos[1] <= 50:
                    current_background = (current_background + 1) % len(backgrounds)
        
        if paused:
            continue
        
        # Apply directions change ONCE PER FRAME
        dx, dy = next_dx, next_dy

        # --- UPDATE SNAKE ---
        # Current head position
        head_x, head_y = snake[0]
        # New head position
        new_x = head_x + dx
        new_y = head_y + dy
        new_head = (new_x, new_y)

        # No walls, snake goes through borders
        # 1. Check for collisions with walls
        if new_x < 0:
            new_head = (CELL_COUNT - 1, new_y)
        elif new_x >= CELL_COUNT:
            new_head = (0, new_y)
        elif new_y < 0:
            new_head = (new_x, CELL_COUNT - 1)
        elif new_y >= CELL_COUNT:
            new_head = (new_x, 0)

        # 2. Check for collisions with self
        if new_head in snake:
            # Hit itself -> Game Over
            running = False

        # Walls around the borders
        #if (new_x < 0 or new_x >= CELL_COUNT or new_y < 0 or new_y >= CELL_COUNT) or new_head in snake:
        #    running = False

        # If still safe, insert new head
        snake.insert(0, new_head)

        # 3. Check if we ate the food
        if new_head == (food[0], food[1]):
            snake_color = food[2] # changes snake color based on food
            # Generate a new food position; don't pop the tail (snake grows)
            temp_food = get_random_food_position()
            while temp_food in snake or temp_food is new_head:
                temp_food = get_random_food_position()
            food = temp_food
        else:
            # Move forward (remove the tail)
            snake.pop()

        # --- DRAW EVERYTHING ---
        screen.blit(pygame.transform.scale(backgrounds[current_background], (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

        # Draw the snake
        for x, y in snake:
            pygame.draw.rect(screen, snake_color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw the food
        pygame.draw.rect(screen, food[2], (food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw buttons
        pygame.draw.rect(screen, WHITE, (10, 10, 100, 40))
        font = pygame.font.Font(None, 24)
        screen.blit(font.render("Change BG", True, BLACK), (20, 20))
        
        pygame.draw.rect(screen, WHITE, (120, 10, 80, 40))
        screen.blit(font.render("Pause", True, BLACK), (140, 20))
        
        pygame.display.flip()

    # Once we exit the loop, the game is over
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()