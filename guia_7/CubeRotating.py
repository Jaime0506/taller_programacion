import turtle
import math

turtle.speed(0)
turtle.penup()

turtle.goto(0,0)

c1 = None
c2 = None

def drawLine(x1, y1, x2, y2):
    turtle.goto(x1, y1)  
    turtle.pendown()
    turtle.goto(x2, y2)
    turtle.penup()

    last_position = [x2, y2]

    return last_position
def Face():
    global c1

    drawLine(c1[0][0], c1[0][1], c1[1][0], c1[1][1])
    drawLine(c1[1][0], c1[1][1], c1[2][0], c1[2][1])
    drawLine(c1[2][0], c1[2][1], c1[3][0], c1[3][1])
    drawLine(c1[3][0], c1[3][1], c1[0][0], c1[0][1])

def Face_2():

    global c2

    drawLine(c2[0][0], c2[0][1], c2[1][0], c2[1][1])
    drawLine(c2[1][0], c2[1][1], c2[2][0], c2[2][1])
    drawLine(c2[2][0], c2[2][1], c2[3][0], c2[3][1])
    drawLine(c2[3][0], c2[3][1], c2[0][0], c2[0][1])

def Vertex_face_1(x, y, t):
    global c1
    c1 = [
        # X              y
        [x + t/2, y + t/2],
        [x + t/2, y - t/2],
        [x - t/2, y - t/2],
        [x - t/2, y + t/2],
    ]

def Vertex_face_2(x, y, t):
    global c2
    c2 = [
        # X              y
        [x + t/2, y + t/2],
        [x + t/2, y - t/2],
        [x - t/2, y - t/2],
        [x - t/2, y + t/2],
    ]

def Vertex_floor(x, y, t):
    global c1
    c1 = [
        # X              y
        [x - t/2, y + t/2],
        [x + t/2, y - t/2],
        [x - t/2, y - t/2],
        [x - t/2, y + t/2],
    ]


def Face_top_floor():
    global c1
    global c2

    for i in range (0, 4):
        drawLine(c1[i][0], c1[i][1], c2[i][0], c2[i][1])

def Rotate(Cx, Cy, angulo, c):

    for rows in range(4):
        
        x_relative = c[rows][0] - Cx
        y_relative = c[rows][1] - Cy

        x_new = x_relative * math.cos(angulo) - y_relative * math.sin(angulo) + Cx
        y_new = x_relative * math.sin(angulo) + y_relative * math.cos(angulo) + Cy

        c[rows] = [x_new, y_new]

start_angule = 1

def drawCircle(i):
    global start_angule

    if (i % 5) == 0:
        start_angule += 1

    Rotate(x, y, start_angule, c1)
    Face()

    Rotate(x + t/2, y + t/2, start_angule, c2)
    Face_2()

    Face_top_floor()

x, y, t = 0, 0, 200

Vertex_face_1(x, y, t)
Vertex_face_2(x + t/2, y + t/2, t)

print(c1)
print(c2)

start_angule = 1

def move(slope_x = 1, slope_y = 0):
    global x
    global y

    if (slope_x == 1):
        x = x + 10

    if (slope_x == -1):
        x = x - 10

    if (slope_y == 1):
        y = y + 10

    if (slope_y == -1):
        y = y - 10

screen = turtle.Screen()
width =  screen.window_width()
heigth = screen.window_height()

direction  = 1
flag = True

for i in range(1, 100):
    drawCircle(i)

    if (x >= 140 and flag):
        direction = -1
        flag = False

    if (x <= -200 and not flag):
        direction = 1
        flag = True
    
    move(direction)

turtle.done()