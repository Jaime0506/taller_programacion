import pygame
import os
import time

# Define path of assets 
assets_dir = os.path.join(os.path.dirname(__file__), 'assets')

paddle_path = os.path.join(assets_dir, 'paddle.png')
ball_path = os.path.join(assets_dir, 'ball.png')
brick_path = os.path.join(assets_dir, 'brick.png')

# Init pygame
pygame.init()

# Window options
height = 640
width = 480

# Background color
windows_fill = (59, 55, 55)

# Create window
window = pygame.display.set_mode((height, width))
pygame.display.set_caption("Tennis")

# Load assets
ball = pygame.image.load(ball_path)
paddle = pygame.image.load(paddle_path)
brick = pygame.image.load(brick_path)

# Resize assets
resize_const_paddle = 4
resize_const_ball = 14
resize_const_brick = 2.5

ball = pygame.transform.scale(ball, (ball.get_width() // resize_const_ball, ball.get_height() // resize_const_ball))
paddle = pygame.transform.scale(paddle, (paddle.get_width() // resize_const_paddle, paddle.get_height() // resize_const_paddle))
brick = pygame.transform.scale(brick, (brick.get_width() // resize_const_brick, brick.get_height() // resize_const_brick))

# Initial position of the ball
ballRect = ball.get_rect()
initial_ball_position = (width // 2 + 100, 250)
ballRect.move_ip(initial_ball_position)

# Initial position of the paddle
paddleRect = paddle.get_rect()
initial_paddle_position = (width // 2 + 30, 380)
paddleRect.move_ip(initial_paddle_position)

# Initial position of the brick
brickRect = brick.get_rect()
initial_brick_position = (width // 2 + 30, 30)
brickRect.move_ip(initial_brick_position)

# Define hitboxes for each item
ball_hitbox = ballRect.inflate(-20, -20)  # Reduce the hitbox size for better collision detection
paddle_hitbox = paddleRect.inflate(-40, -50)
brick_hitbox = brickRect.inflate(-50, -92)

# Fuente y tamaño del texto
font = pygame.font.Font(None, 36)

# Game config
speed = [4, 4]
puntos = 0
incremento_velocidad = 1

def show_points():
    puntaje_texto = font.render(f"Puntaje: {puntos}", True, (0, 0, 0))
    window.blit(puntaje_texto, (10, 10))

def game_over():
    mensaje_texto = font.render("¡Perdiste!", True, (255, 0, 0))
    window.blit(mensaje_texto, (window.get_width() // 2 - 100, window.get_height() // 2))
    pygame.display.update()  # Forzar una actualización inmediata de la pantalla
    time.sleep(2)

jugando = True

while jugando:
    
    # Si el puntaje es múltiplo de 5, aumenta la velocidad
    if puntos % 5 == 0 and puntos != 0:
        speed[0] += incremento_velocidad
        speed[1] += incremento_velocidad

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        paddleRect = paddleRect.move(-5, 0)
        paddle_hitbox = paddleRect.inflate(-40, -50)  # Actualizar la hitbox con la nueva posición
        # Limitar el movimiento hacia la izquierda
        if paddleRect.left < 0:
            paddleRect.left = 0
            paddle_hitbox.left = 0

    if keys[pygame.K_RIGHT]:
        paddleRect = paddleRect.move(5, 0)
        paddle_hitbox = paddleRect.inflate(-40, -50)  # Actualizar la hitbox con la nueva posición
        # Limitar el movimiento hacia la derecha
        if paddleRect.right > window.get_width():
            paddleRect.right = window.get_width()
            paddle_hitbox.right = window.get_width()

    ballRect = ballRect.move(speed)
    ball_hitbox = ballRect.inflate(-20, -20)  # Actualizar la hitbox con la nueva posición
     
    # Restricciones de rebote en los lados de la ventana
    if ballRect.left < 0 or ballRect.right > window.get_width():
        speed[0] = -speed[0]

    # Restricción de rebote en la parte superior de la ventana
    if ballRect.top < 0:
        speed[1] = -speed[1]

    # Restricción de rebote en la parte inferior de la ventana
    if ballRect.bottom > window.get_height():
        ballRect.topleft = initial_ball_position
        puntos = 0
        speed = [4,4]
        game_over()

    # Verificar colisión con la raqueta
    if paddle_hitbox.colliderect(ball_hitbox):
        speed[1] = -speed[1]
        puntos += 1

    # Verificar colisión con el ladrillo
    if brick_hitbox.colliderect(ball_hitbox):
        # Obtener las coordenadas de los bordes de la pelota y el ladrillo
        ball_left, ball_top, ball_right, ball_bottom = ball_hitbox.left, ball_hitbox.top, ball_hitbox.right, ball_hitbox.bottom
        brick_left, brick_top, brick_right, brick_bottom = brick_hitbox.left, brick_hitbox.top, brick_hitbox.right, brick_hitbox.bottom

        # Determinar qué lados de la pelota y el ladrillo están en contacto
        if ball_bottom > brick_top and ball_top < brick_bottom:
            print("Colisión desde arriba o abajo")
        elif ball_right > brick_left and ball_left < brick_right:
            print("Colisión desde la izquierda o derecha")
            print("COliciono")

        speed[1] = -speed[1]
        puntos += 1 

    window.fill(windows_fill)
    show_points()  

    window.blit(ball, ballRect)
    window.blit(paddle, paddleRect)
    window.blit(brick, brickRect)

    # Dibujar hitboxes
    pygame.draw.rect(window, (255, 0, 0), ball_hitbox, 2)
    pygame.draw.rect(window, (255, 0, 0), paddle_hitbox, 2)
    pygame.draw.rect(window, (255, 0, 0), brick_hitbox, 2)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
