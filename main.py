import pygame
import random

# Initialize pygame
pygame.init()

# Game window dimensions
WIDTH, HEIGHT = 400, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy X-Wing")

# Load assets
background = pygame.image.load("background.jpg")
x_wing = pygame.image.load("x-wing.png")
x_wing = pygame.transform.scale(x_wing, (50, 35))
star_destroyer = pygame.image.load("star-destroyer.png")
star_destroyer = pygame.transform.scale(star_destroyer, (70, 400))

# Set up game variables
clock = pygame.time.Clock()
FPS = 20
GRAVITY = 0.6
FLAP_STRENGTH = -9
x_wing_x, x_wing_y = 50, HEIGHT // 2
x_wing_velocity = 0
score = 0
font = pygame.font.Font(pygame.font.get_default_font(), 36)

# Pipes (Star Destroyers) variables
gap = 150
pipe_width = 70
pipe_velocity = 5
pipes = []


# Add the first pipe
def create_pipe():
    height = random.randint(100, HEIGHT - 200)
    pipe_top = pygame.Rect(WIDTH, height - gap - 400, pipe_width, 400)
    pipe_bottom = pygame.Rect(WIDTH, height, pipe_width, 400)
    return pipe_top, pipe_bottom


pipes.append(create_pipe())


# Check for collisions
def check_collision():
    x_wing_rect = pygame.Rect(x_wing_x, x_wing_y, 50, 35)
    for pipe_top, pipe_bottom in pipes:
        # Check if the X-Wing collides with the top or bottom pipe
        if x_wing_rect.colliderect(pipe_top) or x_wing_rect.colliderect(pipe_bottom):
            return True
    # Check if the X-Wing touches the top of the screen (Y < 0) or goes below the screen (Y > HEIGHT)
    if x_wing_y < 0 or x_wing_y > HEIGHT:
        return True
    return False


# Game loop
running = True
game_over = False
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE:
                x_wing_velocity = FLAP_STRENGTH

    # Apply gravity
    if not game_over:
        x_wing_velocity += GRAVITY
        x_wing_y += x_wing_velocity

        # Move pipes
        for i in range(len(pipes)):
            pipes[i][0].x -= pipe_velocity
            pipes[i][1].x -= pipe_velocity

        # Add new pipes
        if pipes[-1][0].x < WIDTH // 2:
            pipes.append(create_pipe())

        # Remove pipes
        if pipes[0][0].x < -pipe_width:
            pipes.pop(0)
            score += 1

        # Check for collisions
        if check_collision():
            game_over = True

    # Draw background, x-wing, and pipes
    window.blit(background, (0, 0))
    window.blit(x_wing, (x_wing_x, x_wing_y))

    for pipe_top, pipe_bottom in pipes:
        window.blit(star_destroyer, pipe_top)
        window.blit(star_destroyer, pipe_bottom)

    # Draw score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    window.blit(score_text, (10, 10))

    # Game over text
    if game_over:
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        window.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))

    pygame.display.update()

pygame.quit()
