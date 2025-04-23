# Web VPython 3.2
from vpython import ceil, pi, cos, rate, box, vec, canvas, color, arange, simple_sphere, label, checkbox

title = """&#x2022; Original <a href="https://github.com/NelsonHackerman/Random_python_ideas/blob/main/double%20slit%20experiment.py">double slit experiment.py</a> by <a href="https://github.com/NelsonHackerman">Nelson Hackerman</a>
&#x2022; Ported from PyGame to Glowscript by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a>, see <a href="https://github.com/zhendrikse/science/blob/main/quantumphysics/code/dynamic_double_slit.py">dynamic_double_slit.py</a>

"""

display = canvas(title=title, background=color.gray(0.075), center=vec(700, 350, 0), forward=vec(0, .65, -.75))

slit_size = 6
slit_distance = 10
inter1 = 50 - slit_distance - slit_size
mid_up = 50 - slit_distance
mid_down = 50 + slit_distance
inter2 = 50 + slit_distance + slit_size - 1

wall_x = 70
dx = dy = 0.07
dt = 1 / 50
velocity_source = 0.065 / dt / 1.5
color_range = 3
floor = -0.5


# Equivalent of NumPy outer
def outer_product(v1, v2):
    return [[v1[i] * v2[j] for j in range(len(v2))] for i in range(len(v1))]


def colour(x, range_):
    red = max(0, min(510 / range_ * x, 255))
    blue = max(0, min(510 - 510 / range_ * x, 255))
    return vec(red, 50, blue) / 255


def initialize_simulation(pixels_are_round):
    x = arange(0, 14, dx)
    y = arange(0, 7, dy)
    const1 = [1 for _ in range(len(x))]
    const2 = [1 for _ in range(len(y))]
    xmesh = outer_product(const2, x)
    ymesh = outer_product(y, const1)

    if pixels_are_round:
        return [
            [simple_sphere(pos=vec(xmesh[j][i] * 100 + 50, ymesh[j][i] * 100 + 50, 0), radius=50 * dx, shininess=0) for
             j in range(len(y))] for i in range(len(x))]

    return [[box(pos=vec(xmesh[j][i] * 100 + 50, ymesh[j][i] * 100 + 50, 0),
                 size=vec(ceil(100 * dx), ceil(100 * dy), 1), shininess=0) for j in range(len(y))] for i in
            range(len(x))]


def initialize_meshes(len_x, len_y):
    umesh = outer_product([0 for _ in range(len_y)], arange(0, 14, dx))
    utmesh = [[0. for _ in range(len_x)] for _ in range(len_y)]
    uttmesh = [[0. for _ in range(len_x)] for _ in range(len_y)]
    return umesh, utmesh, uttmesh


# Calculated once and for all, for enhancing performance
velocity_source_2 = velocity_source * velocity_source
dx_2 = dx * dx
dy_2 = dy * dy
pi_2 = pi / 2


def run_simulation(umesh, utmesh, uttmesh, pixels):
    t = 0
    simulation_time = 10
    while t < simulation_time:
        clock.text = "Time remaining: {:1.2f}".format(simulation_time - t)
        t += dt
        rate(50)

        for n in range(1, len(pixels) - 1):
            for m in range(1, len(pixels[0]) - 1):
                uttmesh[m][n] = velocity_source_2 * ((umesh[m][n - 1] + umesh[m][n + 1] - 2 * umesh[m][n]) / dx_2 + (
                        umesh[m - 1][n] + umesh[m + 1][n] - 2 * umesh[m][n]) / dy_2)

        for n in range(1, len(pixels) - 1):
            for m in range(1, len(pixels[0]) - 1):
                utmesh[m][n] += uttmesh[m][n] * dt
                umesh[m][n] += utmesh[m][n] * dt

        # boundary conditions
        umesh[:][0] = umesh[:][1]
        umesh[:][-1] = umesh[:][-2]
        umesh[0][:] = umesh[1][:]
        umesh[-1][:] = umesh[-2][:]

        if t < pi_2:
            for n in range(len(pixels[0])):
                umesh[n][0] = -cos(t * 20) + 1

        umesh[0][0] = umesh[1][1]
        umesh[0][-1] = umesh[1][-2]
        umesh[-1][0] = umesh[-2][1]
        umesh[-1][-1] = umesh[-2][-2]

        for n in range(len(pixels[0])):
            umesh[n][wall_x] = wall_x - 1
            umesh[n][wall_x - 1] = umesh[n][wall_x - 2]
            umesh[n][wall_x + 1] = umesh[n][wall_x + 2]

        for n in range(mid_up, mid_down):
            umesh[n][wall_x] = wall_x - 1
            umesh[n][wall_x - 1] = umesh[n][wall_x - 2]
            umesh[n][wall_x + 1] = umesh[n][wall_x + 2]

        for n in range(inter2, len(pixels[0])):
            umesh[n][wall_x] = wall_x - 1
            umesh[n][wall_x - 1] = umesh[n][wall_x - 2]
            umesh[n][wall_x + 1] = umesh[n][wall_x + 2]

        umesh[inter1][wall_x] = (umesh[inter1][wall_x - 1] + umesh[inter1][wall_x + 1] + umesh[inter1 + 1][wall_x]) / 3
        umesh[mid_up - 1][wall_x] = (umesh[mid_up - 1][wall_x - 1] + umesh[mid_up - 1][wall_x + 1] + umesh[mid_up - 2][
            wall_x]) / 3
        umesh[mid_down][wall_x] = (umesh[mid_down][wall_x - 1] + umesh[mid_down][wall_x + 1] + umesh[mid_down + 1][
            wall_x]) / 3
        umesh[inter2][wall_x] = (umesh[inter2][wall_x - 1] + umesh[inter2][wall_x + 1] + umesh[inter2 - 1][wall_x]) / 3

        for i in range(len(pixels)):
            for j in range(len(pixels[0])):
                pixels[i][j].color = vec(0, 0, 0) if umesh[j][i] == wall_x - 1 else colour(umesh[j][i] - floor, color_range)


use_round_pixels = False


def toggle_square_pixels(event):
    global use_round_pixels
    use_round_pixels = event.checked


display.append_to_caption("\nRound pixels ")
_ = checkbox(bind=toggle_square_pixels, checked=use_round_pixels)

clock = None
while True:
    clock = label(pos=vec(700, 1100, 0), text="Time remaining: 0:00", height=20, box=False, color=color.green)
    pixels = initialize_simulation(use_round_pixels)
    u_mesh, ut_mesh, utt_mesh = initialize_meshes(len(pixels), len(pixels[0]))
    run_simulation(u_mesh, ut_mesh, utt_mesh, pixels)

    popup = label(pos=vec(700, 350, 0), text="Click mouse to restart", height=25, box=False, color=color.yellow)
    display.waitfor("click")
    popup.visible = False
    for obj in display.objects:
        obj.visible = False
        del obj

