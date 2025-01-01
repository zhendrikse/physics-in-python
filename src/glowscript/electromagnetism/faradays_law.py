# Web VPython 3.2

from vpython import canvas, color, vector, rate, arrow, pi, box, sphere, cos, sin, arange, curve, mag, cylinder, norm

title = """Faraday law: changing-Bs are associated with curly-Es
&#x2022; Rob Salgado (salgado@physics.syr.edu)
&#x2022; Maintained by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>

The thick green vector representing d|B|/dt, i.e. the rate of change of the magnitude 
of the magnetic field) is associated with the spatial arrangement of the electric field 
according to the Faraday Law (as evaluated on the green loop). The sense of circulation 
on the green loop (by the RightHandRule) determines the direction of change of the magnetic 
field, which is opposite to your thumb.

&#x2022; &lt;f&gt; &rarr; show Faraday loop 
&#x2022; &lt;d&gt; &rarr; dim electric field 
&#x2022; &lt;n&gt; &rarr; change color-scheme  
&#x2022; &lt;v&gt; &rarr; verbose output 
&#x2022; &lt;s&gt; &rarr; screenshot 
&#x2022; &lt;space&gt; &rarr; pause animation
&#x2022; &lt;mouse click&gt; &rarr; zoom to selected point

"""

color_scheme = 0  # key n (negative)
background_color = [color.black, color.white]
dimmed_colors_electric_field = [vector(0.0, 0, 0.4), vector(0.5, 0.5, 1)]
electric_field_colors = [color.blue, (0.5, 0.5, 1), color.green]
electric_field_colors[1] = dimmed_colors_electric_field[color_scheme]
faraday_color = electric_field_colors[2]

scene = canvas(title=title, width=800, height=600, x=0, y=0)
scene.background = background_color[color_scheme]
scene.background = color.black;
electric_field_colors = [color.blue, vector(0, 0, .4), color.green]
scene.caption = "\\( \\Phi_B = \\iint_{\\Sigma(t)} \\vec{B}(t) \\cdot d\\vec{A} \\),\n where \\(d\\vec{A}\\) is an element of area vector of the moving surface Σ(t), and \\(\\vec{B}\\) is the magnetic field."
MathJax.Hub.Queue(["Typeset", MathJax.Hub])
scene.forward = vector(-0.75, -0.10, -0.65)
scene.range = 2.5
# scene.ambient = color.gray(0.4)

showFaraday = 0
dimFields = 0

magnetic_field_vector_positions = [
    vector(0.25, 0, 0),
    vector(-0.25, 0, 0),
    vector(0, 0.25, 0),
    vector(0, -0.25, 0),
    vector(0.25, 0, -2),
    vector(-0.25, 0, -2),
    vector(0, 0.25, -2),
    vector(0, -0.25, -2)
]
magnetic_field_vectors = [arrow(pos=arrow_pos, axis=vector(0, 0, 1e-3), shaftwidth=0.04, fixedwidth=1, color=color.red) for arrow_pos in magnetic_field_vector_positions]

N = 8
dBdt = 0.2


def get_electric_field_vectors(count=N):
    vectors = []
    for z in [0, -0.5, 0.5, -1, 1]:
        for r in [0.5, 1, 1.5]:
            for index in arange(0, count):
                theta = 2. * pi * index / count
                theta_hat = vector(-sin(theta), cos(theta), 0)
                electric_field = -dBdt * theta_hat / r
                vectors.append(
                    arrow(pos=vector(r * cos(theta), r * sin(theta), z), axis=electric_field, shaftwidth=0.04,
                          fixedwidth=1,
                          color=color.blue))
    return vectors


def get_tails_for(electric_field_vector_array):
    return [
        box(pos=field_vec.pos + field_vec.axis / 4., axis=field_vec.axis, length=mag(field_vec.axis) / 2., height=0.04,
            width=0.04,
            color=color.blue) for field_vec in electric_field_vector_array]


def get_faraday_vectors_from(magnetic_field_vector_array):
    faraday_vecs = []
    for field_vec in magnetic_field_vectors:
        faraday_vecs.append(
            arrow(pos=field_vec.pos + field_vec.axis, axis=dBdt * norm(field_vec.axis), fixedwidth=1,
                  color=faraday_color,
                  shaftwidth=0.07, headwidth=0.14, visible=False))
    return faraday_vecs


