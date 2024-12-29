from vpython import vector, scene, color, cylinder, arrow, rate, sin, cos, arange, pi, norm, mag, cross

title = """Electromagnetic waves emanating from an antenna. 

&#x2022; <a href="https://lectdemo.github.io/virtual/23_antenna.html">23_antenna.py</a> by Ruth Chabay Spring 2001
&#x2022; Maintained by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>
&#x2022; &lt;s&gt; &rarr; screenshot
&#x2022; &lt;d&gt; &rarr; toggle show electromagnetic wave decrease
&#x2022; &lt;v&gt; &rarr; verbose output
&#x2022; &lt;space&gt; &rarr; toggle background color
&#x2022; &lt;mouse click&gt; &rarr; toggle display of magnetic field

"""

scene.title = title
scene.x = scene.y = 0
scene.width = 1024
scene.height = 768
scene.background = color.black

show_decrease = True
lamb = 2.  ##1e-10
c = 3e8
omega = 2 * pi * c / lamb
d = 2 * lamb
L = 2 * lamb
antenna = cylinder(pos=vector(0, -L / 2, 0), axis=vector(0, L, 0), color=vector(.7, .7, .7), radius=0.5)


dist_to_screen = 4.0 * lamb  ## dist to screen
dts = dist_to_screen
##scene.center = (dist_to_screen*.65,-d/2.,0)
ds = lamb / 20.
dt = lamb / c / 100.
##E0 = lamb/3.0
E0 = lamb * 5

##slit1 = vector(0, 0, -d/2.) ## coord of slit 1

## create waves
slit1 = vector(0, 0, 0)

class ElectromagneticWave:
    def __init__(self):
        self._electric_field = []
        self._magnetic_field = []
        dtheta = pi / 3
        for r1 in [vector(dts * cos(theta), 0, dts * sin(theta)) for theta in arange(0, 2 * pi, dtheta)]:
            dr1 = ds * norm(r1)
            rr1 = slit1 + 10 * dr1  ##vector(0,0,0) ## current loc along wave 1
            ct = 0
            while ct < 120:
                ea = arrow(pos=rr1, axis=vector(0, (E0 * cos(2 * pi * mag(rr1 - slit1)) / lamb), 0), color=color.orange,
                           shaftwidth=lamb / 40.)
                ba = arrow(pos=rr1, axis=vector(0, 0, 0), color=color.cyan,
                           shaftwidth=lamb / 40., visible=0)
                self._magnetic_field.append(ba)
                self._electric_field.append(ea)
                rr1 += dr1
                ct += 1

    def update(self):
        for index in range(len(self._electric_field)):
            field_arrow = self._electric_field[index]
            decrease = 1 / (mag(field_arrow.pos) + lamb / 20) if show_decrease else 1.0
            field_arrow.axis = vector(0, decrease * E0 * cos(omega * t - 2 * pi * mag(field_arrow.pos - slit1) / lamb),
                                      0)
            self._magnetic_field[index].axis = -cross(field_arrow.axis, i_hat) * .7

    def toggle_magnetic_field(self):
        for field_vector in self._magnetic_field:
            field_vector.visible = not field_vector.visible

def toggle_background():
    scene.background = color.white if scene.background is color.black else color.black

def on_key_press(event):
    global show_decrease
    if event.key == "d":
        show_decrease = not show_decrease
    if event.key == " ":
        toggle_background()
    if event.key == 's':
        scene.capture("electric_field_of_charged_disk")
    if event.key == 'v':
        print("scene.center=" + str(scene.center))
        print("scene.forward=" + str(scene.forward))
        print("scene.range=" + str(scene.range))

electromagnetic_wave = ElectromagneticWave()
scene.autoscale = 0
scene.forward = vector(-0.1, -0.4, -0.9)
scene.bind("keydown", on_key_press)
scene.bind("click", electromagnetic_wave.toggle_magnetic_field)

t = 0.0
i_hat = vector(1, 0, 0)
while 1:
    rate(50)
    t = t + dt
    electromagnetic_wave.update()
