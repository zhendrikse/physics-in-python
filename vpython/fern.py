#Web VPython 3.2
from vpython import points, rate, canvas, color, vector, vec, random, radio
from random import uniform

title = """&#x2022; Based on <a href="https://rosettacode.org/wiki/Barnsley_fern#Python">this example</a> (an alternative <a href="https://code.activestate.com/recipes/577134-fern-ifs-fractal">here</a>) 
&#x2022; See also this <a href="https://www.youtube.com/watch?v=km-ctEk8-lE">video</a> on integrated function systems (IFS)
&#x2022; Adapted to <a href="https://vpython.org/">VPython</a> by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in <a href="https://github.com/zhendrikse/science/blob/main/nature/code/fern.py">fern.py</a>

"""

img_x = 512
img_y = 512
display = canvas(title=title, background=color.gray(0.15), height=600, center=vector(0, +5, 0), fov=0.01)

def clear_canvas(range_, forward, center):
    for obj in display.objects:
        obj.visible = False
    display.forward= forward
    display.range = range_
    display.center = center

class BarnsleyFern:
    def __init__(self, pixel_radius=0.85, paint_color=vec(0, .8, 0)):
        self.paint_color = paint_color
        self.pixels = points(radius=pixel_radius)

    def transform(self, x, y):
        rand = uniform(0, 100)
        if rand < 1:
            return 0, 0.16 * y
        elif 1 <= rand < 86:
            return 0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.6
        elif 86 <= rand < 93:
            return 0.2 * x - 0.26 * y, 0.23 * x + 0.22 * y + 1.6
        else:
            return -0.15 * x + 0.28 * y, 0.26 * x + 0.24 * y + 0.44

    def iterate(self, iterations):
        x, y = 0., 0.
        for _ in range(iterations):
            x, y = self.transform(x, y)
            self.pixels.append(pos=vector(x, y, 0), color=self.paint_color)

class BarnsleyFern3D:
    def __init__(self, pixel_radius=0.95, paint_color=vec(0, .8, 0)):
        self.paint_color = paint_color
        self.pixels = points(radius=pixel_radius)

    def transform(self, x, y, z):
        r = random()
        if r <= 0.1:  # 10% probability
            xn = 0.0
            yn = 0.18 * y
            zn = 0.0
        elif 0.1 < r <= 0.7:  # 60% probability
            xn = 0.85 * x
            yn = 0.85 * y + 0.1 * z + 1.6
            zn = -0.1 * y + 0.85 * z
        elif 0.7 < r <= 0.85:  # 15 % probability
            xn = 0.2 * x - 0.2 * y
            yn = 0.2 * x + 0.2 * y + 0.8
            zn = 0.3 * z
        else:
            xn = -0.2 * x + 0.2 * y  # 15% probability
            yn = 0.2 * x + 0.2 * y + 0.8
            zn = 0.3 * z
        return xn, yn, zn

    def iterate(self, iterations):
        x, y, z = 0.5, 0.0, -0.2
        for i in range(1, iterations):
            x, y, z = self.transform(x, y, z)
            xc = 4.0 * x  # linear TF for plot
            yc = 2.0 * y - 7
            zc = z
            self.pixels.append(pos=vec(xc, yc, zc), color=self.paint_color)


def toggle_fractal(event):
    if event.name == "fern":
        clear_canvas(range_=5.5, forward=vector(0, 0, -1), center=vector(0, 5, 0))
        BarnsleyFern().iterate(100000)
        fern_3d_radio.checked = False
    else:
        clear_canvas(range_=10, forward=vector(-.85, -.13, -.51), center=vector(.93, 1.51, -1.02))
        BarnsleyFern3D().iterate(20000)
        fern_radio.checked = False


display.append_to_caption("\n")
fern_radio = radio(text="Barnsley&apos;s fern ", checked=True, name="fern", bind=toggle_fractal)
fern_3d_radio = radio(text="3D Barnsley&apos;s fern ", checked=False, name="fern_3d", bind=toggle_fractal)

#MathJax.Hub.Queue(["Typeset", MathJax.Hub])
BarnsleyFern().iterate(100000)
while True:
    rate(10)
