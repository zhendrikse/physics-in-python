#Web VPython 3.2
from vpython import scene, arange, pi, sphere, vector, sin, cos, ring, vec, arrow, color, mag, norm, rate


title = """Electric field inside charged rings. 

&#x2022; Original <a href="https://lectdemo.github.io/virtual/18-Erings.html">18-Erings.html</a>
&#x2022; Updated by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a>
&#x2022; Located in the <a href="https://github.com/zhendrikse/physics-in-python/">Physics in Python GitHub repository</a>
&#x2022; &lt;f&gt; &rarr; toggle electric field arrows
&#x2022; &lt;s&gt; &rarr; screenshot
&#x2022; &lt;v&gt; &rarr; verbose output
&#x2022; &lt;space&gt; &rarr; toggle background color
&#x2022; &lt;mouse click&gt; &rarr; toggle display of ring charges

"""

scale_factor = 2e-11
L = 6e-3
dL = 1e-3

def hsv_to_rgb(hue, saturation, value):
    if saturation:
        if hue == 1.0: hue = 0.0
        i = int(hue * 6.0)
        f = hue * 6.0 - i

        w = value * (1.0 - saturation)
        q = value * (1.0 - saturation * f)
        t = value * (1.0 - saturation * (1.0 - f))

        if i == 0: return value, t, w
        if i == 1: return q, value, w
        if i == 2: return w, value, t
        if i == 3: return w, q, value
        if i == 4: return t, w, value
        if i == 5: return value, w, q
    else:
        return value, value, value

class ChargedRing:
    def __init__(self, ring_radius=10., point_charges_amount=20, totalq=1e-9, xx=0.):
        self._charges = []
        self._ring_radius = ring_radius
        dtheta = 2 * pi / point_charges_amount
        for theta in arange(0, 2 * pi, dtheta):
            charge = sphere(pos=vector(xx, ring_radius * sin(theta), ring_radius * cos(theta)), radius=ring_radius / 15)
            self._charges.append(charge)
            charge.q = totalq / point_charges_amount
            saturation = 1.5 * abs(totalq) / 1e-8 # 4.5e-9
            hue = 0.0
            if totalq > 1e-15:
                hue = 0.0
            elif totalq < 0:
                hue = (240 / 360)
            elif totalq == 0:
                sat = 0
            rgb = hsv_to_rgb(hue, saturation, 1.0)
            charge.color = vec(rgb[0], rgb[1], rgb[2])
            ring(pos=vector(xx, 0, 0), axis=vector(1, 0, 0), radius=ring_radius, thickness=ring_radius / 75., color=charge.color)

    def toggle_show_charges(self):
        for charge in self._charges:
            charge.visible = not charge.visible

    def electric_field_at(self, location):
        E = vector(0, 0, 0)
        oof = 9e9
        for charge in self._charges:
            r = location - charge.pos
            E = E + (oof * charge.q / mag(r) ** 2) * norm(r)
        return E

    def radius(self):
        return self._ring_radius

class Field:
    def __init__(self, rings):
        self._field_arrows = []
        for x in arange((-L + dL), L - dL, dL / 2):
            for y in arange(-(2 / 3) * rings[0].radius(), rings[0].radius(), rings[0].radius() / 3.):
                location = vector(x, y, 0)
                E = vector(0, 0, 0)
                for a_ring in rings:
                    E += a_ring.electric_field_at(location)
                self._field_arrows += [arrow(pos=location, axis=E * scale_factor, color=color.cyan, shaftwidth=rings[0].radius() / 20.)]

    def toggle_show_field(self):
        for field_arrow in self._field_arrows:
            field_arrow.visible = not field_arrow.visible

def create_rings(dQ=5e-10):
    ##for x in arange (-L,1.1*L,dL):
    count = 0
    rings = []
    total_charge = -3 * dQ # Charge of left ring
    for x in arange(-2 * L, 2.5 * L, dL):
        rings.append(ChargedRing(ring_radius=2e-3, point_charges_amount=20, totalq=total_charge, xx=x))
        print('charge of ring #', count, "=", total_charge)
        total_charge = total_charge + dQ
        count += 1
    return rings

scene.width = 1024
scene.height = 768
scene.title = title
scene.background = color.black
scene.forward=vec(0.18, 0.35, -0.95)

rings = create_rings()
field = Field(rings)

def toggle_background():
    scene.background = color.white if scene.background is color.black else color.black

def toggle_field():
    field.toggle_show_field()

def on_key_press(event):
    if event.key == "f":
        toggle_field()
    if event.key == " ":
        toggle_background()
    if event.key == 's':
        scene.capture("electric_field_of_charged_rings")
    if event.key == 'v':
        print("scene.center=" + str(scene.center))
        print("scene.forward=" + str(scene.forward))
        print("scene.range=" + str(scene.range))

def on_mouse_click():
    for ring in rings:
        ring.toggle_show_charges()


scene.bind("keydown", on_key_press)
scene.bind("click", on_mouse_click)

while 1:
    rate(50)


