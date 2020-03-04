# most complete version of 3D plotter
"""
my 3d plotter based on pygame
press io to move in or out
press dfghjk to rotate around the three axes or use the mouse
can render two equations on the same frame, but becomes slow and jittery

"""


import pygame
import sys
import math
from math import *
import time


white = (255, 255, 255)
black = (0, 0, 0)
gridcolor = (0, 0, 150)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (255, 0, 150)
light_gray = (240, 240, 240)
light_blue = (230, 255, 247)

u = 50  # cube size unit
k = u / 10  # size of the graph grid
FPS = 25


pygame.init()
width = 800
height = 800
white_margin = 400
fov = min(width, height)

# font setup
font = pygame.font.SysFont('Verdana', 16)
font2 = pygame.font.SysFont('Serif', 24)
font3 = pygame.font.SysFont('Arial', 14)

cx = width // 2
cy = height // 2
screen = pygame.display.set_mode((width+white_margin, height))
pygame.display.set_caption("The Most Awesome 3D Plotter")
clock = pygame.time.Clock()

vertices = [
    (u, 0, u),
    (-u, 0, u),
    (-u, 0, -u),
    (u, 0, -u),
    (0, u, u),
    (0, u, -u),
    (0, -u, -u),
    (0, -u, u),
    (u, u, 0),
    (-u, u, 0),
    (-u, -u, 0),
    (u, -u, 0),
    (0, 0, 0),
    (0, 0, u),
    (-u, 0, 0),
    (0, 0, -u),
    (u, 0, 0),
    (0, u, 0),
    (0, -u, 0)
]

edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (8, 9), (9, 10), (10, 11), (11, 8),
    (13, 15), (14, 16), (17, 18)
]

data_points = [
    (10, -6, -4), (0, -2, 18), (5, 9, 22), (-23, -17, -22), (21, -23, -1), (14, 21, 21), (-15, 2, 13), (22, -20, 21), (-10, -25, 13), (-15, -6, 3), (16, -8, -3), (15, -12, -8), (-24, 13, 19), (7, 6, -23), (-23, -9, -24), (-15, 10, 8), (0, -1, 19), (5, -23, -9), (-20, 3, -6), (-13, 21, 16), (14, -10, -19), (-4, 24, -17), (0, -22, -24), (10, -5, -13), (9, -6, 11), (3, -12, 11), (7, 7, 5), (-7, 2, 18), (24, -3, 18), (10, -17, 18), (-15, -1, 7), (11, -7, 17), (3, 21, -11), (-21, -15, -1), (3, 15, 9), (-24, -22, 4), (16, 0, -7), (16, -16, 12), (6, -9, -23), (21, 11, -4), (11, 5, -16), (0, -14, -4), (-9, 18, -3), (11, 9, -8), (-25, 22, 20), (-10, 10, -2), (-21, -3, 15), (-17, -11, -24), (-2, -5, -15), (8, -9, 8)
]

def rotate2d(pos, radian):  # returns the new coordinates after rotation by rad
    x, y = pos
    s, c = math.sin(radian), math.cos(radian)
    return x * c - y * s, y * c + x * s

# x, y = s * math.sin(self.rot[1]), s * math.cos(self.rot[0])
# transformation with rotation with new coordinates x' and y':
# x' = x*cos@ - y*sin@
# y' = x*sin@ + y*cos@


def projection(point):  # converts a 3D point to a projection in 2d
    x = point[0]
    y = point[1]
    z = point[2]
    # getting the rotational transform coordinates for all three axes
    # the order is NB.
    # chose the y axis as that is the dependant variable
    z, x = rotate2d((z, x), cub.rot[1])
    y, z = rotate2d((y, z), cub.rot[0])
    x, y = rotate2d((x, y), cub.rot[2])

    x -= cub.pos[0]
    y -= cub.pos[1]
    z -= cub.pos[2]

    f = fov / z
    x, y = x * f, y * f

    projection_coord = [(cx + int(x), cy + int(y))]
    return projection_coord


