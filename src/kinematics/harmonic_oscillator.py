from vpython import vector, rate, graph, gcurve, color, scene, arange

from src.toolbox.harmonic_oscillator import HarmonicOscillator

def set_scene():
    _ = graph(title="Harmonic oscillator", xtitle="Time", ytitle="Amplitude")
    # scene = canvas(width=500, height=300, align='left')
    animation.title= "Click mouse button to start"
    # scene.camera.pos = vector(150, 75, 120)
    # scene.camera.axis = vector(-115, -150, -190)

curve_left = gcurve(color=color.blue)
curve_right = gcurve(color=color.red)
set_scene()

oscillator = HarmonicOscillator(position=vector(0, 1, 0))
oscillator.compress_by(0.75)

t = 0
dt = 0.01
while True:
  animation.waitfor("click")
  for i in arange(0, 10 / dt):
    t += dt
    rate(1/dt)
    oscillator.update_by(dt)
    curve_left.plot(t, oscillator.left_ball_position().x)
    curve_right.plot(t, oscillator.right_ball_position().x)
