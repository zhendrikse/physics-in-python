#Web VPython 3.2
from vpython import canvas, vec, color, rate, simple_sphere, curve, checkbox, sqrt

title = """&#x2022; Fractals inspired by <a href="https://github.com/jeffvun/fractals/">github.com/jeffvun/fractals</a> 
&#x2022; Ported to <a href="https://vpython.org/">VPython</a> by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in <a href="https://github.com/zhendrikse/science/blob/main/mathematics/code/fractals.py">fractals.py</a>

"""

display = canvas(width=600, height=600, background=color.gray(0.075), title=title)

def clear_canvas(range_, center):
    for obj in display.objects:
        obj.visible = False
        del obj
    display.range = range_
    display.center = center

def sierpinski_triangle(order, length, pos):
    if order == 0:
        triangle_ = curve(pos=[pos,
                               pos + vec(length, 0, 0),
                               pos + vec(length/2, length * sqrt(3)/2, 0),
                               pos], color=color.yellow, radius=.01)
        return [triangle_]
    else:
        sierpinski_triangle(order-1, length/2, pos)
        sierpinski_triangle(order-1, length/2, pos + vec(length/2, 0, 0))
        sierpinski_triangle(order-1, length/2, pos + vec(length/4, length * sqrt(3)/4, 0))

def generate_sierpinski_triangle(order=6, length=10):
    clear_canvas(11 * length / 20, vec(0, 0, 0))
    pos=vec(-length / 2, -length * sqrt(3) / 4, 0)
    sierpinski_triangle(order, length, pos)


def t_square(n, x, y, w):
    if n == 0:
        return
    else:
        curve(pos=[vec(x, y, 0), vec(x+w, y, 0), vec(x+w, y+w, 0), vec(x, y+w, 0), vec(x, y, 0)], color=color.yellow)
        new_w = w/3
        t_square(n-1, x+new_w, y+new_w, new_w)
        t_square(n-1, x+new_w, y+new_w*4, new_w)
        t_square(n-1, x+new_w*4, y+new_w*4, new_w)
        t_square(n-1, x+new_w*4, y+new_w, new_w)

def generate_t_square_fractal(n=5):
    clear_canvas(35, vec(30, 30, 0))
    w = 2**n
    t_square(n, 0, 0, w)

def dragon_curve(n):
    if n == 0:
        return [(0, 0), (1, 0)]
    else:
        prev_points = dragon_curve(n-1)
        new_points = []
        for i in range(len(prev_points)-1):
            x1, y1 = prev_points[i]
            x2, y2 = prev_points[i+1]
            dx, dy = x2 - x1, y2 - y1
            if i % 2 == 0:
                new_dx = dy
                new_dy = -dx
            else:
                new_dx = -dy
                new_dy = dx
            new_x, new_y = x1 + dx/2 + new_dx/2, y1 + dy/2 + new_dy/2
            new_points.extend([(x1, y1), (new_x, new_y)])
        new_points.append((1, 0))
        return new_points

def generate_dragon_curve(n=15):
    global display
    clear_canvas(200, vec(105, -40, 0))

    points_ = dragon_curve(n)
    x, y = zip(*points_)
    for i in range(len(x)):
        simple_sphere(pos=250 * vec(x[i], y[i], 0), radius=1, shininess=0, color=color.hsv_to_rgb(vec(i/len(x), 2, 1)))

def dragon_fractal(event):
    t_square_radio.checked = sierpinski_radio.checked = False
    generate_dragon_curve()

def t_square_fractal(event):
    dragon_radio.checked = sierpinski_radio.checked = False
    generate_t_square_fractal()

def sierpinski_fractal(event):
    dragon_radio.checked = t_square_radio.checked = False
    generate_sierpinski_triangle()

display.append_to_caption("\n")

dragon_radio = checkbox(text="Dragon curve ", checked=True, bind=dragon_fractal)
t_square_radio = checkbox(text="T-square fractal ", bind=t_square_fractal)
sierpinski_radio = checkbox(text="Sierpinski ", bind=sierpinski_fractal)

generate_dragon_curve()
while True:
    rate(10)