class Cube:
    def __init__(self, pos=(0, 0, 0), rot=(3.14, 0, 0)):
        # sets the initial rotation with the y-axis positive pointing up
        self.pos = list(pos)
        self.rot = list(rot)


    def update(self, dt, key):
        s = (dt * u) / 300  # set the update increment as a function of the unit

        # translation   - camera movement -up/down, left/right, forward,backward
        if key[pygame.K_UP]:
            self.pos[1] += s
        if key[pygame.K_DOWN]:
            self.pos[1] -= s
        if key[pygame.K_RIGHT]:
            self.pos[0] -= s
        if key[pygame.K_LEFT]:
            self.pos[0] += s
        if key[pygame.K_o]:
            self.pos[2] -= s
        if key[pygame.K_i]:
            self.pos[2] += s

        # rotation around x
        if key[pygame.K_d]:
            self.rot[0] += dt / 500
        if key[pygame.K_f]:
            self.rot[0] -= dt / 500
        # rotation around y
        if key[pygame.K_g]:
            self.rot[1] += dt / 500
        if key[pygame.K_h]:
            self.rot[1] -= dt / 500
        # rotation around z
        if key[pygame.K_j]:
            self.rot[2] += dt / 500
        if key[pygame.K_k]:
            self.rot[2] -= dt / 500

    def frame(self):
        for edge in edges:
            p1 = edge[0]
            p2 = edge[1]

            points = []

            for point in (vertices[p1], vertices[p2]):
                coords = projection(point)
                points += coords

            pygame.draw.line(screen, black, points[0], points[1], 3)

    def grid(self):
        for i in range(int(2 * u // k)):
            gridx = k * i

            grid_points = [(u - gridx, 0, u), (u - gridx, 0, -u),
                           (-u, 0, u - gridx), (u, 0, u - gridx),
                           (0, u, -u + gridx), (0, -u, -u + gridx),
                           (0, -u + gridx, u), (0, -u + gridx, -u),
                           (-u + gridx, u, 0), (-u + gridx, -u, 0),
                           (-u, u - gridx, 0), (u, u - gridx, 0)
                           ]

            g_points = []
            for point in grid_points:
                points = projection(point)
                g_points += points

            for j in range(0, 11, 2):
                pygame.draw.line(screen, gridcolor, g_points[j],
                                 g_points[j + 1], 1)

    def axes_markers(self):
        # red,green blue markers on each axis to show x,y,z axes
        # the marker shows the positive side of the axis

        points = [(u, 0, 0), (0, u, 0), (0, 0, u)]
        colors = [red, green, blue]
        m_points = []

        for point in points:
            coords = projection(point)
            m_points += coords

        for i in range(3):
            pygame.draw.circle(screen, colors[i], m_points[i], 5)

    def render_cube(self):
        self.frame()
        self.grid()
        self.axes_markers()


def scatter_plot(data_points):

    for point in data_points:
        points = projection(point)
        s_points = points[0]

        pygame.draw.circle(screen, purple, s_points, 3)


def plot_intersection(eq, eq2):
    # eq = 'abs(x+z)/2 -10'
    # eq = '10*cos((z+x)/20)'
    #g = int(k // 2)
    g = 2
    points = []
    i_points = []
    for i in range(-u, u, g):
        for j in range(-u, u, g):
            x = i
            z = j
            y = round(eval(eq))
            v = round(eval(eq2))
            if y == v:
                intersect = (x,y,z)
                # print('intersect=', intersect)
                points+=[intersect]
                for point in points:
                    i_point = projection(point)
                pygame.draw.circle(screen, black, i_point[0], 3)


def equation_func(x, z, eq):
    try:
        y = eval(eq)
    except:
        screen.blit("Error", (width + 20, 300))
    return y


def equation_render(eq, color):
    g = int(k//2)  # calculating the interval of plot points

    for i in range(-u, u, g):
        for j in range(-u, u, g):
            # calculate 3 points: for two lines:current(i,j) to nexti,currentj
            # and current(i,j) to currenti , nextj - forming a grid
            x = i
            z = j
            #y = eval(eq)
            y = equation_func(x, z, eq)
            points = projection((x, y, z))
            e_point1 = points[0]

            # second point
            x = i+g
            z = j
            #y = eval(eq)
            y = equation_func(x, z, eq)
            points = projection((x, y, z))
            e_point2 = points[0]

            # third point
            x = i
            z = j+g
            #y = eval(eq)
            y = equation_func(x, z, eq)
            points = projection((x, y, z))
            e_point3 = points[0]
            pygame.draw.line(screen, color, e_point1, e_point2, 1)
            pygame.draw.line(screen, color, e_point1, e_point3, 1)


def instructions1():
    # instructions and results
    title = font2.render("Henko's Dynamic 3D Plotter", 1, black)
    screen.blit(title, (width + 10, 20))

    instruct = font.render('Type in an equation: eg. -3*x^2 - 3*z -2', 1, black)
    screen.blit(instruct, (width + 10, 70))

    instruct = font.render('Select "Enter" when done or "q" to start over.', 1,
                           black)
    screen.blit(instruct, (width + 20, 100))

    instruct = font.render('Select "backspace" to clear.', 1,
                           black)
    screen.blit(instruct, (width + 20, 130))
    instruct = font3.render(
        's=sin(), c=cos(), t=tan(), r=sqrt, a=abs(), l=log10(), n=log()', 1,
        black)
    screen.blit(instruct, (width + 20, 160))
    instruct = font3.render('e=e, p=pi ', 1,
                            black)
    screen.blit(instruct, (width + 20, 180))


def main():
    loop_exit = False
    active = False
    graph = False
    equation = []

    while not loop_exit:
        dt = clock.tick(FPS) / 4
        s = (dt * u) / 300

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            mouse = pygame.mouse.get_pressed()
            # gets the state of the 3 mouse buttons
            if event.type == pygame.MOUSEMOTION:
                # use mouse position to work the rotation
                x, y = event.rel  # rel gives the x,y co-ords of the mouse
                x /= 100
                y /= 100
                if mouse[0] == 1:
                    # adjusts the rotation of the cube
                    # only if the mouse button is also pressed
                    cub.rot[0] += y
                    cub.rot[1] += x

            if event.type == pygame.MOUSEBUTTONDOWN:
                # use mouse wheel to translate in z axis
                if event.button == 4:
                    cub.pos[2] -= s
                elif event.button == 5:
                    cub.pos[2] += s

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

                # math operations and symbols
                elif event.unicode == u'*':
                    equation.append('*')
                elif event.unicode == u'+':
                    equation.append('+')
                elif event.unicode == u'-':
                    equation.append('-')
                elif event.unicode == u'/':
                    equation.append('/')
                elif event.unicode == u'.':
                    equation.append('.')
                elif event.unicode == u'(':
                    equation.append('(')
                elif event.unicode == u')':
                    equation.append(')')
                elif event.unicode == u'^':
                    equation.append('**')
                elif event.key == pygame.K_x:
                    equation.append('x')
                elif event.key == pygame.K_z:
                    equation.append('z')

                # enter numbers  to be typed into equation and x variable
                elif event.key == pygame.K_1:
                    equation.append('1')
                elif event.key == pygame.K_2:
                    equation.append('2')
                elif event.key == pygame.K_3:
                    equation.append('3')
                elif event.key == pygame.K_4:
                    equation.append('4')
                elif event.key == pygame.K_5:
                    equation.append('5')
                elif event.key == pygame.K_6:
                    equation.append('6')
                elif event.key == pygame.K_7:
                    equation.append('7')
                elif event.key == pygame.K_8:
                    equation.append('8')
                elif event.key == pygame.K_9:
                    equation.append('9')
                elif event.key == pygame.K_0:
                    equation.append('0')

                # math function commands
                elif event.key == pygame.K_s:
                    equation.append('sin(')
                elif event.key == pygame.K_c:
                    equation.append('cos(')
                elif event.key == pygame.K_t:
                    equation.append('tan(')
                elif event.key == pygame.K_r:
                    equation.append('sqrt(')
                elif event.key == pygame.K_a:
                    equation.append('abs(')
                elif event.key == pygame.K_l:
                    equation.append('log10(')
                elif event.key == pygame.K_n:
                    equation.append('log(')
                elif event.key == pygame.K_e:
                    equation.append('e')
                elif event.key == pygame.K_p:
                    equation.append('pi')

                elif event.key == pygame.K_BACKSPACE:
                    try:  # use try in case the equation list is empty
                        equation.pop()
                    except:
                        pass

                elif event.key == pygame.K_q:
                    main()  # pass a space as the equation

                elif event.key == pygame.K_RETURN:
                    active = True

                elif event.key == pygame.K_w:  # choose a second graph
                    eq2 = eq
                    equation = []
                    graph = True
                    active = False

        screen.set_clip(width, 0, width + white_margin, height)
        screen.fill(light_gray)
        instructions1()

        screen.set_clip(width + 10, height - 200, width + white_margin, height)
        screen.fill(light_gray)
        # join equation array without commas
        eq = ''.join(str(e) for e in equation)  # remove commas
        # eq = str.replace(" ", "")  # remove spaces
        # render and blit equation
        eq1_show = font.render("Function  :  y = " + eq, 1, black)
        screen.blit(eq1_show, (width + 20, height - 200))

        if active:
            instruct = font.render('Select "w" to add  another graph', 1,
                                   black)
            screen.blit(instruct, (width + 20, height - 170))

        if graph:
            eq = ''.join(str(e) for e in equation)
            eq1_show = font.render("Function  :  y = " + eq, 1, black)
            screen.blit(eq1_show, (width + 20, height - 200))
            eq2_show = font.render("Function  :  y = " + eq2, 1, black)
            screen.blit(eq2_show, (width + 20, height - 140))

        screen.set_clip(0,0, width,height)
        screen.fill(light_blue)
        pygame.draw.line(screen, black, (width, 0), (width, height), 10)
        cub.render_cube()
        if active:
            try:
                equation_render(eq, red)
            except:
                pass
        #scatter_plot(data_points)   # comment out to not show the scatter points
        if graph and active:
            try:
                equation_render(eq, blue)
                equation_render(eq2, red)
                plot_intersection(eq, eq2)
            except:
                pass

        screen.set_clip(None)

        key = pygame.key.get_pressed()
        cub.update(dt, key)

        speed = clock.get_fps()  # returns the actual fps of the loop
        # print(speed)     # print the frame rate in stdout
        pygame.display.flip()
        pygame.time.wait(20) # need the sleep to limit the churn and reduce the CPU use

    pygame.quit()
    sys.exit()


cub = Cube((0, 0, -3 * u))
main()