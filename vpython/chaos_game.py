#Web VPython 3.2
from vpython import canvas, vec, color, rate, points, radio, random, slider, sin, cos, pi

title = """&#x2022; <a href="https://github.com/zhendrikse/science/blob/main/mathematics/code/chaos_game.py">chaos_game.py</a> by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a>
&#x2022; Inspired by <a href="https://github.com/nnakul/chaos-game/tree/master">nnakul/chaos-game</a> by <a href="https://github.com/nnakul/">Nikhil Nakul</a>

"""

display = canvas(width=600, height=600, title=title, background=color.gray(0.075))

def clear_canvas(range_, center):
    for obj in display.objects:
        obj.visible = False
        del obj
    display.range = range_
    display.center = center

def sierpinski_triangle(a1=-.5, b1=-.433, a2=.5, b2=-.433, a3=0, b3=.3):
    #          (a3, b3)
    #             /\
    #            /  \
    #           /    \
    #          /      \
    #         /________\
    # (a1, b1)           (a2, b2)

    clear_canvas(.5, vec(0, -0.1, 0))
    pixels = points(radius=1.5)
    x, y, colour = 0, 0.3, color.red

    jump_points = [(a1, b1), (a2, b2), (a3, b3)]
    colors = [color.green, color.cyan, color.red]
    for i in range(40000):
        rate(frame_rate)
        index = int(random() * 3)
        x = .5 * (x + jump_points[index][0])
        y = .5 * (y + jump_points[index][1])
        pixels.append(pos=vec(x, y, 0), color=colors[index])

def vicsek_fractal(a1=-1, b1=-1, a2=-1, b2=1, a3=1, b3=1, a4=1, b4=-1, a5=0, b5=0):
    clear_canvas(1.25, vec(0, 0, 0))
    pixels = points(radius=1.5)
    x, y, colour = 0, 0.3, color.red

    jump_points = [(a1, b1), (a2, b2), (a3, b3), (a4, b4), (a5, b5)]
    colors = [color.green, color.cyan, color.red, color.yellow, color.orange]
    for i in range(40000):
        rate(frame_rate)
        index = int(random() * 5)
        x = (x + 2 * jump_points[index][0]) / 3
        y = (y + 2 * jump_points[index][1]) / 3
        pixels.append(pos=vec(x, y, 0), color=colors[index])

def cantor_dust(a1=-1, b1=-1, a2=-1, b2=1, a3=1, b3=1, a4=1, b4=-1):
    # (a2, b2)   (a3, b3)
    #    +--------+
    #    |        |
    #    |        |
    #    +--------+
    # (a1, b1)   (a4, b4)

    clear_canvas(1.25, vec(0, 0, 0))
    pixels = points(radius=1.5)
    x, y, colour = 0, 0.3, color.red

    jump_points = [(a1, b1), (a2, b2), (a3, b3), (a4, b4)]
    colors = [color.green, color.cyan, color.red, color.yellow, color.orange]
    for i in range(40000):
        rate(frame_rate)
        index = int(random() * 4)
        x = .45 * (x + jump_points[index][0])
        y = .45 * (y + jump_points[index][1])
        pixels.append(pos=vec(x, y, 0), color=colors[index])

def fractal_1(a1=-1, b1=-1, a2=-1, b2=1, a3=1, b3=1, a4=1, b4=-1):
    clear_canvas(1.25, vec(0, 0, 0))
    pixels = points(radius=1.5)
    x, y, colour = 0, 0.3, color.red
    current_vertex = int(random() * 4)

    jump_points = [(a1, b1), (a2, b2), (a3, b3), (a4, b4)]
    colors = [color.green, color.cyan, color.red, color.yellow]
    for i in range(40000):
        rate(frame_rate)
        x = .5 * (x + jump_points[current_vertex][0])
        y = .5 * (y + jump_points[current_vertex][1])

        pixels.append(pos=vec(x, y, 0), color=colors[current_vertex])

        sample = [0, 1, 2, 3]
        sample.remove(current_vertex)
        current_vertex = sample[int(random() * 3)]

def fractal_2():
    clear_canvas(.45, vec(.5, .5, 0))
    pixels = points(radius=1.5)
    x, y, colour = 0, 0.3, color.red
    current_vertex = int(random() * 4)

    w = 1
    theta = 2 * pi / 5

    p1 = (w / 2, 0)
    p2 = (w * 0.5 * (1 + sin(theta)), w * 0.5 * (1 - cos(theta)))
    p3 = (w * 0.5 * (1 + sin(theta / 2)), w * 0.5 * (1 + cos(theta / 2)))
    p4 = (w * 0.5 * (1 - sin(theta / 2)), w * 0.5 * (1 + cos(theta / 2)))
    p5 = (w * 0.5 * (1 - sin(theta)), w * 0.5 * (1 - cos(theta)))
    jump_points = [p1, p2, p3, p4, p5]
    colors = [color.green, color.cyan, color.red, color.yellow, color.orange]
    for i in range(40000):
        rate(frame_rate)
        x = .5 * (x + jump_points[current_vertex][0])
        y = .5 * (y + jump_points[current_vertex][1])

        pixels.append(pos=vec(x, y, 0), color=colors[current_vertex])

        sample = [0, 1, 2, 3, 4]
        sample.remove(current_vertex)
        current_vertex = sample[int(random() * 4)]

