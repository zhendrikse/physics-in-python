# Web VPython 3.2

##from random import *
##from visual import *
from vpython import *

"""
Electromagnetism:  Electric Gauss Law
(v3.50) 2022-04-04 Rob Salgado (robertoBsalgado@gmail.com)
(v2.80) 2010-03-22 Rob Salgado (salgado@physics.syr.edu)
Electric Field vectors are orange.
"""

scene = canvas(width=800, height=600, x=0, y=0)

scene.ambient = 0.24 * vec(1, 1, 1)
colorBackground = [color.black, color.white]
colorScheme = 0

scene.background = colorBackground[colorScheme]
scene.title = "GAUSS: Radial E's are associated with ElectricPoint-Charges (n)"
scene.range = 2.5
scene.forward = vec(-0.162765, 0.013403, -0.986574)
scene.autoscale = 1

colorEdimmed = [vec(0.0, 0, 0.4), vec(0.96, 0.96, 0.8)]

electric_field_colors = [color.orange, vec(0.5, 0.5, 1), color.magenta]
electric_field_colors[1] = colorEdimmed[colorScheme]

class ElectricField:
    def __init__(self, arrow_count=24):
        positions = []
        phi_last = 0
        for i in range(0, arrow_count):
            h = -1 + 2 * i / (arrow_count - 1.)
            theta = acos(h)

            q = arrow_count * (1 - h * h)
            phi = 0 if i == 0 or i == arrow_count - 1 else phi_last + 3.6 / sqrt(q)
            phi_last = phi

            positions.append(vector(cos(phi) * sin(theta), sin(phi) * sin(theta), cos(theta)))
            # sp.append( sphere(pos=p[-1],radius=0.05) )

        counter = 0
        count_max = 100
        while counter < count_max:
            min_distance_positions = [positions[0], positions[1]]
            min_distance = mag2(positions[0] - positions[1])
            max_distance = min_distance

            for i in arange(0, len(positions) - 1):
                for j in arange(i + 1, len(positions)):
                    distance = mag2(positions[i] - positions[j])
                    if distance < min_distance:
                        min_distance = distance
                        min_distance_positions = [positions[i], positions[j]]
                    if distance > max_distance:
                        max_distance = distance

            p1 = min_distance_positions[0]
            p2 = min_distance_positions[1]
            min_distance_positions[0] = norm(p1 + 1.1 * (p2 - p1))
            min_distance_positions[1] = norm(p1 - 0.1 * (p2 - p1))

            counter += 1

        self._positions = positions


    def field_arrows(self):
        E = 0.5 * 1 / mag2(self._positions[0])
        for arrow_pos in self._positions:
            field_arrow = arrow(pos=arrow_pos, axis=E * arrow_pos, shaftwidth=0.04, fixedwidth=1,
                                color=electric_field_colors[0])
            box(pos=arrow_pos + field_arrow.axis / 4., axis=field_arrow.axis, length=mag(field_arrow.axis) / 2.,
                height=0.04, width=0.04, color=electric_field_colors[0])
            # Field at twice the distance is 4 times as small
            field_arrow = arrow(pos=2 * arrow_pos, axis=E / 4. * arrow_pos, shaftwidth=0.04, fixedwidth=1,
                                color=electric_field_colors[0])
            box(pos=2 * arrow_pos + field_arrow.axis / 4., axis=field_arrow.axis, length=mag(field_arrow.axis) / 2.,
                height=0.04, width=0.04, color=electric_field_colors[0])


sphere(radius=0.04, color=color.cyan)
field = ElectricField()
field.field_arrows()


def on_key_press(event):
    global colorScheme
    if event.key == 'n':
        colorScheme = (colorScheme + 1) % 2  # TOGGLE colorScheme
        scene.background = colorBackground[colorScheme]
    if event.key == 'z':
        print("scene.center=", scene.center)
        print("scene.forward=", scene.forward)
        print("scene.range=", scene.range)


scene.bind('keydown', on_key_press)


def zoom_in_on(selected_object):
    if selected_object is None:
        return

    ### ANIMATE TO SELECTED POSITION
    temp_color = vec(selected_object.color.x, selected_object.color.y, selected_object.color.z)
    selected_object.color = color.yellow
    target = selected_object.pos
    step = (target - scene.center) / 20.0
    for _ in arange(1, 20, 1):
        rate(10)
        scene.center += step
        scene.range /= 1.037  # (1.037**19=1.99)

    selected_object.color = temp_color


while 1:
    rate(60)
    scene.waitfor('click')
    zoom_in_on(scene.mouse.pick)
