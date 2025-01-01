from vpython import vec, color, pi, rate, scene, curve, label, vector, arrow

from ..toolbox.wave import ElectromagneticWave

scene.ambient = vec(.4, .4, .4)

waves_separation = 4.
step_range = 20
wavelength = step_range

color_scheme = 0



class WaveCollection:
    def __init__(self):
        waves = []
        for z in range(-2, 3, 1):
            waves += [ElectromagneticWave(position=vec(0, 0, z * waves_separation))]
        waves += [ElectromagneticWave(position=vec(0, waves_separation, 0))]
        waves += [ElectromagneticWave(position=vec(0, -waves_separation, 0))]
        self._waves = waves

    def faraday_color_for(self, color_scheme):
        return self._waves[0].magnetic_field_color_for(True, color_scheme)

    def ampere_color_for(self, color_scheme):
        return self._waves[0].electric_field_color_for(True, color_scheme)


def faraday_loop_with(faraday_color):
    height = waves_separation / 2.0
    return curve(
        pos=[vec(-1, -height, 0), vec(-1, height, 0), vec(1, height, 0), vec(1, -height, 0), vec(-1, -height, 0)],
        color=faraday_color)


def ampere_loop_with(ampere_color):
    height = waves_separation / 2.0
    return curve(
        pos=[vec(-1, 0, -height), vec(-1, 0, height), vec(1, 0, height), vec(1, 0, -height), vec(-1, 0, -height)],
        color=ampere_color)


def arrow_with(colour):
    return arrow(pos=vector(wavelength / 2, 0, 0), axis=vec(0, 0, 0), color=colour, shaftwidth=0.35, headwidth=0.7,
                 fixedwidth=1)


def ampere_label_with(ampere_color):
    ampere_label_background = [color.black, 0.2 * vec(1, 1, 1)]  # opacity
    ampere_label_opacity = [0.66, 0.9]  # opacity
    labelFontSizeSelected = 4
    labelFontSizes = [8, 12, 16, 20, 24, 30]
    return label(pos=vector(wavelength / 2, 0, 0), text='dE/dt', color=ampere_color,
                 opacity=ampere_label_opacity[color_scheme], background=ampere_label_background[color_scheme],
                 xoffset=20, yoffset=12, height=labelFontSizes[labelFontSizeSelected], border=6, font="sans")


def faraday_label_with(faraday_color):
    faraday_label_background = [0.0 * vec(1, 1, 1), vec(1, 1, 1)]  # opacity
    faraday_label_opacity = [0.9, 0.9]  # opacity
    label_epsV = vector(.1, .1, .1)
    labelFontSizeSelected = 4
    labelFontSizes = [8, 12, 16, 20, 24, 30]
    return label(pos=vector(wavelength / 2, 0, 0) + label_epsV, text='dB/dt', color=faraday_color,
                 opacity=faraday_label_opacity[color_scheme], background=faraday_label_background[color_scheme],
                 xoffset=20, yoffset=12, height=labelFontSizes[labelFontSizeSelected], border=6, font="sans")


waves = WaveCollection()

faraday_loop = faraday_loop_with(waves.faraday_color_for(color_scheme + 1))
ampere_loop = ampere_loop_with(waves.ampere_color_for(color_scheme + 1))
time_derivative_magnetic_field = arrow_with(waves.faraday_color_for(color_scheme + 1))
time_derivative_electric_field = arrow_with(waves.ampere_color_for(color_scheme + 1))
faraday_label = faraday_label_with(waves.faraday_color_for(color_scheme + 1))
ampere_label = ampere_label_with(waves.ampere_color_for(color_scheme + 1))


def move_frame_to(mouse_x):
    max_range = step_range * 2 * pi / wavelength
    frame_x = max_range if mouse_x >= max_range else mouse_x
    frame_x = -max_range if mouse_x <= -max_range else frame_x

    faraday_loop.modify(0, x=frame_x - 1)
    faraday_loop.modify(1, x=frame_x - 1)
    faraday_loop.modify(2, x=frame_x + 1)
    faraday_loop.modify(3, x=frame_x + 1)
    faraday_loop.modify(4, x=frame_x - 1)

    ampere_loop.modify(0, x=frame_x - 1)
    ampere_loop.modify(1, x=frame_x - 1)
    ampere_loop.modify(2, x=frame_x + 1)
    ampere_loop.modify(3, x=frame_x + 1)
    ampere_loop.modify(4, x=frame_x - 1)

    faraday_label.pos.x = frame_x
    ampere_label.pos.x = frame_x


dt = 0.05
t = 0
fi = 0
while True:
    rate(1 / dt)

    mouse_x = int(scene.mouse.pos.x)
    move_frame_to(mouse_x)

    for wave in waves._waves:
        t += dt
        wave.update(t)