def t_square(a1=-1, b1=-1, a2=-1, b2=1, a3=1, b3=1, a4=1, b4=-1):
    # (a2, b2)   (a3, b3)
    #    +--------+
    #    |        |
    #    |        |
    #    +--------+
    # (a1, b1)   (a4, b4)

    clear_canvas(1.25, vec(0, 0, 0))
    pixels = points(radius=1.5)
    x, y, colour = 0, 0.3, color.red
    current_vertex = int(random() * 4)

    jump_points = [(a1, b1), (a2, b2), (a3, b3), (a4, b4)]
    colors = [color.green, color.cyan, color.red, color.yellow]
    for i in range(40000):
        rate(frame_rate)
        x = .5 * (x + jump_points[current_vertex][0])
        y = .5 * (y + jump_points[current_vertex][1])

        pixels.append(pos=vec(x, y, 0), color=colors[current_vertex])

        sample = [0, 1, 2, 3]
        if current_vertex == 0:
            sample.remove(2)
        elif current_vertex == 1:
            sample.remove(3)
        elif current_vertex == 2:
            sample.remove(0)
        elif current_vertex == 3:
            sample.remove(1)
        current_vertex = sample[int(random() * 3)]

def sierpinski_carpet(a1=-1, b1=-1, a2=-1, b2=1, a3=1, b3=1, a4=1, b4=-1):
    # (a2, b2)   (a3, b3)
    #    +--------+
    #    |        |
    #    |        |
    #    +--------+
    # (a1, b1)   (a4, b4)

    clear_canvas(1.25, vec(0, 0, 0))
    pixels = points(radius=1.5)
    x, y, colour = 0, 0.3, color.red

    jump_points = [(a1, b1), (a2, b2), (a3, b3), (a4, b4), (a1, b1 + b2), (a4, b3 + b4), (a1 + a4, b1), (a2 + a3, b2)]
    colors = [color.green, color.white, color.yellow, color.red, color.purple, color.cyan, color.magenta, color.orange]
    for i in range(40000):
        rate(frame_rate)
        index = int(random() * 8)
        x = (x + 2 * jump_points[index][0]) / 3
        y = (y + 2 * jump_points[index][1]) / 3
        pixels.append(pos=vec(x, y, 0), color=colors[index])


class RadioButton:
    def __init__(self, button_, function_):
        self._button = button_
        self._function = function_

    def uncheck(self):
        self._button.checked = False

    def push(self):
        radio_buttons.disable()
        self._function()
        radio_buttons.enable()
        #MathJax.Hub.Queue(["Typeset", MathJax.Hub])

    def check(self):
        self._button.checked = True

    def name(self):
        return self._button.name

    def enable(self):
        self._button.disabled = False

    def disable(self):
        self._button.disabled = True


class RadioButtons:
    def __init__(self):
        self._radio_buttons = []
        self._selected_button = None

    def enable(self):
        for button_ in self._radio_buttons:
            button_.enable()

    def disable(self):
        for button_ in self._radio_buttons:
            button_.disable()

    def add(self, button_, function_):
        self._radio_buttons.append(RadioButton(button_, function_))

        if (len(self._radio_buttons) % 4) == 0:
            display.append_to_caption("\n\n")

        if (len(self._radio_buttons)) == 1:
            self._radio_buttons[0].check()
            self._selected_button = self._radio_buttons[0]

    def _uncheck_buttons_except(self, button_name):
        for button_ in self._radio_buttons:
            if button_.name() != button_name: button_.uncheck()

    def _get_button_by(self, button_name):
        for button_ in self._radio_buttons:
            if button_.name() == button_name: return button_

    def toggle(self, event):
        self._uncheck_buttons_except(event.name)
        self._selected_button = self._get_button_by(event.name)
        self._selected_button.push()

frame_rate = 15000
def change_speed(event):
    global frame_rate
    frame_rate = event.value

display.append_to_caption("\n")
radio_buttons = RadioButtons()
radio_buttons.add(radio(bind=radio_buttons.toggle, text="Sierpinski carpet ", name="carpet"), sierpinski_carpet)
radio_buttons.add(radio(bind=radio_buttons.toggle, text="Vicsek fractal ", name="vicsek"), vicsek_fractal)
radio_buttons.add(radio(bind=radio_buttons.toggle, text="Sierpinski triangle ", name="triangle"), sierpinski_triangle)
radio_buttons.add(radio(bind=radio_buttons.toggle, text="Cantor dust ", name="dust"), cantor_dust)
radio_buttons.add(radio(bind=radio_buttons.toggle, text="T-square ", name="t_square"), t_square)
radio_buttons.add(radio(bind=radio_buttons.toggle, text="Star ", name="fractal_1"), fractal_1)
radio_buttons.add(radio(bind=radio_buttons.toggle, text="Flower ", name="fractal_2"), fractal_2)

display.append_to_caption("\n\nAnimation speed")
_ = slider(min=1000, max=15000, value=15000, bind=change_speed)

#MathJax.Hub.Queue(["Typeset", MathJax.Hub])
radio_buttons.disable()
sierpinski_carpet()
radio_buttons.enable()
while True:
    rate(10)
