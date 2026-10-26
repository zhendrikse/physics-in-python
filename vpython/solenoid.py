#Web VPython 3.2
from vpython import cylinder, sphere, canvas, vec, vector, cos, sin, pi, color, rate, arrow, cross, mag


title="""&#x2022; Based on <a href="https://glowscript.org/#/user/yizhe/folder/Public/program/25-4.Bsolenoid">25-4.Bsolenoid</a>
&#x2022; Refactored by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> to <a href="https://github.com/zhendrikse/science/blob/main/electromagnetism/code/solenoid.py">solenoid.py</a>

"""

size = 0.4
L = 40
current = 1E8

animation = canvas(range=30, center=vector(0, L / 10, 0), background=color.gray(0.075), title=title)
sphere(pos=vec(0, 0, 0), texture="https://i.imgur.com/1nVWbbd.jpg", radius=60, shininess=0, opacity=0.5)
#animation.lights = []
#animation.ambient = color.white

class Solenoid:
    def __init__(self, r, n, num, direct):
        self._segments = []
        points = [] # The collection of points that make up the solenoid
        for i in range(n):
            position = vector(L / 2 - i * L / n, r * cos(2 * pi / n * num * i), r * sin(2 * pi / n * num * i))
            points.append(sphere(pos=position, radius=0.2 * size, color=color.cyan))

        for i in range(n - 1):
            distance = points[i + 1].pos - points[i].pos if direct else points[i].pos - points[i + 1].pos
            mid = (points[i + 1].pos + points[i].pos) / 2
            self._segments.append(cylinder(pos=mid, axis=distance, radius=1.0 * size, color=color.yellow))

    def field_at(self, position):
        mu = 4 * pi * 1E-7
        field = vector(0, 0, 0)
        for segment in self._segments:
            axis = position - segment.pos
            field += mu * current / (4 * pi) * segment.axis.mag * cross(segment.axis, axis.norm()) / axis.mag2
        return field


class MagneticField:
    def __init__(self, N=5):
        self._fields = []
        locations = []
        for i in range(N + 1):
            for j in range(N + 1):
                for k in range(N + 1):
                    location = vector(L / N * i - L / 2, L / N * j - L / 2, L / N * k - L / 2)
                    locations.append(location)

        for location in locations:
            self._fields.append(arrow(pos=location, axis=vector(0, 0, 0), color=color.green))

    def display_field_around(self, solenoid, max_field_strength=5):
        for field in self._fields:
            value = solenoid.field_at(field.pos)
            if value.mag >= max_field_strength: value = value / value.mag * max_field_strength
            field.axis = value
            field.color = vector(value.mag / max_field_strength, 1 - value.mag / max_field_strength, 0)


charged_solenoid = Solenoid(r=10, n=500, num=10, direct=True)
magnetic_field = MagneticField()
magnetic_field.display_field_around(charged_solenoid)


n_max = 100
n_rot = 10
R_camera = mag(animation.camera.pos)
theta_camera = pi / 2
phi_camera = 0
d_theta_camera = -pi / (5 * n_max)
d_phi_camera = pi / (5 * n_max) * 2
theta_camera_max = 2 * pi / 3
theta_camera_min = pi / 3

while True:
    rate(20)
    if theta_camera > theta_camera_max or theta_camera < theta_camera_min:
        d_theta_camera *= -1
    theta_camera += d_theta_camera
    phi_camera += d_phi_camera
    animation.camera.pos = R_camera * vec(sin(theta_camera) * sin(phi_camera), cos(theta_camera),
                                          sin(theta_camera) * cos(phi_camera))
    animation.camera.axis = -animation.camera.pos
