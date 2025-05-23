# Web VPython 3.2

from vpython import canvas, vec, cylinder, wtext, slider, rate, arrow, cos, sin, pi, arange, floor, color, sqrt, graph, \
    gcurve, label, checkbox, wtext

title = """Visualization of particle confined by a quadratic well

&#x2022; From <a href="https://www.amazon.com/Visualizing-Quantum-Mechanics-Python-Spicklemire/dp/1032569247">Visualizing Quantum Mechanics with Python</a>
&#x2022; Modified by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a>, located in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>
&#x2022; The motion and $x$-axis represent the parameters $t$ and $x$ respectively
&#x2022; The $y$ and $z$-axis represent the real and imaginary parts of $\\Psi$ respectively
"""

background_info = """
<b>Background</b>: Simple Harmonic Oscillator
"""

animation = canvas(width=600, height=300, align='top', title=title, range=6, center=vec(10, 0, 0))
#MathJax.Hub.Queue(["Typeset", MathJax.Hub])


# For complex numbers
# get_library("https://cdnjs.cloudflare.com/ajax/libs/mathjs/14.0.1/math.js")

class Complex:
    def __init__(self, real, imaginary):
        self._real = real
        self._imaginary = imaginary

    def multiplied_by(self, factor):
        real = self._real * factor.real() - self._imaginary * factor.imaginary()
        imaginary = self._imaginary * factor.real() + self._real * factor.imaginary()
        return Complex(real, imaginary)

    def real(self):
        return self._real

    def imaginary(self):
        return self._imaginary


def numpy_linspace(start, end, total):
    return arange(start, end, (end - start) / total)


class Wave:
    def __init__(self, psi, linspace):
        self._x = linspace
        self._arrows = [arrow(pos=vec(xval, 0, 0), axis=vec(0, 1, 0), shaftwidth=0.01 * L, color=color.red) for xval in
                        linspace]
        self._psi = psi

    def _get_psi_values(self, t):
        psi_values, phase_values = [], []
        for xval in self._x:
            psi_value, phase = self._psi.value_at(xval, t)
            psi_values.append(psi_value)
            phase_values.append(phase)
        return psi_values, phase_values

    def _psi_squared(self, psi_values):
        abs_psi = []
        for value in psi_values:
            psi_squared = value.real() * value.real() + value.imaginary() * value.imaginary()
            abs_psi.append(psi_squared)

        return abs_psi

    def update_for(self, t):
        psi_values, phase_values = self._get_psi_values(t)
        abs_psi = self._psi_squared(psi_values)
        sum_psi = sum(abs_psi)

        scale = 1.5 * L / sum_psi
        for count in range(len(psi_values)):
            psi_value, phase = psi_values[count], phase_values[count]
            cycles = phase / (2 * pi)
            cycles -= floor(cycles)
            cphase = 2 * pi * cycles
            colour = color.hsv_to_rgb(vec(1.0 - cphase / (2 * pi), 1.0, 1.0))

            self._arrows[count].axis = scale * vec(0, psi_value.real(), psi_value.imaginary()) * 3
            self._arrows[count].color = colour

        return sum([abs_psi[i] / sum_psi * self._x[i] for i in range(len(self._x))])

    def set_linspace_to(self, linspace):
        count = 0
        for xval in linspace:
            self._arrows[count].pos = vec(xval, 0, 0)
            count += 1
        self._x = linspace


class Psi:
    def __init__(self, k, omega, wave_function):
        self._k = k
        self._omega = omega
        self._psi = wave_function

    def value_at(self, x, t):
        k = self._k
        omega = self._omega
        phase = k * x - omega * t
        return self._psi(k, x, omega, t), phase

    def set_wave_function_to(self, new_wave_function, with_k):
        self._psi = new_wave_function
        self._k = with_k


def phase(omega, t):
    return Complex(sin(omega * t), cos(omega * t))


def third_excited_state(k, x, omega, t):
    return Complex(sin(4 * k * x), 0).multiplied_by(phase(-16 * omega, t))


def second_excited_state(k, x, omega, t):
    return Complex(sin(3 * k * x), 0).multiplied_by(phase(-9 * omega, t))


def first_excited_state(k, x, omega, t):
    return Complex(sin(2 * k * x), 0).multiplied_by(phase(-4 * omega, t))


def ground_state(k, x, omega, t):
    return Complex(sin(k * x), 0).multiplied_by(phase(-1 * omega, t))


