from vpython import vector, rate, box, graph, gcurve, color, mag, button

from ..toolbox.ball import Ball
from ..toolbox.spring import Spring

running = False

def run(button_instance):
    global running
    running = not running
    button_instance.text = "Pause" if running else "Run"

b1 = button(text="Run", bind=run, background=color.cyan)

position_plot = graph(title="Ball on spring", xtitle="Time", ytitle="Height", width=400, height=250)
curve = gcurve(color=color.blue)

spring_size = 1.0
spring_rest_position = vector(0, 0, 0)
ceiling = box(pos=vector(0, 0, 0), size=vector(2, 0.1, 1), color=color.green)
ball = Ball(mass=5.0, position=vector(0, -spring_size - 0.5, 0), radius=0.2, color=color.red)
spring = Spring(axis=ball.position, spring_constant=1000, equilibrium_size=spring_size, radius=0.1, coils=15)#, thickness=0.04)

gravitational_force = vector(0, -9.8 * ball.mass, 0)

def main():
  dt = 0.01
  t = 0
  while True:
     if running:
      rate(1 / (2 * dt))

      ball.move(spring.force + gravitational_force, dt)
      spring.update(ball.position)

      curve.plot(t * dt, ball.position.y)
      t += dt

if __name__=="__main__":
    main()
