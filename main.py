import pygame  # Importing pygame
import os  # Importing OS

pygame.font.init()  # Font initialization
pygame.mixer.init()  # Initialize the Sound effects Library

WIDTH, HEIGHT = 900, 500  # Game Dimensions
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Window to display the game
pygame.display.set_caption("Space Shooter Game")  # Game Title

WHITE = (255, 255, 255)  # Define white color
BLACK = (0, 0, 0)  # Define black color
RED = (255, 0, 0)  # Define red color
YELLOW = (255, 255, 0)  # Define yellow color
BORDER = pygame.Rect(
    (WIDTH // 2) - 5, 0, 10, HEIGHT
)  # ((X value) (Y value) (LENGTH of Width) (Length of Height))

BULLET_HIT_SOUND = pygame.mixer.Sound(
    os.path.join("Assets", "Grenade+1.mp3")
)  # Sound Effects
BULLET_FIRE_SOUND = pygame.mixer.Sound(
    os.path.join("Assets", "Gun+Silencer.mp3")
)  # Sound Effects

FPS = 60  # Game runs at 60 FPS
VELOCITY = 5  # Ship Velocity
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40  # Ships Height & Width

YELLOW_HIT = pygame.USEREVENT + 1  # Custom Event types for yellow player being hit
RED_HIT = pygame.USEREVENT + 2  # Custom Event types for yellow player being hit

HEALTH_FONT = pygame.font.SysFont(
    "comicsans", 40
)  # Font of the health at the top of the screen
WINNER_FONT = pygame.font.SysFont(
    "comicsans", 100
)  # Font of the the winner screen at the end of the game

BULLET_VELOCITY = 9  # Velocity of the bullet
MAX_BULLETS = 5  # Max bullets per player at a single time


SPACE = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT)
)  # load the background image of space

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_yellow.png")
)  # load the image of Yellow Spaceship

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))  # load the image of Red Spaceship

YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    90,
)       # Rotate the Yellow Spaceship

RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    270,
)       # Rotate the Red Spaceship


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):           # drawing Window
    WIN.blit(SPACE, (0, 0))                     # Draws the image of space from the top left part of the WIN screen
    pygame.draw.rect(WIN, BLACK, BORDER)        # Draw the background border in the middle of the screen

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)        # Renders and shows the current health for red at the top of the screen, Anti-aliasing, color white
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)  # Renders and shows the current health for yellow at the top of the screen, Anti-aliasing, color white
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))       # Location of where the red health text is displayed
    WIN.blit(yellow_health_text, (10, 10))                                          # Location of where the yellow health text is displayed

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))                # Drawing Yellow ship at location x and y that depends on user input
    WIN.blit(RED_SPACESHIP, (red.x, red.y))                         # Drawing Red ship at location x and y that depends on user input
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)                          # Draw each Red bullet on the screen
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)                       # Draw each Yellow bullet on the screen
    pygame.display.update()                                         # Refresh the display to show all drawn elements 


def draw_winner(text):                  # Draw the text at the end of the game when there is a winner
    draw_text = WINNER_FONT.render(text, 1, WHITE)          # Render the winner text, Anti-aliasing = 1, color = white
    WIN.blit(
        draw_text,
        (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height()),
    )           # Draw the text centered in the middle of the screen
    pygame.display.update()     # Update the screen to show this winner text
    pygame.time.delay(4000)     # Cause the screen to show for 4000 ms (4 Seconds)


def yellow_handling_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0:  # Left for yellow
        yellow.x -= VELOCITY
    if (
        keys_pressed[pygame.K_d] and yellow.x + VELOCITY + yellow.width < BORDER.x
    ):  # Right for yellow
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0:  # Up for yellow
        yellow.y -= VELOCITY
    if (
        keys_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT - 15
    ):  # Down for yellow
        yellow.y += VELOCITY


def red_handling_movement(keys_pressed, red):
    if (
        keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width
    ):  # Left for Red
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + VELOCITY + red.width < WIDTH:  # Right for Red
        red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0:  # Up for Red
        red.y -= VELOCITY
    if (
        keys_pressed[pygame.K_DOWN] and red.y + VELOCITY + red.height < HEIGHT - 15
    ):  # Down for Red
        red.y += VELOCITY


