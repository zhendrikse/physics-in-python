from vpython import vector, rate, graph, gcurve, color, button, mag, canvas, hat

from ..toolbox.harmonic_oscillator import HarmonicOscillator
from ..toolbox.ball import Ball


def run(button_instance):
    global running
    running = not running
    button_instance.text = "Pause" if running else "Run"


def set_scene():
    position_plot = graph(title="", xtitle="Time", ytitle="Amplitude")
    # scene = canvas(width=500, height=300, align='left')
    b1 = button(text="run", bind=run, background=color.cyan)
    # scene.camera.pos = vector(150, 75, 120)
    # scene.camera.axis = vector(-115, -150, -190)


curve_left = gcurve(color=color.blue)
curve_right = gcurve(color=color.red)
set_scene()

ball_left = Ball(mass=1.0, position=vector(-150, 0, 0), radius=30, color=color.red)
ball_right = Ball(mass=1.0, position=vector(150, 0, 0), radius=30, color=color.blue)
oscillator = HarmonicOscillator(ball_left, ball_right)
oscillator.pull(-100)

dt = 0.1
t = 0
running = False
while True:
    if running:
        rate(2 / dt)
        oscillator.increment_by(dt)
        curve_left.plot(t * dt, oscillator.ball_position_vectors[0].x)
        curve_right.plot(t * dt, oscillator.ball_position_vectors[1].x)
        t += dt
