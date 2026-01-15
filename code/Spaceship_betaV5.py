# nom_du_programme : spaceship_betaV5.py
# createur_du_programme : Samuel_Antunes/Dani_Dordevic
# date_de_creation : 11.12.2024

import pygame
import random
import math
import json
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


# Initialiser son pygame
pygame.mixer.init()
# crée un petit local de musique
music_channel = pygame.mixer.Channel(0)
# Initialiser pygame
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
#                          CHARGEMENT DES IMAGES                               #
################################################################################


# Vaisseaux
spaceship_images = [
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin.png")), (150, 150)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin2.png")), (150, 150)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin3.png")), (150, 150)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin3.png")), (150, 150)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin4.png")), (150, 100)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin10.png")), (150, 200)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin5.png")), (150, 150)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin9.png")), (150, 150)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin7.png")), (150, 150)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin8.png")), (150, 150)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "vaisseau", "spaceship_skin11.png")), (150, 150)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "Boss_alien_alien", "boss_3_final.png")),(150, 150)),
]

# Alien de base (on fera un scale aléatoire lors du spawn)
alien_image = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "Boss_alien_alien", "alien.png")), (55, 55))
alien_en_or_image = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "Boss_alien_alien", "alien_en_or.png")), (55, 55))
alien_en_diamant_image = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "Boss_alien_alien", "alien_en_diamant.png")), (55, 55))
alien_attaquant = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "Boss_alien_alien", "alien_attaquant.png")), (55, 45))

# Balle rouge (dessinée à la main)
bullet_image = pygame.Surface((10, 20), pygame.SRCALPHA)
pygame.draw.ellipse(bullet_image, RED, (0, 0, 10, 20))

# Arrière-plans
background_images = [
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "background", "background12.jpg")), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "background", "background14.jpg")), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "background", "background13.jpg")), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "background", "background3.png")),(WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "background", "background15.jpg")), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "background", "background6.jpg")),(WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "background", "background7.jpg")), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "background", "background9.jpg")),(WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "background", "background10.jpg")), (WIDTH, HEIGHT)),
]

# --- On mélange la liste pour un ordre unique
shuffled_backgrounds = background_images[:]
random.shuffle(shuffled_backgrounds)
background_index = 0  # On part du premier

# Boss
# boss_image = pygame.transform.scale(pygame.image.load(current_directory + "/image/Boss_alien_alien/boss.png"), (800, 400))
boss_image = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "Boss_alien_alien", "boss.png")), (800, 400))
boss_2_image = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "Boss_alien_alien", "boss_image_2.png")), (150, 400))
boss_3_final = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "Boss_alien_alien", "boss_3_final.png")), (800, 400))

# Boutons
button_play = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "bouton", "button_play.png")), (200, 50))
button_quit = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "bouton", "button_quit.png")), (200, 50))
button_settings = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "bouton", "button_settings.png")), (200, 50))
button_restart = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "bouton", "button_restart.png")), (200, 50))
button_continue = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "bouton", "button_continue.png")), (200, 50))
button_pause = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "bouton", "button_pause.png")), (50, 50))

# Titre / croix / pièce / fleche choix skin/ pièce
titre_jeu = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "background", "MainMenu.png")), (200, 80))
croix_retour_page = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "bouton", "croix_noir.png")), (40, 40))
fleche_choix_skin_gauche = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "bouton", "fleches_choix_skin_gauche.png")), (60, 60))
fleche_choix_skin_droite = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "bouton", "fleches_choix_skin_droite.png")), (60, 60))
piece = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "pièces_et_bonus", "pièce.png")), (60, 60))

# Bonus / powerups (icône affichée en jeu)
bonus = pygame.transform.scale(pygame.image.load(os.path.join(current_directory, "image", "pièces_et_bonus", "bonus.png")),(45, 55))


################################################################################
#                      chargement des fichiers audio                           #
################################################################################


# Charger les différents sons dans un dictionnaire
sons = {
    "explosion_alien_vaisseau": pygame.mixer.Sound(os.path.join(current_directory, "son", "explosion_alien_vaisseau.mp3")),
    "explosion_boss": pygame.mixer.Sound(os.path.join(current_directory, "son", "explosion_boss.mp3")),
    "dégât_boss": pygame.mixer.Sound(os.path.join(current_directory, "son", "dégât_boss.mp3")),
    "victoire": pygame.mixer.Sound(os.path.join(current_directory, "son", "victoire.mp3")),
    "défaite": pygame.mixer.Sound(os.path.join(current_directory, "son", "défaite.mp3")),
    "tir": pygame.mixer.Sound(os.path.join(current_directory, "son", "son_de_tir.mp3")),
}

musique = {
    "boss_musique": pygame.mixer.Sound(os.path.join(current_directory, "son", "musique_du_jeu", "music_boss.mp3")),
    "music_game_1": pygame.mixer.Sound(os.path.join(current_directory, "son", "musique_du_jeu", "music_in_game_1.mp3")),
    "music_game_2": pygame.mixer.Sound(os.path.join(current_directory, "son", "musique_du_jeu", "music_in_game_2.mp3")),
    "music_game_3": pygame.mixer.Sound(os.path.join(current_directory, "son", "musique_du_jeu", "music_in_game_3.mp3")),
    "music_game_4": pygame.mixer.Sound(os.path.join(current_directory, "son", "musique_du_jeu", "music_in_game_4.mp3")),
    "music_game_5": pygame.mixer.Sound(os.path.join(current_directory, "son", "musique_du_jeu", "music_in_game_5.mp3")),
    "music_game_6": pygame.mixer.Sound(os.path.join(current_directory, "son", "musique_du_jeu", "music_in_game_6.mp3")),
    "music_game_7": pygame.mixer.Sound(os.path.join(current_directory, "son", "musique_du_jeu", "music_in_game_7.mp3")),
    "music_game_8": pygame.mixer.Sound(os.path.join(current_directory, "son", "musique_du_jeu", "music_in_game_8.mp3")),
    "music_game_9": pygame.mixer.Sound(os.path.join(current_directory, "son", "musique_du_jeu", "music_in_game_9.mp3")),
    "music_start_game": pygame.mixer.Sound(os.path.join(current_directory, "son", "musique_du_jeu", "music_start_game.mp3")),
}

musique_menu = {"music_menu": pygame.mixer.Sound(os.path.join(current_directory, "son", "musique_du_jeu", "music_menu.mp3")),
}

# Liste des musiques mélangées
music_list = list(musique.values())
random.shuffle(music_list)
music_index = 0

# Réduire le volume global si tu veux appliquer à tous les sons
volume_reduit = 0.33  # volume réduit de 3 fois
for son in sons.values():
    son.set_volume(volume_reduit)


################################################################################
#                      VARIABLES GLOBALES / ÉTAT INITIAL                       #
################################################################################


spaceship_x, spaceship_y = WIDTH // 2 - 75, HEIGHT - 150
spaceship_speed = 10

spaceship_speed_base = spaceship_speed  # pour restaurer après un bonus vitesse
bullet_speed = 15
secondary_bullet_speed = 12
alien_speed = 2

# --- Motion / animation des aliens (tuning) ---
ASTEROID_ZIGZAG_CHANCE = 0.35
ASTEROID_ZIGZAG_SPEED_MIN = 1.8
ASTEROID_ZIGZAG_SPEED_MAX = 3.8

ASTEROID_ROTATE_CHANCE = 0.45
ASTEROID_ROTATE_SPEED_MIN = 1.0
ASTEROID_ROTATE_SPEED_MAX = 4.0

SHOOTER_SPEED_X_MIN = 2.8
SHOOTER_SPEED_X_MAX = 4.2
SHOOTER_Y_MIN = 40
SHOOTER_Y_MAX = 200

bonus_spawn_rate = 0.0012  # spawn de bonus 'par frame' (indépendant des aliens)

bullets = []
secondary_bullets = []
enemy_bullets = []
aliens = []

# --- Bonus / powerups (pickups ramassables) ---
bonuses = []  # objets bonus qui tombent et que le joueur peut ramasser
active_powerups = {"speed": 0, "multishot": 0, "shield": 0}  # timestamp (ms) de fin ; 0 = inactif
last_pickup_text = ""
last_pickup_until = 0

SPEED_BOOST_MULT = 1.35
POWERUP_DURATION_MS = {"speed": 8000, "multishot": 9000, "shield": 15000}

BONUS_FALL_SPEED = 3
BONUS_TTL_MS = 15000
score = 0
level = 1
max_level = 10
start_time = 0
end_time = None
shots_fired = 0
shots_hit = 0
alien_spawn_rate = 0.005
alien_en_or_spawn_rate = 0.0005
alien_en_diamant_spawn_rate = 0.0001
alien_attaquant_spawn_rate = 0.002
game_state = "login"

# --- Login / profil ---
player_name = ""
coins = 0

# --- Skins / boutique ---
# Prix par skin (index = skin). Ajuste librement.
SKIN_PRICES = [
    0,  # skin 0 (de base)
    100,
    250,
    500,
    750,
    1000,
    1250,
    1500,
    1800,
    2100,
    3000,
    5000,  # dernier skin (skin du boss final)   
]

unlocked_skins = 1  # skins possédés (1 = uniquement le skin 0)
equipped_skin = 0  # skin utilisé en jeu
selected_skin = 0  # skin actuellement sélectionné dans le menu
boss3_defeated_once = False

current_language = "fr"

spaceship_image = spaceship_images[equipped_skin]

current_difficulty = "moyen"
current_controls = "ad"
weapon1_control = "space"
weapon2_control = "left"

aim_assist = False

# --- Boss (multi-boss) ---
boss_id = None  # 1 / 2 / 3 pendant un combat
pending_level_after_boss = None  # niveau après mort boss (boss1/boss2)
boss_surface = boss_image  # image du boss en cours

# Boss
boss = None
boss_health = 50
boss_max_health = 50
boss_max_health_cap = 120  # évite que le combat devienne infini si tu joues très longtemps
boss_direction = 1

# Hitbox (collision) du boss : on la rend plus juste que le rect de rendu (utile pour le boss 2 plus fin)
boss_hitbox = None

# --- Cinématique mort du boss (freeze + explosion) ---
boss_death_pending = None  # dict: {"center": (x,y), "boss_id": int, "pending_level": int, "freeze": Surface}
boss_death_anim = {"active": False, "freeze": None, "start_ms": 0, "duration_ms": 1500,
                "center": (0, 0), "next_burst_ms": 0, "bursts_left": 0,
                 "shake_end_ms": 0, "flash_end_ms": 0,
                 "powerups_snapshot": None, "boss_id": None, "pending_level": None}


# Timers boss (attaques / scaling PV)
boss_fight_start = 0
boss_last_shot = 0
boss_last_special = 0
boss_last_regen = 0

# Attaques boss (lasers / zones)
boss_lasers = []
boss_zones = []
boss_last_laser = 0
boss_last_zone = 0
boss_last_fan = 0
boss_last_burst = 0
boss_last_minion = 0
boss_last_rain = 0

remaining_bullets = 1000
lives = 5
game_over = False

font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 48)
hud_font = pygame.font.Font(None, 26)  # HUD bonus/powerups


################################################################################
#                         PARTICLES / FX (rétro)                               #
################################################################################


# Deux surfaces alpha dédiées (effets derrière / devant les sprites)
fx_surface_under = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
fx_surface_over = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# Particules : trail (trainée) + explosion
trail_particles = []
explosion_particles = []
shockwaves = []

# Tuning (modifie ici si tu veux +/− d'effets)
TRAIL_SPAWN_MS = 45  # fréquence de génération de la trainée par astéroïde
TRAIL_LIFE_FRAMES = 18  # durée de vie (frames)
TRAIL_ALPHA_START = 190  # alpha initial (0..255)
TRAIL_ALPHA_DECAY = 0.86  # décroissance multiplicative par frame
TRAIL_RADIUS_MIN = 2
TRAIL_RADIUS_MAX = 5
TRAIL_MAX_PARTICLES = 1600

EXPLOSION_PARTICLES_MIN = 22
EXPLOSION_PARTICLES_MAX = 42
EXPLOSION_LIFE_FRAMES = 26
EXPLOSION_ALPHA_START = 230
EXPLOSION_ALPHA_DECAY = 0.88
EXPLOSION_RADIUS_MIN = 2
EXPLOSION_RADIUS_MAX = 6
EXPLOSION_MAX_PARTICLES = 1100

SHOCKWAVE_LIFE_FRAMES = 18


################################################################################
#                               FONCTIONS DE JEU                               #
################################################################################


