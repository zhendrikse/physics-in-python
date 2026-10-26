#Web VPython 3.2

title="""&#x2022; Original <a href="https://www.mso.anu.edu.au/pfrancis/simulations/pulsar.py">plusar.py</a> by <a href="http://www.mso.anu.edu.au/pfrancis/simulations/">Paul Francis</a>
&#x2022; Refactored by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> in <a href="https://github.com/zhendrikse/science/blob/main/astrophysics/code/pulsar.py">pulsar.py</a>

"""

from vpython import canvas, color, vector, sphere, rate, vec, local_light, cone, sin, cos, diff_angle, box, wtext, slider

display = canvas(title=title, background=color.gray(0.075), range=1, width=700, height=400, forward=vec(0.2, 0.6, -1.0))

display.lights = []
display.ambient = color.gray(0.2)


class NeutronStar:
    def __init__(self, position=vector(0.0, 0.0, 0.0), radius=0.1, colour=color.gray(0.4)):
        self._star = sphere(pos=position, radius=radius, color=colour)
        self._beam_length = 20.0
        self._beam_offset = 1.5 * self._beam_length
        self._light_frac = 0.005
        beam_position = self._beam_position(0.0)

        self._beam1 = cone(pos=beam_position, axis=-1.0 * beam_position, color=vec(0.5, 0.4, 1.0),
                     opacity=0.3, width=1.0, emissive=True)
        self._beam1light = local_light(pos=self._light_frac * beam_position, color=vec(1.0, 0.2, 1.0))

        self._beam2 = cone(pos=-1.0 * beam_position, axis=beam_position, color=vec(0.5, 0.4, 1.0),
                     opacity=0.1, width=1.0, emissive=True)
        self._beam2light = local_light(pos=-1.0 * self._light_frac * beam_position, color=vec(1.0, 0.2, 1.0))

        self._flare = box(pos=-1.0 * display.forward, axis=-1.0 * display.forward, width=10, height=10,
                    color=vec(1.0, 0.2, 1.0), visible=False)

    def _beam_position(self, theta):
        return vector(self._beam_length * cos(theta), self._beam_length * sin(theta), self._beam_offset)

    def update(self, theta):
        beam_position = self._beam_position(theta)
        self._beam1.pos = beam_position
        self._beam1.axis = -1.0 * beam_position
        self._beam1light.pos = self._light_frac * beam_position
        angle = diff_angle(self._beam1.axis, display.forward)
        self._beam1.opacity = 0.8 * cos(angle)
        if angle < 0.05:
            self._flare.visible = True
            display.ambient = color.gray(1.0)
        else:
            self._flare.visible = False
            display.ambient = color.gray(0.2)
        self._beam2.pos = -1.0 * beam_position
        self._beam2.axis = beam_position
        self._beam2light.pos = -1.0 * self._light_frac * beam_position


def set_animation_speed(event):
    global d_theta
    d_theta = event.value
    speed_slider_text.text = " = " + str(event.value)


display.append_to_caption("\nAnimation speed")
_ = slider(value=.03, min=.01, max=.1, bind=set_animation_speed)
speed_slider_text = wtext(text=" = .03")

# MathJax.Hub.Queue(["Typeset", MathJax.Hub])

neutron_star = NeutronStar()
d_theta = 0.03
theta = 0.0
while 1:
    rate(100)
    theta += d_theta
    neutron_star.update(theta)
