#Web VPython 3.2

from vpython import scene, curve, color, vector, arrow, arange, ring, pi, vec, label

title = """Add electric field of concentric rings to get E of disk on axis

&#x2022; Original <a href="https://lectdemo.github.io/virtual/15_E_disk_add_rings.html">15_E_disk_add_rings.py</a> by Ruth Chabay 2004
&#x2022; Maintained by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>
&#x2022; &lt;s&gt; &rarr; screenshot
&#x2022; &lt;v&gt; &rarr; verbose output
&#x2022; &lt;space&gt; &rarr; toggle background color
&#x2022; &lt;mouse click&gt; &rarr; add charged rings one mouse click at a time

"""

class Axis:
    def __init__(self, size):
        self._x_axis = arrow(pos=vec(0, 0, 0), axis=vec(size / 5, 0, 0), color=color.yellow, shaftwidth=0.1)
        self._y_axis = arrow(pos=vec(0, 0, 0), axis=vec(0, size / 5, 0), color=color.yellow, shaftwidth=0.1)
        self._z_axis = arrow(pos=vec(0, 0, 0), axis=vec(0, 0, size / 5), color=color.yellow, shaftwidth=0.1)
        self._x_axis_label = label(pos=vec(1, 0, 0), text="x", box=False, color=color.green)
        self._y_axis_label = label(pos=vec(0, 1, 0), text="y", box=False, color=color.green)
        self._z_axis_label = label(pos=vec(0, 0, 1), text="z", box=False, color=color.green)
        curve(pos=[vec(-size, 0, 0), vec(size, 0, 0), vec(0, 0, 0), vec(0, -size, 0), vec(0, size, 0), vec(0, 0, 0),
                   vec(0, 0, -size), vec(0, 0, size)], color=color.green)


def toggle_background():
    scene.background = color.white if scene.background is color.black else color.black

def on_key_press(event):
    if event.key == " ":
        toggle_background()
    if event.key == 's':
        scene.capture("electric_field_of_charged_disk")
    if event.key == 'v':
        print("scene.center=" + str(scene.center))
        print("scene.forward=" + str(scene.forward))
        print("scene.range=" + str(scene.range))

scene.title = title
scene.background = color.black
scene.width = 1024
scene.height = 768
scene.forward = vector(-0.5, -0.60, -0.65)
scene.range = 5.0
#scene.autoscale = 0
##scene.caption = "\\(  \\)"
scene.bind('keydown', on_key_press)

axes = Axis(4)
observer_location = vector(0, 0, 0)
scale_factor = 1
electric_field_arrow = arrow(pos=observer_location, axis=vector(0, 0, 0), shaftwidth=0.3, color=color.orange)
for ring_radius in arange(0.2, 5, 0.2):
    scene.waitfor("click")
    ring(pos=vector(-3, 0, 0), radius=ring_radius, color=color.red, thickness=0.09)
    x = observer_location.x
    electric_field_magnitude = 2 * pi * ring_radius / (ring_radius * ring_radius + (x + 2 ) * (x + 2)) ** 1.5
    electric_field_arrow.axis += scale_factor * electric_field_magnitude * vector(1, 0, 0)
