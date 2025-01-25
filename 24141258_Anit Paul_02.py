from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import math

speed = 1
score = 0
W_Width, W_Height = 500,500
rocketPos = [15,15]
rocketInfo = {'radius': 10, 'center': [0,0], 'color': [1,1,0]}
rocketMissile = {'radius': 5, 'center': [0,0], 'color': [1,0,0]}
missiles = []
enemyMissiles1 = []
stop = False
missed_count = 0

pause_symbol = False
isfrozen = False
isGameOver = False

pause_box = {
    "x": 220,
    "y": 460,
    "width": 40,
    "height": 40
}
pause_box2 = {
    "x": 240,
    "y": 460,
    "width": 20,
    "height": 40
}

arrow_box = {
        'x': 0,
        'y': 460,
        'width': 40,
        'height': 40
    }

cross_box = {
    'x': 460,
    'y': 460,
    "width": 40,
    "height": 40
}

def drawPause():
    global pause_symbol, isfrozen
    if pause_symbol and isfrozen:
        eightWaySymmetry(220, 460, 220, 500, (1, 0.75, 0))
        eightWaySymmetry(220, 460, 260, 480, (1, 0.75, 0))
        eightWaySymmetry(260, 480, 220, 500, (1, 0.75, 0))
    else:
        eightWaySymmetry(240, 460, 240, 500, (1, 0.75, 0))
        eightWaySymmetry(260, 460, 260, 500, (1, 0.75, 0))

def drawArrow():
    eightWaySymmetry(0, 480, 20, 500, (0, 0, 1))
    eightWaySymmetry(0, 480, 20, 460, (0, 0, 1))
    eightWaySymmetry(0, 480, 40, 480, (0, 0, 1))


def drawCross():
    eightWaySymmetry(460, 460, 500, 500, (1, 0, 0))
    eightWaySymmetry(460, 500, 500, 460, (1, 0, 0))

def convertCoordinate(x,y):
    global W_Width, W_Height
    a = x
    b = W_Height-y
    return (a,b)


def drawPoints(x, y, color):
    glColor3f(*color)
    glPointSize(2) #pixel size
    glBegin(GL_POINTS)
    glVertex2f(x,y) # show korbe pixel tar location
    glEnd()


