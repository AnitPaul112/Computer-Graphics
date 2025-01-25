from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

window_size = 512
center_x, center_y = window_size // 2, window_size // 2
outer_radius = 60
inner_radius = 40
pulsating = True
pulsate_step = 0.5
max_radius = 70
min_radius = 10
quadrant_colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0)]

# a single point
def draw_pixel(x, y):
    glBegin(GL_POINTS)
    glVertex2i(int(x), int(y))
    glEnd()

# circle drawing by the midpoint circle algorithm
def draw_circle(xc, yc, radius, color=None):
    x, y = 0, radius
    d = 1 - radius
    if color:
        glColor3f(*color)

    while x <= y:
    # Plot points using 8-way symmetry
        draw_pixel(xc + x, yc + y) 
        draw_pixel(xc + y, yc + x)  
        draw_pixel(xc - x, yc + y)  
        draw_pixel(xc - y, yc + x)  
        draw_pixel(xc + x, yc - y) 
        draw_pixel(xc + y, yc - x)  
        draw_pixel(xc - x, yc - y) 
        draw_pixel(xc - y, yc - x) 


        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1

# dashed line 
def draw_dashed_lines():
    glColor3f(1, 1, 1)
    draw_line(0, window_size // 2, window_size, window_size // 2, dash=True)
    draw_line(window_size // 2, 0, window_size // 2, window_size, dash=True)

# line drawing by midpoint line algorithm for quadrants
def draw_line(x0, y0, x1, y1, dash=False, dash_length=10):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    dash_counter = 0
    draw_flag = True

    while True:
        if draw_flag or not dash:
            draw_pixel(x0, y0)

        if dash:
            dash_counter += 1
            if dash_counter >= dash_length:
                dash_counter = 0
                draw_flag = not draw_flag

        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

# pulsating effect
def update_radius():
    global outer_radius, pulsate_step
    if pulsating:
        outer_radius += pulsate_step
        if outer_radius >= max_radius or outer_radius <= min_radius:
            pulsate_step = -pulsate_step

# circle color
def get_circle_color():
    if center_x < window_size // 2 and center_y > window_size // 2:
        return quadrant_colors[0]  
    elif center_x > window_size // 2 and center_y > window_size // 2:
        return quadrant_colors[1]  
    elif center_x > window_size // 2 and center_y < window_size // 2:
        return quadrant_colors[2] 
    else:
        return quadrant_colors[3]  

# wrapping
def handle_wrapping():
    global center_x, center_y
    if center_x + outer_radius < 0:
        center_x = window_size + outer_radius
    elif center_x - outer_radius > window_size:
        center_x = -outer_radius
    if center_y + outer_radius < 0:
        center_y = window_size + outer_radius
    elif center_y - outer_radius > window_size:
        center_y = -outer_radius

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    update_radius()
    handle_wrapping()
    draw_dashed_lines()
    draw_circle(center_x, center_y, outer_radius, get_circle_color()) # outer circle
    draw_circle(center_x, center_y, min_radius, (1, 1, 1))  # inner circle
    glutSwapBuffers()
    glutPostRedisplay()



def special(key, x, y):
    global center_x, center_y
    if key == GLUT_KEY_LEFT: 
        center_x -= 5
    elif key == GLUT_KEY_RIGHT:
        center_x += 5
    elif key == GLUT_KEY_UP:  
        center_y += 5
    elif key == GLUT_KEY_DOWN:  
        center_y -= 5
    glutPostRedisplay()


def keyboard(key, x, y):
    global pulsating
    if key == b'\x1b':  
        glutLeaveMainLoop()
    elif key == b' ':  
        pulsating = not pulsating
    glutPostRedisplay()

def mouse(button, state, x, y):
    global center_x, center_y
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        center_x = x
        center_y = window_size - y 
        glutPostRedisplay()


def main():
    glutInit([])
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_size, window_size)
    glutCreateWindow(b"Circle Animation")
    glClearColor(0, 0, 0, 0)
    glPointSize(2)
    gluOrtho2D(0, window_size, 0, window_size)
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)  
    glutSpecialFunc(special) 
    glutMouseFunc(mouse)
    glutMainLoop()


if __name__ == "__main__":
    main()




