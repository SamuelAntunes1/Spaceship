# nom_du_programme : spaceship_betaV4.py
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


################################################################################
#                      INITIALISATION ET CONFIGURATIONS                        #
################################################################################


pygame.init()

info = pygame.display.Info()
# mettre 1920, 1080 si sur les écrans de base
WIDTH, HEIGHT = 1680, 1050

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Écran plein écran
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Spaceship Shooter")

FPS = 60
clock = pygame.time.Clock()


################################################################################
#                          CHARGEMENT DES IMAGES                                #
################################################################################


# Vaisseaux
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

# Alien de base (on fera un scale aléatoire lors du spawn)
alien_image = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "Boss_alien_alien", "alien.png")), (55, 55))

# Balle rouge (dessinée à la main)
bullet_image = pygame.Surface((10, 20), pygame.SRCALPHA)
pygame.draw.ellipse(bullet_image, RED, (0, 0, 10, 20))

# Arrière-plans
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

# --- On mélange la liste pour un ordre unique
shuffled_backgrounds = background_images[:]
random.shuffle(shuffled_backgrounds)
background_index = 0  # On part du premier

# Boss
boss_image = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "Boss_alien_alien", "boss.png")), (800, 400))
boss_2_image = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "Boss_alien_alien", "boss_image_2.png")), (800, 400))
boss_3_final = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "Boss_alien_alien", "boss_3_final.png")), (800, 400))

# Boutons
button_play = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "bouton", "button_play.png")), (200, 50))
button_quit = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "bouton", "button_quit.png")), (200, 50))
button_settings = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "bouton", "button_settings.png")), (200, 50))
button_restart = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "bouton", "button_restart.png")), (200, 50))
button_continue = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "bouton", "button_continue.png")), (200, 50))
button_pause = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "bouton", "button_pause.png")), (50, 50))

# Titre / croix / fleche choix skin
titre_jeu = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "background", "MainMenu.png")), (200, 80))
croix_retour_page = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "bouton", "croix_noir.png")), (40, 40))
fleche_choix_skin_gauche = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "bouton", "fleches_choix_skin_gauche.png")), (60, 60))
fleche_choix_skin_droite = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "bouton", "fleches_choix_skin_droite.png")), (60, 60))


################################################################################
#                      VARIABLES GLOBALES / ÉTAT INITIAL                        #
################################################################################


spaceship_x, spaceship_y = WIDTH // 2 - 75, HEIGHT - 150
spaceship_speed = 10

bullet_speed = 15
alien_speed = 2

bullets = []
secondary_bullets = []
aliens = []

score = 0
level = 1
max_level = 10
alien_spawn_rate = 0.005
game_state = "menu"

# Boss
boss = None
boss_health = 50
boss_direction = 1

remaining_bullets = 1000
lives = 5
game_over = False

selected_skin = 0
spaceship_image = spaceship_images[selected_skin]

current_difficulty = "facile"
current_controls = "arrows"

weapon1_control = "space"
weapon2_control = "left"

# Ajout de la variable pour l'Aim Assist
aim_assist = False

font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 48)


################################################################################
#                               FONCTIONS DE JEU                                #
################################################################################


def set_difficulty(difficulty):
    global current_difficulty, remaining_bullets, alien_speed, alien_spawn_rate, lives
    current_difficulty = difficulty
    if difficulty == "facile":
        remaining_bullets = 1000
        alien_speed = 2
        alien_spawn_rate = 0.005
        lives = 5
    elif difficulty == "moyen":
        remaining_bullets = 500
        alien_speed = 2
        alien_spawn_rate = 0.01
        lives = 3
    elif difficulty == "difficile":
        remaining_bullets = 200
        alien_speed = 2.5
        alien_spawn_rate = 0.015
        lives = 2
    elif difficulty == "hardcore":
        remaining_bullets = 100
        alien_speed = 3
        alien_spawn_rate = 0.02
        lives = 1


