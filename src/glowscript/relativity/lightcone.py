from vpython import points, vec, color, rate, cone, scene, label, arrow, cylinder

title = """Photon moving in space-time

&#x2022; Written by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> 
&#x2022; The code resides in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>

&lt;t&gt; &rarr; toggle visibility of xy-mesh  
&lt;v&gt; &rarr; verbose output
&lt;s&gt; &rarr; screenshot
&lt;space&gt; &rarr; change color-scheme 
&lt;mouse click&gt; &rarr; pause animation

"""

x_hat = vec(1, 0, 0)
y_hat = vec(0, 1, 0)
z_hat = vec(0, 0, 1)
base = [x_hat, y_hat, z_hat]
label_text = ("x", "y", "z")

class Base:
    def __init__(self, position=vec(0, 0, 0), axis_color=color.yellow, tick_marks_color=color.red, length=20, num_tick_marks=None, axis_labels=label_text, tick_mark_labels=True, mesh=False):

        num_tick_marks = length - 1 if not num_tick_marks else num_tick_marks
        tick_increment = length / (num_tick_marks - 1)
        radius = length / 200
        self._axis, self._arrows, self._arrow_labels, self._tick_labels = [], [], [], []
        self._position = position

        for base_vec in base:
            self._axis += [cylinder(pos=position - length * base_vec / 2, axis=length * base_vec, radius=radius, color=axis_color)]
            self._arrows += [arrow(pos=position + length * base_vec / 2, axis=base_vec, color=axis_color, shaftwidth=radius)]

        for i in range(len(base)):
            self._arrow_labels.append(label(pos=position + base[i] * (length / 2 + tick_increment), text=axis_labels[i], color=tick_marks_color, box=False))

        offset = [-0.05 * length * y_hat, 0.05 * length * x_hat, -0.05 * length * y_hat]
        positions = []
        for i in range(len(base)):
            for j in range(num_tick_marks):
                pos = position - base[i] * (length  / 2 - j * tick_increment)
                positions.append(pos)
                label_value = pos.x - position.x if i == 0 else pos.y - position.y if i == 1 else pos.z - position.z
                label_value = "" if int(num_tick_marks / 2) == j else str(int(label_value))
                marker = label(pos=pos + offset[i], text=label_value, color=color.gray(0.5), box=False, visible=tick_mark_labels)
                self._tick_labels.append(marker)
        self._tick_marks = points(pos=positions, color=tick_marks_color, radius=radius * 50)

        self._xy_mesh, self._zx_mesh, self._xz_mesh, self._yx_mesh = [], [], [], []
        for j in range(num_tick_marks):
            self._xy_mesh += [cylinder(pos=vec(position.x - length / 2, position.y + j * tick_increment - length /2, position.z), axis=x_hat * length, color=color.gray(.5), radius=radius/2, visible=mesh)]
            self._yx_mesh += [cylinder(pos=vec(position.x - length / 2 + j * tick_increment, position.y - length /2, position.z), axis=y_hat * length, color=color.gray(.5), radius=radius/2, visible=mesh)]
            self._xz_mesh += [cylinder(pos=vec(position.x - length / 2 + j * tick_increment, position.y, position.z - length / 2), axis=z_hat * length, color=color.gray(0.4), radius=radius/2, visible=mesh)]
            self._zx_mesh += [cylinder(pos=vec(position.x - length / 2, position.y, position.z - length / 2 + j * tick_increment), axis=x_hat * length, color=color.gray(0.4), radius=radius/2, visible=mesh)]

    def toggle_xy_mesh(self):
        for i in range(len(self._xy_mesh)):
            self._xy_mesh[i].visible = not self._xy_mesh[i].visible
            self._yx_mesh[i].visible = not self._yx_mesh[i].visible

    def toggle_xz_mesh(self):
        self._xz_mesh.visible = not self._xz_mesh.visible
        self._zx_mesh.visible = not self._zx_mesh.visible


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
