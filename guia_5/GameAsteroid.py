import pygame
import os
import random
import threading
import sys

import firebase_admin
from firebase_admin import credentials, db

# Connection to firebase
key_path = os.path.join(os.path.dirname(__file__), 'firebase')
key = os.path.join(key_path, 'space-shooter-9c882-firebase-adminsdk-tndg0-ca7618fd2e.json')

cred = credentials.Certificate(key)
firebase_admin.initialize_app(cred, {'databaseURL': 'https://space-shooter-9c882-default-rtdb.firebaseio.com/'})

# Referencias a la base de datos de los jugadores
ref_player_1 = db.reference('/player_1')
ref_ship_player_1 = ref_player_1.child('-Nsz_waZceu5sMSuXRXq')

ref_player_2 = db.reference('/player_2')
ref_ship_player_2 = ref_player_2.child('-NtXK3NuN1Ly55ArPwUi')

# Acces path to assets
assest_path = os.path.join(os.path.dirname(__file__), 'assets')

background_path = os.path.join(assest_path, 'background.jpg')

# PLAYER 1
ship_path = os.path.join(assest_path, 'player_1.png')
shot_path = os.path.join(assest_path, 'shot.png')

# PLAYER 2
ship_path_2 = os.path.join(assest_path, 'player_2.png')
shot_path_2 = os.path.join(assest_path, 'shot.png')

asteroid_path = os.path.join(assest_path, 'asteroid.png')
game_over_text_path = os.path.join(assest_path, 'game_over.png')

# Sounds paths
shot_sound_path = os.path.join(assest_path, 'shot.wav')
background_sound_path = os.path.join(assest_path, 'sound_background.wav')
game_over_sound_path = os.path.join(assest_path, 'game_over.wav')

pygame.init()

#  Config windows
width = 640
height = 460

# Create windows
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Asteroid game")

# Load assets

# Player 1
ship = pygame.image.load(ship_path)
shot = pygame.image.load(shot_path)

# Player 2
ship_2 = pygame.image.load(ship_path_2)
shot_2 = pygame.image.load(shot_path_2)

background = pygame.image.load(background_path).convert()
asteroid = pygame.image.load(asteroid_path)
game_over_text = pygame.image.load(game_over_text_path).convert()

#  Load assets sounds
shot_sound = pygame.mixer.Sound(shot_sound_path)

background_sound = pygame.mixer.Sound(background_sound_path)
game_over_sound = pygame.mixer.Sound(game_over_sound_path)

# Resize assets
background = pygame.transform.scale(background, (width, height))