def set_difficulty(difficulty):
    """Configure les paramètres de base selon la difficulté.

    Remarque importante:
    - Les *spawn_rate* sont des probabilités "par frame" (random.random() < rate).
      À 60 FPS, un rate de 0.007 ≈ 0.42 spawn/s en moyenne.
    """

    global current_difficulty
    global remaining_bullets, alien_speed, alien_spawn_rate
    global alien_en_or_spawn_rate, alien_en_diamant_spawn_rate, alien_attaquant_spawn_rate
    global lives, aim_assist, bonus_spawn_rate

    difficulty = (difficulty or "").strip().lower()

    # Valeurs de base (début de partie)
    PROFILES = {
        "facile": {
            "remaining_bullets": 1000,
            "alien_speed": 2.0,
            "alien_spawn_rate": 0.007,  # un peu plus vivant qu'avant
            "alien_en_or_spawn_rate": 0.0005,
            "alien_en_diamant_spawn_rate": 0.0001,
            "alien_attaquant_spawn_rate": 0.002,
            "bonus_spawn_rate": 0.0012,
            "lives": 5,
            "aim_assist": True,
        },
        "moyen": {
            "remaining_bullets": 500,
            "alien_speed": 2.0,
            "alien_spawn_rate": 0.010,
            "alien_en_or_spawn_rate": 0.0010,
            "alien_en_diamant_spawn_rate": 0.00025,
            "alien_attaquant_spawn_rate": 0.004,
            "bonus_spawn_rate": 0.0010,
            "lives": 3,
            "aim_assist": True,
        },
        "difficile": {
            "remaining_bullets": 200,
            "alien_speed": 2.5,
            "alien_spawn_rate": 0.015,
            "alien_en_or_spawn_rate": 0.0015,
            "alien_en_diamant_spawn_rate": 0.0005,
            "alien_attaquant_spawn_rate": 0.008,
            "bonus_spawn_rate": 0.0009,
            "lives": 2,
            "aim_assist": False,
        },
        "hardcore": {
            "remaining_bullets": 100,
            "alien_speed": 3.0,
            "alien_spawn_rate": 0.020,
            "alien_en_or_spawn_rate": 0.0020,
            "alien_en_diamant_spawn_rate": 0.0010,
            "alien_attaquant_spawn_rate": 0.010,
            "bonus_spawn_rate": 0.0008,
            "lives": 1,
            "aim_assist": False,
        },
    }

    if difficulty not in PROFILES:
        # fallback sûr (évite de planter le jeu)
        difficulty = "moyen"

    cfg = PROFILES[difficulty]
    current_difficulty = difficulty

    remaining_bullets = cfg["remaining_bullets"]
    alien_speed = cfg["alien_speed"]
    alien_spawn_rate = cfg["alien_spawn_rate"]
    alien_en_or_spawn_rate = cfg["alien_en_or_spawn_rate"]
    alien_en_diamant_spawn_rate = cfg["alien_en_diamant_spawn_rate"]
    alien_attaquant_spawn_rate = cfg["alien_attaquant_spawn_rate"]
    lives = cfg["lives"]
    aim_assist = cfg["aim_assist"]

    bonus_spawn_rate = cfg.get("bonus_spawn_rate", bonus_spawn_rate)
    persist_save()


def reset_game():
    """
    Réinitialise toutes les variables pour relancer une partie neuve.
    On re-mélange aussi la liste shuffled_backgrounds
    pour s'assurer qu'on ne retrouve pas le même ordre de fonds.
    """
    global spaceship_x, spaceship_y, bullets, secondary_bullets, enemy_bullets, aliens, bonuses, musique
    global score, level, game_state, boss, boss_health, boss_max_health, boss_direction
    global boss_fight_start, boss_last_shot, boss_last_special, boss_last_regen, boss_last_laser, boss_last_zone, boss_last_fan, boss_last_burst, boss_last_minion, boss_last_rain, boss_hitbox, boss_max_health_cap
    global boss_lasers, boss_zones, current_difficulty, aim_assist
    global remaining_bullets, game_over, spaceship_image
    global spaceship_speed, spaceship_speed_base, active_powerups, last_pickup_text, last_pickup_until
    global shuffled_backgrounds, background_index, music_list, music_index
    global coins_gained_this_run
    global start_time, end_time
    global shots_fired, shots_hit
    global boss_death_pending, boss_death_anim
    global boss_id, pending_level_after_boss, boss_surface, equipped_skin

    start_time = pygame.time.get_ticks()
    end_time = None

    spaceship_x, spaceship_y = WIDTH // 2 - 75, HEIGHT - 150

    bullets.clear()
    enemy_bullets.clear()
    boss_lasers.clear()
    boss_zones.clear()
    secondary_bullets.clear()
    aliens.clear()
    boss_lasers.clear()
    boss_zones.clear()

    score = 0
    level = 1
    boss = None
    boss_id = None
    pending_level_after_boss = None
    boss_surface = boss_image
    boss_health = 50
    boss_max_health = 50
    boss_direction = 1
    boss_fight_start = 0
    boss_last_shot = 0
    boss_last_special = 0
    boss_last_regen = 0
    boss_last_laser = 0
    boss_last_zone = 0
    boss_last_fan = 0
    boss_last_burst = 0
    boss_last_minion = 0
    boss_last_rain = 0
    boss_hitbox = None
    boss_max_health_cap = 120
    game_over = False
    coins_gained_this_run = 0
    shots_fired = 0
    shots_hit = 0

    # Bonus / powerups
    bonuses.clear()

    # FX (trainées / explosions)
    trail_particles.clear()
    explosion_particles.clear()
    shockwaves.clear()
    boss_death_pending = None
    boss_death_anim = {"active": False, "freeze": None, "start_ms": 0, "duration_ms": 1500,
                     "center": (0, 0), "next_burst_ms": 0, "bursts_left": 0,
                     "shake_end_ms": 0, "flash_end_ms": 0,
                     "powerups_snapshot": None, "boss_id": None, "pending_level": None}
    active_powerups = {"speed": 0, "multishot": 0, "shield": 0}
    last_pickup_text = ""
    last_pickup_until = 0
    spaceship_speed = spaceship_speed_base

    # On re-mélange les backgrounds (inchangé)
    random.shuffle(shuffled_backgrounds)
    background_index = 0

    # 🎵 --------- MUSIQUE (corrigé) ---------
    random.shuffle(music_list)  # mélange la playlist
    music_index = 0  # recommence au début
    play_next_music()  # lance la musique
    # 🎵 ------------------------------------

    # Skin choisi
    spaceship_image = spaceship_images[equipped_skin]

    # Remet la difficulté courante
    set_difficulty(current_difficulty)


def advance_level(next_level=None):
    """
    Passe au niveau suivant (ou next_level) + augmente légèrement la vitesse de descente
    des aliens/astéroïdes via alien_speed.
    """
    global level, background_index, alien_speed, current_difficulty

    old_level = level
    if next_level is None:
        next_level = level + 1

    # Combien de niveaux on gagne d'un coup (sécurité)
    gained = max(0, next_level - old_level)

    # Réglage de l'augmentation par difficulté (à ajuster selon ton feeling)
    SPEED_GROWTH = {
        "facile": {"inc": 0.1, "max": 3.0},
        "moyen": {"inc": 0.15, "max": 3.5},
        "difficile": {"inc": 0.15, "max": 4.0},
        "hardcore": {"inc": 0.2, "max": 5.0},
    }

    cfg = SPEED_GROWTH.get(current_difficulty, SPEED_GROWTH["moyen"])
    alien_speed = min(cfg["max"], alien_speed + cfg["inc"] * gained)

    level = next_level
    background_index += 1