def reset_game():
    """
    Réinitialise toutes les variables pour relancer une partie neuve.
    On re-mélange aussi la liste shuffled_backgrounds
    pour s'assurer qu'on ne retrouve pas le même ordre de fonds.
    """
    global spaceship_x, spaceship_y, bullets, secondary_bullets, aliens
    global score, level, game_state, boss, boss_health, boss_direction
    global remaining_bullets, game_over, spaceship_image
    global shuffled_backgrounds, background_index

    spaceship_x, spaceship_y = WIDTH // 2 - 75, HEIGHT - 150

    bullets.clear()
    secondary_bullets.clear()
    aliens.clear()

    score = 0
    level = 1
    boss = None
    boss_health = 50
    boss_direction = 1
    game_over = False

    # On re-mélange les backgrounds
    random.shuffle(shuffled_backgrounds)
    background_index = 0

    # Skin choisi
    spaceship_image = spaceship_images[selected_skin]

    # Remet la difficulté courante
    set_difficulty(current_difficulty)


def handle_life_loss():
    global lives, spaceship_x, spaceship_y, aliens, bullets, secondary_bullets, game_over
    spaceship_x, spaceship_y = WIDTH // 2 - 75, HEIGHT - 150
    aliens.clear()
    bullets.clear()
    secondary_bullets.clear()
    lives -= 1
    if lives <= 0:
        game_over = True


def draw_text(text, x, y, color=WHITE, font=None, centered=False):
    if font is None:
        font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if centered:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)


def spawn_alien():
    # Taille aléatoire entre 55 et 90
    size = random.randint(55, 90)
    alien_surface = pygame.transform.scale(alien_image, (size, size))
    x = random.randint(0, WIDTH - size)
    y = 0
    alien_rect = pygame.Rect(x, y, size, size)

    aliens.append({
        "surface": alien_surface,
        "rect": alien_rect
    })


