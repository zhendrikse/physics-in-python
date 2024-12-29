from vpython import curve, box, vector, radians, color, scene, rate, sphere

title = """Symmetry planes in a cubic crystal

&#x2022; Original <a href="https://lectdemo.github.io/virtual/24_crystal_planes.html">24_crystal_planes.py</a> by Ruth Chabay Spring 2001
&#x2022; Maintained by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>
&#x2022; &lt;c&gt; &rarr; toggle wireframe cube
&#x2022; &lt;s&gt; &rarr; screenshot
&#x2022; &lt;v&gt; &rarr; verbose output
&#x2022; &lt;space&gt; &rarr; toggle background color
&#x2022; &lt;mouse click&gt; &rarr; toggle between different symmetry planes

"""

scene.x = scene.y = 0
scene.width = scene.height = 800
scene.forward = vector(1, -0.8, -2)
scene.title = title

class WireFrame:
    def __init__(self, s=5., box_color=vector(0, 1, 1)):
        pts = [vector(-s, -s, -s), vector(-s, -s, s), vector(-s, s, s),
               vector(-s, s, -s), vector(-s, -s, -s), vector(s, -s, -s),
               vector(s, s, -s), vector(-s, s, -s), vector(s, s, -s),
               vector(s, s, s), vector(-s, s, s), vector(s, s, s),
               vector(s, -s, s), vector(-s, -s, s), vector(s, -s, s), vector(s, -s, -s)]
        self._cube = curve(color=box_color, radius=0.05, pos=pts)

    def set_visibility_to(self, true_or_false):
        self._cube.visible = true_or_false

    def toggle_visibility(self):
        self._cube.visible = not self._cube.visible


class SymmetryPlanes:
    def __init__(self):
        self._planes = [box(pos=vector(0, 0, 0), size=vector(6, 0.01, 6), color=color.gray(0.8), visible=False) for _ in
                        range(3)]
        self._current_plane = -1
        self._planes[1].rotate(axis=vector(0, 0, 1), angle=radians(45))
        self._planes[2].rotate(axis=vector(0, 0, 1), angle=radians(90))

    def toggle_visibility(self):
        self._current_plane = 0 if self._current_plane + 1 > 3 else self._current_plane + 1
        for index in range(len(self._planes)):
            self._planes[index].visible = (self._current_plane == index)
        cube.set_visibility_to(self._current_plane == 3)


class Crystal:
    def __init__(self):
        _ = [sphere(pos=vector(x, y, z), radius=0.3, color=vector(1, 0, 1)) for x in range(-2, 3, 2) for z in
             range(-2, 3, 2) for y in range(-2, 3, 2)]
        _ = [sphere(pos=vector(x, y, z), radius=0.3, color=vector(0, 1, 1)) for x in range(-1, 3, 2) for z in
             range(-1, 3, 2) for y in range(-1, 3, 2)]


cube = WireFrame(s=1, box_color=vector(.8, .8, .8))
crystal = Crystal()
symmetry_planes = SymmetryPlanes()


def toggle_background():
    scene.background = color.white if scene.background is color.black else color.black

def toggle_symmetry_planes():
    symmetry_planes.toggle_visibility()

def on_key_press(event):
    if event.key == "c":
        cube.toggle_visibility()
    if event.key == " ":
        toggle_background()
    if event.key == 's':
        scene.capture("crystal_planes")
    if event.key == 'v':
        print("scene.center=" + str(scene.center))
        print("scene.forward=" + str(scene.forward))
        print("scene.range=" + str(scene.range))


scene.bind("keydown", on_key_press)
scene.bind("click", toggle_symmetry_planes)

while 1:
    rate(10)
