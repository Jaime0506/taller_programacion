import pygame, sys, random, threading,os,firebase_admin, os
from firebase_admin import db, exceptions,credentials

# Inicialización de Firebase para el jugador 1
key_path = os.path.join(os.path.dirname(__file__), 'firebase')
key = os.path.join(key_path, 'space-shooter-9c882-firebase-adminsdk-tndg0-ca7618fd2e.json')
firebase_sdk = credentials.Certificate(key)
firebase_admin.initialize_app(firebase_sdk, {'databaseURL': 'https://space-shooter-9c882-default-rtdb.firebaseio.com/'})
try:
    player1 = db.reference('/player_1')
    ref_ship_player1 = player1.child('-Nsz_waZceu5sMSuXRXq')

    player2 = db.reference('/player_2')
    ref_ship_player2 = player2.child('-NtXK3NuN1Ly55ArPwUi')

except exceptions.FirebaseError as firebase_error:
    print(f"Se peto esta mrda: {firebase_error}")

# Inicialización de Pygame
pygame.init()
mi_jugador = 0
# Configuración de la ventana del juego
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Asteroides")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
font = pygame.font.Font(None, 36)
# Carga de imágenes
assest_path = os.path.join(os.path.dirname(__file__), 'assets')
avion_path = os.path.join(assest_path, 'player_1.png')  # Cambia "avion.png" por la ruta de la imagen del avión del jugador 1
avion_img = pygame.image.load(avion_path)
avion_img = pygame.transform.scale(avion_img, (60, 60))
roca_path = os.path.join(assest_path, 'asteroid.png')
roca_img = pygame.image.load(roca_path)
roca_img = pygame.transform.scale(roca_img, (50, 50))
bala_img = pygame.Surface((4, 10))
bala_img.fill(NEGRO)
fondo_path = os.path.join(assest_path, 'background.jpg')
fondo_img = pygame.image.load(fondo_path)
fondo_img = pygame.transform.scale(fondo_img, (ANCHO, ALTO))


class Puntuacion:
    def __init__(self):
        self.puntos = 0

    def aumentar_puntuacion(self):
        self.puntos += 1

    def reiniciar_puntuacion(self):
        self.puntos = 0


class Avion(pygame.sprite.Sprite):
    def __init__(self, jugador_id, pos_x, pos_y):
        super().__init__()
        self.jugador_id = jugador_id
        self.image = avion_img
        self.rect = self.image.get_rect()
        self.rect.centerx = pos_x
        self.rect.centery = pos_y
        self.speed = 5

        # Definir las coordenadas de destino
        self.target_x = pos_x
        self.target_y = pos_y

    def update(self):
        # Mover hacia las coordenadas de destino
        if self.rect.centerx < self.target_x:
            self.rect.centerx += min(self.speed, self.target_x - self.rect.centerx)
        elif self.rect.centerx > self.target_x:
            self.rect.centerx -= min(self.speed, self.rect.centerx - self.target_x)
        if self.rect.centery < self.target_y:
            self.rect.centery += min(self.speed, self.target_y - self.rect.centery)
        elif self.rect.centery > self.target_y:
            self.rect.centery -= min(self.speed, self.rect.centery - self.target_y)

        # Asegurar que el avión no se salga de la pantalla
        self.rect.centerx = max(self.rect.centerx, 0)
        self.rect.centerx = min(self.rect.centerx, ANCHO)
        self.rect.centery = max(self.rect.centery, 0)
        self.rect.centery = min(self.rect.centery, ALTO)


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, rocas_sprites, puntuacion):
        super().__init__()
        self.image = bala_img
        self.rect = self.image.get_rect()
        self.rect.centerx = pos_x
        self.rect.centery = pos_y
        self.speed = 10
        self.rocas_sprites = rocas_sprites
        self.puntuacion = puntuacion

    def update(self):
        self.rect.centery -= self.speed
        if self.rect.bottom < 0:
            self.kill()

        # Verificar colisiones con las rocas
        colisiones = pygame.sprite.spritecollide(self, self.rocas_sprites, True)
        for roca in colisiones:
            self.puntuacion.aumentar_puntuacion()
            self.kill()


