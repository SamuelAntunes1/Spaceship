# date : 13 Décembre 2024
# version : 2.0
# créé par : Dani Dordevic, Samuel Antunes


import  pygame
import random
import math
import os

def parent_dir(path, levels=1):
    for _ in range(levels):
        path = os.path.dirname(path)
    return path

cwd = os.path.dirname(os.path.abspath(__file__))
current_directory = parent_dir(cwd, 1)

# Initialisation de pygame
pygame.init()

# Dimensions de l'écran et mode plein écran
info = pygame.display.Info()
# mettre 1920, 1080 pour les écrans classiques
WIDTH, HEIGHT = 1680, 1050
print("")

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Créer l'écran en mode plein écran
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Spaceship Shooter")

# FPS et horloge
FPS = 60
clock = pygame.time.Clock()

# Chargement des images pour le vaisseau spatial, les balles, les aliens et les arrière-plans
spaceship_images = [
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin.png")), (100, 100)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin2.png")), (100, 100)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin3.png")), (100, 100)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin4.png")), (100, 100)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin10.png")), (100, 100)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin5.png")), (100, 100)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin9.png")), (100, 100)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin7.png")), (100, 100)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin8.png")), (100, 100)),
]

alien_image = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "Boss_alien_alien", "alien.png")), (55, 55))

bullet_image = pygame.Surface((10, 20), pygame.SRCALPHA)
pygame.draw.ellipse(bullet_image, RED, (0, 0, 10, 20))

background_images = [
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "background", "background12.jpg")), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "background", "background14.jpg")), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "background", "background13.jpg")), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "background", "background3.png")), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "background", "background15.jpg")), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "background", "background6.jpg")), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "background", "background7.jpg")), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "background", "background9.jpg")), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "background", "background10.jpg")), (WIDTH, HEIGHT)),
]


boss_image = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "Boss_alien_alien", "boss.png")), (800, 400))

# Initialisation des variables
spaceship_x, spaceship_y = WIDTH // 2 - 50 , HEIGHT - 100  # Vaisseau centré
spaceship_speed = 10
bullet_speed = 15
alien_speed = 2
bullets = []
secondary_bullets = []
aliens = []
score = 0
level = 1
max_level = 10  # Set the maximum level for your game
alien_spawn_rate = 0.005
game_state = "menu"
boss = None
boss_health = 50
boss_direction = 1
remaining_bullets = 1000000
game_over = False
selected_skin = 0
spaceship_image = spaceship_images[selected_skin]

# Polices
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 48)


# Fonctions utilitaires
def reset_game():
    global spaceship_x, spaceship_y, bullets, secondary_bullets, aliens, score, level, alien_speed, alien_spawn_rate
    global game_state, boss, boss_health, remaining_bullets, game_over, spaceship_image
    spaceship_x = WIDTH // 2 - 50  # Vaisseau centré
    spaceship_y = HEIGHT - 100
    bullets.clear()
    secondary_bullets.clear()
    aliens.clear()
    score = 0
    level = 1
    alien_speed = 2
    alien_spawn_rate = 0.005
    boss = None
    boss_health = 50
    remaining_bullets = 100000
    game_over = False
    spaceship_image = spaceship_images[selected_skin]


def handle_life_loss():
    global lives, spaceship_x, spaceship_y, aliens, game_over
    # Reset spaceship to starting position and remove all aliens when a life is lost
    spaceship_x, spaceship_y = WIDTH // 2 - 25, HEIGHT - 100
    aliens.clear()  # Remove all aliens when a life is lost
    lives -= 1
    if lives <= 0:
        game_over = True



def draw_text(text, x, y, color=WHITE, font=font):
    """Affiche du texte à l'écran."""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def spawn_alien():
    """Fait apparaître un nouvel alien à une position x aléatoire."""
    x = random.randint(0, WIDTH - 40)
    aliens.append(pygame.Rect(x, 0, 40, 40))


