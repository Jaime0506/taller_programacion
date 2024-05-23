from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

import json

with open('data/player.json', 'r') as f:
    data = json.load(f)

player_x = data['position_player']['x']
player_y = data['position_player']['y']
player_z = data['position_player']['z']

app = Ursina()

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

player=FirstPersonController(position=(player_x, player_y, player_z))

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
    [5, 1, 1, 1, 1, 1, 1, 1, 5, 2, 2, 2, 2, 2, 2, 2, 2, 5, 3, 3, 3, 3, 3, 3, 3, 6 ],
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
    largoHabitacion=len(nivel_suelo)
    anchoHabitacion=len(nivel_suelo[0])
    xInicio=anchoHabitacion/2
    # Crear un espacio, como una sala
    for z in range(largoHabitacion):

        piso = nivel_suelo[z]
        for x in range (anchoHabitacion):
            # Crea suelo
            if piso[x] == 1:
                cajax= Caja3D(position=(x,piso[x],z),escala= (1, 1))
            # valida si hay techo
            if piso[x] > 1:
                cajax= Caja3D(position=(x,piso[x],z),escala= (1, piso[x]))
            
def exit_game():
    player.enabled = False
    for e in scene.entities:
        if isinstance(e, Button):  # O desactiva otros elementos según sea necesario
            e.enabled = False

    save_game = Text(
        text='Guardando progreso...',
        scale=3,
        position=(0,0),
        origin=(0,0),
        color=color.red
    )

    nueva_posicion = {
        'position_player': {
            'x': player.position.x,
            'y': player.position.y,
            'z': player.position.z
        }
    }

    with open('data/player.json', 'w') as f:
        json.dump(nueva_posicion, f)
    
    # Salir del juego
    invoke(application.quit, delay=1) 

def input(key):
    if key == 'escape':
        exit_game()


crear_niveles(nivel)
arm = Hand()

app.run()