def spawn_boss_by_id(bid):
    """Fait apparaître un boss (1/2/3)."""
    global boss, boss_health, boss_max_health, boss_max_health_cap, boss_hitbox
    global boss_fight_start, boss_last_shot, boss_last_special, boss_last_regen, boss_last_laser, boss_last_zone
    global boss_last_fan, boss_last_burst, boss_last_minion, boss_last_rain
    global boss_lasers, boss_zones
    global boss_id, pending_level_after_boss, boss_surface

    aliens.clear()
    enemy_bullets.clear()
    secondary_bullets.clear()
    boss_lasers.clear()
    boss_zones.clear()

    boss_id = bid
    boss_surface = boss_image if bid == 1 else (boss_2_image if bid == 2 else boss_3_final)

    # PV / cap (1 facile, 2 moyen, 3 difficile)
    if bid == 1:
        boss_max_health = 50
        boss_max_health_cap = 85
    elif bid == 2:
        boss_max_health = 75
        boss_max_health_cap = 130
    else:
        # Boss 3 rendu plus accessible
        boss_max_health = 90
        boss_max_health_cap = 90  # pas de regen infinie sur le boss 3

    boss_health = boss_max_health

    # Rect de rendu = taille exacte de l'image (corrige les hitbox/tailles incohérentes)
    boss = boss_surface.get_rect(midtop=(WIDTH // 2, 30))
    boss_hitbox = compute_boss_hitbox(boss, boss_id)

    boss_fight_start = pygame.time.get_ticks()
    boss_last_shot = boss_fight_start
    boss_last_special = boss_fight_start
    boss_last_regen = boss_fight_start
    boss_last_laser = boss_fight_start
    boss_last_zone = boss_fight_start
    boss_last_fan = boss_fight_start
    boss_last_burst = boss_fight_start
    boss_last_minion = boss_fight_start
    boss_last_rain = boss_fight_start

    pending_level_after_boss = (level + 1) if bid in (1, 2) else None


def handle_level_completion():
    """Appelée quand score%10==0 : boss aux niveaux 3/6/10 sinon level up."""
    global end_time, game_state

    if boss:
        return

    if level == 3:
        spawn_boss_by_id(1)
        return
    if level == 6:
        spawn_boss_by_id(2)
        return
    if level == 10:
        spawn_boss_by_id(3)
        return

    if level < max_level:
        advance_level()
    else:
        end_time = pygame.time.get_ticks()
        game_state = "victory"


def handle_life_loss():
    # Bouclier actif: on ignore la perte de vie
    if is_powerup_active("shield", pygame.time.get_ticks()):
        return

    global lives, spaceship_x, spaceship_y, aliens, bullets, secondary_bullets, enemy_bullets, boss_lasers, boss_zones, game_over, victory, end_time
    spaceship_x, spaceship_y = WIDTH // 2 - 75, HEIGHT - 150
    aliens.clear()
    bullets.clear()
    secondary_bullets.clear()
    enemy_bullets.clear()
    lives -= 1
    sons["explosion_alien_vaisseau"].play()

    if lives <= 0:
        end_time = pygame.time.get_ticks()
        sons["défaite"].play()
        game_over = True
        music_channel.stop()


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


###############################################################################
#                                FX / PARTICULES                               #
###############################################################################


def _fx_palette_for_alien(alien_type):
    """Palette rétro selon le type (normal/gold/diamond/shooter)."""
    if alien_type == "gold":
        return [(255, 220, 80), (255, 140, 0), (255, 255, 255)]
    if alien_type == "diamond":
        return [(90, 220, 255), (180, 80, 255), (255, 255, 255)]
    if alien_type == "shooter":
        return [(255, 80, 80), (255, 220, 90), (255, 255, 255)]
    if alien_type == "boss":
        return [(255, 120, 40), (255, 60, 0), (255, 230, 120), (255, 255, 255)]
    return [(210, 210, 210), (120, 220, 255), (255, 255, 255)]


def _fx_base_color(alien_type):
    if alien_type == "gold":
        return (255, 200, 40)
    if alien_type == "diamond":
        return (80, 220, 255)
    if alien_type == "shooter":
        return (255, 80, 80)
    if alien_type == "boss":
        return (255, 120, 40)
    return (190, 190, 190)


def spawn_asteroid_trail(alien, now_ms):
    """Trainée derrière les astéroïdes (pas pour shooter)."""
    if alien.get("type") == "shooter":
        return

    last = int(alien.get("trail_last_ms", 0))
    if now_ms - last < TRAIL_SPAWN_MS:
        return
    alien["trail_last_ms"] = int(now_ms)

    # Direction de déplacement (vx + chute)
    vx = float(alien.get("vx", 0.0))
    vy = float(alien_speed)  # chute verticale (global)
    speed = math.hypot(vx, vy)
    if speed < 0.001:
        return

    ux, uy = vx / speed, vy / speed  # direction "avant"
    cx, cy = float(alien["pos"][0]), float(alien["pos"][1])

    # Point de spawn "derrière" l'astéroïde
    back_offset = max(12.0, float(alien["rect"].width) * 0.38)
    px = cx - ux * back_offset + random.uniform(-2.5, 2.5)
    py = cy - uy * back_offset + random.uniform(-2.5, 2.5)

    base = _fx_base_color(alien.get("type", "normal"))
    count = 1 if speed < 3.0 else 2

    for _ in range(count):
        trail_particles.append({
            "pos": [px + random.uniform(-3.0, 3.0), py + random.uniform(-3.0, 3.0)],
            # drift vers l'arrière + un peu de jitter
            "vel": [-ux * random.uniform(0.8, 1.7) + random.uniform(-0.6, 0.6),
                    -uy * random.uniform(0.8, 1.7) + random.uniform(-0.6, 0.6)],
            "r": random.randint(TRAIL_RADIUS_MIN, TRAIL_RADIUS_MAX),
            "col": base,
            "a": float(TRAIL_ALPHA_START),
            "life": int(TRAIL_LIFE_FRAMES),
        })

    # Cap (évite les explosions de mémoire si beaucoup d'aliens)
    if len(trail_particles) > TRAIL_MAX_PARTICLES:
        del trail_particles[:len(trail_particles) - TRAIL_MAX_PARTICLES]


def spawn_explosion_fx(x, y, alien_type="normal", scale=1.0):
    """Explosion rétro (sparks + anneau)."""
    palette = _fx_palette_for_alien(alien_type)
    n = random.randint(EXPLOSION_PARTICLES_MIN, EXPLOSION_PARTICLES_MAX)
    n = max(8, int(n * float(scale)))

    for _ in range(n):
        ang = random.uniform(0.0, math.tau)
        spd = random.uniform(1.6, 7.8) * float(scale)
        vx = math.cos(ang) * spd
        vy = math.sin(ang) * spd + random.uniform(-1.2, 1.8)  # léger biais vers le bas
        col = random.choice(palette)

        explosion_particles.append({
            "pos": [float(x), float(y)],
            "vel": [vx, vy],
            "r": random.randint(EXPLOSION_RADIUS_MIN, EXPLOSION_RADIUS_MAX),
            "col": col,
            "a": float(EXPLOSION_ALPHA_START),
            "life": int(EXPLOSION_LIFE_FRAMES),
        })

    shockwaves.append({
        "x": float(x),
        "y": float(y),
        "r": 6.0 * float(scale),
        "dr": 3.7 * float(scale),
        "a": 210.0,
        "life": int(SHOCKWAVE_LIFE_FRAMES),
    })

    if len(explosion_particles) > EXPLOSION_MAX_PARTICLES:
        del explosion_particles[:len(explosion_particles) - EXPLOSION_MAX_PARTICLES]


def update_fx():
    """Update (position + fade) des particules."""
    for p in trail_particles[:]:
        p["pos"][0] += p["vel"][0]
        p["pos"][1] += p["vel"][1]
        p["a"] *= TRAIL_ALPHA_DECAY
        p["life"] -= 1
        if p["life"] <= 0 or p["a"] <= 4:
            trail_particles.remove(p)

    for p in explosion_particles[:]:
        p["pos"][0] += p["vel"][0]
        p["pos"][1] += p["vel"][1]
        # petite gravité pour un rendu plus "arcade"
        p["vel"][1] += 0.05
        p["a"] *= EXPLOSION_ALPHA_DECAY
        p["life"] -= 1
        if p["life"] <= 0 or p["a"] <= 4:
            explosion_particles.remove(p)

    for s in shockwaves[:]:
        s["r"] += s["dr"]
        s["dr"] *= 0.92
        s["a"] *= 0.86
        s["life"] -= 1
        if s["life"] <= 0 or s["a"] <= 6:
            shockwaves.remove(s)


def render_fx_surfaces():
    """Redessine les 2 surfaces FX (under/over). À appeler une fois par frame avant le rendu."""
    fx_surface_under.fill((0, 0, 0, 0))
    fx_surface_over.fill((0, 0, 0, 0))

    # Trainées (derrière)
    for p in trail_particles:
        x, y = int(p["pos"][0]), int(p["pos"][1])
        if x < -10 or x > WIDTH + 10 or y < -10 or y > HEIGHT + 10:
            continue
        r, g, b = p["col"]
        a = int(max(0, min(255, p["a"])))
        rad = int(p["r"])
        pygame.draw.circle(fx_surface_under, (r, g, b, a), (x, y), rad)
        # petit core lumineux
        if rad >= 3:
            pygame.draw.circle(fx_surface_under, (255, 255, 255, min(255, a)), (x, y), max(1, rad - 2))

    # Explosions (devant)
    for p in explosion_particles:
        x, y = int(p["pos"][0]), int(p["pos"][1])
        if x < -30 or x > WIDTH + 30 or y < -30 or y > HEIGHT + 30:
            continue
        r, g, b = p["col"]
        a = int(max(0, min(255, p["a"])))
        pygame.draw.circle(fx_surface_over, (r, g, b, a), (x, y), int(p["r"]))

    # Shockwaves (anneau)
    for s in shockwaves:
        x, y = int(s["x"]), int(s["y"])
        a = int(max(0, min(255, s["a"])))
        pygame.draw.circle(fx_surface_over, (255, 255, 255, a), (x, y), int(s["r"]), width=2)



###############################################################################
#                    CINEMATIQUE : EXPLOSION + FREEZE DU BOSS                 #
###############################################################################

def start_boss_death_sequence(freeze_surface, center, boss_id_local, pending_level_local):
    """Démarre la cinématique : écran figé + explosion animée (non-bloquante)."""
    global game_state, boss_death_anim, trail_particles, explosion_particles, shockwaves, active_powerups

    now = pygame.time.get_ticks()

    # Nettoie les FX existantes pour que l'écran figé reste "propre"
    trail_particles.clear()
    explosion_particles.clear()
    shockwaves.clear()

    boss_death_anim.update({
        "active": True,
        "freeze": freeze_surface.copy(),
        "start_ms": now,
        "center": (int(center[0]), int(center[1])),
        "next_burst_ms": now + 90,
        "bursts_left": 9,
        "shake_end_ms": now + 420,
        "flash_end_ms": now + 140,
        "powerups_snapshot": dict(active_powerups),
        "boss_id": boss_id_local,
        "pending_level": pending_level_local,
    })

    # Explosion initiale (grosse)
    spawn_explosion_fx(center[0], center[1], alien_type="boss", scale=3.0)
    spawn_explosion_fx(center[0], center[1], alien_type="boss", scale=2.0)

    game_state = "boss_dying"


def boss_death_update(now_ms):
    """Update + rendu de la cinématique boss_dying."""
    global boss_death_anim

    if not boss_death_anim.get("active") or boss_death_anim.get("freeze") is None:
        return

    cx, cy = boss_death_anim["center"]

    # Bursts supplémentaires (plusieurs vagues)
    if now_ms >= boss_death_anim["next_burst_ms"] and boss_death_anim["bursts_left"] > 0:
        boss_death_anim["bursts_left"] -= 1
        boss_death_anim["next_burst_ms"] = now_ms + 85

        for _ in range(2):
            ox = random.randint(-25, 25)
            oy = random.randint(-18, 18)
            spawn_explosion_fx(cx + ox, cy + oy, alien_type="boss", scale=random.uniform(1.4, 2.2))

    # On anime les particules
    update_fx()
    render_fx_surfaces()

    # Screen shake (décroissant)
    sx = sy = 0
    if now_ms < boss_death_anim["shake_end_ms"]:
        t = (boss_death_anim["shake_end_ms"] - now_ms) / 420.0
        amp = max(0.0, min(1.0, t)) * 10.0
        sx = int(random.uniform(-amp, amp))
        sy = int(random.uniform(-amp, amp))

    # Rendu : background figé + FX
    screen.fill((0, 0, 0))
    screen.blit(boss_death_anim["freeze"], (sx, sy))
    screen.blit(fx_surface_under, (sx, sy))
    screen.blit(fx_surface_over, (sx, sy))

    # Flash blanc court (impact)
    if now_ms < boss_death_anim["flash_end_ms"]:
        dur = max(1, boss_death_anim["flash_end_ms"] - boss_death_anim["start_ms"])
        a = int(220 * (boss_death_anim["flash_end_ms"] - now_ms) / dur)
        flash = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        flash.fill((255, 255, 255, max(0, min(255, a))))
        screen.blit(flash, (0, 0))

    if now_ms - boss_death_anim["start_ms"] >= int(boss_death_anim.get("duration_ms", 1500)):
        finish_boss_death_sequence()


def finish_boss_death_sequence():
    """Termine la cinématique et enchaîne sur le niveau suivant / victoire."""
    global boss_death_anim, game_state, boss3_defeated_once
    global boss, boss_id, pending_level_after_boss
    global boss_fight_start, boss_last_shot, boss_last_special, boss_last_regen
    global boss_last_laser, boss_last_zone, boss_last_fan, boss_last_burst
    global boss_last_minion, boss_last_rain, boss_hitbox
    global boss_max_health_cap, boss_max_health, boss_health
    global active_powerups, trail_particles, explosion_particles, shockwaves

    now = pygame.time.get_ticks()
    start_ms = boss_death_anim.get("start_ms", now)
    paused_ms = max(0, now - start_ms)

    # Restaure les powerups et compense le temps "figé"
    snap = boss_death_anim.get("powerups_snapshot") or {}
    active_powerups = dict(snap)
    for k, expiry in list(active_powerups.items()):
        if expiry and expiry > start_ms:
            active_powerups[k] = expiry + paused_ms

    # Reset boss (comme avant)
    boss = None
    boss_id = None
    pending_level_after_boss = None
    boss_fight_start = 0
    boss_last_shot = 0
    boss_last_special = 0
    boss_last_regen = 0
    boss_last_laser = 0
    boss_last_zone = 0
    boss_last_fan = 0
    boss_last_burst = 0
    boss_last_minion = 0
    boss_last_rain = 0
    boss_hitbox = None
    boss_max_health_cap = 120
    boss_max_health = 50
    boss_health = 50

    bid = boss_death_anim.get("boss_id", None)

    if bid == 3:
        boss3_defeated_once = True
        persist_save()
        game_state = "victory"
        sons["victoire"].play()
    else:
        advance_level(boss_death_anim.get("pending_level", None))
        game_state = "playing"

    boss_death_anim.update({
        "active": False,
        "freeze": None,
        "powerups_snapshot": None,
        "boss_id": None,
        "pending_level": None
    })

    # Nettoyage FX (évite de garder des restes après la cinématique)
    trail_particles.clear()
    explosion_particles.clear()
    shockwaves.clear()


###############################################################################
#                         BONUS / POWERUPS (RAMASSABLES)                      #
###############################################################################


def is_powerup_active(name, now_ms=None):
    if now_ms is None:
        now_ms = pygame.time.get_ticks()
    return active_powerups.get(name, 0) > now_ms


def update_powerups(now_ms):
    """
    À appeler régulièrement (chaque frame en jeu).
    - Si le bonus vitesse est terminé, on restaure la vitesse de base.
    """
    global spaceship_speed
    if active_powerups.get("speed", 0) and now_ms >= active_powerups["speed"]:
        active_powerups["speed"] = 0
        spaceship_speed = spaceship_speed_base


def activate_speed(now_ms, duration_ms=None):
    global spaceship_speed
    if duration_ms is None:
        duration_ms = POWERUP_DURATION_MS["speed"]

    active_powerups["speed"] = max(active_powerups.get("speed", 0), now_ms + duration_ms)
    spaceship_speed = int(spaceship_speed_base * SPEED_BOOST_MULT)


def activate_multishot(now_ms, duration_ms=None):
    if duration_ms is None:
        duration_ms = POWERUP_DURATION_MS["multishot"]

    active_powerups["multishot"] = max(active_powerups.get("multishot", 0), now_ms + duration_ms)


def activate_shield(now_ms, duration_ms=None):
    """Bouclier: invulnérabilité temporaire."""
    if duration_ms is None:
        duration_ms = POWERUP_DURATION_MS["shield"]

    active_powerups["shield"] = max(active_powerups.get("shield", 0), now_ms + duration_ms)


def apply_bonus(kind, now_ms):
    global remaining_bullets, coins, coins_gained_this_run, lives, last_pickup_text, last_pickup_until

    # Récompenses par difficulté (ammo = balles, coins = pièces)
    reward_by_difficulty = {
        "facile": {"ammo": 20, "coins": 20},
        "moyen": {"ammo": 30, "coins": 30},
        "difficile": {"ammo": 40, "coins": 40},
        "hardcore": {"ammo": 50, "coins": 50},
    }
    rewards = reward_by_difficulty.get(current_difficulty, reward_by_difficulty["moyen"])

    if kind == "ammo":
        gain = rewards["ammo"]
        remaining_bullets += gain
        last_pickup_text = f"+{gain} balles"

    elif kind == "coins":
        gain = rewards["coins"]
        coins += gain
        coins_gained_this_run += gain
        last_pickup_text = f"+{gain} coins"

    elif kind == "speed":
        activate_speed(now_ms)
        dur_s = POWERUP_DURATION_MS["speed"] // 1000
        last_pickup_text = f"Vitesse augmentée ({dur_s}s)"

    elif kind == "multishot":
        activate_multishot(now_ms)
        dur_s = POWERUP_DURATION_MS["multishot"] // 1000
        last_pickup_text = f"Tir multiple ({dur_s}s)"

    elif kind == "shield":
        activate_shield(now_ms)
        dur_s = POWERUP_DURATION_MS["shield"] // 1000
        last_pickup_text = f"Bouclier ({dur_s}s)"

    elif kind == "life":
        lives += 1
        last_pickup_text = "+1 vie"

    else:
        last_pickup_text = "Bonus !"

    last_pickup_until = now_ms + 2000


def spawn_bonus_drop(x, y, kind):
    rect = bonus.get_rect(center=(int(x), int(y)))
    bonuses.append({
        "rect": rect,
        "kind": kind,
        "spawn_ms": pygame.time.get_ticks()
    })


def spawn_falling_bonus(kind=None):
    """Fait apparaître un bonus qui tombe du haut de l'écran.

    Bonus indépendant: il n'est pas lié à la mort des aliens.
    Pour l'obtenir, le joueur doit tirer dessus.
    """
    if kind is None:
        kinds = ["shield", "life", "speed", "multishot", "ammo", "coins"]
        weights = [0.73, 0.07, 0.20, 0.20, 0.20, 0.20]
        kind = random.choices(kinds, weights=weights, k=1)[0]

    margin = 55
    x = random.randint(margin, WIDTH - margin)
    rect = bonus.get_rect(midtop=(x, -bonus.get_height()))

    bonuses.append({
        "rect": rect,
        "kind": kind,
        "spawn_ms": pygame.time.get_ticks(),
    })


def maybe_drop_bonus(x, y, source_type="normal"):
    """
    Appelé quand un alien est détruit.
    source_type: normal / gold / diamond / shooter
    """
    base_chance = 0.07
    if source_type == "gold":
        base_chance = 0.14
    elif source_type == "diamond":
        base_chance = 0.18
    elif source_type == "shooter":
        base_chance = 0.10

    if random.random() > base_chance:
        return

    kinds = ["shield", "life", "speed", "multishot", "ammo", "coins"]
    weights = [0.14, 0.10, 0.18, 0.14, 0.24, 0.20]
    kind = random.choices(kinds, weights=weights, k=1)[0]
    spawn_bonus_drop(x, y, kind)


def update_bonuses_and_handle_hits(now_ms):
    """Met à jour les bonus qui tombent et applique l'effet si le joueur les touche avec un tir."""
    # 1) Déplacement / nettoyage
    for b in bonuses[:]:
        b["rect"].y += BONUS_FALL_SPEED

        if b["rect"].top > HEIGHT or (now_ms - b["spawn_ms"] > BONUS_TTL_MS):
            bonuses.remove(b)

    # 2) Récupération: uniquement en tirant dessus
    for b in bonuses[:]:
        hit = False

        for bullet in bullets[:]:
            if b["rect"].colliderect(bullet["rect"]):
                if bullet in bullets:
                    bullets.remove(bullet)
                hit = True
                break

        if not hit:
            for bullet in secondary_bullets[:]:
                if b["rect"].colliderect(bullet["rect"]):
                    if bullet in secondary_bullets:
                        secondary_bullets.remove(bullet)
                    hit = True
                    break

        if hit:
            apply_bonus(b["kind"], now_ms)
            if b in bonuses:
                bonuses.remove(b)


def draw_bonuses():
    for b in bonuses:
        screen.blit(bonus, b["rect"])


def draw_shield_effect(ship_rect, now_ms):
    """Dessine un bouclier bleu semi-transparent autour du vaisseau."""
    if not is_powerup_active("shield", now_ms):
        return

    # Rayon de base (un peu plus grand que le vaisseau)
    base_r = max(ship_rect.width, ship_rect.height) // 2 + 18

    # Petit "pulse" animé (optionnel)
    pulse = int(3 * math.sin(now_ms / 140))  # varie entre ~-3 et +3
    r = base_r + pulse

    # Surface temporaire en alpha
    size = r * 2 + 12
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2

    # Halo (remplissage léger)
    pygame.draw.circle(surf, (0, 160, 255, 50), (cx, cy), r)

    # Anneau principal
    pygame.draw.circle(surf, (0, 210, 255, 190), (cx, cy), r, 4)

    # Petit anneau externe (effet "énergie")
    pygame.draw.circle(surf, (0, 210, 255, 90), (cx, cy), r + 6, 2)

    # Blit centré sur le vaisseau
    screen.blit(surf, (ship_rect.centerx - cx, ship_rect.centery - cy))


def draw_powerup_status(now_ms):
    """HUD: affiche les powerups actifs + un mini timer + un message quand on récupère un bonus."""
    x = 10
    y = HEIGHT / 2
    bar_w = 140
    bar_h = 6
    gap = 30

    def _draw_timer_line(label, end_ms, duration_ms, y_line):
        # Texte
        sec_left = max(0, int(math.ceil((end_ms - now_ms) / 1000)))
        draw_text(f"{label} ({sec_left}s)", x, y_line, font=hud_font)

        # Barre de temps (clamp au duration_ms pour éviter des barres > 100% si on prolonge)
        remaining = max(0, end_ms - now_ms)
        remaining = min(remaining, duration_ms)
        ratio = 0 if duration_ms <= 0 else (remaining / duration_ms)

        bg = pygame.Rect(x, y_line + 18, bar_w, bar_h)
        fg = pygame.Rect(x, y_line + 18, int(bar_w * ratio), bar_h)
        pygame.draw.rect(screen, (255, 255, 255), bg, 1)
        pygame.draw.rect(screen, (255, 255, 0), fg)

    # Powerups actifs
    if is_powerup_active("shield", now_ms):
        _draw_timer_line("Bouclier", active_powerups["shield"], POWERUP_DURATION_MS["shield"], y)
        y += gap

    if is_powerup_active("speed", now_ms):
        _draw_timer_line("Vitesse +", active_powerups["speed"], POWERUP_DURATION_MS["speed"], y)
        y += gap

    if is_powerup_active("multishot", now_ms):
        _draw_timer_line("Tir multiple", active_powerups["multishot"], POWERUP_DURATION_MS["multishot"], y)
        y += gap

    # Petit message temporaire quand on récupère un bonus
    if last_pickup_text and now_ms < last_pickup_until:
        draw_text(last_pickup_text, WIDTH // 2, HEIGHT - 35, color=(255, 255, 0), centered=True)


def fire_primary_weapon():
    """
    Tir principal (weapon1).
    Supporte le powerup "multishot" (3 tirs en éventail).
    """
    global remaining_bullets, shots_fired

    if game_state != "playing":
        return
    if remaining_bullets <= 0:
        return

    ship_w = spaceship_images[selected_skin].get_width()
    ship_center_x = spaceship_x + ship_w // 2

    offsets = [0]
    if is_powerup_active("multishot"):
        offsets = [-18, 0, 18]

    for off in offsets:
        bullets.append({
            "rect": pygame.Rect(ship_center_x + off - (5 // 2), spaceship_y, 5, 15),
            "velocity": (0, -bullet_speed)
        })
        shots_fired += 1

    # Coût du tir : 1 balle par "pression" (plus fun)
    remaining_bullets -= 1
    if remaining_bullets < 0:
        remaining_bullets = 0

    sons["tir"].play()


def spawn_alien():
    size = random.randint(55, 90)
    alien_surface = pygame.transform.scale(alien_image, (size, size))
    MARGIN = 55  # ajuste (30–80 selon ton feeling)
    x = random.randint(MARGIN, WIDTH - size - MARGIN)
    y = 0
    alien_rect = pygame.Rect(x, y, size, size)

    alien = {
        "surface": alien_surface,
        "rect": alien_rect,
        "type": "normal"
    }
    init_alien_motion(alien, alien_surface, can_zigzag=True, can_rotate=True)
    aliens.append(alien)


def spawn_alien_en_or():
    size = random.randint(55, 90)
    alien_en_or_surface = pygame.transform.scale(alien_en_or_image, (size, size))
    MARGIN = 55  # ajuste (30–80 selon ton feeling)
    x = random.randint(MARGIN, WIDTH - size - MARGIN)
    y = 0
    alien__en_or_rect = pygame.Rect(x, y, size, size)

    alien = {
        "surface": alien_en_or_surface,
        "rect": alien__en_or_rect,
        "type": "gold"
    }
    init_alien_motion(alien, alien_en_or_surface, can_zigzag=True, can_rotate=True)
    aliens.append(alien)


def spawn_alien_en_diamant():
    size = random.randint(55, 90)
    alien_en_diamant_surface = pygame.transform.scale(alien_en_diamant_image, (size, size))
    MARGIN = 55  # ajuste (30–80 selon ton feeling)
    x = random.randint(MARGIN, WIDTH - size - MARGIN)
    y = 0
    alien_en_diamant_rect = pygame.Rect(x, y, size, size)

    alien = {
        "surface": alien_en_diamant_surface,
        "rect": alien_en_diamant_rect,
        "type": "diamond"
    }
    init_alien_motion(alien, alien_en_diamant_surface, can_zigzag=True, can_rotate=True)
    aliens.append(alien)


def spawn_alien_shooter():
    size = random.randint(60, 90)
    alien_surface = pygame.transform.scale(alien_attaquant, (size, size))
    x = random.randint(0, WIDTH - size)
    y = random.randint(SHOOTER_Y_MIN, SHOOTER_Y_MAX)
    alien_rect = pygame.Rect(x, y, size, size)

    vx = random.choice([-1, 1]) * random.uniform(SHOOTER_SPEED_X_MIN, SHOOTER_SPEED_X_MAX)

    alien = {
        "surface": alien_surface,
        "rect": alien_rect,
        "type": "shooter",
        "last_shot": pygame.time.get_ticks()
    }
    # Shooter: déplacement gauche <-> droite uniquement, pas de rotation/zigzag aléatoire
    init_alien_motion(alien, alien_surface, vx=vx, can_zigzag=False, can_rotate=False)
    aliens.append(alien)


def play_next_music():
    global music_index
    music_channel.stop()
    music_channel.play(music_list[music_index], loops=-1)
    music_index = (music_index + 1) % len(music_list)


def draw_boss_health_bar(current_health, max_health, boss_rect, y_offset=-20):
    """Dessine la barre de vie centrée sur le boss (toutes tailles de sprites)."""
    bar_width = 500
    bar_height = 20

    health_percentage = 0 if max_health <= 0 else max(0, min(1, current_health / max_health))

    x = boss_rect.centerx - bar_width // 2
    y = boss_rect.y + y_offset

    pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (x, y, int(bar_width * health_percentage), bar_height))


def spawn_enemy_bullet(x, y, vx, vy, w=12, h=20):
    """
    Spawn d'une balle ennemie (aliens shooters + boss).
    Supporte vitesse X/Y (vx, vy) en float ou int.
    La position float est stockée pour éviter les saccades si vx/vy ne sont pas des entiers.
    """
    enemy_bullets.append({
        "rect": pygame.Rect(int(x), int(y), w, h),
        "pos": [float(x), float(y)],
        "speed_x": float(vx),
        "speed_y": float(vy),
    })


def spawn_boss_aimed_shot(boss_rect, ship_rect, speed=13):
    """
    Tir "aimé" (vise le joueur). Légèrement moins de composante horizontale
    pour rester esquivable, même si tu accélères le jeu plus tard.
    """
    bx, by = boss_rect.centerx, boss_rect.bottom
    sx, sy = ship_rect.centerx, ship_rect.centery

    dx = sx - bx
    dy = sy - by
    dist = math.hypot(dx, dy)

    if dist == 0:
        vx, vy = 0.0, float(speed)
    else:
        vx = (dx / dist) * (speed * 0.6)
        vy = (dy / dist) * speed
        # sécurité: si le joueur est quasi aligné, on évite un vy trop petit
        if vy < 6:
            vy = 6.0

    spawn_enemy_bullet(bx - 6, by, vx, vy)


def clamp(value, lo, hi):
    return max(lo, min(hi, value))


def init_alien_motion(alien, base_surface, *, vx=0.0, can_zigzag=True, can_rotate=True):
    """Initialise les paramètres de mouvement/rotation d'un alien (astéroïde ou shooter).

    - alien["pos"] : centre (x,y) en float
    - alien["vx"] : vitesse horizontale (float) (0 = trajectoire verticale)
    - alien["angular_speed"] : vitesse de rotation (degrés par frame) (0 = pas de rotation)
    """
    # position en centre (plus stable si la surface tourne)
    alien["pos"] = [float(alien["rect"].centerx), float(alien["rect"].centery)]
    alien["vx"] = float(vx)

    # rotation
    alien["base_surface"] = base_surface
    alien["angle"] = 0.0
    alien["angular_speed"] = 0.0

    # zigzag (astéroïdes uniquement)
    if can_zigzag and random.random() < ASTEROID_ZIGZAG_CHANCE:
        alien["vx"] = random.choice([-1, 1]) * random.uniform(ASTEROID_ZIGZAG_SPEED_MIN, ASTEROID_ZIGZAG_SPEED_MAX)

    # rotation (astéroïdes uniquement)
    if can_rotate and random.random() < ASTEROID_ROTATE_CHANCE:
        alien["angular_speed"] = random.choice([-1, 1]) * random.uniform(ASTEROID_ROTATE_SPEED_MIN,
                                                                         ASTEROID_ROTATE_SPEED_MAX)


def spawn_boss_laser(target_x, now_ms, width=90, warn_ms=650, active_ms=550, offset_ms=0):
    """
    Laser vertical télégraphié :
    - warn_ms : phase d'avertissement (rectangle en contour)
    - active_ms : phase active (rectangle plein qui fait perdre une vie)
    """
    global boss_lasers
    x = clamp(int(target_x), width // 2, WIDTH - width // 2)
    rect = pygame.Rect(x - width // 2, 0, width, HEIGHT)
    boss_lasers.append({
        "rect": rect,
        "t0": int(now_ms) + int(offset_ms),
        "warn_ms": int(warn_ms),
        "active_ms": int(active_ms),
    })


def spawn_boss_zone(ship_rect, now_ms, start_r=35, grow_per_frame=3.2, life_ms=3200, hit_delay_ms=380):
    """
    Zone circulaire qui grandit. Elle enlève une vie si le joueur RESTE dedans
    pendant hit_delay_ms (ça évite les hits instantanés frustrants).
    """
    global boss_zones

    # On "biais" la zone vers le joueur, mais pas exactement sur lui (pour rester esquivable)
    cx = clamp(ship_rect.centerx + random.randint(-260, 260), 120, WIDTH - 120)
    cy = clamp(ship_rect.centery + random.randint(-180, 180), HEIGHT // 3, HEIGHT - 150)

    boss_zones.append({
        "cx": float(cx),
        "cy": float(cy),
        "r": float(start_r),
        "grow": float(grow_per_frame),
        "t0": int(now_ms),
        "life_ms": int(life_ms),
        "hit_delay_ms": int(hit_delay_ms),
        "inside_since": None,
    })


def compute_boss_hitbox(draw_rect, bid):
    """Retourne une hitbox plus juste que le rect de rendu (utile pour boss fins)."""
    # Réduction (en %) de la largeur/hauteur du rect de rendu
    if bid == 1:
        shrink_w, shrink_h = (0.18, 0.20)
    elif bid == 2:
        shrink_w, shrink_h = (0.50, 0.22)  # boss 2 plus fin → hitbox plus étroite
    else:
        shrink_w, shrink_h = (0.24, 0.22)

    hb = draw_rect.copy()
    hb.inflate_ip(-max(2, int(draw_rect.width * shrink_w)),
                  -max(2, int(draw_rect.height * shrink_h)))
    return hb


def spawn_boss_fan_shot(boss_rect, count=5, spread_deg=50, speed=10):
    """Tir en éventail vers le bas depuis le centre du boss."""
    if count <= 0:
        return
    cx = boss_rect.centerx
    cy = boss_rect.bottom

    if count == 1:
        angles = [90.0]
    else:
        start = 90.0 - (spread_deg / 2.0)
        step = spread_deg / (count - 1)
        angles = [start + step * i for i in range(count)]

    for ang in angles:
        rad = math.radians(ang)
        vx = math.cos(rad) * speed
        vy = math.sin(rad) * speed
        spawn_enemy_bullet(cx, cy, vx, vy)


def spawn_boss_arc_burst(boss_rect, count=12, start_deg=20, end_deg=160, speed=9):
    """Barrage en arc (semi-cercle vers le bas)."""
    if count <= 0:
        return
    cx = boss_rect.centerx
    cy = boss_rect.bottom

    if count == 1:
        angles = [(start_deg + end_deg) / 2.0]
    else:
        step = (end_deg - start_deg) / (count - 1)
        angles = [start_deg + step * i for i in range(count)]

    for ang in angles:
        rad = math.radians(ang)
        vx = math.cos(rad) * speed
        vy = math.sin(rad) * speed
        spawn_enemy_bullet(cx, cy, vx, vy, w=10, h=16)


def spawn_boss_rain(now_ms, count=10, speed=12, avoid_x=None, avoid_radius=0, lane_width=80):
    """Pluie de tirs verticaux depuis le haut de l'écran.

    Ajustements anti-"impossible" :
    - positions en "lanes" (évite les tirs collés)
    - option d'éviter une zone autour du joueur (avoid_x / avoid_radius)
    - projectiles légèrement plus petits
    """
    # Construire des lanes régulières
    x_min, x_max = 30, WIDTH - 30
    lanes = list(range(x_min, x_max + 1, lane_width))
    random.shuffle(lanes)

    chosen = []
    for x in lanes:
        if avoid_x is not None and abs(x - avoid_x) < avoid_radius:
            continue
        chosen.append(x)
        if len(chosen) >= count:
            break

    # Si on n'a pas assez de lanes (ex: écran petit + gros avoid), on relâche un peu l'évitement
    if len(chosen) < count:
        for x in lanes:
            if x in chosen:
                continue
            if avoid_x is not None and abs(x - avoid_x) < max(0, avoid_radius * 0.6):
                continue
            chosen.append(x)
            if len(chosen) >= count:
                break

    for x in chosen:
        spawn_enemy_bullet(x, 0, 0, speed, w=10, h=16)


def spawn_boss_minions(boss_rect, now_ms, count=2, shooter_chance=0.6):
    """Fait apparaître des petits aliens (minions) depuis le boss, sans impacter le level-up."""
    for _ in range(count):
        size = random.randint(45, 65)
        x_min = max(0, boss_rect.left)
        x_max = min(WIDTH - size, boss_rect.right - size)
        if x_max < x_min:
            x_min, x_max = 0, WIDTH - size

        x = random.randint(x_min, x_max)
        y = boss_rect.bottom - int(size * 0.35)

        is_shooter = (random.random() < shooter_chance)
        if is_shooter:
            surf = pygame.transform.scale(alien_attaquant, (size, size))
            rect = pygame.Rect(x, y, size, size)
            aliens.append({
                "rect": rect,
                "surface": surf,
                "type": "shooter",
                "last_shot": now_ms,
                "is_minion": True
            })
        else:
            surf = pygame.transform.scale(alien_image, (size, size))
            rect = pygame.Rect(x, y, size, size)
            aliens.append({
                "rect": rect,
                "surface": surf,
                "type": "normal",
                "is_minion": True
            })


def fire_secondary_weapon(mouse_x, mouse_y):
    global remaining_bullets, shots_fired
    if remaining_bullets > 0:
        dx = mouse_x - (spaceship_x + 75)
        dy = mouse_y - spaceship_y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        if dist > 0:
            velocity = (dx / dist * secondary_bullet_speed, dy / dist * secondary_bullet_speed)
            secondary_bullets.append({
                "rect": pygame.Rect(spaceship_x + 75 - 5, spaceship_y + 75 - 5, 10, 10),
                "velocity": velocity
            })
        remaining_bullets -= 1
        shots_fired += 1
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


def draw_button(image, rect, surface, hover_scale=1.08, border_color=(255, 255, 0)):
    """
    Dessine un bouton image avec effet hover (zoom léger + contour).
    - Image : surface du bouton (ton PNG)
    - Rect  : pygame.Rect pour la position logique et les collisions
    - Surface : là où on dessine (screen)
    """
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = rect.collidepoint(mouse_pos)

    # Par défaut : on dessine l'image telle quelle
    img_to_draw = image
    draw_rect = rect

    if is_hovered:
        # Zoom léger (ex : 1.08 = 8% plus grand)
        w, h = image.get_size()
        new_w, new_h = int(w * hover_scale), int(h * hover_scale)
        img_to_draw = pygame.transform.smoothscale(image, (new_w, new_h))

        # On centre le bouton agrandi sur le rect d'origine
        draw_rect = img_to_draw.get_rect(center=rect.center)

        # Dessiner un contour "glow" autour de la zone d'origine
        glow_rect = rect.inflate(10, 10)
        pygame.draw.rect(surface, border_color, glow_rect, width=2, border_radius=8)

    surface.blit(img_to_draw, draw_rect)

    return is_hovered


SAVE_VERSION = 2


# --- Gestion sauvegarde (par pseudo) ---
def get_save_file(player_name):
    # Sauvegardes stockées dans le dossier "code"
    save_dir = os.path.join(current_directory, "code")
    os.makedirs(save_dir, exist_ok=True)
    return os.path.join(save_dir, f"{player_name}_save.json")


def default_save():
    return {
        "version": SAVE_VERSION,
        "coins": 0,
        # Skins
        "unlocked_skins": 1,  # nombre de skins possédés (>=1)
        "equipped_skin": 0,  # skin actuellement équipé
        "boss3_defeated_once": False,  # nécessaire pour acheter le dernier skin
        # Settings
        "language": "fr",
        "difficulty": "moyen",
        "controls": "ad",
        "weapon1": "space",
        "weapon2": "left",
        "aim_assist": False,
    }


def load_save(player_name):
    save_file = get_save_file(player_name)
    if not os.path.exists(save_file):
        return default_save()

    try:
        with open(save_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return default_save()

    # Migration depuis ancien format: {"coins": ...}
    if isinstance(data, dict) and "version" not in data and "coins" in data:
        migrated = default_save()
        migrated["coins"] = int(data.get("coins", 0))
        return migrated

    base = default_save()
    if not isinstance(data, dict):
        return base
    base.update(data)
    return base


def save_game(player_name, data):
    save_file = get_save_file(player_name)
    data = dict(data)
    data["version"] = SAVE_VERSION
    with open(save_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def apply_save_data(data):
    global coins, unlocked_skins, equipped_skin, selected_skin, boss3_defeated_once
    global current_language, current_difficulty, current_controls, weapon1_control, weapon2_control, aim_assist

    coins = int(data.get("coins", 0))

    unlocked_skins = int(data.get("unlocked_skins", 1))
    unlocked_skins = max(1, min(unlocked_skins, len(spaceship_images)))

    equipped_skin = int(data.get("equipped_skin", 0))
    equipped_skin = max(0, min(equipped_skin, unlocked_skins - 1))

    selected_skin = equipped_skin
    boss3_defeated_once = bool(data.get("boss3_defeated_once", False))

    current_language = str(data.get("language", "fr"))
    current_difficulty = str(data.get("difficulty", "moyen"))
    current_controls = str(data.get("controls", "ad"))
    weapon1_control = str(data.get("weapon1", "space"))
    weapon2_control = str(data.get("weapon2", "left"))
    aim_assist = bool(data.get("aim_assist", False))


def persist_save():
    global player_name
    if not player_name:
        return

    data = default_save()
    data.update({
        "coins": int(coins),
        "unlocked_skins": int(unlocked_skins),
        "equipped_skin": int(equipped_skin),
        "boss3_defeated_once": bool(boss3_defeated_once),
        "language": str(current_language),
        "difficulty": str(current_difficulty),
        "controls": str(current_controls),
        "weapon1": str(weapon1_control),
        "weapon2": str(weapon2_control),
        "aim_assist": bool(aim_assist),
    })
    save_game(player_name, data)


# Récompenses en fonction de la difficulté
coins_reward = {
    "facile": {"alien": 1, "alien_en_or": 5, "alien_en_diamant": 25, "alien_attaquant": 3, "boss": 40},
    "moyen": {"alien": 2, "alien_en_or": 5, "alien_en_diamant": 25, "alien_attaquant": 3, "boss": 45},
    "difficile": {"alien": 3, "alien_en_or": 5, "alien_en_diamant": 25, "alien_attaquant": 3, "boss": 50},
    "hardcore": {"alien": 5, "alien_en_or": 5, "alien_en_diamant": 25, "alien_attaquant": 3, "boss": 55},
}


################################################################################
#                          BOUCLE PRINCIPALE DU JEU                            #
################################################################################


last_state = None
running = True
while running:
    clock.tick(FPS)

    # --- Gestion musique selon changement d'état ---
    if game_state != last_state:
        in_menu_group_now = game_state in ["menu", "settings"]
        in_menu_group_before = last_state in ["menu", "settings"]

        # ➜ On vient d'entrer dans le groupe menu/settings (ex: login -> menu, playing -> menu)
        if in_menu_group_now and not in_menu_group_before:
            # On coupe la musique de JEU (channel 0) au cas où
            music_channel.stop()
            # Puis, on démarre la musique du menu
            musique_menu["music_menu"].play(-1)

        # ➜ On vient de quitter le groupe menu/settings (ex: menu -> playing)
        if in_menu_group_before and not in_menu_group_now:
            musique_menu["music_menu"].stop()

        # ➜ On arrive dans le JEU (depuis un état qui n'est NI playing NI pause)
        if game_state == "playing" and last_state not in ["playing", "pause", "boss_dying"]:
            play_next_music()

        last_state = game_state

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # === LOGIN : saisie du pseudo ===
        if game_state == "login":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Valider
                    if player_name.strip() == "":
                        player_name = "???"
                    data = load_save(player_name)
                    apply_save_data(data)
                    set_difficulty(current_difficulty)  # applique les paramètres de difficulté au run
                    spaceship_image = spaceship_images[equipped_skin]
                    game_state = "menu"
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    # Ajouter le caractère tapé (si imprimable) et limiter la longueur
                    if getattr(event, "unicode", "") and event.unicode.isprintable() and len(player_name) < 12:
                        player_name += event.unicode
            # Tant qu'on est sur l'écran login, on ignore les autres handlers (ESC, tirs, clics…)
            continue

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
                if event.key == pygame.K_SPACE:
                    fire_primary_weapon()

        # --- GESTION DES CLICS SOURIS ---
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # ÉTAT : MENU
            if game_state == "menu":

                if event.button == 1:  # clic gauche
                    if button_play_rect.collidepoint(mouse_x, mouse_y):
                        reset_game()
                        game_state = "playing"
                        spaceship_image = spaceship_images[equipped_skin]
                        persist_save()
                        if not pygame.mixer.get_busy():
                            play_next_music()


                    elif button_quit_rect.collidepoint(mouse_x, mouse_y):
                        running = False

                    elif button_settings_rect.collidepoint(mouse_x, mouse_y):
                        game_state = "settings"

                    elif fleche_gauche_rect.collidepoint(mouse_x, mouse_y):
                        selected_skin = (selected_skin - 1) % len(spaceship_images)
                        spaceship_image = spaceship_images[selected_skin]

                        # Si le skin est déjà possédé → on l'équipe automatiquement
                        if selected_skin < unlocked_skins:
                            equipped_skin = selected_skin
                            spaceship_image = spaceship_images[equipped_skin]
                            persist_save()


                    elif fleche_droite_rect.collidepoint(mouse_x, mouse_y):
                        selected_skin = (selected_skin + 1) % len(spaceship_images)
                        spaceship_image = spaceship_images[selected_skin]

                        # Si le skin est déjà possédé → on l'équipe automatiquement
                        if selected_skin < unlocked_skins:
                            equipped_skin = selected_skin
                            spaceship_image = spaceship_images[equipped_skin]
                            persist_save()

                    elif buy_rect.collidepoint(mouse_x, mouse_y):
                        # Achat séquentiel strict
                        if selected_skin == unlocked_skins:
                            # Condition boss skin final
                            if selected_skin == len(spaceship_images) - 1 and not boss3_defeated_once:
                                pass
                            else:
                                price = SKIN_PRICES[selected_skin] if selected_skin < len(SKIN_PRICES) else 999999
                                if coins >= price:
                                    coins -= price
                                    unlocked_skins += 1
                                    equipped_skin = selected_skin
                                    spaceship_image = spaceship_images[equipped_skin]
                                    persist_save()


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
                pause_pos_y = 140
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
                pause_pos_y = 140
                pause_button_rect = button_pause.get_rect(topleft=(pause_pos_x, pause_pos_y))

                if pause_button_rect.collidepoint(mouse_x, mouse_y):
                    # On met le jeu en pause
                    game_state = "pause"
                else:
                    # Tirs
                    if (weapon1_control == "left"
                            and event.button == 1):
                        fire_primary_weapon()

                    if weapon2_control == "left" and event.button == 1:
                        fire_secondary_weapon(mouse_x, mouse_y)
                        # Jouer le son de tir
                        sons["tir"].play()

                    elif weapon2_control == "right" and event.button == 3:
                        fire_secondary_weapon(mouse_x, mouse_y)
                        # Jouer le son de tir
                        sons["tir"].play()


    ############################################################################
    #                            GESTION DES ETATS                              #
    ############################################################################


    # --- AFFICHAGE LOGIN ---

    if game_state == "login":
        medium_font = pygame.font.Font(None, 40)

        screen.fill((0, 0, 30))
        title_surface = large_font.render("Connexion...", True, (255, 255, 255))
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, HEIGHT // 4))

        text_surface = medium_font.render("Entrez votre pseudo :", True, (255, 255, 255))
        screen.blit(text_surface, (WIDTH // 2 - 150, HEIGHT // 2 - 50))

        pygame.draw.rect(screen, (255, 255, 255), (WIDTH // 2 - 150, HEIGHT // 2, 300, 40), 2)
        input_surface = medium_font.render(player_name, True, (255, 255, 0))
        screen.blit(input_surface, (WIDTH // 2 - 140, HEIGHT // 2 + 5))


    elif game_state == "menu":
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

        preview = spaceship_images[selected_skin]
        if selected_skin >= unlocked_skins:
            preview = pygame.Surface((150, 150), pygame.SRCALPHA)
            preview.fill((40, 40, 40, 220))
            q = medium_font.render("?", True, (255, 255, 255))
            preview.blit(q, (75 - q.get_width() // 2, 75 - q.get_height() // 2))

        screen.blit(preview, preview.get_rect(midtop=(WIDTH // 2, HEIGHT // 2 + 250)))

        # --- Bouton acheter ---
        buy_rect = pygame.Rect(WIDTH // 2 - 90, HEIGHT // 2 + 420, 180, 45)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hover = buy_rect.collidepoint(mouse_x, mouse_y)

        # visible seulement si skin sélectionné verrouillé
        if selected_skin >= unlocked_skins:
            col = (180, 160, 0) if hover else (110, 110, 110)
            pygame.draw.rect(screen, col, buy_rect, border_radius=8)

            price = SKIN_PRICES[selected_skin] if selected_skin < len(SKIN_PRICES) else 999999
            txt = medium_font.render(f"Acheter ({price})", True, (0, 0, 0))
            screen.blit(txt, (buy_rect.x + (buy_rect.width - txt.get_width()) // 2,
                              buy_rect.y + (buy_rect.height - txt.get_height()) // 2))

            # Message si dernier skin verrouillé par boss final
            if selected_skin == len(spaceship_images) - 1 and not boss3_defeated_once:
                warn = medium_font.render("Bats le boss final d'abord", True, (255, 80, 80))
                screen.blit(warn, (WIDTH // 2 - warn.get_width() // 2, buy_rect.y - 40))

        # pseudo du joueur
        pseudo_surface = medium_font.render(f"Player : {player_name}", True, (255, 255, 0))
        screen.blit(pseudo_surface, (20, 20))  # en haut à gauche

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

        draw_button(button_play, button_play_rect, screen)
        draw_button(button_quit, button_quit_rect, screen)
        draw_button(button_settings, button_settings_rect, screen)

        fleche_gauche_x = x_position - 45
        fleche_gauche_y = y_position_settings + 182
        fleche_droite_x = x_position + 185
        fleche_droite_y = y_position_settings + 180

        fleche_gauche_rect = fleche_choix_skin_gauche.get_rect(
            topleft=(fleche_gauche_x, fleche_gauche_y)
        )
        fleche_droite_rect = fleche_choix_skin_droite.get_rect(
            topleft=(fleche_droite_x, fleche_droite_y)
        )

        # Dessin avec hover (légèrement moins de zoom car elles sont petites)
        draw_button(fleche_choix_skin_gauche, fleche_gauche_rect, screen, hover_scale=1.08, border_color=(255, 255, 0))
        draw_button(fleche_choix_skin_droite, fleche_droite_rect, screen, hover_scale=1.08, border_color=(255, 255, 0))

        fleche_gauche_rect = fleche_choix_skin_gauche.get_rect(topleft=(fleche_gauche_x, fleche_gauche_y))
        fleche_droite_rect = fleche_choix_skin_droite.get_rect(topleft=(fleche_droite_x, fleche_droite_y))

        # --- AFFICHAGE DES PIÈCES ---
        screen.blit(piece, (20, 65))  # l’icône de la pièce
        draw_text(f": {coins}", 90, 90, WHITE, font)



    elif game_state == "settings":
        screen.blit(background_images[0], (0, 0))

        font_params = pygame.font.Font(None, 80)
        settings_text = font_params.render("Paramètres", True, WHITE)
        screen.blit(settings_text, (WIDTH // 2 - settings_text.get_width() // 2, HEIGHT // 25))

        cross_x, cross_y = 30, 30
        croix_rect = croix_retour_page.get_rect(topleft=(cross_x, cross_y))
        draw_button(croix_retour_page, croix_rect, screen, hover_scale=1.08, border_color=(255, 0, 0))


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

        # --- 0) REDESSINER LA SCÈNE DE JEU EN FOND (mais figée) ---

        # fond
        if background_index < len(shuffled_backgrounds):
            screen.blit(shuffled_backgrounds[background_index], (0, 0))
        else:
            screen.blit(shuffled_backgrounds[-1], (0, 0))

        # aliens
        for alien in aliens:
            screen.blit(alien["surface"], alien["rect"])

        # bonus / powerups (cibles)
        draw_bonuses()

        # balles du joueur
        for bullet in bullets:
            screen.blit(bullet_image, bullet["rect"])

        for bullet in secondary_bullets:
            pygame.draw.ellipse(screen, BLUE, bullet["rect"])

        # balles ennemies
        for e_bullet in enemy_bullets:
            pygame.draw.rect(screen, (255, 255, 0), e_bullet["rect"])

        # Attaques du boss en pause (affichage figé)
        pause_now = pygame.time.get_ticks()

        # Zones
        for zone in boss_zones:
            age = pause_now - zone["t0"]
            if age < 0 or age >= zone["life_ms"]:
                continue
            pygame.draw.circle(screen, (255, 80, 80),
                               (int(zone["cx"]), int(zone["cy"])), int(zone["r"]), 3)

        # Lasers
        for laser in boss_lasers:
            age = pause_now - laser["t0"]
            if age < 0 or age >= (laser["warn_ms"] + laser["active_ms"]):
                continue
            if age < laser["warn_ms"]:
                pygame.draw.rect(screen, (255, 255, 0), laser["rect"], 2)
            else:
                pygame.draw.rect(screen, (255, 0, 0), laser["rect"])

        # boss si présent
        if boss:
            screen.blit(boss_surface, boss)
            draw_boss_health_bar(boss_health, boss_max_health, boss, y_offset=-20)

        # vaisseau + HUD
        screen.blit(spaceship_image, (spaceship_x, spaceship_y))
        draw_shield_effect(ship_rect, pygame.time.get_ticks())
        show_level(level)
        draw_text(f"Score: {score}", 10, 10)
        draw_text(f"Vie : {lives}", WIDTH - 85, 45)
        draw_text(f" : {coins}", 65, 90)
        draw_text(f"Balles restantes: {remaining_bullets}", 10, 40)
        draw_powerup_status(pygame.time.get_ticks())
        screen.blit(piece, (10, 65))

        # --- 1) Overlay sombre sur tout l'écran (effet pause) ---
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))  # un peu moins sombre qu'avant
        screen.blit(overlay, (0, 0))

        # --- 2) Panneau pour les boutons ---
        panel_width = button_continue.get_width() + 150
        panel_height = button_continue.get_height() * 3 + 300

        panel_x = x_position_pause - 75
        panel_y = y_position_pause - 225

        # Glow doux derrière le panneau
        glow_surface = pygame.Surface((panel_width + 40, panel_height + 40), pygame.SRCALPHA)
        pygame.draw.rect(
            glow_surface,
            (255, 255, 255, 40),  # blanc très transparent
            glow_surface.get_rect(),
            border_radius=15
        )
        screen.blit(glow_surface, (panel_x - 20, panel_y - 20))

        # Panneau semi-transparent avec bordure
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(
            panel_surface,
            (0, 0, 0, 200),  # noir, semi-transparent
            pygame.Rect(0, 0, panel_width, panel_height),
            border_radius=20
        )
        pygame.draw.rect(
            panel_surface,
            (255, 255, 255, 230),  # bordure blanche
            pygame.Rect(0, 0, panel_width, panel_height),
            width=2,
            border_radius=20
        )
        screen.blit(panel_surface, (panel_x, panel_y))

        # --- 3) Titre PAUSE ---
        pause_font = pygame.font.Font(None, 72)
        pause_text = pause_font.render("PAUSE", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(WIDTH // 2, panel_y + 60))
        screen.blit(pause_text, pause_rect)

        # --- 4) Boutons avec hover ---
        button_continue_rect = button_continue.get_rect(
            topleft=(x_position_pause, y_position_pause - 100)
        )
        button_restart_rect = button_restart.get_rect(
            topleft=(x_position_pause, y_position_pause)
        )
        button_quit_rect2 = button_quit.get_rect(
            topleft=(x_position_pause, y_position_pause + 100)
        )

        draw_button(button_continue, button_continue_rect, screen)
        draw_button(button_restart, button_restart_rect, screen)
        draw_button(button_quit, button_quit_rect2, screen)

        # Bouton pause en haut à gauche pour reprendre
        pause_pos_x = 10
        pause_pos_y = 140
        pause_button_rect = button_pause.get_rect(topleft=(pause_pos_x, pause_pos_y))
        draw_button(button_pause, pause_button_rect, screen, hover_scale=1.05, border_color=(255, 255, 0))



    elif game_state == "boss_dying":
        boss_death_update(pygame.time.get_ticks())



    elif game_state == "playing":
        if background_index < len(shuffled_backgrounds):
            screen.blit(shuffled_backgrounds[background_index], (0, 0))
        else:
            screen.blit(shuffled_backgrounds[-1], (0, 0))

        show_level(level)

        if not game_over:

            # --- Défaite si plus aucune balle en réserve ET en vol ---
            if remaining_bullets <= 0 and not bullets and not secondary_bullets and not game_over:
                # Il reste encore des ennemis ou un boss ? alors c'est perdu
                if aliens or boss:
                    end_time = pygame.time.get_ticks()
                    sons["défaite"].play()
                    music_channel.stop()
                    game_over = True

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
                spaceship_rect = spaceship_images[selected_skin].get_rect(topleft=(spaceship_x, spaceship_y))
                pygame.draw.line(
                    screen,
                    GREEN,
                    (spaceship_rect.centerx, spaceship_rect.top),  # départ = haut du vaisseau
                    (spaceship_rect.centerx, 0),  # ligne qui monte vers le haut de l’écran
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

            if not boss and random.random() < alien_en_or_spawn_rate:
                spawn_alien_en_or()

            if not boss and random.random() < alien_en_diamant_spawn_rate:
                spawn_alien_en_diamant()

            if not boss and random.random() < alien_attaquant_spawn_rate:
                spawn_alien_shooter()

            # Bonus indépendant (tombe comme un alien) : le joueur doit tirer dessus
            rate = bonus_spawn_rate * (0.5 if boss else 1.0)
            if random.random() < rate:
                spawn_falling_bonus()

            current_time = pygame.time.get_ticks()
            update_fx()
            update_powerups(current_time)

            # Rect du vaisseau (taille réelle du skin)
            ship_rect = spaceship_image.get_rect(topleft=(spaceship_x, spaceship_y))
            update_bonuses_and_handle_hits(current_time)

            draw_shield_effect(ship_rect, pygame.time.get_ticks())

            # --- MISE À JOUR DES BALLES ENNEMIES (UNE SEULE FOIS PAR FRAME) ---
            for e_bullet in enemy_bullets[:]:
                # Support ancien format {"speed": ...} + nouveau format {"speed_x": ..., "speed_y": ...}
                if "pos" not in e_bullet:
                    e_bullet["pos"] = [float(e_bullet["rect"].x), float(e_bullet["rect"].y)]

                vx = float(e_bullet.get("speed_x", 0.0))
                vy = float(e_bullet.get("speed_y", e_bullet.get("speed", 0.0)))

                e_bullet["pos"][0] += vx
                e_bullet["pos"][1] += vy
                e_bullet["rect"].x = int(e_bullet["pos"][0])
                e_bullet["rect"].y = int(e_bullet["pos"][1])

                # Hors écran
                if (e_bullet["rect"].top > HEIGHT or
                        e_bullet["rect"].right < 0 or
                        e_bullet["rect"].left > WIDTH):
                    if e_bullet in enemy_bullets:
                        enemy_bullets.remove(e_bullet)
                    continue

                # Collision vaisseau
                if ship_rect.colliderect(e_bullet["rect"]):
                    if e_bullet in enemy_bullets:
                        enemy_bullets.remove(e_bullet)
                    handle_life_loss()
                    break  # IMPORTANT: handle_life_loss() clear() enemy_bullets, donc on sort de la boucle
            # --- MISE À JOUR DES ATTAQUES DU BOSS (LASERS / ZONES) ---
            if boss:
                life_lost_from_boss = False

                # Lasers verticaux
                for laser in boss_lasers[:]:
                    age = current_time - laser["t0"]

                    # Laser pas encore "armé" (offset)
                    if age < 0:
                        continue

                    # Fin de vie du laser
                    if age >= (laser["warn_ms"] + laser["active_ms"]):
                        boss_lasers.remove(laser)
                        continue

                    # Collision uniquement en phase active
                    if age >= laser["warn_ms"]:
                        if ship_rect.colliderect(laser["rect"]):
                            boss_lasers.clear()
                            boss_zones.clear()
                            handle_life_loss()
                            life_lost_from_boss = True
                            break

                # Zones qui grandissent
                if not life_lost_from_boss:
                    for zone in boss_zones[:]:
                        age = current_time - zone["t0"]

                        if age >= zone["life_ms"]:
                            boss_zones.remove(zone)
                            continue

                        # Croissance (par frame)
                        zone["r"] += zone["grow"]

                        sx, sy = ship_rect.centerx, ship_rect.centery
                        dx = sx - zone["cx"]
                        dy = sy - zone["cy"]

                        inside = (dx * dx + dy * dy) <= (zone["r"] * zone["r"])

                        if inside:
                            if zone["inside_since"] is None:
                                zone["inside_since"] = current_time
                            elif current_time - zone["inside_since"] >= zone["hit_delay_ms"]:
                                boss_lasers.clear()
                                boss_zones.clear()
                                handle_life_loss()
                                break
                        else:
                            zone["inside_since"] = None

            # --- MISE À JOUR DES ALIENS ---
            for alien in aliens[:]:
                # --- Déplacement ---

                # On travaille en centre (pos) pour être stable quand la surface tourne

                if "pos" not in alien:
                    alien["pos"] = [float(alien["rect"].centerx), float(alien["rect"].centery)]

                if "vx" not in alien:
                    alien["vx"] = 0.0

                if "base_surface" not in alien:
                    alien["base_surface"] = alien["surface"]

                    alien["angle"] = 0.0

                    alien["angular_speed"] = 0.0

                if alien["type"] == "shooter":

                    # Shooter: gauche <-> droite (pas de chute)

                    alien["pos"][0] += float(alien.get("vx", 0.0))

                else:

                    # Astéroïdes: chute + éventuel zigzag (vx)

                    alien["pos"][1] += alien_speed

                    alien["pos"][0] += float(alien.get("vx", 0.0))

                # --- Rotation (certains astéroïdes) ---

                if float(alien.get("angular_speed", 0.0)) != 0.0:
                    alien["angle"] = (float(alien.get("angle", 0.0)) + float(alien["angular_speed"])) % 360.0

                    alien["surface"] = pygame.transform.rotate(alien["base_surface"], alien["angle"])

                # Reconstruire le rect autour du centre

                cx, cy = alien["pos"]

                alien["rect"] = alien["surface"].get_rect(center=(int(cx), int(cy)))

                # --- Rebond horizontal (zigzag + shooter) ---

                vx = float(alien.get("vx", 0.0))

                if vx != 0.0:

                    half_w = alien["rect"].width / 2

                    if alien["pos"][0] - half_w <= 0:

                        alien["pos"][0] = half_w

                        alien["vx"] = abs(vx)

                    elif alien["pos"][0] + half_w >= WIDTH:

                        alien["pos"][0] = WIDTH - half_w

                        alien["vx"] = -abs(vx)

                    alien["rect"].centerx = int(alien["pos"][0])

                # FX: trainée derrière les astéroïdes
                if alien.get("type") != "shooter":
                    spawn_asteroid_trail(alien, current_time)

                # Collision alien (astéroïde) <-> vaisseau
                if ship_rect.colliderect(alien["rect"]):
                    if is_powerup_active("shield", current_time):
                        # Bouclier: on détruit l\'astéroïde sans perdre de vie
                        spawn_explosion_fx(alien["rect"].centerx, alien["rect"].centery,
                                           alien_type=alien.get("type", "normal"), scale=0.7)
                        if alien in aliens:
                            aliens.remove(alien)
                        continue
                    handle_life_loss()
                    break

                # Alien sort en bas
                if alien["type"] != "shooter" and alien["rect"].top > HEIGHT:
                    # On retire l\'alien sorti de l\'écran
                    if alien in aliens:
                        aliens.remove(alien)
                    # Bouclier: pas de perte de vie
                    if is_powerup_active("shield", current_time):
                        continue
                    handle_life_loss()
                    break

                # Tir des aliens shooters (création uniquement)
                if alien["type"] == "shooter":
                    if current_time - alien["last_shot"] > 2000:
                        enemy_bullets.append({
                            "rect": pygame.Rect(alien["rect"].centerx - 5, alien["rect"].bottom, 10, 15),
                            "speed": 17.5
                        })
                        alien["last_shot"] = current_time
                # --- Collisions tirs joueur <-> aliens ---
                alien_destroyed = False

                # 1) Bullets classiques (rouges)
                for b in bullets[:]:
                    if b["rect"].colliderect(alien["rect"]):
                        bullets.remove(b)
                        # FX: explosion à la destruction
                        spawn_explosion_fx(alien["rect"].centerx, alien["rect"].centery,
                                           alien_type=alien.get("type", "normal"), scale=1.0)
                        if alien in aliens:
                            aliens.remove(alien)
                        shots_hit += 1
                        sons["explosion_alien_vaisseau"].play()

                        if alien["type"] == "gold":
                            coins += coins_reward[current_difficulty]["alien_en_or"]
                            score += 1
                            if score % 10 == 0:
                                handle_level_completion()
                        elif alien["type"] == "diamond":
                            coins += coins_reward[current_difficulty]["alien_en_diamant"]
                            score += 1
                            if score % 10 == 0:
                                handle_level_completion()
                        else:
                            gain = coins_reward[current_difficulty]["alien"]
                            coins += gain
                            coins_gained_this_run += gain

                            if not alien.get("is_minion"):
                                score += 1
                                if score % 10 == 0:
                                    handle_level_completion()

                        alien_destroyed = True
                        break  # cet alien est détruit

                # 2) Bullets secondaires (bleues) seulement si l'alien existe encore
                if not alien_destroyed:
                    for b in secondary_bullets[:]:
                        if b["rect"].colliderect(alien["rect"]):
                            secondary_bullets.remove(b)
                            # FX: explosion à la destruction
                            spawn_explosion_fx(alien["rect"].centerx, alien["rect"].centery,
                                               alien_type=alien.get("type", "normal"), scale=1.0)
                            if alien in aliens:
                                aliens.remove(alien)
                            shots_hit += 1
                            sons["explosion_alien_vaisseau"].play()

                            if alien["type"] == "gold":
                                coins += coins_reward[current_difficulty]["alien_en_or"]
                                score += 1
                                if score % 10 == 0:
                                    handle_level_completion()
                            elif alien["type"] == "diamond":
                                coins += coins_reward[current_difficulty]["alien_en_diamant"]
                                score += 1
                                if score % 10 == 0:
                                    handle_level_completion()
                            else:
                                gain = coins_reward[current_difficulty]["alien"]
                                coins += gain
                                coins_gained_this_run += gain

                                if not alien.get("is_minion"):
                                    score += 1
                                    if score % 10 == 0:
                                        handle_level_completion()

                            break

            if boss:
                # Mouvement du boss
                boss.x += boss_direction * 5
                if boss.left <= 0 or boss.right >= WIDTH:
                    boss_direction *= -1

                boss_hitbox = compute_boss_hitbox(boss, boss_id if boss_id is not None else 1)

                # --- Boss : PV qui augmentent si le combat dure trop longtemps (3s = +1) ---
                if current_time - boss_last_regen >= 3000:
                    if boss_max_health < boss_max_health_cap:
                        boss_max_health += 1
                        boss_health += 1
                    boss_last_regen = current_time

                # --- Boss : phases + patterns par boss (3 phases différentes) ---
                hp_ratio = boss_health / boss_max_health if boss_max_health > 0 else 0.0

                if hp_ratio <= 0.33:
                    boss_phase = 3
                elif hp_ratio <= 0.66:
                    boss_phase = 2
                else:
                    boss_phase = 1

                bid = boss_id if boss_id is not None else 1

                # Boss 1 : facile (lisible, peu de combos)
                if bid == 1:
                    slow1 = 1.25  # +25% plus lent (augmente pour ralentir encore)
                    aimed_cooldown = int((1050 if boss_phase == 1 else (900 if boss_phase == 2 else 780)) * slow1)
                    aimed_speed = 8 if boss_phase == 1 else (9 if boss_phase == 2 else 10)

                    if current_time - boss_last_shot >= aimed_cooldown:
                        spawn_boss_aimed_shot(boss, ship_rect, speed=aimed_speed)
                        boss_last_shot = current_time

                    if boss_phase >= 2:
                        if current_time - boss_last_fan >= 2600:
                            spawn_boss_fan_shot(boss, count=2, spread_deg=26, speed=9)
                            boss_last_fan = current_time

                    if boss_phase >= 3:
                        if current_time - boss_last_laser >= 3200:
                            spawn_boss_laser(ship_rect.centerx, current_time, width=80, warn_ms=750, active_ms=550)
                            boss_last_laser = current_time

                        # Zones circulaires (désactivées pour Boss 1)
                        # if current_time - boss_last_zone >= 3300:
                        #     spawn_boss_zone(ship_rect, current_time, start_r=30, grow_per_frame=1.6,
                        #                     life_ms=1800, hit_delay_ms=450)
                        #     boss_last_zone = current_time

                # Boss 2 : moyen (éventails + lasers plus fréquents)
                elif bid == 2:
                    slow2 = 1.20  # +20% plus lent (augmente pour ralentir encore)
                    aimed_cooldown = int((900 if boss_phase == 1 else (780 if boss_phase == 2 else 680)) * slow2)
                    aimed_speed = 10 if boss_phase == 1 else (11 if boss_phase == 2 else 12)

                    if current_time - boss_last_shot >= aimed_cooldown:
                        spawn_boss_aimed_shot(boss, ship_rect, speed=aimed_speed)
                        boss_last_shot = current_time

                    if boss_phase >= 2:
                        fan_cd = int((1900 if boss_phase == 2 else 1550) * slow2)
                        if current_time - boss_last_fan >= fan_cd:
                            spawn_boss_fan_shot(boss, count=2, spread_deg=50, speed=10)
                            boss_last_fan = current_time

                        laser_cd = int((2500 if boss_phase == 2 else 2050) * slow2)
                        if current_time - boss_last_laser >= laser_cd:
                            spawn_boss_laser(ship_rect.centerx, current_time, width=85, warn_ms=700, active_ms=600)

                            if random.random() < (0.40 if boss_phase == 2 else 0.60):
                                spawn_boss_laser(random.randint(80, WIDTH - 120), current_time,
                                                 width=85, warn_ms=700, active_ms=520, offset_ms=320)

                            boss_last_laser = current_time

                    if boss_phase >= 3:
                        if current_time - boss_last_zone >= 2800:
                            spawn_boss_zone(ship_rect, current_time, start_r=38, grow_per_frame=2.0,
                                            life_ms=2100, hit_delay_ms=420)
                            boss_last_zone = current_time

                        if current_time - boss_last_minion >= 6500:
                            spawn_boss_minions(boss, current_time, count=1, shooter_chance=0.75)
                            boss_last_minion = current_time

                # Boss 3 : difficile (arc burst + pluie + minions)
                else:
                    # Boss 3 nerf : moins de pression + projectiles plus lents
                    aimed_cooldown = 1100 if boss_phase == 1 else (1000 if boss_phase == 2 else 900)
                    aimed_speed = 9 if boss_phase == 1 else (10 if boss_phase == 2 else 11)

                    if current_time - boss_last_shot >= aimed_cooldown:
                        spawn_boss_aimed_shot(boss, ship_rect, speed=aimed_speed)
                        boss_last_shot = current_time

                    fan_cd = 2400 if boss_phase == 1 else (2100 if boss_phase == 2 else 1900)
                    if current_time - boss_last_fan >= fan_cd:
                        spawn_boss_fan_shot(
                            boss,
                            count=4,
                            spread_deg=50 if boss_phase == 1 else 60,
                            speed=9
                        )
                        boss_last_fan = current_time

                    laser_cd = 2800 if boss_phase == 1 else (2600 if boss_phase == 2 else 2400)
                    if current_time - boss_last_laser >= laser_cd:
                        spawn_boss_laser(ship_rect.centerx, current_time, width=75, warn_ms=750, active_ms=550)

                        # laser secondaire moins fréquent
                        if random.random() < (0.35 if boss_phase == 1 else 0.45):
                            spawn_boss_laser(
                                random.randint(80, WIDTH - 120), current_time,
                                width=75, warn_ms=750, active_ms=520, offset_ms=320
                            )

                        # 3e laser en phase 3 très rare
                        if boss_phase >= 3 and random.random() < 0.15:
                            spawn_boss_laser(
                                random.randint(80, WIDTH - 120), current_time,
                                width=70, warn_ms=720, active_ms=480, offset_ms=420
                            )

                        boss_last_laser = current_time

                    if boss_phase >= 2:
                        burst_cd = 6500 if boss_phase == 2 else 6000
                        if current_time - boss_last_burst >= burst_cd:
                            spawn_boss_arc_burst(
                                boss,
                                count=4,
                                start_deg=45, end_deg=135,
                                speed=6
                            )
                            boss_last_burst = current_time

                    if boss_phase >= 3:
                        if current_time - boss_last_zone >= 3200:
                            spawn_boss_zone(
                                ship_rect, current_time,
                                start_r=42, grow_per_frame=1.8,
                                life_ms=2200, hit_delay_ms=520
                            )
                            boss_last_zone = current_time

                        if current_time - boss_last_minion >= 6500:
                            spawn_boss_minions(boss, current_time, count=1, shooter_chance=0.55)
                            boss_last_minion = current_time

                        if current_time - boss_last_rain >= 6000:
                            spawn_boss_rain(current_time, count=3, speed=8, avoid_x=ship_rect.centerx, avoid_radius=90)
                            boss_last_rain = current_time

                boss_dead = False

                # ---------------------------------------------------------
                # 1) Collisions avec les balles normales
                # ---------------------------------------------------------
                for bullet in bullets[:]:
                    if bullet["rect"].colliderect(boss_hitbox if boss_hitbox else boss):
                        bullets.remove(bullet)
                        boss_health -= 1
                        shots_hit += 1
                        sons["dégât_boss"].play()

                        if boss_health <= 0:
                            boss_dead = True
                            break  # on casse la boucle car le boss est mort

                # ---------------------------------------------------------
                # 2) Collisions balles secondaires (si le boss n'est pas mort)
                # ---------------------------------------------------------
                if not boss_dead:
                    for bullet in secondary_bullets[:]:
                        if bullet["rect"].colliderect(boss_hitbox if boss_hitbox else boss):
                            secondary_bullets.remove(bullet)
                            boss_health -= 1
                            shots_hit += 1
                            sons["dégât_boss"].play()

                            if boss_health <= 0:
                                boss_dead = True
                                break

                # ---------------------------------------------------------
                # 3) Si le boss meurt → on gère tout ici (une seule fois)
                # ---------------------------------------------------------
                if boss_dead:
                    bullets.clear()
                    secondary_bullets.clear()
                    enemy_bullets.clear()
                    boss_lasers.clear()
                    boss_zones.clear()

                    # Récompenses
                    gain_boss = coins_reward[current_difficulty]["boss"]
                    coins += gain_boss
                    coins_gained_this_run += gain_boss

                    # +100 balles (ammo)
                    remaining_bullets += 100

                    end_time = pygame.time.get_ticks()

                    sons["explosion_boss"].play()

                    # Prépare la cinématique (freeze + explosion) sans bloquer la boucle
                    boss_center = (boss_hitbox.center if boss_hitbox else boss.center)
                    boss_death_pending = {"center": (int(boss_center[0]), int(boss_center[1])),
                                          "boss_id": boss_id,
                                          "pending_level": pending_level_after_boss}

                    # On retire le boss immédiatement (il sera remplacé par l'explosion)
                    boss = None
                    boss_hitbox = None

                    persist_save()

                else:
                    # Affichage du boss (uniquement s'il est vivant)
                    screen.blit(boss_surface, boss)
                    draw_boss_health_bar(boss_health, boss_max_health, boss, y_offset=-20)

                if boss:
                    screen.blit(boss_surface, boss)
                    draw_boss_health_bar(boss_health, boss_max_health, boss, y_offset=-20)

            # FX: rendu des particules (trainées derrière / explosions devant)
            render_fx_surfaces()
            screen.blit(fx_surface_under, (0, 0))

            for alien in aliens:
                screen.blit(alien["surface"], alien["rect"])

            # bonus / powerups (cibles)
            draw_bonuses()

            for bullet in bullets:
                screen.blit(bullet_image, bullet["rect"])

            for bullet in secondary_bullets:
                pygame.draw.ellipse(screen, BLUE, bullet["rect"])

            # Attaques du boss (affichage)
            for zone in boss_zones:
                age = current_time - zone["t0"]
                if age < 0 or age >= zone["life_ms"]:
                    continue
                pygame.draw.circle(screen, (255, 80, 80),
                                   (int(zone["cx"]), int(zone["cy"])), int(zone["r"]), 3)

            for laser in boss_lasers:
                age = current_time - laser["t0"]
                if age < 0 or age >= (laser["warn_ms"] + laser["active_ms"]):
                    continue
                if age < laser["warn_ms"]:
                    pygame.draw.rect(screen, (255, 255, 0), laser["rect"], 2)
                else:
                    pygame.draw.rect(screen, (255, 0, 0), laser["rect"])

            for e_bullet in enemy_bullets:
                pygame.draw.rect(screen, (255, 255, 0), e_bullet["rect"])

            # FX au-dessus des sprites
            screen.blit(fx_surface_over, (0, 0))

            screen.blit(spaceship_image, (spaceship_x, spaceship_y))
            draw_text(f"Score: {score}", 10, 10)
            draw_text(f"Vie : {lives}", WIDTH - 85, 45)
            draw_text(f" : {coins}", 65, 90)
            draw_text(f"Balles restantes: {remaining_bullets}", 10, 40)
            draw_powerup_status(current_time)

            # On affiche aussi le bouton Pause pour "reprendre" la partie (avec hover)
            pause_pos_x = 10
            pause_pos_y = 140
            pause_button_rect = button_pause.get_rect(topleft=(pause_pos_x, pause_pos_y))
            draw_button(button_pause, pause_button_rect, screen, hover_scale=1.05, border_color=(255, 255, 0))

            # On dessine (affiche) l'image de la pièce
            pause_pos_x_2 = 10
            pause_pos_y_2 = 65
            screen.blit(piece, (pause_pos_x_2, pause_pos_y_2))

            # --- Cinématique mort du boss (freeze + explosion) ---
            if boss_death_pending is not None and not boss_death_anim.get("active", False):
                freeze_surface = screen.copy()
                start_boss_death_sequence(freeze_surface,
                                          boss_death_pending["center"],
                                          boss_death_pending["boss_id"],
                                          boss_death_pending["pending_level"])
                boss_death_pending = None

    # GAME OVER
    if game_over:

        if end_time is None:
            end_time = pygame.time.get_ticks()  # sécurité au cas où

        elapsed_time = (end_time - start_time) // 1000
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60

        if shots_fired > 0:
            accuracy = int((shots_hit / shots_fired) * 100)
        else:
            accuracy = 0

        # Dessin du fond
        larger_font_titre = pygame.font.Font(None, 100)  # Taille 150 pour un texte plus grand
        larger_font_text = pygame.font.Font(None, 35)  # Taille 150 pour un texte plus grand

        screen.blit(background_images[0], (0, 0))
        draw_text("GAME OVER!", WIDTH // 2, HEIGHT // 8 - 50, RED, larger_font_titre, centered=True)
        draw_text("VOUS AVEZ PERDU, SOUHAITEZ VOUS RECOMMENCER OU QUITTER ?", WIDTH // 2, HEIGHT // 7, WHITE,
                  larger_font_text, centered=True)

        draw_text(f"Vous avez détruits {score} astéroides et aliens.", WIDTH // 2, HEIGHT // 1.6, WHITE,
                  larger_font_text, centered=True)
        draw_text(f"Vous avez atteint le niveau max félicitation !!", WIDTH // 2, HEIGHT // 1.5, WHITE,
                  larger_font_text, centered=True)
        draw_text(f"Ils vous restaient {remaining_bullets} balles.", WIDTH // 2, HEIGHT // 1.41, WHITE,
                  larger_font_text, centered=True)
        draw_text(f"Vous avez récoltés {coins_gained_this_run} pièces durant votre partie.", WIDTH // 2, HEIGHT // 1.33,
                  WHITE, larger_font_text, centered=True)
        draw_text(f"Votre partie à durée {minutes} minutes et {seconds} secondes.", WIDTH // 2, HEIGHT // 1.26, WHITE,
                  larger_font_text, centered=True)
        draw_text(f"Précision de vos tir : {accuracy}%", WIDTH // 2, HEIGHT // 1.2, WHITE, larger_font_text,
                  centered=True)

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
        pause_pos_y = 140
        pause_button_rect = button_pause.get_rect(topleft=(pause_pos_x, pause_pos_y))

        # Dessin des boutons-
        draw_button(button_restart, button_restart_rect, screen)
        draw_button(button_quit, button_quit_rect2, screen)

        # Gestion des événements souris
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:  # Clic gauche
            if button_restart_rect.collidepoint(mouse_x, mouse_y):
                reset_game()
                game_state = "playing"
            elif button_quit_rect2.collidepoint(mouse_x, mouse_y):
                reset_game()
                game_state = "menu"


    # VICTORY
    elif game_state == "victory":

        if end_time is None:
            end_time = pygame.time.get_ticks()  # sécurité au cas où

        elapsed_time = (end_time - start_time) // 1000
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60

        if shots_fired > 0:
            accuracy = int((shots_hit / shots_fired) * 100)
        else:
            accuracy = 0

        music_channel.stop()

        larger_font_titre = pygame.font.Font(None, 100)  # Taille 150 pour un texte plus grand
        larger_font_text = pygame.font.Font(None, 35)  # Taille 150 pour un texte plus grand

        screen.blit(background_images[0], (0, 0))
        draw_text("FÉLICITATIONS, VOUS AVEZ GAGNÉ!", WIDTH // 2, HEIGHT // 8 - 50, WHITE, large_font, centered=True)

        draw_text(f"Vous avez détruits {score} astéroides et aliens.", WIDTH // 2, HEIGHT // 1.6, WHITE,
                  larger_font_text, centered=True)
        draw_text(f"Vous avez atteint le niveau max félicitation !!", WIDTH // 2, HEIGHT // 1.5, WHITE,
                  larger_font_text, centered=True)
        draw_text(f"Ils vous restaient {lives} vies.", WIDTH // 2, HEIGHT // 1.41, WHITE, larger_font_text,
                  centered=True)
        draw_text(f"Ils vous restaient {remaining_bullets} balles.", WIDTH // 2, HEIGHT // 1.33, WHITE,
                  larger_font_text, centered=True)
        draw_text(f"Vous avez récoltés {coins_gained_this_run} pièces durant votre partie.", WIDTH // 2, HEIGHT // 1.26,
                  WHITE, larger_font_text, centered=True)
        draw_text(f"Votre partie à durée {minutes} minutes et {seconds} secondes.", WIDTH // 2, HEIGHT // 1.2, WHITE,
                  larger_font_text, centered=True)
        draw_text(f"Précision de vos tir : {accuracy}%", WIDTH // 2, HEIGHT // 1.145, WHITE, larger_font_text,
                  centered=True)

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
        pause_pos_y = 140
        pause_button_rect = button_pause.get_rect(topleft=(pause_pos_x, pause_pos_y))

        # Dessin des boutons
        screen.blit(button_restart, button_restart_rect.topleft)
        screen.blit(button_quit, button_quit_rect2.topleft)

        # Gestion des événements souris
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:  # Clic gauche
            if button_restart_rect.collidepoint(mouse_x, mouse_y):
                reset_game()
                game_state =     "playing"
            elif button_quit_rect2.collidepoint(mouse_x, mouse_y):
                reset_game()
                game_state = "menu"

    pygame.display.flip()

# permet d'enregistrer le nombre de pièces
persist_save()
pygame.quit()