class Wire:
    def __init__(self, charge_count=N):
        self._wire = cylinder(radius=0.04, pos=vector(0, 0, -2), axis=vector(0, 0, 4), color=color.yellow)
        self._charge_count = charge_count
        self._charge_positions = [vector(self._wire.pos + self._wire.axis * i / N) for i in range(charge_count)]
        self._charges = [sphere(pos=self._charge_positions[i], radius=0.05, color=self._wire.color) for i in
                         range(charge_count)]

    def update(self, t):
        for i in arange(self._charge_count):
            self._charges[i].pos = self._charge_positions[i] + (t % 4) * vector(0, 0, 0.125)


electric_field_vectors = get_electric_field_vectors(N)
electric_field_vector_tails = get_tails_for(electric_field_vectors)
faraday_vectors = get_faraday_vectors_from(magnetic_field_vectors)
faraday_loop_positions = [mag(electric_field_vectors[0].pos) * vector(cos(2. * pi * n / 40.), sin(2. * pi * n / 40.), 0) for n in range(40)]
faraday_loop = curve(color=faraday_color, pos=faraday_loop_positions, visible=False)
wire = Wire()


def toggle_show_faraday(show=True):
    faraday_loop.visible = show
    for k in faraday_vectors:
        k.visible = show

    if show:
        for l in range(0, N):
            electric_field_vectors[l].color = faraday_color
            electric_field_vector_tails[l].color = faraday_color
    else:
        for l in range(0, N):
            electric_field_vectors[l].color = color.blue
            electric_field_vector_tails[l].color = color.blue


def toggle_show_fields(show=0):
    for i in range(N, len(electric_field_vectors)):
        electric_field_vectors[i].color = electric_field_colors[show]
        electric_field_vector_tails[i].color = electric_field_colors[show]
    for i in range(1, 4 * N + 1):
        electric_field_vectors[-i].visible = (1 - show)
        electric_field_vector_tails[-i].visible = (1 - show)


def toggle_color_scheme(color_scheme=0):
    scene.background = background_color[color_scheme]
    electric_field_colors[1] = dimmed_colors_electric_field[color_scheme]
    scene.background = background_color[color_scheme]

    for i in range(N, len(electric_field_vectors)):
        electric_field_vectors[i].color = electric_field_colors[dimFields]
        electric_field_vector_tails[i].color = electric_field_colors[dimFields]
    for i in range(1, 4 * N + 1):
        electric_field_vectors[-i].visible = (1 - dimFields)
        electric_field_vector_tails[-i].visible = (1 - dimFields)


def pause_animation():
    global dt
    dt += 1
    dt %= 2


class KeyboardEventProcessor:
    def __init__(self):
        self._show_faraday = False
        self._show_fields = 0
        self._color_scheme = 0

    def toggle_show_faraday(self):
        self._show_faraday = not self._show_faraday
        return self._show_faraday

    def toggle_show_fields(self):
        self._show_fields += 1
        return self._show_fields % 2

    def toggle_color_schemes(self):
        self._color_scheme += 1
        return self._color_scheme % 2

    def on_key_press(self, key):
        if key == 's':
            scene.capture("faradays_law")
        if key == 'f':
            toggle_show_faraday(keyboard_event_processor.toggle_show_faraday())
        if key == 'd':
            toggle_show_fields(keyboard_event_processor.toggle_show_fields())
        if key == 'n':
            toggle_color_scheme(keyboard_event_processor.toggle_color_schemes())
        if key == 'v':
            print("scene.center=" + str(scene.center))
            print("scene.forward=" + str(scene.forward))
            print("scene.range=" + str(scene.range))
            print("t=" + str(t) + "\n")
        if key == ' ':
            pause_animation()


keyboard_event_processor = KeyboardEventProcessor()


def key_pressed(event):
    key = event.key
    keyboard_event_processor.on_key_press(key)


scene.bind('keydown', key_pressed)


def on_mouse_click():
    selected_object = scene.mouse.pick
    if selected_object is None:
        return

    ### ANIMATE TO SELECTED POSITION
    temp_color = vector(selected_object.color.x, selected_object.color.y, selected_object.color.z)
    selected_object.color = color.yellow
    target = selected_object.pos
    step = (target - scene.center) / 20.0
    for _ in arange(1, 20, 1):
        rate(20)
        scene.center += step
        scene.range /= 1.037  # (1.037**19=1.99)

    selected_object.color = temp_color


scene.bind('click', on_mouse_click)

t = 9.50
dt = 1
while 1:
    rate(10)
    t += dt
    wire.update(t)

    count = 0
    for mag_vector in magnetic_field_vectors:
        mag_vector.length = (t % 20) / 10. + 1e-3
        faraday_vectors[count].pos = mag_vector.pos + mag_vector.axis
        count += 1