def draw_boss_health_bar(boss_health, max_health, x, y):
    """Affiche la barre de vie du boss."""
    bar_width = 500
    bar_height = 20
    health_percentage = boss_health / max_health
    pygame.draw.rect(screen, RED, (x + 225, y, bar_width, bar_height))  # Fond (rouge)
    pygame.draw.rect(screen, GREEN, (x + 225, y, bar_width * health_percentage, bar_height))  # Avant-plan (vert)

def fire_secondary_weapon(mouse_x, mouse_y):
    """Tire une balle vers la position du clic de la souris."""
    global remaining_bullets
    if remaining_bullets > 0:
        dx = mouse_x - (spaceship_x + 50)  # Centrer le tir
        dy = mouse_y - spaceship_y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:  # Éviter la division par zéro
            # Normaliser le vecteur de vitesse et l'adapter à la vitesse de la balle
            velocity = (dx / distance * bullet_speed, dy / distance * bullet_speed)
            secondary_bullets.append({"rect": pygame.Rect(spaceship_x + 50 - 5, spaceship_y + 50 - 5, 10, 10), "velocity": velocity})
        remaining_bullets -= 1  # Réduire le nombre de balles


# Updated draw_text Function
def draw_text(text, x, y, color=WHITE, font=font, centered=False):
    """Affiche du texte à l'écran, centré si nécessaire."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if centered:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def show_level(level):
    """Affiche le niveau actuel à l'écran, aligné en haut à droite."""
    text = f"Niveau: {level}"
    text_surface = large_font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.topright = (WIDTH - 10, 10)  # Positionné en haut à droite avec une marge de 10 pixels
    screen.blit(text_surface, text_rect)




