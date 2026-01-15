# nom_du_programme : spaceship_betaV3.py
# createur_du_programme : Samuel_Antunes
# date_de_creation : 11.12.2024
import pygame
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
# mettre 1920, 1080 si sur les écrans de base
WIDTH, HEIGHT = 1680, 1050

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
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin.png")), (150, 110)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin2.png")), (150, 150)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin3.png")), (150, 150)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin4.png")), (150, 150)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin10.png")), (150, 150)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin5.png")), (150, 150)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin9.png")), (150, 150)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin7.png")), (150, 150)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin8.png")), (150, 150)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "Boss_alien_alien", "boss_3_final.png")), (150, 150)),
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
boss_2_image = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "Boss_alien_alien", "boss_image_2.png")), (800, 400))
boss_3_final = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "Boss_alien_alien", "boss_3_final.png")), (800, 400))
button_play = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "bouton", "button_play.png")), (200, 50))
button_quit = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "bouton", "button_quit.png")), (200, 50))
button_settings = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "bouton", "button_settings.png")), (200, 50))

titre_jeu = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "background", "MainMenu.png")), (200, 80))

# Initialisation des variables
spaceship_x, spaceship_y = WIDTH // 2 - 75, HEIGHT - 150  # Vaisseau centré
lives = 3
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
    global game_state, boss, boss_health, remaining_bullets, game_over, spaceship_image, lives  # Add lives here
    spaceship_x, spaceship_y = WIDTH // 2 - 75, HEIGHT - 150  # Vaisseau centré

    lives = 3  # Reset the lives to 3
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

    # Mettez à jour l'image du vaisseau en fonction du skin sélectionné
    spaceship_image = spaceship_images[selected_skin]


def handle_life_loss():
    global lives, spaceship_x, spaceship_y, aliens, bullets, secondary_bullets, game_over
    spaceship_x, spaceship_y = WIDTH // 2 - 75, HEIGHT - 150  # Réinitialiser la position du vaisseau
    aliens.clear()  # Effacer les aliens
    bullets.clear()  # Effacer les balles
    secondary_bullets.clear()  # Effacer les balles secondaires
    lives -= 1  # Réduire les vies
    print(f"Lives after loss: {lives}")  # Afficher les vies après la perte

    if lives <= 0:
        game_over = True  # Terminer le jeu si aucune vie ne reste


def draw_text(text, x, y, color=WHITE, font=font):
    """Affiche du texte à l'écran."""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def spawn_alien():
    """Fait apparaître un nouvel alien à une position x aléatoire."""
    x = random.randint(75, WIDTH - 75)
    aliens.append(pygame.Rect(x, 0, 55, 55))


def draw_boss_health_bar(boss_health, max_health, x, y):
    """Affiche la barre de vie du boss."""
    bar_width = 500
    bar_height = 20
    health_percentage = boss_health / max_health
    pygame.draw.rect(screen, RED, (x + 225, y, bar_width, bar_height))  # Fond (rouge)
    pygame.draw.rect(screen, GREEN, (x + 225, y, bar_width * health_percentage, bar_height))  # Avant-plan (vert)


