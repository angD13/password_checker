import pygame
import sys
from main import check_password

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 700, 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 80, 80)
GREEN = (80, 200, 120)
YELLOW = (255, 215, 0)
FONT = pygame.font.SysFont("arial", 24)
BIG_FONT = pygame.font.SysFont("arial", 32)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Password Checker")

# Input box setup
input_box = pygame.Rect(50, 50, 600, 40)
color_active = pygame.Color('dodgerblue2')
color_inactive = GRAY
color = color_inactive
active = False
user_text = ''

# Button
button_rect = pygame.Rect(270, 110, 200, 50)

# Output
result = None

# Mask password with asterisks
def mask_text(text):
    return '*' * len(text)

def draw_result(result):
    if not result:
        return

    # Strength color
    strength = result['strength']
    if strength == "Very Weak":
        strength_color = RED
    elif strength == "Weak":
        strength_color = (255, 140, 0)
    elif strength == "Medium":
        strength_color = YELLOW
    elif strength == "Strong":
        strength_color = (100, 180, 100)
    else:
        strength_color = GREEN

    # Draw result
    strength_text = FONT.render(f"Strength: {strength}", True, strength_color)
    crack_time_text = FONT.render(f"Estimated Crack Time: {result['crack_time']}", True, BLACK)

    screen.blit(strength_text, (50, 180))
    screen.blit(crack_time_text, (50, 220))

    y = 260
    for warning in result['warnings']:
        warning_text = FONT.render(f"- {warning}", True, RED)
        screen.blit(warning_text, (70, y))
        y += 30

# Main loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle input box
            if input_box.collidepoint(event.pos):
                active = True
            else:
                active = False

            # Check button clicked
            if button_rect.collidepoint(event.pos):
                result = check_password(user_text)
                user_text = ''  # Clear input

        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    result = check_password(user_text)
                    user_text = ''  # Clear input
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

    # Draw input box
    color = color_active if active else color_inactive
    pygame.draw.rect(screen, color, input_box, 2)
    masked = mask_text(user_text)
    text_surface = FONT.render(masked, True, BLACK)
    screen.blit(text_surface, (input_box.x + 10, input_box.y + 5))

    # Draw button
    pygame.draw.rect(screen, GRAY, button_rect)
    button_text = FONT.render("Check Password", True, BLACK)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

    # Draw results
    draw_result(result)

    pygame.display.flip()

pygame.quit()
sys.exit()