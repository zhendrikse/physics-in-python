# Available on GitHub: https://github.com/zhendrikse/physics-in-python
#
# Refactored from Dot Physics
# - https://www.youtube.com/watch?v=2BisyQhNBFM

from vpython import vector, color, rate, graph, gcurve, textures, sqrt, mag, norm, canvas
from src.toolbox.celestial_object import Earth, Moon
from src.toolbox.mouse import zoom_in_on

def on_mouse_click():
    zoom_in_on(scene)


scene = canvas(title="Earth-moon orbit")
scene.bind('click', on_mouse_click)

plot = graph(title="Earth moon",xtitle="t [s]",ytitle="Px [kg*m/s]",width=400, height=200)
moon_curve = gcurve(color=color.blue)
earth_curve = gcurve(color=color.red)
sum_curve = gcurve(color=color.green)

moon  = Moon()
earth = Earth()

fifty_days = 50 * 24 * 60 * 60
dt = 500
for day in range(0, fifty_days, dt):
  rate(1000)
  moon.move(moon.force_between(earth), dt)
  earth.move(-moon.force_between(earth), dt)

  moon_curve.plot(day, moon.momentum.y)
  earth_curve.plot(day, earth.momentum.y)
  sum_curve.plot(day, moon.momentum.y + earth.momentum.y)
