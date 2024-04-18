import turtle

turtle.speed(0)
turtle.penup()

turtle.goto(0,0)

def drawLine(x1, y1, x2, y2):  
    turtle.goto(x1, y1)
    turtle.pendown()
    turtle.goto(x2, y2)
    turtle.penup()

    last_position = [x2, y2]

    return last_position

def drawCube(x, y, z, size):
    # Right Face
    [x_last, y_last] = drawLine(x, y, x + size/2, y + size/2)
    [x_last, y_last] = drawLine(x_last, y_last, x_last, y_last + size)
    [x_last, y_last] = drawLine(x_last, y_last, x_last - size/2, y_last - size/2)
    [x_last, y_last] = drawLine(x_last, y_last, x_last, y_last - size)

    [x_last, y_last] = drawLine(x_last, y_last, x_last - size, y_last)

    # Left Face
    [x_last, y_last] = drawLine(x_last, y_last, x_last, y_last + size)
    [x_last, y_last] = drawLine(x_last, y_last, x_last + size/2, y_last + size/2)
    [x_last, y_last] = drawLine(x_last, y_last, x_last, y_last - size)
    [x_last, y_last] = drawLine(x_last, y_last, x_last - size/2, y_last - size/2)

    # Floor Face
    [x_last, y_last] = drawLine(x_last, y_last, x_last + size/2, y_last + size/2)
    [x_last, y_last] = drawLine(x_last, y_last, x_last + size, y_last)
    
    [x_last, y_last] = drawLine(x_last, y_last, x_last, y_last + size)

    # Top Face
    [x_last, y_last] = drawLine(x_last, y_last, x_last - size, y_last)
    [x_last, y_last] = drawLine(x_last, y_last, x_last - size/2, y_last - size/2)
    [x_last, y_last] = drawLine(x_last, y_last, x_last + size, y_last)

    turtle.hideturtle()

drawCube(0, 0, 0, 100)

turtle.done()