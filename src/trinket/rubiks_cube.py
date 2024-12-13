#
# Refactored from 
# https://github.com/mtking2/VPython-Rubiks-Cube/blob/master/PyCube.py
#
from vpython import canvas, box, color, dot, cross, acos, textures, vector, rate, pi, local_light, sphere

cube_scene = canvas(title="PyCube", pos=vector(0, 0, 0),
                width=750, height=550,
                center=vector(0, 0, 0), background=vector(0, 0, 0))


def make_walls():
    # length_wall
    box(texture=textures.wood, pos=vector(0, 0, -25),
        length=55, height=25, width=5)

    # floor
    box(texture=textures.wood, pos=vector(0, -15, 0),
        length=55, height=5, width=55)

    # width_wall
    box(texture=textures.wood, pos=vector(-25, 0, 0),
        length=5, height=25, width=55)


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


# Map keyboard keys to respective faces.
faces = {'r': (color.red, vector(1, 0, 0)),
         'l': (color.orange, vector(-1, 0, 0)),
         'b': (color.yellow, vector(0, 0, -1)),
         'u': (vector(0.2, 0.2, 0.8), vector(0, 1, 0)),
         'f': (color.white, vector(0, 0, 1)),
         'd': (vector(0.2, 0.8, 0.2), vector(0, -1, 0))}

# Create colored stickers on each face, one layer at a time.
stickers = []
for face_color, axis in faces.values():
    for x in (-1, 0, 1):
        for y in (-1, 0, 1):
            sticker = box(texture=textures.metal, color=face_color, pos=vector(x, y, 1.52),
                          length=0.85, height=0.85, width=0.03)
            cos_angle = dot(vector(0, 0, 1), axis)
            pivot = (cross(vector(0, 0, 1), axis) if cos_angle == 0 else vector(1, 0, 0))
            sticker.rotate(angle=acos(cos_angle), axis=pivot, origin=vector(0, 0, 0))
            stickers.append(sticker)

            back = box(color=color.gray(0.1), texture=textures.granite, pos=vector(x, y, 1),
                       length=1, height=1, width=1)
            back.rotate(angle=acos(cos_angle), axis=pivot, origin=vector(0, 0, 0))
            stickers.append(back)


make_walls()
make_lights()

fps = 10

def key_pressed(event):
    key = event.key
    if key.lower() in faces:
        face_color, axis = faces[key.lower()]
        angle = (pi / 2) if key.isupper() else (3 * pi / 2)
        r = 0
        while r < angle:
            rate(fps * 6)
            for sticker in stickers:
                if dot(sticker.pos, axis) > 0.5:
                    sticker.rotate(angle=angle/fps, axis=axis, origin=vector(0, 0, 0))    
            r += angle / fps

cube_scene.bind('keydown', key_pressed)

while True:
    pass
