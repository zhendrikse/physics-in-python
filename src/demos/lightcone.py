from vpython import points, vec, color, rate, cone, scene, label
from ..toolbox.axis import Base

title = """Photon moving in space-time

&#x2022; Written by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> 
&#x2022; The code resides in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>

&lt;t&gt; &rarr; toggle visibility of xy-mesh  
&lt;v&gt; &rarr; verbose output
&lt;s&gt; &rarr; screenshot
&lt;space&gt; &rarr; change color-scheme 
&lt;mouse click&gt; &rarr; pause animation

"""

axis = Base(mesh=True, axis_labels=["x", "ct", "y"], tick_mark_labels=False)
axis.toggle_xy_mesh()

light_cone_top = cone(pos=vec(0, 10, 0), radius=10, opacity=0.4, axis=vec(0, -10, 0))
light_cone_bottom = cone(pos=vec(0, -10, 0), radius=10, opacity=0.4, axis=vec(0, 10, 0))
spaceship = label(text="Spaceship", color=color.cyan, box=False)
photon = label(text="Photon", color=color.yellow, box=False)

def on_mouse_click():
    pause_animation()


def pause_animation():
    global dt
    dt += 1
    dt %= 2


def on_key_press(event):
    if event.key == " ":
        scene.background = color.white if scene.background == color.black else color.black
    if event.key == "t":
        axis.toggle_xy_mesh()
    if event.key == 's':
        scene.capture("electric_field_of_charged_rings")
    if event.key == 'v':
        print("scene.center=" + str(scene.center))
        print("scene.forward=" + str(scene.forward))
        print("scene.range=" + str(scene.range))


scene.bind("keydown", on_key_press)
scene.bind("click", on_mouse_click)
scene.title = title
scene.forward = vec(-0.25, -0.48, -0.83)
scene.range = 14

t = 0
dt = 1
while t < 7:
    # Update photon
    points(pos=[vec(t * 1.5, t * 1.5, 0)], radius=5, color=color.yellow)
    photon.pos = vec(t * 1.5 + 1, t * 1.5, 0)

    # Update spaceship
    points(pos=[vec(-t * .5, t * 1.5, 0)], radius=3, color=color.cyan)
    spaceship.pos = vec(-t * .3 - 3, t * 1.5, 0)

    rate(2)
    t += dt / 5

while True:
    rate(100)
