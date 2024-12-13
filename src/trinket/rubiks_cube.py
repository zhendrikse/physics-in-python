#
# Refactored from  https://github.com/mtking2/VPython-Rubiks-Cube/blob/master/PyCube.py
# Please also take a look at my Git repo: https://github.com/zhendrikse/physics-in-python/
#
from vpython import canvas, box, color, dot, cross, acos, textures, vector, rate, pi, local_light, sphere

zero_vec = vector(0, 0, 0)
fps = 10

cube_scene = canvas(title="PyCube by Michael King, updated by Zeger Hendrikse", pos=zero_vec, width=750, height=550, center=zero_vec, background=zero_vec)


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

def turn_face(key):
    face_color, axis = faces[key.lower()]
    angle = (pi / 2) if key.isupper() else (-1 * pi / 2)
    r = 0
    while r < abs(angle):
        rate(fps * 6)
        for sticker in stickers:
            if dot(sticker.pos, axis) > 0.5:
                sticker.rotate(angle=angle/fps, axis=axis, origin=zero_vec)    
        r += abs(angle / fps)

def put_sticker_on_face(x, y, face_color):
    sticker = box(texture=textures.metal, color=face_color, pos=vector(x, y, 1.52), length=0.85, height=0.85, width=0.03)
    cos_angle = dot(vector(0, 0, 1), axis)
    pivot = (cross(vector(0, 0, 1), axis) if cos_angle == 0 else vector(1, 0, 0))
    sticker.rotate(angle=acos(cos_angle), axis=pivot, origin=vector(0, 0, 0))
    stickers.append(sticker)

    back = box(color=color.gray(0.1), texture=textures.granite, pos=vector(x, y, 1), length=1, height=1, width=1)
    back.rotate(angle=acos(cos_angle), axis=pivot, origin=vector(0, 0, 0))
    stickers.append(back)

def key_pressed(event):
    key = event.key
    if key.lower() in faces:
        turn_face(key)

def run_demo():
  for key in "uuddllrrffbb":
    turn_face(key)
  for t in range(0, fps * 3):
    rate(fps)
  for key in "uuddllrrffbb":
    turn_face(key)


# Map keyboard keys to respective faces.
faces = {}
faces['u'] = [vector(0.2, 0.2, 0.8), vector(0, 1, 0)] # blue
faces['d'] = [vector(0.2, 0.8, 0.2), vector(0, -1, 0)] # green
faces['r'] = [vector(1, 0, 0), vector(1, 0, 0)] # red
faces['l'] = [vector(1.0, 0.6, 0.4), vector(-1, 0, 0)] # orange
faces['b'] = [vector(1, 1, 0), vector(0, 0, -1)] # yellow
faces['f'] = [vector(1, 1, 1), vector(0, 0, 1)] # white

# Create colored stickers on each face, one layer at a time.
stickers = []
for face_color, axis in faces.values():
    for x in (-1, 0, 1):
        for y in (-1, 0, 1):
            put_sticker_on_face(x, y, face_color)

make_walls()
make_lights()
run_demo()

cube_scene.bind('keydown', key_pressed)
cube_scene.caption = 'Use upper and lower case u, d, l, r, f, b keys to rorate the sides'