# PLayer 1
ship = pygame.transform.scale(ship, (ship.get_width() // 4, ship.get_height() // 4))
shot = pygame.transform.scale(shot, (shot.get_width() // 12, shot.get_height() // 12))

# Player 2
ship_2 = pygame.transform.scale(ship_2, (ship_2.get_width() // 4, ship_2.get_height() // 4))
shot_2 = pygame.transform.scale(shot_2, (shot_2.get_width() // 12, shot_2.get_height() // 12))

asteroid = pygame.transform.scale(asteroid, (asteroid.get_width() // 2.5, asteroid.get_height() // 2.5))
game_over_text = pygame.transform.scale(game_over_text, (width, height))

#  Initial position ship

# Player 1
shipRect = ship.get_rect()
x_ship, y_ship = width / 2 - shipRect.width / 2 + 200, height - 100

shipRect.move_ip(x_ship, y_ship)

# Shot
shotRect = shot.get_rect()
x_shot, y_shot = x_ship + 18, y_ship - 30

shotRect.move_ip(x_shot, y_shot)

# Player 2
shipRect_2 = ship_2.get_rect()
x_ship_2, y_ship_2 = width / 2 - shipRect.width / 2 - 200, height - 100

shotRect_2 = shot_2.get_rect()
x_shot_2, y_shot_2 = x_ship_2 + 18, y_ship_2 - 30

shipRect_2.move_ip(x_ship_2, y_ship_2)
shotRect_2.move_ip(x_shot_2, y_shot_2)

# Asteroid
asteroidRect = asteroid.get_rect()

# Game over
game_over_text_rect = game_over_text.get_rect()
game_over_text_rect.move_ip(width / 2 - game_over_text.get_width() / 2, height / 2 - game_over_text.get_height() / 2)

font = pygame.font.Font(None, 36)

playing = True

# Config speed

speed_ship = 4
speed_asteroid = 3
speed_shot = 4

bullets = []
asteroids = []

last_shot_time = 0
last_asteroid_time = 0

score = 0
internal_score = 0

# Last position ship
last_position_ship = x_ship

def loading_screen():
    loading = True

    while loading:

        player1 = ref_player_1.get()
        player2 = ref_player_2.get()

        player1_selected = player1['-Nsz_waZceu5sMSuXRXq']['active']
        player2_selected = player2['-NtXK3NuN1Ly55ArPwUi']['active']
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0,0,0))
        loading_text = font.render("Waiting for Players...",True,(255,255,255))
        screen.blit(loading_text, (width//2 - loading_text.get_width()//2, height//2 - loading_text.get_height()//2))
        pygame.display.flip()

        if player1_selected and player2_selected:
            loading = False
            print("The players are ready")

def selected_player():
    global key

    player1 = ref_player_1.get()
    player2 = ref_player_2.get()

    player1_selected = player1['-Nsz_waZceu5sMSuXRXq']['active']
    player2_selected = player2['-NtXK3NuN1Ly55ArPwUi']['active']

    selected = False
    
    while not selected:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if not player1_selected:
                        key = 1
                        ref_ship_player_1.update({'active':True})
                        print('Player 1 selected')
                        selected = True
                    else:
                        print("player 1 already exists")
                if event.key == pygame.K_2:
                    if not player2_selected:
                        key = 2
                        ref_ship_player_2.update({'active':True})
                        print('Player 2 selected')
                        selected = True
                    else:
                        print("player 2 already exists")
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        #lOADING - MESSAGE
        screen.fill((0,0,0))
        selection_text = font.render("Selected Players:", True, (255, 255, 255))
        player1_text = font.render("Press '1' to choose player 1", True, (255, 255, 255))
        player2_text = font.render("Press '2' to choose player 2", True, (255, 255, 255))
        screen.blit(selection_text, (width//2 - selection_text.get_width()//2, height//2 - 50))
        screen.blit(player1_text, (width//2 - player1_text.get_width()//2, height//2))
        screen.blit(player2_text, (width//2 - player2_text.get_width()//2, height//2 + 50))
        pygame.display.flip()

def update_database():
    global x_ship
    global last_position_ship

    if last_position_ship != x_ship:
        ref_ship_player_1.update({'x_ship': x_ship})
        last_position_ship = x_ship

def ship_functions(keys):
    move_ship(keys)

def move_ship(keys):
    global shipRect
    global x_ship
    global last_position_ship

    if keys[pygame.K_LEFT] and  shipRect.x > 0:
        shipRect = shipRect.move(-speed_ship, 0)
        x_ship -= speed_ship

    if keys[pygame.K_RIGHT] and shipRect.x < 555:
        shipRect = shipRect.move(speed_ship, 0)
        x_ship += speed_ship

    update_thred = threading.Thread(target=update_database)
    update_thred.start()

def fire_bullet():
    global last_shot_time
    global shotRect

    current_time = pygame.time.get_ticks()

    if current_time - last_shot_time >= 500:
        new_bullet = shot.get_rect(midtop=(x_ship + 43, y_ship - 30))
        bullets.append(new_bullet)

        last_shot_time = current_time

        background_sound.stop()
        shot_sound.play()
        background_sound.play()

def generade_random_position():
    x_asteroid = random.randint(int(0 + asteroid.get_width() / 2), int(555 -  asteroid.get_width() / 2))

    return x_asteroid

def generate_asteroids():
    global last_asteroid_time
    current_time = pygame.time.get_ticks()

    if current_time - last_asteroid_time >= 500:
        if len(asteroids) < 3:
            x_asterod = generade_random_position()

            new_asteroid = asteroid.get_rect(midtop=(x_asterod, -30))
            asteroids.append(new_asteroid)
            
            last_asteroid_time = current_time

def check_collisions_between_bullets_asteroids():
    global bullets
    global asteroids
    global score
    global internal_score

    # Iterating over each bullet and asteroid to check for collision
    for bullet in bullets:
        for asteroid in asteroids:
            if bullet.colliderect(asteroid):
                bullets.remove(bullet)
                asteroids.remove(asteroid)
                score += 1
                internal_score += 1
                break

def game_over():
    global playing
    global screen
    global score
    global internal_score

    screen.blit(game_over_text, game_over_text_rect)

    shot_sound.stop()
    background_sound.stop()
    game_over_sound.play()

    score = 0
    internal_score = 0

    pygame.display.flip()
    pygame.time.delay(3000)
    playing = False

def check_collisions_between_asteroids_ship():
    global asteroids

    for rock in asteroids:
        if  shipRect.colliderect(rock):
            background_sound.stop()

            game_over()

def increment_speed():
    global speed_asteroid
    global score
    global internal_score

    if score % 5 == 0 and score > 0 and internal_score == 5:
        speed_asteroid += 1
        internal_score = 0

def draw_collision_rectangles():
    global screen
    global shipRect
    global bullets
    global asteroids

    # Dibujar rectángulo alrededor de la nave
    pygame.draw.rect(screen, (255, 0, 0), shipRect, 2)

    # Dibujar rectángulos alrededor de las balas
    for bullet in bullets:
        pygame.draw.rect(screen, (0, 255, 0), bullet, 2)

    # Dibujar rectángulos alrededor de los asteroides
    for asteroid in asteroids:
        pygame.draw.rect(screen, (0, 0, 255), asteroid, 2)

def draw_player_2():
    global screen

    player2 = ref_player_2.get()
    isActive = player2['-NtXK3NuN1Ly55ArPwUi']['active']
    
    if (isActive):
        screen.blits(ship_2, shipRect_2)

def move_player_2():

    print("me muevo")
# selected_player()
# loading_screen()

while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
    keys = pygame.key.get_pressed()

    background_sound.play()

    # Exit game when press the ESC key
    if keys[pygame.K_ESCAPE]:
        playing = False

    if keys[pygame.K_SPACE]:
        fire_bullet()

    ship_functions(keys)
    generate_asteroids()

    draw_player_2()

    for rock in asteroids:
        rock.move_ip(0, +speed_asteroid)

    asteroids = [rock for rock in asteroids if rock.y < 500]

    for bullet in bullets:
        bullet.move_ip(0, -speed_shot)

    bullets = [bullet for bullet in bullets if bullet.y > 0]

    check_collisions_between_bullets_asteroids()
    check_collisions_between_asteroids_ship()

    screen.blit(background, (0,0))
    screen.blit(ship, shipRect)

    for asteroidRec in asteroids:
        screen.blit(asteroid, asteroidRec)
        
    # Draw each  bullet in the list of active bullets
    for bullet in bullets:
        screen.blit(shot, bullet)
    
    draw_collision_rectangles()

     # Render score text
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # Render score text
    screen.blit(score_text, (10, 10))  # Blit score text on screen

    # Increment velocity asteroids
    increment_speed()

    # Show changes in the display
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()

# Resetear a CERO

if key == 1:
    ref_ship_player_1.update({'active': False})

if key == 2:
    ref_ship_player_2.update({'active': False})