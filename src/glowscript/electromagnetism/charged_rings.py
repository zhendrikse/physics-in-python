#Web VPython 3.2
from vpython import canvas, arange, pi, sphere, vector, sin, cos, ring, vec, arrow, color, mag, norm, rate, checkbox

title = """Electric field inside charged rings. 

&#x2022; Original <a href="https://lectdemo.github.io/virtual/18-Erings.html">18-Erings.html</a>
&#x2022; Maintained by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>
&#x2022; &lt;s&gt; &rarr; screenshot
&#x2022; &lt;v&gt; &rarr; verbose output

"""

animation = canvas(width="1024", height="768", title=title, background=color.black, forward=vec(0.18, 0.35, -0.95))

scale_factor = 2e-11
L = 6e-3
dL = 1e-3

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
                saturation = 0
            charge.color = color.hsv_to_rgb(vec(hue, saturation, 1.0))
            ring(pos=vector(xx, 0, 0), axis=vector(1, 0, 0), radius=ring_radius, thickness=ring_radius / 75., color=charge.color)

    def visible_is(self, visible):
        for charge in self._charges:
            charge.visible = visible

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
            for y in arange(-(2 / 3) * rings.radius(), rings.radius(), rings.radius() / 3.):
                location = vector(x, y, 0)
                E = rings.field_at(location)
                self._field_arrows += [arrow(pos=location, axis=E * scale_factor, color=color.cyan, shaftwidth=rings.radius() / 20.)]

    def visible_is(self, visible):
        for field_arrow in self._field_arrows:
            field_arrow.visible = visible

class Rings:
    def __init__(self, ring_radius=2e-3, dQ=5e-10):
        ##for x in arange (-L,1.1*L,dL):
        self._radius = ring_radius
        self._rings = []
        total_charge = -3 * dQ # Charge of left ring
        count = 0
        for x in arange(-2 * L, 2.5 * L, dL):
            self._rings.append(ChargedRing(ring_radius, point_charges_amount=20, totalq=total_charge, xx=x))
            total_charge = total_charge + dQ
            count += 1

    def field_at(self, location):
        field = vec(0, 0, 0)
        for a_ring in self._rings:
            field += a_ring.electric_field_at(location)
        return field

    def charges_visible_is(self, visible):
        for ring in self._rings:
            ring.visible_is(visible)

    def radius(self):
        return self._radius

rings = Rings(ring_radius=2e-3)
electric_field = Field(rings)

def toggle_charges(event):
    rings.charges_visible_is(event.checked)

def toggle_field(event):
    electric_field.visible_is(event.checked)

def toggle_background(event):
    animation.background = color.black if event.checked else color.white

def on_key_press(event):
    if event.key == 's':
        animation.capture("electric_field_of_charged_rings")
    if event.key == 'v':
        print("scene.center=" + str(animation.center))
        print("scene.forward=" + str(animation.forward))
        print("scene.range=" + str(animation.range))

animation.append_to_caption("\n")
background_box = checkbox(text="Dark background", checked=True, bind=toggle_background)
field_box = checkbox(text="Show field", checked=True, bind=toggle_field)
charges_box = checkbox(text="Show charges", checked=True, bind=toggle_charges)
animation.bind("keydown", on_key_press)

while True:
    rate(50)


#Web VPython 3.2
from vpython import canvas, arange, pi, sphere, vector, sin, cos, ring, vec, arrow, color, mag, norm, rate, checkbox

title = """Electric field inside charged rings. 

&#x2022; Original <a href="https://lectdemo.github.io/virtual/18-Erings.html">18-Erings.html</a>
&#x2022; Maintained by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>
&#x2022; &lt;s&gt; &rarr; screenshot
&#x2022; &lt;v&gt; &rarr; verbose output

"""

animation = canvas(width="1024", height="768", title=title, background=color.black, forward=vec(0.18, 0.35, -0.95))

scale_factor = 2e-11
L = 6e-3
dL = 1e-3

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
                saturation = 0
            charge.color = color.hsv_to_rgb(vec(hue, saturation, 1.0))
            ring(pos=vector(xx, 0, 0), axis=vector(1, 0, 0), radius=ring_radius, thickness=ring_radius / 75., color=charge.color)

    def visible_is(self, visible):
        for charge in self._charges:
            charge.visible = visible

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
            for y in arange(-(2 / 3) * rings.radius(), rings.radius(), rings.radius() / 3.):
                location = vector(x, y, 0)
                E = rings.field_at(location)
                self._field_arrows += [arrow(pos=location, axis=E * scale_factor, color=color.cyan, shaftwidth=rings.radius() / 20.)]

    def visible_is(self, visible):
        for field_arrow in self._field_arrows:
            field_arrow.visible = visible

class Rings:
    def __init__(self, ring_radius=2e-3, dQ=5e-10):
        ##for x in arange (-L,1.1*L,dL):
        self._radius = ring_radius
        self._rings = []
        total_charge = -3 * dQ # Charge of left ring
        count = 0
        for x in arange(-2 * L, 2.5 * L, dL):
            self._rings.append(ChargedRing(ring_radius, point_charges_amount=20, totalq=total_charge, xx=x))
            total_charge = total_charge + dQ
            count += 1

    def field_at(self, location):
        field = vec(0, 0, 0)
        for a_ring in self._rings:
            field += a_ring.electric_field_at(location)
        return field

    def charges_visible_is(self, visible):
        for ring in self._rings:
            ring.visible_is(visible)

    def radius(self):
        return self._radius

rings = Rings(ring_radius=2e-3)
electric_field = Field(rings)

def toggle_charges(event):
    rings.charges_visible_is(event.checked)

def toggle_field(event):
    electric_field.visible_is(event.checked)

def toggle_background(event):
    animation.background = color.black if event.checked else color.white

def on_key_press(event):
    if event.key == 's':
        animation.capture("electric_field_of_charged_rings")
    if event.key == 'v':
        print("scene.center=" + str(animation.center))
        print("scene.forward=" + str(animation.forward))
        print("scene.range=" + str(animation.range))

animation.append_to_caption("\n")
background_box = checkbox(text="Dark background", checked=True, bind=toggle_background)
field_box = checkbox(text="Show field", checked=True, bind=toggle_field)
charges_box = checkbox(text="Show charges", checked=True, bind=toggle_charges)
animation.bind("keydown", on_key_press)

while True:
    rate(50)


