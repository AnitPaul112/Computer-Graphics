import pygame
from OpenGL.GL import *

window_size = 512
center_x, center_y = window_size // 2, window_size // 2
outer_radius = 50
inner_radius = 30
is_pulsating = True
pulsate_delta = 0.5
max_radius = 70
min_radius = 40
colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0)]

# Draw a single pixel
def draw_pixel(x, y):
    glBegin(GL_POINTS)
    glVertex2i(int(x), int(y))  # Ensure x and y are integers
    glEnd()

# Midpoint Circle Algorithm with eight-way symmetry
def midpoint_circle(xc, yc, r, color=None):
    x, y = 0, r
    d = 1 - r
    if color:
        glColor3f(*color)
    while x <= y:
        for dx, dy in [(x, y), (-x, y), (x, -y), (-x, -y), (y, x), (-y, x), (y, -x), (-y, -x)]:
            draw_pixel(xc + dx, yc + dy)
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1

# Draw dashed lines for quadrants
def draw_dashed_line():
    glColor3f(1, 1, 1)
    for i in range(0, window_size, 10):
        draw_pixel(i, window_size // 2)
        draw_pixel(window_size // 2, i)

# Draw the outer circle with quadrant-based coloring
def draw_outer_circle():
    global outer_radius
    # Determine color based on quadrant
    if center_x < window_size // 2 and center_y > window_size // 2:
        color = colors[0]  # Red
    elif center_x > window_size // 2 and center_y > window_size // 2:
        color = colors[1]  # Green
    elif center_x > window_size // 2 and center_y < window_size // 2:
        color = colors[2]  # Blue
    else:
        color = colors[3]  # Yellow
    midpoint_circle(center_x, center_y, outer_radius, color)

# Display callback function
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_dashed_line()

    # Draw the inner circle (constant white)
    glColor3f(1, 1, 1)
    midpoint_circle(center_x, center_y, inner_radius)

    # Draw the pulsating outer circle
    draw_outer_circle()

    pygame.display.flip()

# Main function
def main():
    global center_x, center_y, outer_radius, is_pulsating, pulsate_delta

    pygame.init()
    pygame.display.set_mode((window_size, window_size), pygame.OPENGL | pygame.DOUBLEBUF)
    glClearColor(0, 0, 0, 0)
    glOrtho(0, window_size, 0, window_size, -1, 1)

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    center_x -= 5
                    if center_x < 0:
                        center_x = window_size
                elif event.key == pygame.K_RIGHT:
                    center_x += 5
                    if center_x > window_size:
                        center_x = 0
                elif event.key == pygame.K_UP:
                    center_y += 5
                    if center_y > window_size:
                        center_y = 0
                elif event.key == pygame.K_DOWN:
                    center_y -= 5
                    if center_y < 0:
                        center_y = window_size
                elif event.key == pygame.K_SPACE:
                    is_pulsating = not is_pulsating
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                center_x, center_y = pygame.mouse.get_pos()
                center_y = window_size - center_y

        if is_pulsating:
            outer_radius += pulsate_delta
            if outer_radius > max_radius or outer_radius < min_radius:
                pulsate_delta = -pulsate_delta

        display()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
