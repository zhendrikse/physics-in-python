# Available on GitHub: https://github.com/zhendrikse/physics-in-python
#
# Refactored from Dot Physics
# - https://www.youtube.com/watch?v=ExxDuRTIe0E
# - https://trinket.io/glowscript/58d3d4ba0b

from vpython import vector, rate, box, graph, gcurve, color

from toolbox.ball import Ball
from toolbox.spring import Spring 

gravitational_force_vector = vector(0, -9.8, 0)

g1 = graph(title="Ball on spring", xtitle="Time", ytitle="Height", width=400, height=250)
curve = gcurve(color=color.blue)

floor = box(pos=vector(0, 0, 0), size=vector(2, 0.05, 1))
ball = Ball(position=vector(0, 2.4, 0))
spring = Spring()

def main():
  dt = 0.01
  for i in range(0, 500):
    rate(100)
    gravitational_force = ball.mass * gravitational_force_vector
    ball.move(spring.force(ball.position) + gravitational_force, dt)
    spring.update(ball.position)
    curve.plot(i * dt, ball.position.y)

if __name__=="__main__":
    main()
