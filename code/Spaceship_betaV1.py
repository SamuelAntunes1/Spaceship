# date : 13 Décembre 2024
# version : 1.0
# créé par : Dani Dordevic, Samuel Antunes

import pygame
import random
import os

def parent_dir(path, levels=1):
    for _ in range(levels):
        path = os.path.dirname(path)
    return path

cwd = os.path.dirname(os.path.abspath(__file__))
current_directory = parent_dir(cwd, 1)

# Initialize pygame
pygame.init()

# Screen dimensions and fullscreen mode
info = pygame.display.Info()
# mettre 1920, 1080 pour les autres grands écrans
WIDTH, HEIGHT = 1680, 1050

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the screen in fullscreen mode
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Spaceship Shooter")

# FPS and clock
FPS = 63
clock = pygame.time.Clock()

# Load images for spaceship, bullets, aliens, and backgrounds
spaceship_images = [
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin.png")), (50, 50)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin2.png")), (50, 50)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin3.png")), (50, 50)),
]

alien_image = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "Boss_alien_alien", "alien.png")), (40, 40))

bullet_image = pygame.Surface((10, 20), pygame.SRCALPHA)  # Taller bullets
pygame.draw.ellipse(bullet_image, (255, 255, 0), (0, 0, 10, 20))  # Yellow bullet with an ellipse shape

background_images = [
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "background", "background7.jpg")), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "background", "background3.png")), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "background", "background9.jpg")), (WIDTH, HEIGHT)),
]

boss_image = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "boss_alien_alien", "boss_3_final.png")), (800, 400))

# Initialize variables
spaceship_x, spaceship_y = WIDTH // 2 - 25, HEIGHT - 100
spaceship_speed = 13.5
bullet_speed = 25
alien_speed = 2
bullets = []
aliens = []
score = 0
level = 1
alien_spawn_rate = 0.005
game_state = "menu"
boss = None
boss_health = 30
boss_direction = 1
remaining_bullets = 100
game_over = False
selected_skin = 0
spaceship_image = spaceship_images[selected_skin]

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 48)


# Helper functions
def reset_game():
    global spaceship_x, spaceship_y, bullets, aliens, score, level, alien_speed, alien_spawn_rate
    global game_state, boss, boss_health, remaining_bullets, game_over, spaceship_image
    spaceship_x = WIDTH // 2 - 25
    spaceship_y = HEIGHT - 100
    bullets.clear()
    aliens.clear()
    score = 0
    level = 1
    alien_speed = 2
    alien_spawn_rate = 0.005
    boss = None
    boss_health = 30
    remaining_bullets = 100
    game_over = False
    spaceship_image = spaceship_images[selected_skin]


def draw_text(text, x, y, color=WHITE, font=font):
    """Render text to the screen."""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def spawn_alien():
    """Spawn a new alien at a random x position."""
    x = random.randint(0, WIDTH - 40)
    aliens.append(pygame.Rect(x, 0, 40, 40))


