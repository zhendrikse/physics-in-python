#Web VPython 3.2

from vpython import *

title="""Relativistic electric field around a moving proton

&#x2022; Original by Ruth Chabay Spring 2001
&#x2022; Updated by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a>
&#x2022; Located in the <a href="https://github.com/zhendrikse/physics-in-python/">Physics in Python GitHub repository</a>
&#x2022; &lt;v&gt; &rarr; verbose output
&#x2022; &lt;s&gt; &rarr; make screenshot
&#x2022; &lt;space&gt; &rarr; toggle background color
&#x2022; &lt;mouse click&gt; &rarr; to toggle the motion

"""

## proton at rest in lab frame
## moving frame has speed <v,0,0>

c = 3e8
c2 = c ** 2

v = 0.99 * c  ## speed of moving frame
v2 = v ** 2

kel = 9e9
kmag = 1e-7
gamma = 1 / sqrt(1 - (v2 / c2))

proton = sphere(radius=1e-12, color=color.red)
proton.v = vector(-v, 0, 0)
proton.q = 1.6e-19

R = 1e-11
escale = R / 3e13

observer_location = []
dtheta = pi / 8.
for theta in arange(0, 2 * pi, dtheta):
    a = vector(R * cos(theta), R * sin(theta), 0)
    observer_location.append(a)
observer_location_2 = []
for theta in arange(dtheta, pi, dtheta):
    a = vector(R * cos(theta), 0, -R * sin(theta))
    observer_location_2.append(a)
    b = vector(-R * cos(theta), 0, R * sin(theta))
    observer_location_2.append(b)

arr0 = []
arr2 = []
for pt in observer_location:
    r = pt - proton.pos
    E = norm(r) * kel * proton.q / (mag(r) ** 2)
    Eprime = vector(E.x, gamma * E.y, gamma * E.z)
    aa = arrow(pos=pt, axis=escale * Eprime, color=vector(1, .5, 0), shaftwidth=.8e-12)
    arr0.append(aa)
for pt in observer_location_2:
    r = pt - proton.pos
    E = norm(r) * kel * proton.q / (mag(r) ** 2)
    Eprime = vector(E.x, gamma * E.y, gamma * E.z)
    aa = arrow(pos=pt, axis=escale * Eprime, color=vector(1, .5, 0), shaftwidth=.8e-12)
    arr2.append(aa)

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

def on_mouse_click():
    for ee in arr2:
        ee.visible = not ee.visible


#scene.autoscale = 0
scene.title=title
scene.background = color.black
scene.bind("keydown", on_key_press)
scene.bind("click", on_mouse_click)
scene.forward=vector(-2.40482, -0.795294, -4.537)
scene.range=5.2e-11
scene.width = scene.height = 1000
scene.x = scene.y = 0

while 1:
    rate(50)

