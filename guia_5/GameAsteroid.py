import pygame
import os
import random
import threading
import firebase_admin
from firebase_admin import credentials, db, exceptions

# Connection to firebase
key_path = os.path.join(os.path.dirname(__file__), 'firebase')
key = os.path.join(key_path, 'space-shooter-9c882-firebase-adminsdk-tndg0-ca7618fd2e.json')

cred = credentials.Certificate(key)
firebase_admin.initialize_app(cred, {'databaseURL': 'https://space-shooter-9c882-default-rtdb.firebaseio.com/'})
try:
    player1 = db.reference('/player_1')
    ref_ship_player1 = player1.child('-Nsz_waZceu5sMSuXRXq')
    player2 = db.reference('/player_2')
    ref_ship_player2 = player2.child('-NtXK3NuN1Ly55ArPwUi')
except exceptions.FirebaseError as firebase_error:
    print(f"Se peto esta mrda: {firebase_error}")

# Acces path to assets
assest_path = os.path.join(os.path.dirname(__file__), 'assets')

background_path = os.path.join(assest_path, 'background.jpg')

ship_path_player1 = os.path.join(assest_path, 'player_1.png')
shot_path_player1 = os.path.join(assest_path, 'shot.png')

ship_path_player2 = os.path.join(assest_path, 'player_2.png')
shot_path_player2 = os.path.join(assest_path, 'shot.png')

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
ship_player1 = pygame.image.load(ship_path_player1)
ship_player2 = pygame.image.load(ship_path_player2)

shot_player1 = pygame.image.load(shot_path_player1)
shot_player2 = pygame.image.load(shot_path_player2)

background = pygame.image.load(background_path).convert()
asteroid = pygame.image.load(asteroid_path)

game_over_text = pygame.image.load(game_over_text_path).convert()

#  Load assets sounds
shot_sound = pygame.mixer.Sound(shot_sound_path)
background_sound = pygame.mixer.Sound(background_sound_path)
game_over_sound = pygame.mixer.Sound(game_over_sound_path)

# Resize assets
background = pygame.transform.scale(background, (width, height))