class Roca(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = roca_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1,8)  # Reducir la velocidad vertical máxima
        self.speedx = random.randrange(-3,3)  # Reducir la velocidad horizontal máxima

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > ALTO + 10 or self.rect.left < -25 or self.rect.right > ANCHO + 20:
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1,8)  # Reducir la velocidad vertical máxima
            # self.speedx = 1  # Reducir la velocidad horizontal máxima


# Función para manejar eventos de teclado para el jugador 1
def manejar_eventos_teclado_jugador1(avion_local, todos_sprites, rocas_sprites, puntuacion):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    keys = pygame.key.get_pressed()

    # Actualizar las coordenadas del avión local según las entradas del teclado
    if keys[pygame.K_LEFT]:  # Tecla de flecha izquierda
        avion_local.target_x -= avion_local.speed
    if keys[pygame.K_RIGHT]:  # Tecla de flecha derecha
        avion_local.target_x += avion_local.speed
    if keys[pygame.K_UP]:  # Tecla de flecha arriba
        avion_local.target_y -= avion_local.speed
    if keys[pygame.K_DOWN]:  # Tecla de flecha abajo
        avion_local.target_y += avion_local.speed
    if keys[pygame.K_SPACE]:  # Tecla de espacio para disparar láser
        laser = Laser(avion_local.rect.centerx, avion_local.rect.centery, rocas_sprites, puntuacion)
        todos_sprites.add(laser)

    # Establecer límites para las coordenadas target
    avion_local.target_x = min(max(avion_local.target_x, 0), ANCHO)
    avion_local.target_y = min(max(avion_local.target_y, 0), ALTO)

    # Escribir las coordenadas del avión local en Firebase para el jugador 1
    ref = db.reference('/player_1/-Nsz_waZceu5sMSuXRXq')
    ref.update({
        'x_ship': avion_local.target_x,
        'y_ship': avion_local.target_y

    })

    return True

# Función para manejar eventos de teclado para el jugador 2
def manejar_eventos_teclado_jugador2(avion_remoto, todos_sprites, rocas_sprites, puntuacion):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    keys = pygame.key.get_pressed()

    # Actualizar las coordenadas del avión local según las entradas del teclado
    if keys[pygame.K_a]:  # Tecla de flecha izquierda
        avion_remoto.target_x -= avion_remoto.speed
    if keys[pygame.K_d]:  # Tecla de flecha derecha
        avion_remoto.target_x += avion_remoto.speed
    if keys[pygame.K_w]:  # Tecla de flecha arriba
        avion_remoto.target_y -= avion_remoto.speed
    if keys[pygame.K_s]:  # Tecla de flecha abajo
        avion_remoto.target_y += avion_remoto.speed
    if keys[pygame.K_k]:  # Tecla de espacio para disparar láser
        laser = Laser(avion_remoto.rect.centerx, avion_remoto.rect.centery, rocas_sprites, puntuacion)
        todos_sprites.add(laser)

    # Establecer límites para las coordenadas target
    avion_remoto.target_x = min(max(avion_remoto.target_x, 0), ANCHO)
    avion_remoto.target_y = min(max(avion_remoto.target_y, 0), ALTO)

    # Escribir las coordenadas del avión local en Firebase para el jugador 1
    ref = db.reference('/player_2/-NtXK3NuN1Ly55ArPwUi')
    ref.update({
        'x_ship': avion_remoto.target_x,
        'y_ship': avion_remoto.target_y

    })

    return True


# Función para leer las coordenadas del avión remoto desde Firebase
def leer_coordenadas_jugador2(avion_remoto):
    while True:
        ref = db.reference('/player_2/-NtXK3NuN1Ly55ArPwUi')
        coordenadas_jugador2 = ref.get()
        if coordenadas_jugador2 is not None:
            avion_remoto.target_x = coordenadas_jugador2['x_ship']
            avion_remoto.target_y = coordenadas_jugador2['y_ship']

