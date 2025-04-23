# Web VPython 3.2
from vpython import box, rate, canvas, vector, sqrt, color, checkbox, cylinder

title = """&#x2022; <a href="https://github.com/zhendrikse/science/blob/main/mathematics/code/mandelbrot.py">mandelbrot.py</a> by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a>

"""

display = canvas(title=title, width=600, height=400, background=color.gray(0.075), range=1)
MathJax.Hub.Queue(["Typeset", MathJax.Hub])

# Parameters
width = 600  # resolution along x-axis
height = 400  # resolution along y-axis
max_iter = 100  # max iterations for Mandelbrot
scale = 0.1  # scale for 3D placement

# Mapping parameters
x_min, x_max = -2.0, 1.0
y_min, y_max = -1.0, 1.0

pixel_width = (x_max - x_min) / width
pixel_height = (y_max - y_min) / height


def complex_(re_, im_):
    return re_, im_


def z_squared_minus_c(z_, c_):
    return z_[0] * z_[0] - z_[1] * z_[1] + c_[0], 2 * z_[0] * z_[1] + c_[1]


def abs_z_squared(z_):
    return z_[0] * z_[0] + z_[1] * z_[1]


def mandelbrot_3d(re, im, z, c):
    n = 0
    while abs_z_squared(z) <= 4 and n < max_iter:
        z = z_squared_minus_c(z, c)
        n += 1

    colour = vector(n / max_iter, 0.3, 1 - n / max_iter)
    brightness = n / max_iter
    voxel_height = 5 * brightness
    # colour = vector(brightness, sqrt(brightness), brightness ** 0.2)

    cylinder(
        pos=vector(re / scale, im / scale, .5 * voxel_height),
        radius=0.08,
        color=colour,
        axis=vector(0, 0, 0.08 / scale),
        shininess=0)


def mandelbrot_2d(re, im, z, c):
    n = 0
    while abs_z_squared(z) <= 4 and n < max_iter:
        z = z_squared_minus_c(z, c)
        n += 1
    brightness = n / max_iter
    if .01 < brightness < 1:
        colour = vector(brightness, sqrt(brightness), brightness ** 0.2)
        size = vector(pixel_width, pixel_height, 0.01)
        box(pos=vector(re, im, 0), color=colour, size=size, shininess=0)


def render_mandelbrot(three_dim=False):
    selector.disabled = True
    step = 0
    for x in range(width):
        if step % 20 == 0:
            # Do a screen refresh so that the user sees what's going on
            rate(10000)
        for y in range(height):
            # Map pixel to complex plane
            re = x_min + (x / width) * (x_max - x_min)
            im = y_min + (y / height) * (y_max - y_min)
            c = complex_(re, im)
            z = complex_(0, 0)
            _ = mandelbrot_3d(re, im, z, c) if three_dim else mandelbrot_2d(re, im, z, c)
        step += 1

    selector.disabled = False


def render(event):
    three_dimensional = event.checked
    for obj in display.objects:
        obj.visible = False
        del obj
    display.range = 15 if three_dimensional else 1
    display.forward = vector(0, .7, -.7) if three_dimensional else vector(0, 0, -1)
    display.center = vector(-6, 0, 0) if three_dimensional else vector(-.5, 0, 0)
    render_mandelbrot(three_dimensional)


selector = checkbox(text="Three dimensional ", checked=False, bind=render)

display.range = 1
display.forward = vector(0, 0, -1)
display.center = vector(-.5, 0, 0)
render_mandelbrot()
while True:
    rate(10)
