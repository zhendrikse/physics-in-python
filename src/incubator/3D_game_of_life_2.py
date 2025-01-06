# https://metakatie.wordpress.com/2008/09/25/a-3d-version-of-the-game-of-life-with-vpython/

from vpython import *

def zeros(m, n, channels = 3):
    panel = []
    for k in range(channels):
        panel.append([])
        for j in range(m):
            panel[k].append([0 for i in range(n)])
    return panel

def alive_neighbour_counter(z, y, x):  # counts the number of alive neighbours (wraps around canvas edges)

    counter = 0

    z_minus_1 = len(grid) - 1 if z == 0 else z - 1
    z_plus_1 = 0 if z == len(grid) - 1 else  z + 1
    y_minus_1 = len(grid) - 1 if y == 0 else y - 1
    y_plus_1 = 0 if y == len(grid) - 1 else y + 1
    x_minus_1 = len(grid) - 1 if x == 0 else x - 1
    x_plus_1 = 0 if x == len(grid) - 1 else x + 1

    if grid[z_minus_1][y_minus_1][x_minus_1] == 1: counter += 1
    if grid[z_minus_1][y][x_minus_1] == 1: counter += 1
    if grid[z_minus_1][y_minus_1][x] == 1: counter += 1
    if grid[z_minus_1][y][x_plus_1] == 1: counter += 1
    if grid[z_minus_1][y_plus_1][x] == 1: counter += 1
    if grid[z_minus_1][y_plus_1][x_plus_1] == 1: counter += 1
    if grid[z_minus_1][y_plus_1][x_minus_1] == 1: counter += 1
    if grid[z_minus_1][y_minus_1][x_plus_1] == 1: counter += 1
    if grid[z][y_minus_1][x_minus_1] == 1: counter += 1
    if grid[z][y][x_minus_1] == 1: counter += 1
    if grid[z][y_minus_1][x] == 1: counter += 1
    if grid[z][y][x_plus_1] == 1: counter += 1
    if grid[z][y_plus_1][x] == 1: counter += 1
    if grid[z][y_plus_1][x_plus_1] == 1: counter += 1
    if grid[z][y_plus_1][x_minus_1] == 1: counter += 1
    if grid[z][y_minus_1][x_plus_1] == 1: counter += 1
    if grid[z_plus_1][y_minus_1][x_minus_1] == 1: counter += 1
    if grid[z_plus_1][y][x_minus_1] == 1: counter += 1
    if grid[z_plus_1][y_minus_1][x] == 1: counter += 1
    if grid[z_plus_1][y][x_plus_1] == 1: counter += 1
    if grid[z_plus_1][y_plus_1][x] == 1: counter += 1
    if grid[z_plus_1][y_plus_1][x_plus_1] == 1: counter += 1
    if grid[z_plus_1][y_plus_1][x_minus_1] == 1: counter += 1
    if grid[z_plus_1][y_minus_1][x_plus_1] == 1: counter += 1

    return counter


def kill(grid):  # kills if the number of alive neighbours is other than 2 or 3

    gridkilled = zeros(10, 10, 10)
    for z in range(len(grid)):
        for y in range(len(grid)):
            for x in range(len(grid)):
                gridkilled[z][y][x] = grid[z][y][x]
                if grid[z][y][x] == 1:
                    a_counter = alive_neighbour_counter(z, y, x)
                    if a_counter:
                        gridkilled[z][y][x] = 0

    return gridkilled


def come_to_life(grid):  # brings to life if there are exactly 3 alive neighbours
    gridcametolife = zeros(10, 10, 10)

    for z in range(len(grid)):
        for y in range(len(grid)):
            for x in range(len(grid)):
                if grid[z][y][x] == 0:

                    ancounter = alive_neighbour_counter(z, y, x)
                    if ancounter == 4:
                        gridcametolife[z][y][x] = 1

    return gridcametolife


# set up window display:
animation = canvas(width=600, height=600, title="3D game of life", background=vec(0.1, 0.7, 0.63), range=15)

# boxlist is a 3D list corresponding to grid, which holds the box objects

X = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Y = [X, X, X, X, X, X, X, X, X, X]
boxlist = [Y, Y, Y, Y, Y, Y, Y, Y, Y, Y]

# set up the initial state of the system (0 means 'dead', 1 means 'alive'):

grid = zeros(10, 10, 10)
grid[2][2][1] = grid[2][2][3] = grid[2][2][5] = 1
grid[3][3][1] = grid[3][3][2] = grid[3][3][3] = 1
grid[2][3][3] = 1
grid[3][3][4] = 1

while True:

    rate(2)  # set number of times loop is repeated per second

    for obj in animation.objects:
        obj.visible = 0  # erase all the boxes

    gridkilled = kill(grid)
    gridcametolife = come_to_life(grid)

    for z in range(len(grid)):
        for y in range(len(grid)):
            for x in range(len(grid)):
                if gridkilled[z][y][x] == gridcametolife[z][y][x] == 1:
                    grid[z][y][x] = 1
                else:
                    grid[z][y][x] = gridkilled[z][y][x] + gridcametolife[z][y][x]

                if grid[z][y][x] == 1:
                    boxlist[z][y][x] = box(pos=vec(x, y, z), length=0.8, height=0.8, width=0.8,
                                           color=vec(0.8, 0.1, 0.18))  # draw new boxes