#Definir pantalla de carga
def loading_screen():
    loading = True
    while loading:
        value1 = player1.get()
        value2 = player2.get()
        player1_selected = value1['-Nsz_waZceu5sMSuXRXq']['active']
        player2_selected = value2['-NtXK3NuN1Ly55ArPwUi']['active']
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        ventana.fill((0,0,0))
        loading_text = font.render("Waiting for players. . .",True,(255,255,255))
        ventana.blit(loading_text, (ANCHO // 2 - loading_text.get_width() // 2, ALTO // 2 - loading_text.get_height() // 2))
        pygame.display.flip()

        if player1_selected and player2_selected:
            loading = False
            print("The players are ready")
#Seleccionar jugador de forma manual
def selectPlayer():
    global mi_jugador
    value1 = player1.get()
    value2 = player2.get()
    player1_selected = value1['-Nsz_waZceu5sMSuXRXq']['active']
    player2_selected = value2['-NtXK3NuN1Ly55ArPwUi']['active']
    selected = False
    
    while not selected:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if not player1_selected:
                        mi_jugador = 1
                        ref_ship_player1.update({'active': True})
                        print('Player 1 selected')
                        selected = True
                    else:
                        print("player 1 already exists")
                if event.key == pygame.K_2:
                    if not player2_selected:
                        mi_jugador = 2
                        ref_ship_player2.update({'active': True})
                        print('Player 2 selected')
                        selected = True
                    else:
                        print("player 2 already exists")
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        # lOADING
        ventana.fill((0, 0, 0))
        selection_text = font.render("Selected Players:", True, (255, 255, 255))
        player1_text = font.render("Press '1' to choose player 1", True, (255, 255, 255))
        player2_text = font.render("Press '2' to choose player 2", True, (255, 255, 255))
        ventana.blit(selection_text, (ANCHO // 2 - selection_text.get_width() // 2, ALTO // 2 - 50))
        ventana.blit(player1_text, (ANCHO // 2 - player1_text.get_width() // 2, ALTO // 2))
        ventana.blit(player2_text, (ANCHO // 2 - player2_text.get_width() // 2, ALTO // 2 + 50))
        pygame.display.flip()
# Función principal del juego
def main():
    # Inicializacion de mi jugador
    selectPlayer()
    loading_screen()
    avion_local = Avion(mi_jugador, ANCHO // 2, ALTO // 2)  # Crear avión local
    avion_remoto = Avion(2 if mi_jugador == 1 else 1, ANCHO // 2, ALTO // 2)  # Crear avión remoto

    todos_sprites = pygame.sprite.Group()  # Grupo para todos los sprites (aviones, láseres, asteroides, etc.)
    rocas_sprites = pygame.sprite.Group()  # Grupo para los asteroides

    puntuacion = Puntuacion()  # Crear objeto de puntuación

    # Generar asteroides
    for _ in range(5):  # Reducir el número de asteroides
        roca = Roca()
        todos_sprites.add(roca)
        rocas_sprites.add(roca)
        pygame.time.wait(200)  # Añadir un pequeño retraso entre la generación de cada asteroide

    # Crear y arrancar el hilo para leer las coordenadas del avión remoto
    hilo_lectura = threading.Thread(target=leer_coordenadas_jugador2, args=(avion_remoto,))
    hilo_lectura.start()

    jugando = True
    while jugando:
        if mi_jugador == 1:
            jugando = manejar_eventos_teclado_jugador1(avion_local, todos_sprites, rocas_sprites, puntuacion)
        elif mi_jugador == 2:
            jugando = manejar_eventos_teclado_jugador2(avion_remoto, todos_sprites, rocas_sprites, puntuacion)

        ventana.fill((0, 0, 0))  # Limpia la ventana antes de redibujar los aviones
        avion_local.update()
        avion_remoto.update()
        todos_sprites.update()  # Actualiza todos los sprites
        rocas_sprites.update()  # Actualiza los asteroides

        # Dibujar todos los sprites en la pantalla
        ventana.blit(fondo_img, (0, 0))  # Dibujar el fondo
        ventana.blit(avion_local.image, avion_local.rect)
        ventana.blit(avion_remoto.image, avion_remoto.rect)
        todos_sprites.draw(ventana)
        rocas_sprites.draw(ventana)

        # Mostrar puntuación en pantalla
        texto_puntuacion = font.render("Puntuación: " + str(puntuacion.puntos), True, BLANCO)
        ventana.blit(texto_puntuacion, (10, 10))

        pygame.display.flip()  # Actualizar la pantalla
    pygame.quit()
ref_ship_player1.update({'active':False})
ref_ship_player2.update({'active':False})
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Se produjo un error en el juego: {e}")
        pygame.quit()