def superposition(k, x, omega, t):
    real = ground_state_weight * ground_state(k, x, omega, t).real()
    imaginary = ground_state_weight * ground_state(k, x, omega, t).imaginary()
    real += first_state_weight * first_excited_state(k, x, omega, t).real()
    imaginary += first_state_weight * first_excited_state(k, x, omega, t).imaginary()
    real += second_state_weight * second_excited_state(k, x, omega, t).real()
    imaginary += second_state_weight * second_excited_state(k, x, omega, t).imaginary()
    real += third_state_weight * third_excited_state(k, x, omega, t).real()
    imaginary += third_state_weight * third_excited_state(k, x, omega, t).imaginary()
    return Complex(real, imaginary)


ground_state_weight = 1.0


def set_ground_state_weight():
    global ground_state_weight
    ground_state_weight = ground_state_slider.value
    ground_state_text.text = "contribution = " + str(ground_state_weight)


first_state_weight = 1.0


def set_first_state_weight():
    global first_state_weight
    first_state_weight = first_state_slider.value
    first_state_text.text = "contribution = " + str(first_state_weight)


second_state_weight = 0.0


def set_second_state_weight():
    global second_state_weight
    second_state_weight = second_state_slider.value
    second_state_text.text = "contribution = " + str(second_state_weight)


third_state_weight = 0.0


def set_third_state_weight():
    global third_state_weight
    third_state_weight = third_state_slider.value
    third_state_text.text = "contribution = " + str(third_state_weight)


def toggle_info(event):
    if event.checked:
        # animation.width = 1200
        animation.caption = background_info
        MathJax.Hub.Queue(["Typeset", MathJax.Hub])  # , animation.title])  # LaTeX formatting
    else:
        # animation.width = 600
        animation.caption = ""
        MathJax.Hub.Queue(["Typeset", MathJax.Hub])  # , animation.title])  # LaTeX formatting


_ = checkbox(pos=animation.title_anchor, text="Show more background information in the caption", bind=toggle_info,
             checked=False)
animation.append_to_title("\n\n$\\Psi = \\sin(kx)e^{-i\\omega t}$")
ground_state_slider = slider(pos=animation.title_anchor, text="Ground state", value=1.0, min=0, max=1,
                             bind=set_ground_state_weight)
ground_state_text = wtext(pos=animation.title_anchor, text="contribution = 1")

animation.append_to_title("\n\n$\\Psi = \\sin(2kx)e^{-4i\\omega t}$")
first_state_slider = slider(pos=animation.title_anchor, text="First excited state", value=1.0, min=0, max=1,
                            bind=set_first_state_weight)
first_state_text = wtext(pos=animation.title_anchor, text="contribution = 1")

animation.append_to_title("\n\n$\\Psi = \\sin(3kx)e^{-9i\\omega t}$")
second_state_slider = slider(pos=animation.title_anchor, text="Second excited state", value=0.0, min=0, max=1,
                             bind=set_second_state_weight)
second_state_text = wtext(pos=animation.title_anchor, text="contribution = 0")

animation.append_to_title("\n\n$\\Psi = \\sin(4kx)e^{-16i\\omega t}$")
third_state_slider = slider(pos=animation.title_anchor, text="Third excited state", value=0.0, min=0, max=1,
                            bind=set_third_state_weight)
third_state_text = wtext(pos=animation.title_anchor, text="contribution = 0")

animation.append_to_title("\n\n")
animation.append_to_caption("\n\n")

frequency = 2
a = 15

left = cylinder(pos=vec(-0.5, -3, 0), axis=vec(0, 6, 0), radius=0.1, color=color.yellow)
right = cylinder(pos=vec(a, -3, 0), axis=vec(0, 6, 0), radius=0.1, color=color.yellow)
info = label(pos=vec(a / 2, 3, 0), text="Click mouse to restart", box=False, color=color.yellow, visible=False)

psi = Psi(k=pi / a, omega=2 * pi / frequency, wave_function=superposition)
wave = Wave(psi, numpy_linspace(-a / 2, a / 2, 80))

t = 0
dt = 0.002
while True:
    gd = graph(title="Probability finding the particle at x", xtitle="t", ytitle="<x>", width=640, height=300)
    gr = gcurve(color=color.red)

    while t < 10:
        rate(100)
        gr.plot(t, wave.update_for(t))
        t += dt

    info.visible = True
    animation.waitfor("click")
    info.visible = False
    gr.delete()
    gd.delete()
    t = 0
