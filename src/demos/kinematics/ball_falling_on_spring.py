# Available on GitHub: https://github.com/zhendrikse/physics-in-python
#
# Refactored from Dot Physics
# - https://www.youtube.com/watch?v=ExxDuRTIe0E
# - https://trinket.io/glowscript/58d3d4ba0b

from vpython import vector, rate, box, graph, gcurve, color, mag, button

from src.toolbox.ball import Ball
from src.toolbox.spring import Spring

running = False


def run(button_instance):
    global running
    running = not running
    button_instance.text = "Pause" if running else "Run"


b1 = button(text="Run", bind=run, background=color.cyan)
position_plot = graph(title="Ball on spring", xtitle="Time", ytitle="Height", width=400, height=250)
curve = gcurve(color=color.blue)

spring_size = 0.7
spring_rest_position = vector(0, spring_size, 0)

floor = box(pos=vector(0, 0, 0), size=vector(2, 0.05, 1), color=color.green)
ball = Ball(position=vector(0, 2 + spring_size, 0), colour=color.red, radius=0.15)
spring = Spring(axis=spring_rest_position, spring_constant=1000, radius=0.1, thickness=0.06)

gravitational_force = vector(0, -9.8 * ball.mass, 0)


def main():
    dt = 0.01
    t = 0
    while True:
        if running:
            rate(1 / (2 * dt))
            ball.move(spring.force + gravitational_force, dt)
            spring_axis = ball.position if mag(ball.position) - spring_size < 0 else spring_rest_position
            spring.update(spring_axis)

            curve.plot(t * dt, ball.position.y)
            t += dt


if __name__ == "__main__":
    main()
