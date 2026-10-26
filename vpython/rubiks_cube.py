#Web VPython 3.2

title = """&#x2022; Based on <a href="https://github.com/mtking2/VPython-Rubiks-Cube/blob/master/PyCube.py">PyCube.py</a> and updated by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> to <a href="https://github.com/zhendrikse/science/blob/main/fun/code/rubiks_cube.py">rubiks_cube.py</a>

&#x2022; &lt;u&gt; and &lt;U&gt; &rarr; rotate top face (clockwise and counterclockwise)
&#x2022; &lt;d&gt; and &lt;D&gt; &rarr; rotate bottom face (clockwise and counterclockwise)
&#x2022; &lt;l&gt; and &lt;L&gt; &rarr; rotate left face (clockwise and counterclockwise)
&#x2022; &lt;r&gt; and &lt;R&gt; &rarr; rotate right face (clockwise and counterclockwise)
&#x2022; &lt;f&gt; and &lt;F&gt; &rarr; rotate front face (clockwise and counterclockwise)
&#x2022; &lt;b&gt; and &lt;B&gt; &rarr; rotate back face (clockwise and counterclockwise)

"""

from vpython import canvas, box, color, dot, cross, acos, textures, vector, rate, pi, local_light, sphere

zero_vec = vector(0, 0, 0)
fps = 10

cube_scene = canvas(range=7, title=title, center=zero_vec, background=color.gray(0.075),
                    forward=vector(-0.6, -0.5, -0.65))


def make_walls():
    # length_wall
    box(texture=textures.wood, pos=vector(0, 0, -25), length=55, height=25, width=5)

    # floor
    box(texture=textures.wood, pos=vector(0, -15, 0), length=55, height=5, width=55)

    # width_wall
    box(texture=textures.wood, pos=vector(-25, 0, 0), length=5, height=25, width=55)


def make_lights():
    cube_scene.lights = []
    local_light(pos=vector(25, 15, 25), color=color.gray(0.6))
    # sphere(pos=(25, 15, 25), radius=0.5)

    local_light(pos=vector(-25, 15, -25), color=color.gray(0.4))
    # sphere(pos=(-15, 15, -15), radius=0.5)

    local_light(pos=vector(0, -12, 0), color=color.gray(0.4))
    # sphere(pos=(0, -12, 0), radius=0.5)

    local_light(pos=vector(0, 12, 0), color=color.gray(0.4))
    # sphere(pos=(0, 15, 0), radius=0.5)


def run_demo(cube):
    for i in range(0, 2):
        for t in range(0, fps * 3): rate(fps)
        for key in "uuddllrrffbb": cube.turn_face(key)

    for i in range(0, 3):
        for t in range(0, fps * 3): rate(fps)
        for key in "FbrLuDFb": cube.turn_face(key)


class Cube:
    def __init__(self):
        # Map keyboard keys to respective faces.
        self._faces = {}
        self._faces['u'] = [vector(0.2, 0.2, 0.8), vector(0, 1, 0)]  # blue
        self._faces['d'] = [vector(0.2, 0.8, 0.2), vector(0, -1, 0)]  # green
        self._faces['r'] = [vector(1, 0, 0), vector(1, 0, 0)]  # red
        self._faces['l'] = [vector(1.0, 0.6, 0.4), vector(-1, 0, 0)]  # orange
        self._faces['b'] = [vector(1, 1, 0), vector(0, 0, -1)]  # yellow
        self._faces['f'] = [vector(1, 1, 1), vector(0, 0, 1)]  # white

        # Create colored stickers on each face, one layer at a time.
        self._stickers = []
        for face_color, axis in self._faces.values():
            for x in (-1, 0, 1):
                for y in (-1, 0, 1):
                    self._put_sticker_on_face(x, y, face_color, axis)

    def turn_face(self, key):
        if not key.lower() in self._faces:
            return

        face_color, axis = self._faces[key.lower()]
        angle = (pi / 2) if key.isupper() else (-1 * pi / 2)
        r = 0
        while r < abs(angle):
            rate(fps * 6)
            for sticker in self._stickers:
                if dot(sticker.pos, axis) > 0.5:
                    sticker.rotate(angle=angle / fps, axis=axis, origin=zero_vec)
            r += abs(angle / fps)

    def _put_sticker_on_face(self, x, y, face_color, axis):
        sticker = box(texture=textures.metal, color=face_color, pos=vector(x, y, 1.52), length=0.85, height=0.85,
                      width=0.03)
        cos_angle = dot(vector(0, 0, 1), axis)
        pivot = (cross(vector(0, 0, 1), axis) if cos_angle == 0 else vector(1, 0, 0))
        sticker.rotate(angle=acos(cos_angle), axis=pivot, origin=vector(0, 0, 0))
        self._stickers.append(sticker)

        back = box(color=color.gray(0.1), texture=textures.granite, pos=vector(x, y, 1), length=1, height=1, width=1)
        back.rotate(angle=acos(cos_angle), axis=pivot, origin=vector(0, 0, 0))
        self._stickers.append(back)


cube = Cube()

make_walls()
make_lights()
run_demo(cube)


def on_key_press(event):
    key = event.key
    if key in ['u', 'd', 'r', 'l', 'b', 'f', 'U', 'D', 'R', 'L', 'B', 'F']:
        cube.turn_face(key)


cube_scene.bind('keydown', on_key_press)
