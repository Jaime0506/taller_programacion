import turtle
import math

class Cube3D:
    vertex_front_face = None
    vertex_back_face = None

    x = None
    y = None
    t = None

    x_2 = None
    y_2 = None
    
    width_window = None
    height_window = None

    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.t = t

        self.x_2 = self.x + self.t/2
        self.y_2 = self.y + self.t/2

        self.set_vertex_front_face()
        self.set_vertex_back_face()

        turtle.speed(0)
        turtle.penup()
        turtle.goto(self.x, self.y)

    def set_vertex_front_face(self):
        self.vertex_front_face = [
            # X              y
            [self.x + self.t/2, self.y + self.t/2],
            [self.x + self.t/2, self.y - self.t/2],
            [self.x - self.t/2, self.y - self.t/2],
            [self.x - self.t/2, self.y + self.t/2],
        ]
    
    def set_vertex_back_face(self):
        self.vertex_back_face = [
            # X              y
            [self.x_2 + self.t/2, self.y_2 + self.t/2],
            [self.x_2 + self.t/2, self.y_2 - self.t/2],
            [self.x_2 - self.t/2, self.y_2 - self.t/2],
            [self.x_2 - self.t/2, self.y_2 + self.t/2],
        ]
    def print_properties(self):
        for i in range(len(self.vertex_front_face)):
            print(self.vertex_front_face[i])

        for k in range(len(self.vertex_back_face)):
            print(self.vertex_back_face[k])

    def draw_line(self, x1, y1, x2, y2):
        turtle.goto(x1, y1)
        turtle.pendown()
        turtle.goto(x2, y2)
        turtle.penup()

    def draw_face(self, type_face):
        if (type_face == 1):
            self.draw_line(self.vertex_front_face[0][0], self.vertex_front_face[0][1], self.vertex_front_face[1][0], self.vertex_front_face[1][1])
            self.draw_line(self.vertex_front_face[1][0], self.vertex_front_face[1][1], self.vertex_front_face[2][0], self.vertex_front_face[2][1])
            self.draw_line(self.vertex_front_face[2][0], self.vertex_front_face[2][1], self.vertex_front_face[3][0], self.vertex_front_face[3][1])
            self.draw_line(self.vertex_front_face[3][0], self.vertex_front_face[3][1], self.vertex_front_face[0][0], self.vertex_front_face[0][1])
        
        if (type_face == 2):
            self.draw_line(self.vertex_back_face[0][0], self.vertex_back_face[0][1], self.vertex_back_face[1][0], self.vertex_back_face[1][1])
            self.draw_line(self.vertex_back_face[1][0], self.vertex_back_face[1][1], self.vertex_back_face[2][0], self.vertex_back_face[2][1])
            self.draw_line(self.vertex_back_face[2][0], self.vertex_back_face[2][1], self.vertex_back_face[3][0], self.vertex_back_face[3][1])
            self.draw_line(self.vertex_back_face[3][0], self.vertex_back_face[3][1], self.vertex_back_face[0][0], self.vertex_back_face[0][1])
            
    def join_faces(self):
        for i in range(0, 4):
            self.draw_line(self.vertex_front_face[i][0], self.vertex_front_face[i][1], self.vertex_back_face[i][0], self.vertex_back_face[i][1])

    def move(self, slope_x = 1, slope_y = 0):

        if (slope_x == 1):
            self.x = slope_x + 10

        if (slope_x == -1):
            self.x = slope_x - 10

        if (slope_y == 1):
            self.y = slope_y + 10

        if (slope_y == -1):
            self.y = slope_y - 10

    def rotate(self, angule, face):

        if (face == 1):
            for rows in range(4):
                x_relative = self.vertex_front_face[rows][0] - self.x
                y_relative = self.vertex_front_face[rows][1] - self.y

                x_new = x_relative * math.cos(angule) - y_relative * math.sin(angule) + self.x
                y_new = x_relative * math.sin(angule) + y_relative * math.cos(angule) + self.y

                self.vertex_front_face = [x_new, y_new]

        if (face == 2):
            for rows in range(4):
                x_relative = self.vertex_back_face[rows][0] - self.x_2
                y_relative = self.vertex_back_face[rows][1] - self.y_2

                x_new = x_relative * math.cos(angule) - y_relative * math.sin(angule) + self.x_2
                y_new = x_relative * math.sin(angule) + y_relative * math.cos(angule) + self.y_2

                self.vertex_back_face = [x_new, y_new]
    

start_angule = 1

cube3D = Cube3D(0, 0, 200)

cube3D.draw_face(1)
cube3D.draw_face(2)
cube3D.join_faces()

cube3D.rotate(10, 1)
cube3D.draw_face(1)
cube3D.join_faces()

turtle.done()

# cube3D.print_properties()