'''

#task1(commented)

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W_Width, W_Height = 500, 500

raindrops = []
rain_direction = [0, -5]

background_color = [0.0, 0.0, 0.0]

class Raindrop:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(0, W_Width)
        self.y = W_Height
        self.speed = random.uniform(1.0,3.)

    def fall(self):
        self.x += rain_direction[0]
        self.y += rain_direction[1] * self.speed
        if self.y < 0:
            self.reset()

def init_rain(num_drops):
    global raindrops
    raindrops = [Raindrop() for i in range(num_drops)]

def draw_house():
    glColor3f(0.1, 0.5, 0.4)
    glBegin(GL_QUADS)
    glVertex2f(150, 100)
    glVertex2f(350, 100)
    glVertex2f(350, 300)
    glVertex2f(150, 300)
    glEnd()

    glColor3f(0.9, 0.1, 0.6)
    glBegin(GL_TRIANGLES)
    glVertex2f(130, 300)
    glVertex2f(370, 300)
    glVertex2f(250, 400)
    glEnd()

    glColor3f(0.0, 0.1, 0.2)
    glBegin(GL_QUADS)
    glVertex2f(200, 100)
    glVertex2f(250, 100)
    glVertex2f(250, 200)
    glVertex2f(200, 200)
    glEnd()

    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(275, 225)
    glVertex2f(325, 225)
    glVertex2f(325, 275)
    glVertex2f(275, 275)
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(300, 225)
    glVertex2f(300, 275)
    glVertex2f(275, 250)
    glVertex2f(325, 250)
    glEnd()

def draw_rain():
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    for drop in raindrops:
        glVertex2f(drop.x, drop.y)
        glVertex2f(drop.x + rain_direction[0], drop.y + rain_direction[1] * drop.speed)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(*background_color, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    draw_house()
    draw_rain()

    glutSwapBuffers()

def animate():
    for drop in raindrops:
        drop.fall()
    glutPostRedisplay()

def keyboardListener(key, x, y):
    global background_color
    if key == b'd':
        background_color = [min(c + 0.05, 1.0) for c in background_color]
    elif key == b'a':
        background_color = [max(c - 0.05, 0.0) for c in background_color]
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global rain_direction
    if key == GLUT_KEY_LEFT:
        rain_direction[0] -= 1
    elif key == GLUT_KEY_RIGHT:
        rain_direction[0] += 1
    glutPostRedisplay()

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, W_Width, 0.0, W_Height)
    glMatrixMode(GL_MODELVIEW)

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL House in Rainfall")

init()
init_rain(100)

glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)

glutMainLoop()

'''

# Task 2 Code (Uncommented)
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time

W_Width, W_Height = 500, 500

points = []
speed = 0.1
ball_size = 5
freeze = False
blink_interval = 500

class Point:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.dark = [0,0,0]
        self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]
        self.is_visible = True


def convert_coordinate(x,y):
    global W_Width, W_Height
    a = x - (W_Width/2)
    b = (W_Height/2) - y 
    return a,b

def draw_points(x, y, s, color):
    glColor3f(color[0], color[1], color[2])
    glPointSize(s)
    glBegin(GL_POINTS)
    glVertex2f(x,y)
    glEnd()
    
def generate_movable_point(x, y):
    global points
    color = [random.random(), random.random(), random.random()]
    points.append(Point(x, y, color))


def draw_list_points():
    global points
    for point in points:
        draw_points(point.x, point.y, ball_size, point.color)

def keyboardListener(key, x, y):
    global ball_size, speed, freeze
    if key == b'w':
        ball_size += 1
        print("Size Increased")
    elif key == b's':
        ball_size -= 1
        print("Size Decreased")
    elif key == b' ':
        freeze = not freeze
        if freeze:
            print("Freeze")
        else:
            print("Unfreeze")

    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global speed
    if key == GLUT_KEY_UP:
            speed *= 2
            print("Speed Increased")
    elif key == GLUT_KEY_DOWN:
        speed /= 2
        print("Speed Decreased")
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        c_x, c_y = convert_coordinate(x, y)
        generate_movable_point(c_x, c_y)

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        for point in points:
            point.color, point.dark =  point.dark, point.color
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
        
        for point in points:
            point.color, point.dark =  point.dark, point.color

    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0,0,0,0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0,0,200,	0,0,0,	0,1,0)
    glMatrixMode(GL_MODELVIEW)
    draw_list_points()
    glutSwapBuffers()

def animate():
    global points, freeze
    if not freeze:
        for point in points:
            point.x += speed * point.direction[0]
            point.y += speed * point.direction[1]

            if abs(point.x) > W_Width/2:
                point.direction[0] *= -1
            if abs(point.y) > W_Height/2:
                point.direction[1] *= -1
    glutPostRedisplay()

def init():
    glClearColor(0,0,0,0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104,	1,	1,	1000.0)

glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

wind = glutCreateWindow(b"Task 2")
init()

glutDisplayFunc(display)
glutIdleFunc(animate)

glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()

def convert_coordinate(x, y):
    global W_Width, W_Height
    a = x - (W_Width / 2)
    b = (W_Height / 2) - y
    return a, b

def draw_points(x, y, s, color):
    glColor3f(color[0], color[1], color[2])
    glPointSize(s)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def generate_movable_point(x, y):
    global points
    color = [random.random(), random.random(), random.random()]
    points.append(Point(x, y, color))

def draw_list_points():
    global points
    for point in points:
        if point.is_visible:
            draw_points(point.x, point.y, ball_size, point.color)

def blink_points(value):
    global points, freeze
    if not freeze:
        for point in points:
            point.is_visible = not point.is_visible
        glutTimerFunc(blink_interval, blink_points, 0)

def keyboardListener(key, x, y):
    global ball_size, speed, freeze
    if key == b'w':
        ball_size += 1
        print("Size Increased")
    elif key == b's':
        ball_size -= 1
        print("Size Decreased")
    elif key == b' ':
        freeze = not freeze
        if freeze:
            print("Freeze")
        else:
            glutTimerFunc(blink_interval, blink_points, 0)
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global speed
    if key == GLUT_KEY_UP:
        if speed < 0.25:
            speed *= 2
            print("Speed Increased")
    elif key == GLUT_KEY_DOWN:
        speed /= 2
        print("Speed Decreased")
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global points
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        c_x, c_y = convert_coordinate(x, y)
        for i in range(-20, 21, 10):
            for j in range(-20, 21, 10):
                if random.random() > 0.75:
                    generate_movable_point(c_x + i, c_y + j)

    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)

    glMatrixMode(GL_MODELVIEW)
    draw_list_points()
    glutSwapBuffers()

def animate():
    global points, freeze
    if not freeze:
        for point in points:
            point.x += speed * point.direction[0]
            point.y += speed * point.direction[1]

            if point.x < -W_Width / 2 or point.x > W_Width / 2:
                point.direction[0] *= -1
            if point.y < -W_Height / 2 or point.y > W_Height / 2:
                point.direction[1] *= -1
    
    glutPostRedisplay()

def reshape(w, h):
    global W_Width, W_Height
    W_Width, W_Height = w, h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-W_Width / 2, W_Width / 2, -W_Height / 2, W_Height / 2)
    glMatrixMode(GL_MODELVIEW)

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-W_Width / 2, W_Width / 2, -W_Height / 2, W_Height / 2)
    glMatrixMode(GL_MODELVIEW)

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Movable Points")

init()

glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutReshapeFunc(reshape)
glutTimerFunc(blink_interval, blink_points, 0)

glutMainLoop()

