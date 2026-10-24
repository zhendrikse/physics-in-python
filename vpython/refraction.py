#Web VPython 3.2
from vpython import simple_sphere, color, canvas, radians, slider, box, vec, rate, sin, cos, sphere, cylinder, checkbox, button, asin, radio

title="""&#x2022; <a href="https://glowscript.org/#/user/owendix/folder/Interactives/program/RefractionRaysandWavefrontInteractive">Original code</a> by <a href="https://github.com/owendix">Owen Dix</a>
&#x2022; Refactored by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> to <a href="https://github.com/zhendrikse/science/blob/main/optics/code/refraction.py">refraction.py</a>

"""

canvas_width = 600
canvas_height = (9 / 16) * canvas_width
initial_range = 1
display = canvas(width=canvas_width, height=canvas_height, range=initial_range, title=title)

lambda_red = 750
lambda_blue = 380

# incident angle in degrees
initial_angle = 45
initial_rate = 500
the_rate = initial_rate
dt = 1e-3

n1 = 1.0
n2 = 1.5  # glass: 1.5
c = 1  # scale; c = 299792458 #m/s, speed of light in vacuum, exact

ang1 = radians(initial_angle)
med_fac = 5
med_thick = med_fac * initial_range
medium2 = box(pos=vec(0.5 * med_thick, 0, -0.25 * med_thick), axis=vec(1, 0, 0), length=med_thick, width=med_thick, height=med_thick, color=vec(0.75, 0.75, 1), opacity=0.25)


def wavelength_to_rgb(wavelength):
    '''This converts a given wavelength of light to an
    approximate RGB color value, with a false color spectrum
    This scales the wavelength to the visible light spectrum
    '''

    gamma = 0.8
    red = green = blue = 0
    if 380 <= wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - lambda_blue) / (440 - lambda_blue)
        red = ((-(wavelength - 440) / (440 - lambda_blue)) * attenuation) ** gamma
        blue = (1.0 * attenuation) ** gamma
    elif 440 <= wavelength <= 490:
        green = ((wavelength - 440) / (490 - 440)) ** gamma
        blue = 1.0
    elif 490 <= wavelength <= 510:
        green = 1.0
        blue = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif 510 <= wavelength <= 580:
        red = ((wavelength - 510) / (580 - 510)) ** gamma
        green = 1.0
    elif 580 <= wavelength <= 645:
        red = 1.0
        green = (-(wavelength - 645) / (645 - 580)) ** gamma
    elif 645 <= wavelength <= lambda_red:
        attenuation = 0.3 + 0.7 * (lambda_red - wavelength) / (lambda_red - 645)
        red = (1.0 * attenuation) ** gamma

    return vec(red, green, blue)


v1 = c / n1  # m/s, speed of light in medium 1 (left)
v2 = c / n2  # m/s, speed of light in medium 2 (right)

n12 = n1 / n2
ang2 = asin(n12 * sin(ang1))

rad_fac = 1e-3
shift_fac = 100

class Ray:
    def __init__(self, position, radius):
        self._ray = simple_sphere(pos=position, radius=radius, color=color.white, make_trail=True, trail_radius=radius)
        self._velocity = vec(0, 0, 0)

    def change_color_to(self, colour):
        self._ray.color = colour
        self._ray.trail_color = colour

    def update(self, angle):
        if self._ray.pos.x >= 0:
            self._velocity = v2 * vec(cos(angle), sin(angle), 0)

        self._ray.pos += self._velocity * dt

    def reset(self, angle, ray_shift):
        self._ray.clear_trail()
        self._ray.make_trail = False
        self._ray.pos = med_thick * vec(-cos(angle), -sin(angle), 0) + ray_shift
        self._ray.radius = rad_fac * med_thick
        self._ray.color = color.white
        self._ray.make_trail = True
        self._ray.trail_radius = self._ray.radius
        self._ray.v = v1 * vec(cos(angle), sin(angle), 0)

    def pos(self):
        return self._ray.pos

    def radius(self):
        return self._ray.radius

    def update_position(self):
        self._ray.pos += self._velocity * dt