# Boucle principale du jeu
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RETURN:
                if game_state in ["game_over", "victory"]:
                    reset_game()
                    game_state = "menu"
                elif game_state == "menu":
                    reset_game()
                    game_state = "playing"
                elif game_state == "playing" and game_over:
                    reset_game()
                    game_state = "playing"
            elif event.key == pygame.K_LEFT and game_state == "menu":
                selected_skin = (selected_skin - 1) % len(spaceship_images)
            elif event.key == pygame.K_RIGHT and game_state == "menu":
                selected_skin = (selected_skin + 1) % len(spaceship_images)
            elif event.key == pygame.K_SPACE and game_state == "playing" and remaining_bullets > 0:
                bullets.append(
                    {"rect": pygame.Rect(spaceship_x + 50 - 2, spaceship_y, 5, 15), "velocity": (0, -bullet_speed)}
                )
                remaining_bullets -= 1
        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == "playing" and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            fire_secondary_weapon(mouse_x, mouse_y)

    # Écran du menu
    if game_state == "menu":
        screen.blit(background_images[0], (0, 0))
        draw_text("SPACESHIP SHOOTER", WIDTH // 2, HEIGHT // 6 - 30, RED, large_font, centered=True)
        draw_text("Appuyez sur ENTRÉE pour commencer", WIDTH // 2, HEIGHT // 6, WHITE, centered=True)
        draw_text("Utilisez GAUCHE/DROITE pour choisir le vaisseau", WIDTH // 2, HEIGHT // 6 + 40, WHITE, centered=True)
        screen.blit(spaceship_images[selected_skin], (WIDTH // 2 - 50, HEIGHT // 2 + 100))

    # Écran de jeu
    elif game_state == "playing":
        screen.blit(background_images[(level - 1) % len(background_images)], (0, 0))
        show_level(level)

        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and spaceship_x > 0:
                spaceship_x -= spaceship_speed
            if keys[pygame.K_RIGHT] and spaceship_x < WIDTH - 100:
                spaceship_x += spaceship_speed

            pygame.draw.line(screen, GREEN, (spaceship_x + 50, spaceship_y + 50), (spaceship_x + 50, 0), 2)

            # Mise à jour des balles
            for bullet in bullets[:]:
                bullet["rect"].x += bullet["velocity"][0]
                bullet["rect"].y += bullet["velocity"][1]
                if bullet["rect"].y < 0:
                    bullets.remove(bullet)

            for bullet in secondary_bullets[:]:
                bullet["rect"].x += bullet["velocity"][0]
                bullet["rect"].y += bullet["velocity"][1]
                if bullet["rect"].y < 0 or bullet["rect"].x < 0 or bullet["rect"].x > WIDTH:
                    secondary_bullets.remove(bullet)

            # Apparition des aliens
            if not boss and random.random() < alien_spawn_rate:
                spawn_alien()

            # Mise à jour des aliens
            for alien in aliens[:]:
                alien.y += alien_speed
                if alien.y > HEIGHT:
                    game_over = True
                if pygame.Rect(spaceship_x, spaceship_y, 100, 100).colliderect(alien):
                    game_over = True
                for bullet in bullets[:]:
                    if bullet["rect"].colliderect(alien):
                        bullets.remove(bullet)
                        aliens.remove(alien)
                        score += 1
                        if score % 10 == 0 and level < max_level:
                            level += 1
                            alien_speed += 0.5
                            alien_spawn_rate += 0.002
                        elif score % 10 == 0 and level == max_level:
                            game_state = "victory"
                        break
                for bullet in secondary_bullets[:]:
                    if bullet["rect"].colliderect(alien):
                        secondary_bullets.remove(bullet)
                        aliens.remove(alien)
                        score += 1
                        if score % 10 == 0 and level < max_level:
                            level += 1
                            alien_speed += 0.5
                            alien_spawn_rate += 0.002
                        elif score % 10 == 0 and level == max_level:
                            game_state = "victory"
                        break

            # Apparition du boss
            if level == max_level and 2 and boss is None:
                boss = pygame.Rect(WIDTH // 2, 50, 800, 400)
                boss_health = 50

            if boss:
                boss.x += boss_direction * 5
                if boss.left <= 0 or boss.right >= WIDTH:
                    boss_direction *= -1
                for bullet in bullets[:]:
                    if bullet["rect"].colliderect(boss):
                        bullets.remove(bullet)
                        boss_health -= 1
                        if boss_health <= 0:
                            boss = None
                            game_state = "victory"
                for bullet in secondary_bullets[:]:
                    if bullet["rect"].colliderect(boss):
                        secondary_bullets.remove(bullet)
                        boss_health -= 2
                        if boss_health <= 0:
                            boss = None
                            game_state = "victory"

                if boss:
                    screen.blit(boss_image, boss)
                    draw_boss_health_bar(boss_health, 50, boss.x, boss.y - 20)

            for alien in aliens:
                screen.blit(alien_image, alien)

            for bullet in bullets:
                screen.blit(bullet_image, bullet["rect"])

            for bullet in secondary_bullets:
                pygame.draw.ellipse(screen, BLUE, bullet["rect"])

            screen.blit(spaceship_image, (spaceship_x, spaceship_y))
            draw_text(f"Score: {score}", 10, 10)
            draw_text(f"Balles restantes: {remaining_bullets}", 10, 40)

        if game_over:
            screen.fill(BLACK)
            draw_text("GAME OVER!", WIDTH // 2, HEIGHT // 2 - 50, RED, large_font, centered=True)
            draw_text("Appuyez sur ENTRÉE pour recommencer", WIDTH // 2, HEIGHT // 2 + 10, WHITE, centered=True)

    elif game_state == "victory":
        screen.blit(background_images[0], (0, 0))
        draw_text("FÉLICITATIONS, VOUS AVEZ GAGNÉ!", WIDTH // 2, HEIGHT // 6 - 30, WHITE, large_font, centered=True)
        draw_text("Appuyez sur ENTRÉE pour recommencer", WIDTH // 2, HEIGHT // 6 + 10, WHITE, centered=True)

    pygame.display.flip()
pygame.quit()