def convertzone0(x, y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (y, -x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (-y, x)
    elif zone == 7:
        return (x, -y)

def convertzoneM(x,y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (-y, x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (y, -x)
    elif zone == 7:
        return (x, -y)

def findzone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx <= 0 and dy >= 0:
            return 3
        elif dx <= 0 and dy <= 0:
            return 4
        elif dx >= 0 and dy <= 0:
            return 7
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx <= 0 and dy >= 0:
            return 2
        elif dx <= 0 and dy <= 0:
            return 5
        elif dx >= 0 and dy <= 0:
            return 6

def midpointLine(x1, y1, x2, y2, zone, color):
    dx = x2 - x1
    dy = y2 - y1
    d = 2*dy - dx
    incE = 2*dy
    incNE = 2*(dy-dx)
    y = y1

    for x in range(x1, x2+1):
        oz_x, oz_y = convertzoneM(x, y, zone)

        drawPoints(oz_x , oz_y, color)
        if d <= 0:
            d += incE
        else:
            d += incNE
            y += 1

def eightWaySymmetry(x1, y1, x2, y2, color = (1, 1, 0)):
    zone = findzone(x1, y1, x2, y2)
    #print(zone)
    x1, y1 = convertzone0(x1, y1, zone)
    x2, y2 = convertzone0(x2, y2, zone)
    midpointLine(x1, y1, x2, y2, zone, color)

def midpointCircle(radius, color, center = (0,0)):
    x = 0
    y = radius
    d = 1 - radius
    cirPoints(x, y, color, center)
    while x < y:
        if d < 0:
            d = d + 2*x+3
            x = x+1
        else:
            d = d + 2*(x-y)+5
            x = x+1
            y = y-1
        cirPoints(x, y, color, center)

def summonEnemyMissiles():
    global enemyMissiles1
    if len(enemyMissiles1) < 5:
        new_enemy = summonNewEnemy()
        collided = False
        for existing in enemyMissiles1:
            if has_collided(new_enemy, existing):
                collided = True
                break
        if collided == False:
            enemyMissiles1.append(new_enemy)

import math


def summonNewEnemy():
    x = random.randint(10, 490)
    y = random.randint(350, 450)
    radius = random.randint(10, 15)

    is_green = random.random() < 0.2
    color = [0, 1, 0] if is_green else [1, 1, 0]

    return {'radius': radius, 'center': [x, y], 'color': color, 'is_green': is_green, 'original_radius': radius, 'pulsation_time': 0}

def drawEnemyMissiles():
    global enemyMissiles1, rocketInfo, rocketMissile
    for enemy in enemyMissiles1:

        enemy['center'][1] -= 0.05     #enemy vertical pos


        if enemy['is_green']:

            pulsation_amplitude = 10
            pulsation_frequency = .5  # dukduk speed
            enemy['radius'] = enemy['original_radius'] + pulsation_amplitude * math.sin(pulsation_frequency * enemy['pulsation_time'])
            enemy['pulsation_time'] += 0.05


        midpointCircle(enemy['radius'], enemy['color'], enemy['center']) #base enemy





def cirPoints(x, y, color, center):
    drawPoints(x+center[0], y+center[1], color)
    drawPoints(-x+center[0], y+center[1], color)
    drawPoints(x+center[0], -y+center[1], color)
    drawPoints(-x+center[0], -y+center[1], color)
    drawPoints(y+center[0], x+center[1], color)
    drawPoints(-y+center[0], x+center[1], color)
    drawPoints(y+center[0], -x+center[1], color)
    drawPoints(-y+center[0], -x+center[1], color)


def drawRocket():
    global rocketPos, rocketInfo


    triangle_height = 40
    triangle_base = 40

    #center calc for circle
    triangle_center_x = rocketPos[0]
    triangle_center_y = rocketPos[1] + (triangle_height / 2)


    p1 = [triangle_center_x - triangle_base / 2, triangle_center_y - (triangle_height / 2)]  # Left corner
    p2 = [triangle_center_x + triangle_base / 2, triangle_center_y - (triangle_height / 2)]  # Right corner
    p3 = [triangle_center_x, triangle_center_y + (triangle_height / 2)]  # Top corner


    glColor3f(0, 0, 1)
    glLineWidth(4)
    glBegin(GL_LINE_LOOP)  # only outline
    glVertex2f(p1[0], p1[1])
    glVertex2f(p2[0], p2[1])
    glVertex2f(p3[0], p3[1])
    glEnd()
    # The center of triangle is center of shooter. for positioning
    rocketInfo['center'][0] = triangle_center_x
    rocketInfo['center'][1] = triangle_center_y
    # mini circle
    mini_circle_radius = 6
    mini_circle_offset = 6  # circle er dist


    bottom_line_y = triangle_center_y - (triangle_height / 2)  # triangle er tola


    left_mini_circle_center = [triangle_center_x - mini_circle_offset, bottom_line_y + mini_circle_radius]
    midpointCircle(mini_circle_radius, [1, 0, 0], left_mini_circle_center)

    right_mini_circle_center = [triangle_center_x + mini_circle_offset, bottom_line_y + mini_circle_radius]
    midpointCircle(mini_circle_radius, [1, 0, 0], right_mini_circle_center)


    line_y = bottom_line_y + mini_circle_radius * 2
    glColor3f(0, 0, 1)
    glLineWidth(4)
    glBegin(GL_LINES)
    glVertex2f(p1[0] + 8, line_y)
    glVertex2f(p2[0] - 8, line_y)
    glEnd()
    glLineWidth(1)



def drawMissiles():
    global missiles
    for missile in missiles:
        missile['center'][1] += missile['speed']
        midpointCircle(missile['radius'], missile['color'], missile['center'])
        if missile['center'][1] > 500:
            missiles.remove(missile)


def fireMissiles():
    global rocketPos, rocketInfo, rocketMissile
    missile0 = {'radius': 5, 'center': [rocketPos[0], rocketPos[1]+rocketInfo['radius']], 'color': [1,0,0], 'speed': 1}
    missiles.append(missile0)
 

def animate():
    global isGameOver, isfrozen
    if not isGameOver and not isfrozen:
        drawMissiles()
        drawEnemyMissiles()
        glutPostRedisplay()
        time.sleep(0.001)


def checkMissileEnemyCollision():
    global missiles, enemyMissiles1, score
    for missile2 in missiles:
        for enemy_circle in enemyMissiles1:
            if has_collided(missile2, enemy_circle):
                missiles.remove(missile2)
                enemyMissiles1.remove(enemy_circle)

                if enemy_circle['is_green']:
                    score += 2
                else:
                    score += 1

                print(f"Score: {score}")
                return



def has_collided(circle1, circle2):
    circle1_center_x, circle1_center_y = circle1['center']
    circle2_center_x, circle2_center_y = circle2['center']
    distance = ((circle1_center_x - circle2_center_x) ** 2 + (circle1_center_y - circle2_center_y) ** 2) ** 0.5
    return distance < (circle1['radius'] + circle2['radius'])

def checkGameOver():
    global enemyMissiles1, rocketInfo, isGameOver, missed_count

    for enemy_circle in enemyMissiles1:
        if has_collided(enemy_circle, rocketInfo):
            print("Game Over!!!!!!!! Enemy fired at the spaceship rocket! Rocket go BOOOMMM!!!!")
            isGameOver = True
            return

    for enemy_circle in enemyMissiles1:
        if enemy_circle['center'][1] < 0:
            missed_count += 1
            enemyMissiles1.remove(enemy_circle)

            print(f"Remaining Lives: {3 - missed_count}")

            if missed_count >= 3:
                print("Game Over!!!! All of your lives are over")
                isGameOver = True
                return

def specialKeyListener(key, x, y):
    global rocketPos, rocketInfo, isGameOver, isfrozen
    if not isGameOver and not isfrozen:
        if key==GLUT_KEY_RIGHT:
            if rocketInfo['center'][0] + rocketInfo['radius'] < 490:
                rocketPos[0] += 10

        elif key==GLUT_KEY_LEFT:
            if rocketInfo['center'][0] - rocketInfo['radius'] > 10:
                rocketPos[0] -= 10



    glutPostRedisplay()







def keyboardListener(key, x, y):
    global isfrozen, isGameOver
    if not isGameOver and not isfrozen:
        if key==b' ':
            fireMissiles()
        if key==b'a':
            if rocketInfo['center'][0] - rocketInfo['radius'] > 10:
                rocketPos[0] -= 25

        if key==b'd':
            if rocketInfo['center'][0] + rocketInfo['radius'] < 490:
                rocketPos[0] += 25

        glutPostRedisplay()


def mouseListener(button, state, x, y):
    global rocketPos, rocketInfo, missiles, enemyMissiles1, score, isGameOver, pause_symbol, isfrozen, arrow_box, cross_box, pause_box, pause_box2
    if button==GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            adj_x, adj_y = convertCoordinate(x, y)
            if adj_x >= arrow_box['x'] and adj_x <= arrow_box['x'] + arrow_box['width'] and adj_y >= arrow_box['y'] and adj_y <= arrow_box['y'] + arrow_box['height']:
                rocketPos = [15,15]
                rocketInfo = {'radius': 10, 'center': [0,0], 'color': [1,1,0]}
                missiles = []
                enemyMissiles1 = []
                score = 0
                isGameOver = False
                pause_symbol = False
                isfrozen = False
                print("Starting over")


            if adj_x >= cross_box['x'] and adj_x <= cross_box['x'] + cross_box['width'] and adj_y >= cross_box['y'] and adj_y <= cross_box['y'] + cross_box['height']:

                print("GoodBye")
                glutLeaveMainLoop()

            if pause_symbol:
                if adj_x >= pause_box["x"] and adj_x <= pause_box["x"] + pause_box["width"] and adj_y >= pause_box["y"] and adj_y <= pause_box["y"] + pause_box["height"]:

                    pause_symbol = not pause_symbol
                    isfrozen = not isfrozen
            elif adj_x >= pause_box2["x"] and adj_x <= pause_box2["x"] + pause_box2["width"] and adj_y >= pause_box2["y"] and adj_y <= pause_box2["y"] + pause_box2["height"]:

                pause_symbol = not pause_symbol
                isfrozen = not isfrozen



def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    global rocketInfo
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    drawRocket()
    drawMissiles()
    drawEnemyMissiles()
    checkMissileEnemyCollision()
    summonEnemyMissiles()
    checkGameOver()
    drawArrow()
    drawPause()
    drawCross()
    if isGameOver:
        print(f"Game Over! Your score is: {score}")
    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Space Shooter")
glutDisplayFunc(showScreen)
glutIdleFunc(animate)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutKeyboardFunc(keyboardListener)
glutMainLoop()