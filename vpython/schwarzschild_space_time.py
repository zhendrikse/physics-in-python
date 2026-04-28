# Web VPython 3.2
from vpython import curve, vec, cos, pi, sqrt, sin, color, rate, sphere, slider, canvas, checkbox, button

title = """&#x2022; Original <a href="https://www.glowscript.org/#/user/Luinthoron/folder/English/program/embedding-diagram">idea &amp; code</a> by M. Ryston (Department of Physics Education)
&#x2022; Faculty of Mathematics and Physics, Charles University,Prague, Czech Republic
&#x2022; Described in <a href="https://iopscience.iop.org/article/10.1088/1742-6596/1286/1/012049">Interactive animations as a tool in teaching general relativity [...]</a>
&#x2022; Refactored by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> in <a href="https://github.com/zhendrikse/science/blob/main/relativity/code/schwarzschild_space_time.py">schwarzschild_space_time.py</a>

"""

display = canvas(title=title, width=600, height=450, background=color.gray(0.075), forward=vec(0, -.75, -.85), range=80)
stars = sphere(pos=vec(0, 0, 0), texture="https://www.hendrikse.name/science/astrophysics/images/textures/universe.jpg", radius=200, shininess=0, opacity=0.5)
stars.rotate(angle=pi/2, axis=vec(0, 1, 0))
# display.range = 1.3 * r_max # r_max from SchwarzschildSpaceTime
# display.forward = vec(-0.64, -0.77, 0.0)
# display.center = vec(-10,0,0.2)

class Sun:
    def __init__(self, position, radius=0.8):
        self._sun = sphere(pos=position, radius=radius,
                           texture="https://www.hendrikse.name/science/astrophysics/images/textures/sun.jpg",
                           visible=True)

    def visibility_is(self, checked):
        self._sun.visible = checked


class Comet:
    def __init__(self, start_position, radius, colour, sour=None):
        self._sphere = sphere(pos=start_position, radius=radius, color=colour, visible=True, make_trail=True, trail_radius=.25 * radius)
        self._sour = sour
        self._start_sour = None if sour is None else [elem for elem in sour]
        self._start_position = start_position
        self._is_moving = False

    def update_real_motion_by(self, M, y_offset, dt):
        if not self._is_moving:
            return

        r = self._sour[1]
        bracket = r - 2.0 * M
        buff = [0, 0, 0, 0, 0, 0]
        buff[1] = self._sour[1] + 0.5 * dt * self._sour[4]
        buff[2] = self._sour[2] + 0.5 * dt * self._sour[5]
        buff[3] = self._sour[3] - 0.5 * dt * (M / r / bracket ** 2 * self._sour[3] * self._sour[4])
        buff[4] = self._sour[4] + 0.5 * dt * (
                    -M * bracket / r ** 3 * self._sour[3] ** 2 + M / r / bracket * self._sour[4] ** 2 + bracket *
                    self._sour[5] ** 2)
        buff[5] = self._sour[5] - 0.5 * dt * 2.0 / r * self._sour[3] * self._sour[5]

        self._sour[0] += dt * buff[3]
        self._sour[1] += dt * buff[4]
        self._sour[2] += dt * buff[5]
        self._sour[3] += -dt * (M / r / bracket ** 2 * buff[3] * buff[4])
        self._sour[4] += dt * (
                    -M * bracket / r ** 3 * buff[3] ** 2 + M / r / bracket * buff[4] ** 2 + bracket * buff[5] ** 2)
        self._sour[5] += -dt * 2.0 / r * buff[3] * buff[5]
        self._sphere.pos = vec(self._sour[1] * cos(self._sour[2]), y_offset, self._sour[1] * sin(self._sour[2]))

    def update_by(self, M, dt):
        if not self._is_moving:
            return

        buff = [0, 0, 0, 0]
        buff[0] = self._sour[0] + 0.5 * dt * self._sour[2]
        buff[1] = self._sour[1] + 0.5 * dt * self._sour[3]
        buff[2] = self._sour[2] + 0.5 * dt * (
                    M / self._sour[0] / (self._sour[0] - 2.0 * M) * self._sour[2] ** 2 + (self._sour[0] - 2.0 * M) *
                    self._sour[3] ** 2)
        buff[3] = self._sour[3] - 0.5 * dt * 2 / self._sour[0] * self._sour[2] * self._sour[3]

        self._sour[0] += dt * buff[2]
        self._sour[1] += dt * buff[3]
        self._sour[2] += dt * (M / buff[0] / (buff[0] - 2.0 * M) * buff[2] ** 2 + (buff[0] - 2.0 * M) * buff[3] ** 2)
        self._sour[3] += -dt * 2 / buff[0] * buff[2] * buff[3]
        self._sphere.pos = vec(self._sour[0] * cos(self._sour[1]), sqrt(8 * M * self._sour[0] - 16 * M ** 2),
                               self._sour[0] * sin(self._sour[1]))

    def r(self):
        return sqrt(self._sphere.pos.x * self._sphere.pos.x + self._sphere.pos.z * self._sphere.pos.z)

    def reset(self):
        self._sphere.clear_trail()
        self._sphere.pos = self._start_position
        self._sour = None if self._sour is None else [elem for elem in self._start_sour]

    def visibility_is(self, checked):
        self._sphere.visible = checked

    def follow(self, comet, y_offset):
        if not self._is_moving:
            return

        self._sphere.pos = comet.pos()
        self._sphere.pos.y = y_offset

    def pos(self):
        return self._sphere.pos

    def leave_trail_is(self, checked):
        if not checked:
            self._sphere.clear_trail()
        self._sphere.make_trail = checked

    def modify_start_position(self, value, sour):
        if self._is_moving:
            return

        self._sphere.pos = value
        self._start_position = value
        self._sour = sour
        self._start_sour = sour

    def stop_movement(self):
        self._is_moving = False

    def start_movement(self):
        self._is_moving = True


