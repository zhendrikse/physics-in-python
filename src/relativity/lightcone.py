from vpython import points, vec, color, rate, cone, scene, label
from src.toolbox.axis import Base

title = """Photon moving in space-time

&#x2022; Written by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> 
&#x2022; The code resides in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>

&lt;t&gt; &rarr; toggle visibility of xy-mesh  
&lt;v&gt; &rarr; verbose output
&lt;s&gt; &rarr; screenshot
&lt;space&gt; &rarr; change color-scheme 
&lt;mouse click&gt; &rarr; pause animation

"""

axis = Base(axis_labels=["x", "ct", "y"])
axis.show_xy_mesh()
axis.hide_tick_labels()

light_cone_top = cone(pos=vec(0, 0, 0), radius=0, opacity=0.4, axis=vec(0, -1, 0))
light_cone_bottom = cone(pos=vec(0, -10, 0), radius=10, opacity=0.4, axis=vec(0, 10, 0))
spaceship = label(pos=vec(-3, 0, 0), text="Spaceship", color=color.cyan, box=False)
photon = label(pos=vec(0, 1, 0), text="Photon", color=color.yellow, box=False)


def on_mouse_click():
    pause_animation()


dt = 1
def pause_animation():
    global dt
    dt += 1
    dt %= 2


def on_key_press(event):
    if event.key == " ":
        animation.background = color.white if animation.background == color.black else color.black
    if event.key == "t":
        axis.toggle_xy_mesh()
    if event.key == 's':
        animation.capture("lightcone_animation")
    if event.key == 'v':
        print("scene.center=" + str(animation.center))
        print("scene.forward=" + str(animation.forward))
        print("scene.range=" + str(animation.range))


animation.bind("keydown", on_key_press)
animation.bind("click", on_mouse_click)
animation.title = title
animation.forward = vec(-0.25, -0.48, -0.83)
animation.range = 14

height = 0
while height <= 11:
    rate (10)
    light_cone_top.pos = vec(0, height, 0)
    light_cone_top.radius = height
    light_cone_top.axis = vec(0, -height, 0)

    height += dt / 5

t = 0
while t < 7:
    rate(5)

    # Update photon
    points(pos=[vec(t * 1.5, t * 1.5, 0)], radius=5, color=color.yellow)
    photon.pos = vec(t * 1.5 + 1, t * 1.5, 0)

    # Update spaceship
    points(pos=[vec(-t * .5, t * 1.5, 0)], radius=3, color=color.cyan)
    spaceship.pos = vec(-t * .3 - 3, t * 1.5, 0)

    t += dt / 5

while True:
    rate(100)
