from vpython import scene, arange, pi, sphere, vector, sin, cos, ring, vec, arrow, color, mag, norm

oof = 9e9
sf = 2e-11
L = 6e-3
dL = 1e-3

scalar = float  # a scale value (0.0 to 1.0)
def hsv_to_rgb(hue: scalar, saturation: scalar, value: scalar, a: scalar) -> tuple:
    if saturation:
        if hue == 1.0: hue = 0.0
        i = int(hue * 6.0)
        f = hue * 6.0 - i

        w = value * (1.0 - saturation)
        q = value * (1.0 - saturation * f)
        t = value * (1.0 - saturation * (1.0 - f))

        if i == 0: return value, t, w, a
        if i == 1: return q, value, w, a
        if i == 2: return w, value, t, a
        if i == 3: return w, q, value, a
        if i == 4: return t, w, value, a
        if i == 5: return value, w, q, a
    else:
        return value, value, value, a

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
            rgb = hsv_to_rgb(hue, saturation, 1.0, 1.0)
            charge.color = vec(rgb[0], rgb[1], rgb[2])
            ring(pos=vector(xx, 0, 0), axis=vector(1, 0, 0), radius=ring_radius, thickness=ring_radius / 75., color=charge.color)

    def toggle_show_charges(self):
        for charge in self._charges:
            charge.visible = not charge.visible

    def electric_field_at(self, location):
        E = vector(0, 0, 0)
        for charge in self._charges:
            r = location - charge.pos
            E = E + (oof * charge.q / mag(r) ** 2) * norm(r)
        return E

    def radius(self):
        return self._ring_radius


rings = []
dQ = 5e-10
##print 'dQ=',dQ
Q = -3 * dQ  ## charge of leftmost ring
count = 0
vis = 1
##for x in arange (-L,1.1*L,dL):
for x in arange(-2 * L, 2.5 * L, dL):
    rings.append(ChargedRing(ring_radius=2e-3, point_charges_amount=20, totalq=Q, xx=x))
    print('charge of ring #', count, "=", Q)
    Q = Q + dQ
    count += 1

print('len(rings)=', len(rings))
print("Click to see electric field")
scene.width = 1024
scene.height = 768
scene.background = color.white

scene.waitfor("click")
for ring in rings:
    ring.toggle_show_charges()

class Field:
    def __init__(self, rings):
        self._field_arrows = []
        for x in arange((-L + dL), L - dL, dL / 2):
            for y in arange(-(2 / 3) * rings[0].radius(), rings[0].radius(), rings[0].radius() / 3.):
                location = vector(x, y, 0)
                E = vector(0, 0, 0)
                for a_ring in rings:
                    E += a_ring.electric_field_at(location)
                self._field_arrows += [arrow(pos=location, axis=E * sf, color=color.cyan, shaftwidth=rings[0].radius() / 20.)]

    def toggle_show_field(self):
        for field_arrow in self._field_arrows:
            field_arrow.visible = not field_arrow.visible

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
        scene.capture("electric_field_of_charged_disk")
    if event.key == 'v':
        print("scene.center=" + str(scene.center))
        print("scene.forward=" + str(scene.forward))
        print("scene.range=" + str(scene.range))

scene.bind("keydown", on_key_press)

while 1:
    scene.waitfor("click")
    for ring in rings:
        ring.toggle_show_charges()


