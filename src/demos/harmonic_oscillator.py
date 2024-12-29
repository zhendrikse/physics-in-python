from vpython import vector, rate, graph, gcurve, color, scene, mag, canvas, hat

from ..toolbox.harmonic_oscillator import HarmonicOscillator
from ..toolbox.ball import Ball

def on_mouse_click():
    global running
    running = not running

def set_scene():
    _ = graph(title="Harmonic oscillator", xtitle="Time", ytitle="Amplitude")
    # scene = canvas(width=500, height=300, align='left')
    scene.bind("click", on_mouse_click)
    scene.title="Click mouse button to start/pause the animation"
    # scene.camera.pos = vector(150, 75, 120)
    # scene.camera.axis = vector(-115, -150, -190)

curve_left = gcurve(color=color.blue)
curve_right = gcurve(color=color.red)
set_scene()

ball_left = Ball(mass=1.0, position=vector(-0, 110, 0), radius=30, color=color.red)
ball_right = Ball(mass=1.0, position=vector(300, 110, 0), radius=30, color=color.cyan)
oscillator = HarmonicOscillator(ball_left, ball_right, spring_constant=10)
oscillator.pull(-100)

dt = 0.1
t = 0
running = False
while True:
    if running:
        rate(1 / dt)
        oscillator.increment_by(dt)
        curve_left.plot(t * dt, oscillator.ball_position_vectors[0].x)
        curve_right.plot(t * dt, oscillator.ball_position_vectors[1].x)
        t += dt
