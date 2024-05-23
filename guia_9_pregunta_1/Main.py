from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# Controlador de tiempo para el laberinto
time_game_duration = 20
start_time = time.time()

# Texto que se muestra en el juego
timer_text = Text(text='00:00', scale=2, position=(0, 0.45), origin=(0,0))

start_game_text = Text(text='Encuentra el bloque verde o perderas', scale=2, position=(0, 0), origin=(0,0))

# Texto de Game over y Mision cumplida
quest_complete_text = None
game_over_text = None

player=FirstPersonController(position=(1, 10, 10))

# Bloque donde gane el jugador
green_block = None

class Caja3D(Button):
    sprite_index="wall.png"

    def __init__(self, position=(0,0,0), escala=(1,1,1)):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            collider='box',
            texture=self.sprite_index,
            color=color.gray,
            scale=escala,
            highlight_color=color.lime)

class Hand(Entity):
    xInicio=0 # Posición del arma en el eje X
    yInicio=-0.4 # Posición del arma en el eje Y
    image_speed=0.4
    image_index=0 # Imagen fija
    textura_mano="arm.png"
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='cube',
            texture=self.textura_mano,
            scale=0.4,
            color=color.white,
            rotation=Vec3(0,0,0), # girar el arma
            position=Vec2(self.xInicio,self.yInicio)
        )

# 1 Piso
# 5 Pared
# 2 Escalera
nivel = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 3, 3, 3, 3, 6, 0, 7, 7, 7, 7, 7, 0, 0, 0, 0 ],
    [0, 0, 0, 5, 5, 5, 5, 5, 0, 0, 6, 3, 3, 3, 3, 6, 0, 7, 4, 4, 4, 7, 0, 0, 0, 0 ],
    [0, 0, 0, 5, 2, 2, 2, 5, 5, 5, 6, 3, 3, 3, 3, 6, 0, 7, 4, 4, 4, 7, 0, 0, 0, 0 ],
    [0, 0, 0, 5, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 6, 5, 7, 4, 4, 4, 7, 1, 1, 1, 1 ],
    [0, 0, 0, 5, 2, 2, 2, 5, 5, 5, 6, 3, 3, 3, 3, 6, 2, 7, 4, 4, 4, 7, 1, 1, 1, 1 ],
    [0, 5, 5, 5, 2, 2, 2, 5, 5, 5, 5, 5, 3, 3, 5, 5, 5, 5, 7, 4, 7, 6, 6, 6, 6, 6 ],
    [5, 1, 1, 1, 1, 1, 1, 1, 5, 2, 2, 2, 2, 2, 2, 2, 2, 5, 3, 3, 3, 3, 3, 3, -1, 6 ],
    [5, 1, 1, 1, 1, 1, 1, 1, 5, 2, 2, 2, 2, 2, 2, 2, 2, 5, 3, 3, 3, 3, 3, 3, 3, 6 ],
    [5, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 6 ],
    [5, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 6 ],
    [5, 1, 1, 1, 1, 1, 1, 1, 5, 2, 2, 2, 2, 2, 2, 2, 2, 5, 3, 3, 3, 3, 3, 3, 3, 6 ],
    [5, 1, 1, 1, 1, 1, 1, 1, 5, 2, 2, 2, 2, 2, 2, 2, 2, 5, 3, 3, 3, 3, 3, 3, 3, 6 ],
    [0, 5, 5, 5, 2, 2, 2, 5, 5, 5, 5, 5, 2, 2, 5, 5, 5, 6, 6, 3, 6, 6, 6, 6, 6, 6 ],
    [0, 0, 0, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 6, 1, 1, 1, 1 ],
    [0, 0, 0, 5, 2, 2, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 3, 3, 3, 6, 1, 1, 1, 1 ],
    [0, 0, 0, 5, 2, 2, 2, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 3, 3, 3, 6, 0, 0, 0, 0 ],
    [0, 0, 0, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 3, 3, 3, 6, 0, 0, 0, 0 ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 0, 0, 0, 0 ],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
]

def crear_niveles(nivel_suelo):
    global green_block

    largoHabitacion=len(nivel_suelo)
    anchoHabitacion=len(nivel_suelo[0])
    xInicio=anchoHabitacion/2
    # Crear un espacio, como una sala
    for z in range(largoHabitacion):

        piso = nivel_suelo[z]
        for x in range (anchoHabitacion):
            # Crea suelo
            if piso[x] == -1:
                green_block= Entity(model='cube', position=(x, piso[x] + 3.5, z), escala= (1, 1), color=color.green, collider='box')

            if piso[x] == 1:
                cajax= Caja3D(position=(x,piso[x],z),escala= (1, 1))
            # valida si hay techo
            if piso[x] > 1:
                cajax= Caja3D(position=(x,piso[x],z),escala= (1, piso[x]))
            
def exit_game():
    invoke(application.quit, delay=2)

def game_over():
    global game_over_text

    if not game_over_text:
        game_over_text = Text(text='GAME OVER', scale=3, position=(0,0), origin=(0,0), color=color.red)
        exit_game()

def update():
    global game_over_text, quest_complete_text

    # Calcular el tiempo que lleva de juego
    elapsed_time = time.time() - start_time
    remaining_time = time_game_duration - elapsed_time

    # Detectar si estan en el mismo lugar
    if green_block.position.x - 0.5 < player.position.x < green_block.position.x + 0.5 and green_block.position.z - 0.5 < player.position.z < green_block.position.z + 0.5:
        if not quest_complete_text:
            quest_complete_text = Text(
                text='Mision cumplida',
                scale=4,
                position=(0,0),
                origin=(0,0),
                color=color.green
            )

            green_block.color = color.black

            exit_game()

    else:
        if (elapsed_time > 2):
            start_game_text.text = ""

        if (remaining_time <= 0 and quest_complete_text == None):
            game_over()
        else:
            # Transformar el tiempo a minutos y segundos para mostrat en pantalla
            minutes, seconds = divmod(int(remaining_time), 60)
            timer_text.text=f'{minutes:02}:{seconds:02}'

    # print(f'Posicion del controlador: {player.position}')
    # print(f'Posicion de caja: {green_block.position}')

crear_niveles(nivel)
arm = Hand()

app.run()