# Web VPython 3.2

from vpython import canvas, color, vec, pi, rate, checkbox, wtext, slider

from src.toolbox.axis import Base
from src.toolbox.plane_wave import PlaneWave

title = """Visualization of plane waves \\( \psi(x, t) = A \cdot e^{k x -i \omega t} \\)

&#x2022; From <a href="https://www.amazon.com/Visualizing-Quantum-Mechanics-Python-Spicklemire/dp/1032569247">Visualizing Quantum Mechanics with Python</a>
&#x2022; Modified by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a>, located in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>
&#x2022; The motion and x-axis represent the parameters \\(t \\text{ and } x\\) respectively
&#x2022; The colors represent the wave number \\( k \\)

"""

animation = canvas(forward=vec(0.37, -0.55, -0.75), width=600, height=450, align='top', background=color.black,
                   title=title, range=11.5)

animation.append_to_caption("\n")

def toggle_tick_marks(event):
    axis.tick_marks_visible(event.checked)


def toggle_tick_labels(event):
    axis.tick_labels_visible(event.checked)


def toggle_xz_mesh(event):
    axis.xz_mesh_visible(event.checked)


def toggle_xy_mesh(event):
    axis.xy_mesh_visible(event.checked)


def toggle_axis(event):
    axis.axis_visible(event.checked)


def adjust_k():
    complex_function.set_k_to(k_slider.value)
    k_slider_text.text = str(round(k_slider.value / pi)) + " * π"


def adjust_amplitude():
    complex_function.set_amplitude_to(amplitude_slider.value)
    amplitude_slider_text.text = str(amplitude_slider.value) + " units"


def adjust_omega():
    complex_function.set_omega_to(omega_slider.value)
    omega_slider_text.text = str(round(omega_slider.value / pi, 2)) + " * π"


omega_slider = slider(min=0, max=6 * pi, value=2 * pi, bind=adjust_omega)
animation.append_to_caption(" Omega = ")
omega_slider_text = wtext(text="2 * π")
animation.append_to_caption("\n\n")

k_slider = slider(min=-2 * pi / 3, max=2 * pi / 3, value=2 * pi / 5, bind=adjust_k)
animation.append_to_caption(" Wave number k = ")
k_slider_text = wtext(text="2 * π  / 5")
animation.append_to_caption("\n\n")

amplitude_slider = slider(min=1, max=6, value=3, bind=adjust_amplitude)
animation.append_to_caption(" Amplitude = ")
amplitude_slider_text = wtext(text="3 units")
animation.append_to_caption("\n\n")

_ = checkbox(text='Tick marks', bind=toggle_tick_marks, checked=True)
_ = checkbox(text='Tick labels', bind=toggle_tick_labels, checked=False)
_ = checkbox(text='XZ mesh', bind=toggle_xz_mesh, checked=True)
_ = checkbox(text='XY mesh', bind=toggle_xy_mesh, checked=False)
_ = checkbox(text='Axis', bind=toggle_axis, checked=True)

axis = Base(length=16, axis_labels=["x", "Re(ψ)", "Im(ψ)"])
axis.hide_tick_labels()
axis.show_xz_mesh()
complex_function = PlaneWave()

dt = 0.01
t = 0
while True:
    rate(30)
    complex_function.update(t)
    t += dt