ship_player1 = pygame.transform.scale(ship_player1, (ship_player1.get_width() // 4, ship_player1.get_height() // 4))
ship_player2 = pygame.transform.scale(ship_player2, (ship_player2.get_width() // 4, ship_player2.get_height() // 4))

shot_player1 = pygame.transform.scale(shot_player1, (shot_player1.get_width() // 12, shot_player1.get_height() // 12))
shot_player2 = pygame.transform.scale(shot_player1, (shot_player1.get_width() // 12, shot_player1.get_height() // 12))

asteroid = pygame.transform.scale(asteroid, (asteroid.get_width() // 2.5, asteroid.get_height() // 2.5))
game_over_text = pygame.transform.scale(game_over_text, (width, height))

#  Initial position ship
ship_react_player1 = ship_player1.get_rect()
x_ship_player1, y_ship_player1 = 450, height - 100

ship_react_player2 = ship_player2.get_rect()
x_ship_player2, y_ship_player2 = 200, height - 100

ship_react_player1.move_ip(x_ship_player1, y_ship_player1)
ship_react_player2.move_ip(x_ship_player2, y_ship_player2)

# Shot
shot_rect_player1 = shot_player1.get_rect()
x_shot_player1, y_shot_player1 = x_ship_player1 + 18, y_ship_player1 - 30

shot_rect_player2 = shot_player2.get_rect()
x_shot_player2, y_shot_player2 = x_ship_player2 + 18, y_ship_player2 - 30

shot_rect_player1.move_ip(x_shot_player1, y_shot_player1)
shot_rect_player2.move_ip(x_shot_player2, y_shot_player2)

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
# last_position_ship = x_ship_player1

# player2.push({'x_ship': x_ship_player1})
key = 0

global player
global ship_player 
global ship_react_player 
global x_ship_player
global y_ship_player

global x_shot_player

global last_position_ship
global shot_player

global ref_ship_player


def selectPlayer():
    global key
    value1 = player1.get()
    value2 = player2.get()

    active_player1 = value1['-Nsz_waZceu5sMSuXRXq']['active']
    active_player2 = value2['-NtXK3NuN1Ly55ArPwUi']['active']

    if active_player1 and active_player2:
        key = random.randint(1, 2)
        if key == 1:
            ref_ship_player1.update({'active': True})
            print('You are player 1')
        else:
            ref_ship_player2.update({'active': True})
            print('You are player 2')
    elif active_player1:
        key = 1
        ref_ship_player1.update({'active': True})
        print('You are player 1')
    elif active_player2:
        key = 2
        ref_ship_player2.update({'active': True})
        print('You are player 2')
    else:
        print("No active players found.")

selectPlayer()
if key == 1:
    player = player1
    ship_player = ship_player1
    ship_react_player = ship_react_player1
    x_ship_player = x_ship_player1
    y_ship_player = y_ship_player1
    x_shot_player = x_shot_player1
    last_position_ship = x_ship_player
    shot_player = shot_player1
    ref_ship_player = ref_ship_player1
elif key == 2:
    player = player2
    ship_player = ship_player2
    ship_react_player = ship_react_player2
    x_ship_player = x_ship_player2
    y_ship_player = y_ship_player2
    x_shot_player = x_shot_player2
    last_position_ship = x_ship_player
    shot_player = shot_player2
    ref_ship_player = ref_ship_player2

print(ship_react_player)

def update_database():
    global x_ship_player
    global last_position_ship

    with threading.Lock():
        if last_position_ship != x_ship_player:
            ref_ship_player.update({'x_ship': x_ship_player})
            last_position_ship = x_ship_player

#listen changes in firebase
def listen_player_online():
    global x_ship_player1, y_ship_player1, x_ship_player2, y_ship_player2

    def callback(event):
        data = event.data
        if data is not None:
            if key == 1:
                x_ship_player2 = data.get('x_ship', x_ship_player)
                y_ship_player2 = data.get('y_ship', y_ship_player)  # Se actualiza y_ship_player2
            elif key == 2:
                x_ship_player1 = data.get('x_ship', x_ship_player)
                y_ship_player1 = data.get('y_ship', y_ship_player)  # Se actualiza y_ship_player1

    player_ref1 = player1.child('-Nsz_waZceu5sMSuXRXq')
    player_ref2 = player2.child('-NtXK3NuN1Ly55ArPwUi')
    player_ref1.listen(callback)
    player_ref2.listen(callback)

#New Thread
threading.Thread(target=listen_player_online).start()



def move_ship(keys):
    global ship_react_player, x_ship_player, x_ship_player1, x_ship_player2, last_position_ship, ship_player1, ship_player
    
    if keys[pygame.K_LEFT] and ship_react_player.x > 0:
        ship_react_player = ship_react_player.move(-speed_ship, 0)
        if key == 1:
            x_ship_player1 -= speed_ship
            x_ship_player = x_ship_player1
           
           
        elif key == 2:
            x_ship_player2 -= speed_ship
            x_ship_player = x_ship_player2
            
            

    if keys[pygame.K_RIGHT] and ship_react_player.x < 555:
        ship_react_player = ship_react_player.move(speed_ship, 0)
        if key == 1:
            x_ship_player1 += speed_ship
            x_ship_player = x_ship_player1
            
            
        elif key == 2:
            x_ship_player2 += speed_ship
            x_ship_player = x_ship_player2
            
            
    last_position_ship = x_ship_player
    update_database()
    screen.blit(background, (0,0))
    screen.blit(ship_player, ship_react_player)
    screen.blit(ship_player, ship_react_player)
    #update thread
    update_thread = threading.Thread(target=update_database)
    update_thread.start()

def fire_bullet():
    global last_shot_time
    #aqui borre el global shot_rect_player
    current_time = pygame.time.get_ticks()

    if current_time - last_shot_time >= 500:
        new_bullet = shot_player.get_rect(midtop=(x_ship_player + 43, y_ship_player - 30))
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
        if  ship_react_player.colliderect(rock):
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
    global ship_react_player1, ship_react_player2
    global bullets
    global asteroids

    # Dibujar rectángulo alrededor de la nave
    pygame.draw.rect(screen, (255, 0, 0), ship_react_player1, 2)
    pygame.draw.rect(screen, (255,0,0),ship_react_player2,2)

    # Dibujar rectángulos alrededor de las balas
    for bullet in bullets:
        pygame.draw.rect(screen, (0, 255, 0), bullet, 2)

    # Dibujar rectángulos alrededor de los asteroides
    for asteroid in asteroids:
        pygame.draw.rect(screen, (0, 0, 255), asteroid, 2)

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

    move_ship(keys)#move players
    generate_asteroids()

    for rock in asteroids:
        rock.move_ip(0, +speed_asteroid)

    asteroids = [rock for rock in asteroids if rock.y < 500]

    for bullet in bullets:
        bullet.move_ip(0, -speed_shot)

    bullets = [bullet for bullet in bullets if bullet.y > 0]

    check_collisions_between_bullets_asteroids()
    check_collisions_between_asteroids_ship()

    # ###aqui estaba el dibujado de la nave
    # screen.blit(background, (0,0))
    # screen.blit(ship_player1, ship_react_player1)
    # screen.blit(ship_player2, ship_react_player2)
    
    for asteroidRec in asteroids:
        screen.blit(asteroid, asteroidRec)
        
    # Draw each  bullet in the list of active bullets
    for bullet in bullets:
        screen.blit(shot_player, bullet)
    
    draw_collision_rectangles()

     # Render score text
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # Render score text
    screen.blit(score_text, (10, 10))  # Blit score text on screen

    # Increment velocity asteroids
    increment_speed()

    # Show changes in the display
    pygame.display.flip()
    pygame.time.Clock().tick(60)

    update_database()

pygame.quit()