def handle_bullets(yellow_bullets, red_bullets, yellow, red):       # Function to handle the movement of bullets and collisions
    for bullet in yellow_bullets:                                   # Loop through each bullet in the yellow bullets list
        bullet.x += BULLET_VELOCITY                                 # Move the bullet to the right by the bullet velocity
        if red.colliderect(bullet):                                 # Check if the bullet collides with the red spaceship
            pygame.event.post(pygame.event.Event(RED_HIT))          # Post a RED_HIT event if collision occurs
            yellow_bullets.remove(bullet)                           # Remove the bullet from the yellow bullets list if it hits the red spaceship
        elif bullet.x > WIDTH:                                      # Check if the bullet has moved off the screen to the right
            yellow_bullets.remove(bullet)                           # Remove the bullet from the yellow bullets list if it is off the screen

    for bullet in red_bullets:                                      # Loop through each bullet in the red bullets list
        bullet.x -= BULLET_VELOCITY                                 # Move the bullet to the right by the bullet velocity
        if yellow.colliderect(bullet):                              # Check if the bullet collides with the yellow spaceship
            pygame.event.post(pygame.event.Event(YELLOW_HIT))       # Post a YELLOW_HIT event if collision occurs
            red_bullets.remove(bullet)                              # Remove the bullet from the red bullets list if it hits the yellow spaceship
        elif bullet.x < 0:                                          # Check if the bullet has moved off the screen to the left
            red_bullets.remove(bullet)                              # Remove the bullet from the red bullets list if it is off the screen


def main():

    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)              # Set the red spaceship's starting position and size
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)           # Set the yellow spaceship's starting position and size

    clock = pygame.time.Clock()                                                 # Create a clock object to manage the game's frame rate
    run = True                                                                  # Variable to control the main game loop, set to True to start the loop

    red_health = 10                                                             # Initial health for the red spaceship
    yellow_health = 10                                                          # Initial health for the yellow spaceship

    yellow_bullets = []                                                         # List to store the yellow bullets currently on the screen
    red_bullets = []                                                            # List to store the red bullets currently on the screen

    while run:
        clock.tick(FPS)                                                         # Run the game at specific FPS
        for event in pygame.event.get():                                        # Loop through all events in the event queue
            if event.type == pygame.QUIT:                                       # Check if the user has requested to close the window
                run = False                                                     # Set the run variable to False to exit the main game loop
                pygame.quit()                                                   # Quit the Pygame library properly

            if event.type == pygame.KEYDOWN:                                                    # Event type is created depending on the user input
                if event.key == pygame.K_SPACE and len(yellow_bullets) < MAX_BULLETS:           # When space is clicked and length of yellow bullets is less than the MAX_BULLETS do the following
                    bullet = pygame.Rect(
                        yellow.x + yellow.width,                                                # Position the bullet at the right edge of the yellow spaceship 
                        yellow.y + yellow.height // 2 - 2,                                      # Center the bullet vertically relative to the yellow spaceship
                        10,                                                                     # Set the bullet's width
                        5,                                                                      # Set the bullet's height
                    )                                                                           # Create a new bullet rectangle positioned at the front of the yellow spaceship
                    yellow_bullets.append(bullet)                                               # Add the yellow bullets to yellow bullets list
                    BULLET_FIRE_SOUND.play()                                                    # Play the sound effect for firing a bullet

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:              # When space is clicked and length of red bullets is less than the MAX_BULLETS do the following
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)             # Create a bullet for the red spaceship at (x position, y position, width, height)
                    red_bullets.append(bullet)                                                  # Add the red bullets to red bullets list
                    BULLET_FIRE_SOUND.play()                                                    # Play the sound effect for firing a bullet

            if event.type == RED_HIT:                                                           # If the red ship is hit do the following
                red_health -= 1                                                                 # Decrease the health of the red ship by 1
                BULLET_HIT_SOUND.play()                                                         # Play the sound effect for being hit

            if event.type == YELLOW_HIT:                                                        # If the yellow ship is hit do the following
                yellow_health -= 1                                                              # Decrease the health of the yellow ship by 1
                BULLET_HIT_SOUND.play()                                                         # Play the sound effect for being hit

        winner_text = ""                                                                        # Empty text to display for the winner at the end screen

        if red_health <= 0:                                                                     # If health of red reaches 0 do the following
            winner_text = "Yellow Wins!"                                                        # Change the winner_text to say Yellow wins

        if yellow_health <= 0:                                                                  # If health of yellow reaches 0 do the following
            winner_text = "Red Wins!"                                                           # Change the winner_text to say red wins

        if winner_text != "":                                                                   # If there is a winner (winner_text is not empty)
            draw_winner(winner_text)                                                            # Call the function to display the winner text
            break                                                                               # Exit the game loop

        keys_pressed = pygame.key.get_pressed()                                                 # Get the current state of all keyboard keys
        yellow_handling_movement(keys_pressed, yellow)                                          # Update the yellow spaceship's position based on key presses
        red_handling_movement(keys_pressed, red)                                                # Update the red spaceship's position based on key presses

        handle_bullets(yellow_bullets, red_bullets, yellow, red)                                # Update bullet positions and check for collisions

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)        # Draw all game elements on the screen

    main()                                                                                      # Restart the main function to run the game again

if __name__ == "__main__":                                                                      # Check if this script is being run directly 
    main()                                                                                      # Call the main function to start the game