class Rays:
    def __init__(self, ray_count=6, angle=45):
        self._rays = []
        self._ray_count = ray_count
        if ray_count > 10:
            self._ray_count = 10
        elif ray_count < 1:
            self._ray_count = 1

        angle = radians(angle)
        ray_shifts = self.ray_shifts(angle)
        for i in range(len(ray_shifts)):
            position = med_thick * vec(-cos(angle), -sin(angle), 0) + ray_shifts[i]
            radius = rad_fac * med_thick
            self._rays.append(simple_sphere(pos=position, radius=radius, color=color.white, make_trail=True, trail_radius=radius))

    def ray_shifts(self, angle):
        Nfacs = range(-int((self._ray_count - 1) / 2), int(self._ray_count / 2) + 1)
        return [Nfac * shift_fac * rad_fac * vec(-sin(angle), cos(angle), 0) for Nfac in Nfacs]

    def change_color_to(self, colour):
        for ray in self._rays:
            ray.color = colour
            ray.trail_color = colour

    def update(self, angle):
        for ray in self._rays:
            if ray.pos.x >= 0:
                ray.v = v2 * vec(cos(angle), sin(angle), 0)

            ray.pos += ray.v * dt

    def position_of_ray(self, index):
        return self._rays[index].pos

    def initialize(self, angle):
        ray_xmax_idx = 0
        ray_xmax = -med_thick
        ray_shifts = self.ray_shifts(angle)
        for i, ray in enumerate(self._rays):
            ray.clear_trail()
            ray.make_trail = False
            ray.pos = med_thick * vec(-cos(angle), -sin(angle), 0) + ray_shifts[i]
            ray.radius = rad_fac * med_thick
            ray.color = color.white
            ray.make_trail = True
            ray.trail_radius = ray.radius
            ray.v = v1 * vec(cos(angle), sin(angle), 0)
            if ray.pos.x > ray_xmax:
                ray_xmax_idx = i
                ray_xmax = ray.pos.x
        return ray_xmax_idx

    def advance_to_mid_screen(self, ray_xmax_idx):
        while rays.position_of_ray(ray_xmax_idx).x < -0.666 * initial_range:
            for ray in self._rays:
                ray.pos += ray.v * dt
            wave_front.update(self)


class WaveFront:
    def __init__(self, rays):
        self._wavefront = []
        self._initialize(rays)

    def _initialize(self, rays):
        self._wavefront = []
        for i, r in enumerate(rays[:-1]):
            self._wavefront.append(cylinder(pos=r.pos, axis=rays[i + 1].pos - r.pos, radius=r.radius, color=color.white))

    def toggle_wavefront(self, event):
        for wave in self._wavefront:
            wave.visible = event.checked

    def change_color_to(self, colour):
        for wave in self._wavefront:
            wave.color = colour

    def update(self, rays):
        for i, w in enumerate(self._wavefront):
            w.pos = rays.position_of_ray(i)
            # at boundary, this will not be correct on length scale between rays
            w.axis = rays.position_of_ray(i + 1) - rays.position_of_ray(i)


rays = Rays()
wave_front = WaveFront(rays._rays)

def vary_color(event):
    is_white = True
    try:
        if 'white' in event.text:  # it's the radio
            is_white = event.checked
    # Comment out the AttributeError when in Glowscript
    except AttributeError:  # it's the slider
        is_white = False
        lc_radio.checked = False

    light_color = color.white if is_white else wavelength_to_rgb(event.value)
    rays.change_color_to(light_color)
    wave_front.change_color_to(light_color)

def set_ang1(a):
    global ang1
    ang1 = radians(a.value)
    let_there_be_light()

dang = 1  # 5 degrees
ang_lim = 90 - dang  # +- limit of incident angle
display.append_to_caption('\nIncident angle:')
slider(value=initial_angle, min=-ang_lim, max=ang_lim, step=dang, length=.75 * canvas_width, bind=set_ang1)

def set_rate(event):
    global the_rate
    the_rate = event.value

display.append_to_caption('\n\nAnimation speed:')
slider(value=initial_rate, min=0, max=initial_rate * 5, length=.75 * canvas_width, bind=set_rate)

# wavelength in nanometers
display.append_to_caption('\n\nWavelength:')
_ = slider(value=585, min=lambda_blue, max=lambda_red, step=1, length=0.75 * canvas_width, bind=vary_color)
display.append_to_caption('\t')
lc_radio = radio(text='white', checked=True, bind=vary_color)
display.append_to_caption('\n\n')
_ = checkbox(text="Wavefront", bind=wave_front.toggle_wavefront, checked=True)


def move_light():
    rays.update(ang2)
    wave_front.update(rays)


def let_there_be_light():
    global ang2
    ang2 = asin(n12 * sin(ang1))
    ray_xmax_idx = rays.initialize(ang1)
    wave_front.update(rays)
    rays.advance_to_mid_screen(ray_xmax_idx)


let_there_be_light()

while True:
    rate(the_rate)
    move_light()