def fire_secondary_weapon(mouse_x, mouse_y):
    """Tire une balle vers la position du clic de la souris."""
    global remaining_bullets  # Ensure you're modifying the global remaining_bullets variable

    if remaining_bullets > 0:  # Only fire if there are remaining bullets
        dx = mouse_x - (spaceship_x + 75)  # Centrer le tir sur le vaisseau
        dy = mouse_y - spaceship_y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > 0:  # Éviter la division par zéro
            # Normaliser le vecteur de vitesse et l'adapter à la vitesse de la balle
            velocity = (dx / distance * bullet_speed, dy / distance * bullet_speed)
            secondary_bullets.append(
                {"rect": pygame.Rect(spaceship_x + 75 - 5, spaceship_y + 75 - 5, 10, 10), "velocity": velocity})
        remaining_bullets -= 1  # Réduire le nombre de balles après un tir

        if remaining_bullets < 0:
            remaining_bullets = 0  # Ensure it doesn't go below 0


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
                    {"rect": pygame.Rect(spaceship_x + 75 - 4, spaceship_y, 5, 15), "velocity": (0, -bullet_speed)}
                )
                remaining_bullets -= 1

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if game_state == "menu":

                    # Check if the mouse click is within the "Play" button's rectangle
                    if button_play.get_rect().collidepoint(mouse_x, mouse_y):
                        game_state = "playing"

                    elif button_quit.get_rect().collidepoint(mouse_x, mouse_y):
                        running = False

                elif game_state == "playing":
                    fire_secondary_weapon(mouse_x, mouse_y)  # Fire secondary weapon

    if game_state == "menu":
        screen.blit(background_images[0], (0, 0))

        # Agrandir l'image du titre
        titre_jeu_grand = pygame.transform.scale(titre_jeu, (titre_jeu.get_width() * 2, titre_jeu.get_height() * 2))

        # Affichage du titre agrandi
        screen.blit(titre_jeu_grand,(WIDTH // 2 - titre_jeu_grand.get_width() // 2, HEIGHT // 6 - titre_jeu_grand.get_height() // 2))

        # Affichage de l'image du vaisseau sélectionné
        screen.blit(spaceship_images[selected_skin], (WIDTH // 2 - 75, HEIGHT // 2 + 250))

        # Taille des boutons
        button_width = button_play.get_width()  # Largeur du bouton
        button_height = button_play.get_height()  # Hauteur du bouton

        # Calcul de la position du bouton "Play"
        x_position = (WIDTH - button_width) // 2
        y_position = (HEIGHT - button_height) // 2 - 50

        # Définir un rectangle pour le bouton "Play" avec 15 px de moins en largeur et hauteur
        button_play_rect = button_play.get_rect(topleft=(x_position + 12, y_position + 12))

        # Réduire de 15 px la largeur et la hauteur du rectangle
        button_play_rect.width -= 22
        button_play_rect.height -= 24

        # Affichage du bouton "Play"
        screen.blit(button_play, (x_position, y_position))

        # Vérifier si un clic a eu lieu dans la zone du bouton
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Vérifiez si le clic est dans la zone du bouton
                if button_play_rect.collidepoint(mouse_x, mouse_y):
                    game_state = "playing"  # Commencer le jeu
                    # Appliquer le skin sélectionné lorsque le jeu commence
                    spaceship_image = spaceship_images[selected_skin]


    # Écran de jeu
    elif game_state == "playing":
        screen.blit(background_images[(level - 1) % len(background_images)], (0, 0))
        show_level(level)

        if not game_over:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT] and spaceship_x > 0:
                spaceship_x -= spaceship_speed

            if keys[pygame.K_RIGHT] and spaceship_x < WIDTH - 155:
                spaceship_x += spaceship_speed
            pygame.draw.line(screen, GREEN, (spaceship_x + 75, spaceship_y + 75), (spaceship_x + 75, 0), 2)

            # Mise à jour des balles
            for bullet in bullets[:]:
                bullet["rect"].x += bullet["velocity"][0]
                bullet["rect"].y += bullet["velocity"][1]

                if bullet["rect"].y < 0:
                    bullets.remove(bullet)

            # Mise à jour des balles secondaires
            for bullet in secondary_bullets[:]:
                bullet["rect"].x += bullet["velocity"][0]
                bullet["rect"].y += bullet["velocity"][1]

                # Vérifie si les balles sont sorties de l'écran (haut, gauche, ou droit)
                if bullet["rect"].y < 0 or bullet["rect"].x < 0 or bullet["rect"].x > WIDTH:
                    secondary_bullets.remove(bullet)

            # Apparition des aliens
            if not boss and random.random() < alien_spawn_rate:
                spawn_alien()

            for alien in aliens[:]:
                alien.y += alien_speed  # Déplacer l'alien vers le bas

                # Vérifiez si l'alien touche le bas de l'écran
                if alien.y > HEIGHT:
                    handle_life_loss()  # Perdre une vie si l'alien atteint le bas de l'écran
                    break  # Sortir de la boucle après avoir perdu une vie

                # Vérifiez la collision avec le vaisseau spatial
                if pygame.Rect(spaceship_x, spaceship_y, 150, 125).colliderect(alien):
                    handle_life_loss()  # Perdre une vie si collision avec le vaisseau

                # Vérifiez les collisions avec les balles
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

            if level == max_level and boss is None:
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
            draw_text(f"Lives: {lives}", 1810, 40)  # Display lives on the screen
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