class SchwarzschildSpaceTime:
    def __init__(self, mass, grid_y_offset=-10):
        self._mass = mass
        self._grid_y_offset = grid_y_offset
        self._surface = []
        self._grid = []

    def r_min_r_max(self):
        r_min = 2 * self._mass + 0.1
        r_max = 13 * self._mass
        return r_min, r_max

    def draw_grid(self):
        _, r_max = self.r_min_r_max()
        for i in range(20):
            self._grid += [curve(
                pos=[vec(-r_max + i * 2 * r_max / 19, self._grid_y_offset, -r_max),
                     vec(-r_max + i * 2 * r_max / 19, self._grid_y_offset, r_max)],
                color=color.green, radius=0.2)]
            self._grid += [curve(
                pos=[vec(-r_max, self._grid_y_offset, -r_max + i * 2 * r_max / 19),
                     vec(r_max, self._grid_y_offset, -r_max + i * 2 * r_max / 19)],
                color=color.green, radius=0.2)]

    def mass(self):
        return self._mass

    def grid_y_offset(self):
        return self._grid_y_offset

    def z_as_function_of(self, r):
        return sqrt(8 * self._mass * r - 16 * self._mass * self._mass)

    # def radius(self, t):
    #     return (t ** 2 + 4 * self._M ** 2) / (8 * self._M)

    def draw(self):
        r_min, r_max = self.r_min_r_max()
        for i in range(15):
            r = r_min + i * (r_max - r_min) / 14
            t = 0
            c = curve(pos=vec(r * cos(t), self.z_as_function_of(r), r * sin(t)), color=color.yellow, radius=0.2)
            for j in range(200):
                t += 2 * pi / 200
                c.append(vec(r * cos(t), self.z_as_function_of(r), r * sin(t)))
            self._surface.append(c)

        for i in range(12):
            phi = i * 2 * pi / 12
            r = r_min
            c = curve(pos=vec(r * cos(phi), self.z_as_function_of(r), r * sin(phi)), color=color.yellow, radius=0.2)
            for j in range(100):
                r += (r_max - r_min) / 100
                c.append(vec(r * cos(phi), self.z_as_function_of(r), r * sin(phi)))
            self._surface.append(c)

    def modify_grid(self, thickness):
        for element in self._surface:
            element.radius = thickness
        for element in self._grid:
            element.radius = thickness

    def grid_visibility_is(self, checked):
        for line in self._grid:
            line.visible = checked

    def cone_visibility_is(self, checked):
        for line in self._surface:
            line.visible = checked


