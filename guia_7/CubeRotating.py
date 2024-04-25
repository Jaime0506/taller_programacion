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

def Face_2(x, y, t):

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

def rotate(Cx, Cy, angulo, n_coord):

    x_new = (c1[n_coord][0] - Cx) * math.cos(angulo) - (c1[n_coord][1]) * math.sin(angulo) + Cx
    y_new = (c1[n_coord][0] - Cx) * math.sin(angulo) + (c1[n_coord][1] - Cy) * math.cos(angulo) + Cy

    turtle.goto(x_new, y_new)
    turtle.pendown()
    

    return x_new, y_new

x, y, t = 0, 0, 200

# Cara 1
Vertex_face_1(x, y, t)
Face()

# Cara 2
# x = x + t/2
# y = y + t/2

# Vertex_face_2(x, y, t)
# Face_2(x, y, 200)

# Face_top_floor()

[x_new, y_new] = rotate(0, 0, 45, 0)
[x_new, y_new] = rotate(0, 0, 45, 1)
[x_new, y_new] = rotate(0, 0, 45, 2)
[x_new, y_new] = rotate(0, 0, 45, 3)
[x_new, y_new] = rotate(0, 0, 45, 0)

turtle.penup()

[x_new, y_new] = rotate(0, 0, 90, 0)
[x_new, y_new] = rotate(0, 0, 90, 1)
[x_new, y_new] = rotate(0, 0, 90, 2)
[x_new, y_new] = rotate(0, 0, 90, 3)
[x_new, y_new] = rotate(0, 0, 90, 0)


# [x_new, y_new] = rotate(0, 0, 45, 1)
# drawLine(x_new, y_new, x_new + t, y_new - t/2)
# Vertex_face_1(x_new, y_new, t)
# Face()

turtle.done()