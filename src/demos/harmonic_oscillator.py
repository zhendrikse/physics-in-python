from vpython import vector, rate, graph, gcurve, color, button, scene, canvas
from toolbox.ball import Ball
from toolbox.spring import Spring

running = False

def set_scene():
    global scene
    scene = canvas(width=500, height=300, align='left')
    b1 = button(text="Run", bind=Run, background=color.cyan)
    position_plot = graph(title="", xtitle="Time", ytitle="Amplitude")
    # scene.camera.pos = vector(150, 75, 120)
    # scene.camera.axis = vector(-115, -150, -190)

def Run(r):
    global running
    running = not running
    r.text = "Pause" if running else "Run"

set_scene()

curve_left = gcurve(color=color.blue)
curve_right = gcurve(color=color.red)

left_ball  = Ball(mass=1.0, position=vector(-150, 0, 0), radius=30, color=color.red)
right_ball = Ball(mass=1.0, position=vector( 150, 0, 0), radius=30, color=color.blue)
distance = left_ball.distance_to(right_ball)
spring = Spring(position=-distance / 2, axis=distance, spring_constant=1.0, equilibrium_size=200.0, radius=20, thickness=3)

dt = 0.1
t = 0
while True:
  if running:
      rate(2/dt)
      right_ball.move(spring.force, dt)
      left_ball.move(-spring.force, dt)
      distance = left_ball.distance_to(right_ball)
      spring.update(distance, -distance / 2)
      curve_left.plot(t * dt, left_ball.position.x)
      curve_right.plot(t * dt, right_ball.position.x)
      t += dt
