#Web VPython 3.2
from vpython import box, vec, rate, color, canvas, random, slider

title = """&#x2022; Based on <a href="https://beltoforion.de/de/unterhaltungsmathematik/2d-wellengleichung.php">this example</a> from <a href="https://github.com/beltoforion/recreational_mathematics_with_python">Recreational Mathematics with Python</a>
&#x2022; Ported to <a href="https://vpython.org/">VPython</a> by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in <a href="https://github.com/zhendrikse/science/blob/main/nature/code/raindrop_waves.py">raindrop_waves.py</a>

"""

dim_x, dim_y = 150, 100
display = canvas(width=600, height=400, range=.5 * dim_x, center=vec(dim_x / 2, dim_y / 2, 0), forward=vec(0, .85, -.5),
                 background=color.gray(0.075), title=title)
MathJax.Hub.Queue(["Typeset", MathJax.Hub])

dh = 1  # spatial step width
dt = 1  # time step width
raindrop_frequency = 0.02

def init_simulation():
    c = 0.5  # The "original" wave propagation speed
    u = [[[0. for _ in range(dim_y)] for _ in range(dim_x)] for _ in range(3)]  # The three-dimensional simulation grid
    colors = [[[0. for _ in range(dim_y)] for _ in range(dim_x)] for _ in range(3)]

    wave_propagation_velocity = ((c * dt) / dh) ** 2
    alpha = [[wave_propagation_velocity for _ in range(dim_y)] for _ in range(dim_x)]
    return u, alpha, colors


def timestep(u, alpha):
    for i in range(dim_x):
        for j in range(dim_y):
            u[2][i][j] = u[1][i][j]
            u[1][i][j] = u[0][i][j]

    for c in range(1, dim_x - 1):
        for r in range(1, dim_y - 1):
            u[0][c][r] = alpha[c][r] * (u[1][c - 1][r] + u[1][c + 1][r] + u[1][c][r - 1] + u[1][c][r + 1] - 4 * u[1][c][r])
            u[0][c][r] += 2 * u[1][c][r] - u[2][c][r]

    # Not part of the wave equation, but we need to remove energy from the system.
    # The boundary conditions are closed. Energy cannot leave and the simulation keeps adding energy.
    for i in range(1, dim_x - 1):
        for j in range(1, dim_y - 1):
            u[0][i][j] *= 0.995


def place_raindrops(grid):
    if random() > raindrop_frequency:
        return

    x = int(5 + random() * (dim_x - 10))
    y = int(5 + random() * (dim_y - 10))
    # raindrop = sphere(pos=vec(x, y, 100), color=color.cyan)
    # while raindrop.pos.z > 0:
    #     rate(50)
    #     raindrop.pos -= vec(0, 0, 1)
    # raindrop.visible = False

    for i in range(x - 2, x + 2):
        for j in range(y - 2, y + 2):
            grid[0][i][j] = 120


def modify_rain_intensity(event):
    global raindrop_frequency
    raindrop_frequency = event.value


def update(colors, grid):
    for i in range(0, dim_x):
        for j in range(0, dim_y):
            for k in range(3):
                colors[k][i][j] = grid[k][i][j] + 128
                if colors[k][i][j] < 0:
                    colors[k][i][j] = 0
                if colors[k][i][j] > 255:
                    colors[k][i][j] = 255

def update_pixels(grid, alpha, colors, pixels, frame_rate):
    rate(frame_rate)
    place_raindrops(grid)
    timestep(grid, alpha)
    update(colors, grid)

    for x in range(dim_x - 1):
        for y in range(dim_y - 1):
            pixels[x][y].color = vec(colors[0][x][y] * .15, colors[1][x][y] * .3, colors[2][x][y]) / 255


display.append_to_caption("\nRain intensity")
_ = slider(min=0, max=.1, value=raindrop_frequency, bind=modify_rain_intensity)


def main():
    pixels = [[box(pos=vec(r, c, 0), shininess=0) for c in range(dim_y - 1)] for r in range(dim_x - 1)]
    u, alpha, colors = init_simulation()

    while True:
        update_pixels(u, alpha, colors, pixels, 50)


if __name__ == "__main__":
    main()