schwarzschild = SchwarzschildSpaceTime(mass=5.0)
schwarzschild.draw()
schwarzschild.draw_grid()
sun = Sun(position=vec(0, 2, 0), radius=2 * schwarzschild.mass())

r_min, r_max = schwarzschild.r_min_r_max()
start_r = r_max - 5
position=vec(start_r, schwarzschild.z_as_function_of(start_r), 0)
comet = Comet(start_position=position, radius=1.25, colour=color.cyan, sour=[start_r, 0, -25.2, 0.49])
flat_motion_comet = Comet(vec(position.x, schwarzschild.grid_y_offset(), position.z), 1.25, color.red)

#real_motion_comet = Comet(vec(start_r, schwarzschild.grid_y_offset(), 0), 1.5, color.orange, sour=[0, start_r, 0, 0, 0, 0])

def toggle_grid(event):
    schwarzschild.grid_visibility_is(event.checked)

def toggle_sun(event):
    sun.visibility_is(event.checked)

def toggle_cone(event):
    schwarzschild.cone_visibility_is(event.checked)

def toggle_flat_motion(event):
    flat_motion_comet.visibility_is(event.checked)
    flat_motion_comet.reset()
    #real_motion_comet.reset()

def toggle_trail(event):
    comet.leave_trail_is(event.checked)
    flat_motion_comet.leave_trail_is(event.checked)
    #real_motion_comet.leave_trail_is(event.checked)

display.append_to_caption('\n')
_ = checkbox(text="Cone", bind=toggle_cone, checked=True)
_ = checkbox(text="Grid", bind=toggle_grid, checked=True)
_ = checkbox(text="Central mass", bind=toggle_sun, checked=True)
_ = checkbox(text="Flat motion", bind=toggle_flat_motion, checked=True)
_ = checkbox(text="Leave trail", bind=toggle_trail, checked=True)



def top_view(b):
    display.forward = vec(0, -1, 0)
    display.up = vec(-1, 0, 0)
    display.range = 1.5 * r_max

def flip_up(b):
    display.up = vec(0, 1, 0)

def flip_down(b):
    display.up = vec(0, -1, 0)


display.append_to_caption('\n\n')
_ = button(text="Top view", bind=top_view)
_ = button(text="Flip up", bind=flip_up)
_ = button(text="Flip down", bind=flip_down)

def modify_grid_thickness(event):
    schwarzschild.modify_grid(event.value)

def modify_start_position(event):
    flat_motion_comet.reset()
    comet.reset()
    #real_motion_comet.reset()
    pos = vec(event.value, schwarzschild.z_as_function_of(event.value), 0)
    comet.modify_start_position(pos, [pos.x, 0, -25.2, 0.49])
    #real_motion_comet.modify_start_position(vec(pos.x, schwarzschild.grid_y_offset(), pos.z), [0, pos.x, 0, 0, 0, 0])


display.append_to_caption('\n\nInitial radius:')
slider(min=r_min + 0.1, max=r_max - 0.1, value=start_r, step=0.1, bind=modify_start_position)
display.append_to_caption('\n\nGrid thickness')
slider(min=0.1, max=0.5, value=0.2, bind=modify_grid_thickness)


def restart(event):
    comet.reset()
    flat_motion_comet.reset()
    #real_motion_comet.reset()

    comet.start_movement()
    flat_motion_comet.start_movement()
    #real_motion_comet.start_movement()


display.bind('click', restart)

#MathJax.Hub.Queue(["Typeset", MathJax.Hub])

delta_t = 0.01
while True:
    rate(1 / delta_t)
    if r_min < comet.r() < r_max:
        comet.update_by(schwarzschild.mass(), delta_t)
        flat_motion_comet.follow(comet, schwarzschild.grid_y_offset())
    else:
        comet.stop_movement()

    #if r_min < real_motion_comet.r() < r_max:
    #    real_motion_comet.update_real_motion_by(schwarzschild.mass(), schwarzschild.grid_y_offset(), delta_t)
    #else:
    #    real_motion_comet.stop_movement()