# Game loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False  # Exit the game when Escape is pressed
            elif event.key == pygame.K_RETURN:
                if game_state == "game_over" or game_state == "victory":
                    reset_game()
                    game_state = "menu"
                elif game_state == "menu":
                    reset_game()
                    game_state = "playing"
            elif event.key == pygame.K_LEFT:
                selected_skin = (selected_skin - 1) % 3
            elif event.key == pygame.K_RIGHT:
                selected_skin = (selected_skin + 1) % 3
            elif event.key == pygame.K_SPACE and game_state == "playing" and remaining_bullets > 0:
                # Fire a bullet when space bar is pressed
                bullets.append({"rect": pygame.Rect(spaceship_x + 25, spaceship_y, 5, 15), "velocity": (0, -bullet_speed)})
                remaining_bullets -= 1

    # Menu screen
    if game_state == "menu":
        screen.blit(background_images[0], (0, 0))
        draw_text("SPACESHIP SHOOTER", WIDTH // 2 - 150, HEIGHT // 2 - 50, RED, large_font)
        draw_text("Press ENTER to start", WIDTH // 2 - 100, HEIGHT // 2, WHITE)
        draw_text("Use LEFT/RIGHT to choose spaceship", WIDTH // 2 - 200, HEIGHT // 2 + 40, WHITE)
        screen.blit(spaceship_images[selected_skin], (WIDTH // 2 - 25, HEIGHT // 2 + 100))

    # Victory screen
    elif game_state == "victory":
        draw_text("VICTORY!", WIDTH // 2 - 100, HEIGHT // 2, WHITE, large_font)
        draw_text("Press ENTER to restart", WIDTH // 2 - 150, HEIGHT // 2 + 40, WHITE)

    # Playing screen
    elif game_state == "playing":
        if boss and boss_health <= 0:
            game_state = "victory"

        screen.blit(background_images[(level - 1) % len(background_images)], (0, 0))

        # Allow movement only if game is not over
        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and spaceship_x > 0:
                spaceship_x -= spaceship_speed
            if keys[pygame.K_RIGHT] and spaceship_x < WIDTH - 50:
                spaceship_x += spaceship_speed
            if keys[pygame.K_UP] and spaceship_y > 0:
                spaceship_y -= spaceship_speed
            if keys[pygame.K_DOWN] and spaceship_y < HEIGHT - 50:
                spaceship_y += spaceship_speed

            # Draw the aiming line (fixed direction: up from spaceship, all the way to the top)
            pygame.draw.line(screen, RED, (spaceship_x + 25, spaceship_y + 25), (spaceship_x + 25, 0), 2)

            # Update bullets
            for bullet in bullets[:]:
                bullet["rect"].x += bullet["velocity"][0]
                bullet["rect"].y += bullet["velocity"][1]
                if bullet["rect"].x < 0 or bullet["rect"].x > WIDTH or bullet["rect"].y < 0:
                    bullets.remove(bullet)

            # Spawn aliens
            if random.random() < alien_spawn_rate:
                spawn_alien()

            # Update aliens
            for alien in aliens[:]:
                alien.y += alien_speed
                if alien.y > HEIGHT:
                    game_over = True  # Game over if alien reaches the bottom
                for bullet in bullets[:]:
                    if bullet["rect"].colliderect(alien):
                        bullets.remove(bullet)
                        aliens.remove(alien)
                        score += 1
                        if score % 10 == 0:
                            level += 1
                            alien_speed += 0.5
                            alien_spawn_rate += 0.002
                        break

            # Boss logic
            if level > 3 and not boss:
                boss = pygame.Rect(WIDTH // 2 - 400, 50, 800, 400)

            if boss:
                boss.x += 3 * boss_direction
                if boss.x <= 0 or boss.x >= WIDTH - boss.width:
                    boss_direction *= -1
                for bullet in bullets[:]:
                    if boss.colliderect(bullet["rect"]):
                        bullets.remove(bullet)
                        boss_health -= 1
                        if boss_health <= 0:
                            boss = None
                            game_state = "victory"
                screen.blit(boss_image, boss)

            # Draw entities
            for alien in aliens:
                screen.blit(alien_image, alien)

            for bullet in bullets:
                screen.blit(bullet_image, bullet["rect"])

            screen.blit(spaceship_image, (spaceship_x, spaceship_y))

            # Display score and remaining bullets
            draw_text(f"Score: {score}", 10, 10)
            draw_text(f"Remaining Bullets: {remaining_bullets}", 10, 40)

        # Game over screen
        if game_over:
            draw_text("GAME OVER!", WIDTH // 2 - 100, HEIGHT // 2, RED, large_font)
            draw_text("Press ENTER to restart", WIDTH // 2 - 150, HEIGHT // 2 + 40, WHITE)

    pygame.display.flip()

pygame.quit()