def draw_boss_health_bar(current_health, max_health, x, y):
    bar_width = 500
    bar_height = 20
    health_percentage = current_health / max_health
    pygame.draw.rect(screen, RED, (x + 225, y, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (x + 225, y, bar_width * health_percentage, bar_height))


def fire_secondary_weapon(mouse_x, mouse_y):
    global remaining_bullets
    if remaining_bullets > 0:
        dx = mouse_x - (spaceship_x + 75)
        dy = mouse_y - spaceship_y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        if dist > 0:
            velocity = (dx / dist * bullet_speed, dy / dist * bullet_speed)
            secondary_bullets.append({
                "rect": pygame.Rect(spaceship_x + 75 - 5, spaceship_y + 75 - 5, 10, 10),
                "velocity": velocity
            })
        remaining_bullets -= 1
        if remaining_bullets < 0:
            remaining_bullets = 0


def show_level(level):
    text_surface = large_font.render(f"Niveau: {level}", True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.topright = (WIDTH - 10, 10)
    screen.blit(text_surface, text_rect)


def set_weapon1(control):
    global weapon1_control, weapon2_control
    # Empêche que les 2 armes soient sur "left" en même temps
    if control == "left" and weapon2_control == "left":
        return
    weapon1_control = control


def set_weapon2(control):
    global weapon1_control, weapon2_control
    # Empêche que les 2 armes soient sur "left" en même temps
    if control == "left" and weapon1_control == "left":
        return
    weapon2_control = control


################################################################################
#                          BOUCLE PRINCIPALE DU JEU                            #
################################################################################


running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        # Quitter si on ferme la fenêtre
        if event.type == pygame.QUIT:
            running = False

        # --- GESTION DU CLAVIER ---
        if event.type == pygame.KEYDOWN:
            # Touche Échap => toggle pause <-> playing
            if event.key == pygame.K_ESCAPE:
                if game_state == "playing":
                    game_state = "pause"
                elif game_state == "pause":
                    game_state = "playing"

            # Tir principal si weapon1_control == "space"
            if weapon1_control == "space":
                if (event.key == pygame.K_SPACE
                        and game_state == "playing"
                        and remaining_bullets > 0):
                    bullets.append({
                        "rect": pygame.Rect(spaceship_x + 75 - 4, spaceship_y, 5, 15),
                        "velocity": (0, -bullet_speed)
                    })
                    remaining_bullets -= 1

        # --- GESTION DES CLICS SOURIS ---
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # ÉTAT : MENU
            if game_state == "menu":
                if event.button == 1:  # clic gauche
                    if button_play_rect.collidepoint(mouse_x, mouse_y):
                        reset_game()
                        game_state = "playing"
                        spaceship_image = spaceship_images[selected_skin]

                    elif button_quit_rect.collidepoint(mouse_x, mouse_y):
                        running = False

                    elif button_settings_rect.collidepoint(mouse_x, mouse_y):
                        game_state = "settings"

                    elif fleche_gauche_rect.collidepoint(mouse_x, mouse_y):
                        selected_skin = (selected_skin - 1) % len(spaceship_images)
                        spaceship_image = spaceship_images[selected_skin]

                    elif fleche_droite_rect.collidepoint(mouse_x, mouse_y):
                        selected_skin = (selected_skin + 1) % len(spaceship_images)
                        spaceship_image = spaceship_images[selected_skin]

            # ÉTAT : SETTINGS
            elif game_state == "settings":
                pass  # (Voir plus bas : gestion complète du paramétrage)

            # ÉTAT : PAUSE
            elif game_state == "pause":
                # On conserve l'affichage "Continue / Restart / Quit"
                x_position_pause = (WIDTH - button_continue.get_width()) // 2
                y_position_pause = (HEIGHT - button_continue.get_height()) // 2

                button_continue_rect = button_continue.get_rect(
                    topleft=(x_position_pause, y_position_pause - 100)
                )
                button_restart_rect = button_restart.get_rect(
                    topleft=(x_position_pause, y_position_pause)
                )
                button_quit_rect2 = button_quit.get_rect(
                    topleft=(x_position_pause, y_position_pause + 100)
                )

                # --- On affiche le bouton Pause au même endroit qu'en playing
                pause_pos_x = 10
                pause_pos_y = 70
                pause_button_rect = button_pause.get_rect(topleft=(pause_pos_x, pause_pos_y))

                # Si on clique sur le bouton Pause, on repasse en "playing"
                if pause_button_rect.collidepoint(mouse_x, mouse_y):
                    game_state = "playing"
                # Sinon, on gère continue / restart / quit
                elif button_continue_rect.collidepoint(mouse_x, mouse_y):
                    game_state = "playing"
                elif button_restart_rect.collidepoint(mouse_x, mouse_y):
                    reset_game()
                    game_state = "playing"
                elif button_quit_rect2.collidepoint(mouse_x, mouse_y):
                    reset_game()
                    game_state = "menu"

            # ÉTAT : PLAYING
            elif game_state == "playing":
                # On calcule la position du bouton Pause
                pause_pos_x = 10
                pause_pos_y = 70
                pause_button_rect = button_pause.get_rect(topleft=(pause_pos_x, pause_pos_y))

                if pause_button_rect.collidepoint(mouse_x, mouse_y):
                    # On met le jeu en pause
                    game_state = "pause"
                else:
                    # Tirs
                    if (weapon1_control == "left"
                            and event.button == 1
                            and remaining_bullets > 0):
                        bullets.append({
                            "rect": pygame.Rect(spaceship_x + 75 - 4, spaceship_y, 5, 15),
                            "velocity": (0, -bullet_speed)
                        })
                        remaining_bullets -= 1

                    if weapon2_control == "left" and event.button == 1:
                        fire_secondary_weapon(mouse_x, mouse_y)
                    elif weapon2_control == "right" and event.button == 3:
                        fire_secondary_weapon(mouse_x, mouse_y)


    ############################################################################
    #                            GESTION DES ETATS                              #
    ############################################################################


    if game_state == "menu":
        screen.blit(background_images[0], (0, 0))

        titre_jeu_grand = pygame.transform.scale(
            titre_jeu, (titre_jeu.get_width() * 2, titre_jeu.get_height() * 2)
        )
        screen.blit(
            titre_jeu_grand,
            (
                WIDTH // 2 - titre_jeu_grand.get_width() // 2,
                HEIGHT // 10 - titre_jeu_grand.get_height() // 2
            )
        )

        screen.blit(spaceship_images[selected_skin], (WIDTH // 2 - 75, HEIGHT // 2 + 250))

        button_width = button_play.get_width()
        button_height = button_play.get_height()

        x_position = (WIDTH - button_width) // 2
        y_position = (HEIGHT - button_height) // 2

        y_position_quit = y_position + button_height + 20
        y_position_settings = y_position_quit + button_height + 20

        button_play_rect = button_play.get_rect(topleft=(x_position, y_position - 28))
        button_quit_rect = button_quit.get_rect(topleft=(x_position + 4, y_position_quit + 3))
        button_settings_rect = button_settings.get_rect(topleft=(x_position + 4, y_position_settings + 34))

        button_play_rect.width -= 2
        button_play_rect.height -= 2
        button_quit_rect.width -= 4
        button_quit_rect.height -= 2
        button_settings_rect.width -= 2
        button_settings_rect.height -= 2

        screen.blit(button_play, (x_position, y_position - 30))
        screen.blit(button_quit, (x_position, y_position_quit))
        screen.blit(button_settings, (x_position, y_position_settings + 30))

        fleche_gauche_x = x_position - 45
        fleche_gauche_y = y_position_settings + 182
        fleche_droite_x = x_position + 185
        fleche_droite_y = y_position_settings + 180

        screen.blit(fleche_choix_skin_gauche, (fleche_gauche_x, fleche_gauche_y))
        screen.blit(fleche_choix_skin_droite, (fleche_droite_x, fleche_droite_y))

        fleche_gauche_rect = fleche_choix_skin_gauche.get_rect(topleft=(fleche_gauche_x, fleche_gauche_y))
        fleche_droite_rect = fleche_choix_skin_droite.get_rect(topleft=(fleche_droite_x, fleche_droite_y))


    elif game_state == "settings":
        screen.blit(background_images[0], (0, 0))

        font_params = pygame.font.Font(None, 80)
        settings_text = font_params.render("Paramètres", True, WHITE)
        screen.blit(settings_text, (WIDTH // 2 - settings_text.get_width() // 2, HEIGHT // 25))

        cross_x, cross_y = 30, 30
        screen.blit(croix_retour_page, (cross_x, cross_y))
        croix_rect = croix_retour_page.get_rect(topleft=(cross_x, cross_y))

        # --------------------------------------------------------
        # TOUT LE CODE DE DIFFICULTÉ, CONTROLES, AIM ASSIST ...
        # (inchangé, vous avez toutes vos lignes)
        # --------------------------------------------------------

        # Par exemple :
        font_grosse = pygame.font.Font(None, 55)
        settings_text_difficulte = font_grosse.render("Difficulté :", True, WHITE)
        screen.blit(settings_text_difficulte, (WIDTH // 25, HEIGHT // 3.9 - 70))

        font_buttons = pygame.font.Font(None, 36)
        easy_text = font_buttons.render("Facile", True, WHITE)
        medium_text = font_buttons.render("Moyen", True, WHITE)
        hard_text = font_buttons.render("Difficile", True, WHITE)
        hardcore_text = font_buttons.render("Hardcore", True, WHITE)

        button_width = 200
        button_height = 50
        total_width = 4 * button_width + 3 * 50
        start_x = (WIDTH - total_width) // 2
        y_position_diff = HEIGHT // 4 - 70

        easy_button = pygame.Rect(start_x, y_position_diff, button_width, button_height)
        medium_button = pygame.Rect(start_x + button_width + 50, y_position_diff, button_width, button_height)
        hard_button = pygame.Rect(start_x + 2 * (button_width + 50), y_position_diff, button_width, button_height)
        hardcore_button = pygame.Rect(start_x + 3 * (button_width + 50), y_position_diff, button_width, button_height)

        if current_difficulty == "facile":
            pygame.draw.rect(screen, (0, 150, 0), easy_button)
        else:
            pygame.draw.rect(screen, (100, 100, 100), easy_button)

        if current_difficulty == "moyen":
            pygame.draw.rect(screen, (190, 180, 0), medium_button)
        else:
            pygame.draw.rect(screen, (100, 100, 100), medium_button)

        if current_difficulty == "difficile":
            pygame.draw.rect(screen, (160, 0, 0), hard_button)
        else:
            pygame.draw.rect(screen, (100, 100, 100), hard_button)

        if current_difficulty == "hardcore":
            pygame.draw.rect(screen, (75, 0, 150), hardcore_button)
        else:
            pygame.draw.rect(screen, (100, 100, 100), hardcore_button)

        screen.blit(easy_text, (easy_button.x + 60, easy_button.y + 12.5))
        screen.blit(medium_text, (medium_button.x + 55, medium_button.y + 12.5))
        screen.blit(hard_text, (hard_button.x + 50, hard_button.y + 12.5))
        screen.blit(hardcore_text, (hardcore_button.x + 50, hardcore_button.y + 12.5))

        settings_text_moves = font_grosse.render("Mouvement :", True, WHITE)
        screen.blit(settings_text_moves, (WIDTH // 25, HEIGHT // 2.2 - 130))

        move_button_width, move_button_height = 150, 50
        total_width_moves = 3 * move_button_width + 2 * 50
        start_x_moves = (WIDTH - total_width_moves) // 2
        y_position_moves = int(HEIGHT // 4 + 90)

        ad_button = pygame.Rect(start_x_moves + (move_button_width + 50), y_position_moves, move_button_width,
                                move_button_height)
        qd_button = pygame.Rect(start_x_moves + 2 * (move_button_width + 50), y_position_moves, move_button_width,
                                move_button_height)
        arrows_button = pygame.Rect(start_x_moves, y_position_moves, move_button_width, move_button_height)

        if current_controls == "ad":
            pygame.draw.rect(screen, (0, 180, 180), ad_button)
        else:
            pygame.draw.rect(screen, (100, 100, 100), ad_button)

        if current_controls == "qd":
            pygame.draw.rect(screen, (0, 180, 180), qd_button)
        else:
            pygame.draw.rect(screen, (100, 100, 100), qd_button)

        if current_controls == "arrows":
            pygame.draw.rect(screen, (0, 180, 180), arrows_button)
        else:
            pygame.draw.rect(screen, (100, 100, 100), arrows_button)

        ad_text = font_buttons.render("A - D", True, WHITE)
        qd_text = font_buttons.render("Q - D", True, WHITE)
        arrows_text = font_buttons.render("Flèches", True, WHITE)

        screen.blit(ad_text, (ad_button.x + 40, ad_button.y + 12.5))
        screen.blit(qd_text, (qd_button.x + 40, qd_button.y + 12.5))
        screen.blit(arrows_text, (arrows_button.x + 27, arrows_button.y + 12.5))

        weapon_text = font_grosse.render("Touche de tir :", True, WHITE)
        screen.blit(weapon_text, (WIDTH // 25, HEIGHT // 4 + 250))

        weapon_text_arme_1 = font_grosse.render("Arme 1", True, WHITE)
        screen.blit(weapon_text_arme_1, (WIDTH // 3.15, HEIGHT // 4 + 250))

        weapon_text_arme_2 = font_grosse.render("Arme 2", True, WHITE)
        screen.blit(weapon_text_arme_2, (WIDTH // 1.615, HEIGHT // 4 + 250))

        weapon1_button_width, weapon1_button_height = 150, 50
        total_width_w1 = 2 * weapon1_button_width + 50
        start_x_w1 = int((WIDTH - total_width_w1) // 3.15)
        y_position_w1 = int(HEIGHT // 4 + 300)

        w1_space_button = pygame.Rect(start_x_w1, y_position_w1, weapon1_button_width, weapon1_button_height)
        w1_left_button = pygame.Rect(start_x_w1 + weapon1_button_width + 50, y_position_w1, weapon1_button_width,
                                     weapon1_button_height)

        if weapon1_control == "space":
            pygame.draw.rect(screen, (160, 0, 0), w1_space_button)
            pygame.draw.rect(screen, (100, 100, 100), w1_left_button)
        else:
            pygame.draw.rect(screen, (100, 100, 100), w1_space_button)
            pygame.draw.rect(screen, (160, 0, 0), w1_left_button)

        w1_space_text = font_buttons.render("Espace", True, WHITE)
        w1_left_text = font_buttons.render("Clic Gauche", True, WHITE)
        screen.blit(w1_space_text, (w1_space_button.x + 30, w1_space_button.y + 12.5))
        screen.blit(w1_left_text, (w1_left_button.x + 4, w1_left_button.y + 12.5))

        weapon2_button_width, weapon2_button_height = 150, 50
        total_width_w2 = 2 * weapon2_button_width + 50
        start_x_w2 = int((WIDTH - total_width_w2) // 1.44)
        y_position_w2 = int(HEIGHT // 4 + 300)

        w2_left_button = pygame.Rect(start_x_w2, y_position_w2, weapon2_button_width, weapon2_button_height)
        w2_right_button = pygame.Rect(start_x_w2 + weapon2_button_width + 50, y_position_w2, weapon2_button_width,
                                      weapon2_button_height)


        if weapon2_control == "left":
            pygame.draw.rect(screen, (0, 0, 150), w2_left_button)
            pygame.draw.rect(screen, (100, 100, 100), w2_right_button)
        else:
            pygame.draw.rect(screen, (100, 100, 100), w2_left_button)
            pygame.draw.rect(screen, (0, 0, 150), w2_right_button)

        w2_left_text = font_buttons.render("Clic Gauche", True, WHITE)
        w2_right_text = font_buttons.render("Clic Droite", True, WHITE)
        screen.blit(w2_left_text, (w2_left_button.x + 4, w2_left_button.y + 12.5))
        screen.blit(w2_right_text, (w2_right_button.x + 15, w2_right_button.y + 12.5))

        # Ajout du Aim Assist
        aimassist_text = font_grosse.render("Aim Assist :", True, WHITE)
        screen.blit(aimassist_text, (WIDTH // 25, HEIGHT // 4 + 440))

        aimassist_button_width = 100
        aimassist_button_height = 50
        start_x_aimassist = int(WIDTH // 2.3)
        y_position_aimassist = int(HEIGHT // 4 + 430)

        aimassist_yes_button = pygame.Rect(
            start_x_aimassist,
            y_position_aimassist,
            aimassist_button_width,
            aimassist_button_height
        )
        aimassist_no_button = pygame.Rect(
            start_x_aimassist + aimassist_button_width + 50,
            y_position_aimassist,
            aimassist_button_width,
            aimassist_button_height
        )

        aimassist_yes_text = font_buttons.render("Oui", True, WHITE)
        aimassist_no_text = font_buttons.render("Non", True, WHITE)

        if aim_assist:
            pygame.draw.rect(screen, (0, 150, 0), aimassist_yes_button)
            pygame.draw.rect(screen, (100, 100, 100), aimassist_no_button)
        else:
            pygame.draw.rect(screen, (100, 100, 100), aimassist_yes_button)
            pygame.draw.rect(screen, (160, 0, 0), aimassist_no_button)

        screen.blit(
            aimassist_yes_text,
            (
                aimassist_yes_button.x + (aimassist_button_width - aimassist_yes_text.get_width()) // 2,
                aimassist_yes_button.y + (aimassist_button_height - aimassist_yes_text.get_height()) // 2
            )
        )
        screen.blit(
            aimassist_no_text,
            (
                aimassist_no_button.x + (aimassist_button_width - aimassist_no_text.get_width()) // 2,
                aimassist_no_button.y + (aimassist_button_height - aimassist_no_text.get_height()) // 2
            )
        )


        # Gestion des clics dans "settings"
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if croix_rect.collidepoint(mouse_x, mouse_y):
                game_state = "menu"
            elif easy_button.collidepoint(mouse_x, mouse_y):
                set_difficulty("facile")
            elif medium_button.collidepoint(mouse_x, mouse_y):
                set_difficulty("moyen")
            elif hard_button.collidepoint(mouse_x, mouse_y):
                set_difficulty("difficile")
            elif hardcore_button.collidepoint(mouse_x, mouse_y):
                set_difficulty("hardcore")
            elif ad_button.collidepoint(mouse_x, mouse_y):
                current_controls = "ad"
            elif qd_button.collidepoint(mouse_x, mouse_y):
                current_controls = "qd"
            elif arrows_button.collidepoint(mouse_x, mouse_y):
                current_controls = "arrows"
            elif w1_space_button.collidepoint(mouse_x, mouse_y):
                set_weapon1("space")
            elif w1_left_button.collidepoint(mouse_x, mouse_y):
                set_weapon1("left")
            elif w2_left_button.collidepoint(mouse_x, mouse_y):
                set_weapon2("left")
            elif w2_right_button.collidepoint(mouse_x, mouse_y):
                set_weapon2("right")
            elif aimassist_yes_button.collidepoint(mouse_x, mouse_y):
                aim_assist = True
            elif aimassist_no_button.collidepoint(mouse_x, mouse_y):
                aim_assist = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if game_state == "settings":
                game_state = "menu"

    elif game_state == "pause":
        x_position_pause = (WIDTH - button_continue.get_width()) // 2
        y_position_pause = (HEIGHT - button_continue.get_height()) // 2

        screen.blit(button_continue, (x_position_pause, y_position_pause - 100))
        screen.blit(button_restart, (x_position_pause, y_position_pause))
        screen.blit(button_quit, (x_position_pause, y_position_pause + 100))

        # On affiche aussi le bouton Pause pour "reprendre" la partie
        pause_pos_x = 10
        pause_pos_y = 70
        screen.blit(button_pause, (pause_pos_x, pause_pos_y))

    elif game_state == "playing":
        if background_index < len(shuffled_backgrounds):
            screen.blit(shuffled_backgrounds[background_index], (0, 0))
        else:
            screen.blit(shuffled_backgrounds[-1], (0, 0))

        show_level(level)

        if not game_over:
            keys = pygame.key.get_pressed()

            if current_controls == "arrows":
                if keys[pygame.K_LEFT] and spaceship_x > 0:
                    spaceship_x -= spaceship_speed
                if keys[pygame.K_RIGHT] and spaceship_x < WIDTH - 155:
                    spaceship_x += spaceship_speed

            elif current_controls == "ad":
                if keys[pygame.K_a] and spaceship_x > 0:
                    spaceship_x -= spaceship_speed
                if keys[pygame.K_d] and spaceship_x < WIDTH - 155:
                    spaceship_x += spaceship_speed

            elif current_controls == "qd":
                if keys[pygame.K_q] and spaceship_x > 0:
                    spaceship_x -= spaceship_speed
                if keys[pygame.K_d] and spaceship_x < WIDTH - 155:
                    spaceship_x += spaceship_speed

            if aim_assist:
                pygame.draw.line(
                    screen,
                    GREEN,
                    (spaceship_x + 75, spaceship_y + 75),
                    (spaceship_x + 75, 0),
                    2
                )

            for bullet in bullets[:]:
                bullet["rect"].x += bullet["velocity"][0]
                bullet["rect"].y += bullet["velocity"][1]
                if bullet["rect"].y < 0:
                    bullets.remove(bullet)

            for bullet in secondary_bullets[:]:
                bullet["rect"].x += bullet["velocity"][0]
                bullet["rect"].y += bullet["velocity"][1]
                if (bullet["rect"].y < 0 or
                        bullet["rect"].x < 0 or
                        bullet["rect"].x > WIDTH or
                        bullet["rect"].y > HEIGHT):
                    secondary_bullets.remove(bullet)

            if not boss and random.random() < alien_spawn_rate:
                spawn_alien()

            for alien in aliens[:]:
                alien["rect"].y += alien_speed

                if alien["rect"].y > HEIGHT:
                    handle_life_loss()
                    break

                if pygame.Rect(spaceship_x, spaceship_y, 150, 125).colliderect(alien["rect"]):
                    handle_life_loss()

                for bullet in bullets[:]:
                    if bullet["rect"].colliderect(alien["rect"]):
                        bullets.remove(bullet)
                        aliens.remove(alien)
                        score += 1

                        if score % 10 == 0 and level < max_level:
                            level += 1
                            background_index += 1
                            alien_speed += 0.5
                            alien_spawn_rate += 0.001
                        elif score % 10 == 0 and level == max_level:
                            game_state = "victory"
                        break

                for bullet in secondary_bullets[:]:
                    if bullet["rect"].colliderect(alien["rect"]):
                        secondary_bullets.remove(bullet)
                        aliens.remove(alien)
                        score += 1

                        if score % 10 == 0 and level < max_level:
                            level += 1
                            background_index += 1
                            alien_speed += 0.5
                            alien_spawn_rate += 0.001
                        elif score % 10 == 0 and level == max_level:
                            game_state = "victory"
                        break

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
                screen.blit(alien["surface"], alien["rect"])

            for bullet in bullets:
                screen.blit(bullet_image, bullet["rect"])

            for bullet in secondary_bullets:
                pygame.draw.ellipse(screen, BLUE, bullet["rect"])

            screen.blit(spaceship_image, (spaceship_x, spaceship_y))
            draw_text(f"Score: {score}", 10, 10)
            draw_text(f"Vie : {lives}", WIDTH - 85, 45)
            draw_text(f"Balles restantes: {remaining_bullets}", 10, 40)

            # On dessine (affiche) le bouton Pause
            pause_pos_x = 10
            pause_pos_y = 70
            screen.blit(button_pause, (pause_pos_x, pause_pos_y))


    # GAME OVER
    if game_over:
        # Dessin du fond
        larger_font_titre = pygame.font.Font(None, 100)  # Taille 150 pour un texte plus grand
        larger_font_text = pygame.font.Font(None, 35)  # Taille 150 pour un texte plus grand

        screen.blit(background_images[0], (0, 0))
        draw_text("GAME OVER!", WIDTH // 2, HEIGHT // 8 - 50, RED, larger_font_titre, centered=True)
        draw_text("VOUS AVEZ PERDU, SOUHAITé VOUS RECOMMENCER OU QUITTER ?", WIDTH // 2, HEIGHT // 7, WHITE, larger_font_text, centered=True)


        # Position des boutons
        x_position_pause = (WIDTH - button_continue.get_width()) // 2
        y_position_pause = (HEIGHT - button_continue.get_height()) // 2

        button_restart_rect = button_restart.get_rect(
            topleft=(x_position_pause, y_position_pause - 50)
        )
        button_quit_rect2 = button_quit.get_rect(
            topleft=(x_position_pause, y_position_pause + 50)
        )

        pause_pos_x = 10
        pause_pos_y = 70
        pause_button_rect = button_pause.get_rect(topleft=(pause_pos_x, pause_pos_y))

        # Dessin des boutons
        screen.blit(button_restart, button_restart_rect.topleft)
        screen.blit(button_quit, button_quit_rect2.topleft)

        # Gestion des événements souris
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:  # Clic gauche
            if pause_button_rect.collidepoint(mouse_x, mouse_y):
                game_state = "playing"
            elif button_restart_rect.collidepoint(mouse_x, mouse_y):
                reset_game()
                game_state = "playing"
            elif button_quit_rect2.collidepoint(mouse_x, mouse_y):
                reset_game()
                game_state = "menu"


    # VICTORY
    elif game_state == "victory":

        larger_font_titre = pygame.font.Font(None, 100)  # Taille 150 pour un texte plus grand
        larger_font_text = pygame.font.Font(None, 35)  # Taille 150 pour un texte plus grand

        screen.blit(background_images[0], (0, 0))
        draw_text("FÉLICITATIONS, VOUS AVEZ GAGNÉ!", WIDTH // 2, HEIGHT // 8 - 50, WHITE, large_font, centered=True)

        # Position des boutons
        x_position_pause = (WIDTH - button_continue.get_width()) // 2
        y_position_pause = (HEIGHT - button_continue.get_height()) // 2

        button_restart_rect = button_restart.get_rect(
            topleft=(x_position_pause, y_position_pause - 50)
        )
        button_quit_rect2 = button_quit.get_rect(
            topleft=(x_position_pause, y_position_pause + 50)
        )

        pause_pos_x = 10
        pause_pos_y = 70
        pause_button_rect = button_pause.get_rect(topleft=(pause_pos_x, pause_pos_y))

        # Dessin des boutons
        screen.blit(button_restart, button_restart_rect.topleft)
        screen.blit(button_quit, button_quit_rect2.topleft)

        # Gestion des événements souris
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:  # Clic gauche
            if pause_button_rect.collidepoint(mouse_x, mouse_y):
                game_state = "playing"
            elif button_restart_rect.collidepoint(mouse_x, mouse_y):
                reset_game()
                game_state = "playing"
            elif button_quit_rect2.collidepoint(mouse_x, mouse_y):
                reset_game()
                game_state = "menu"

    pygame.display.flip()

pygame.quit()