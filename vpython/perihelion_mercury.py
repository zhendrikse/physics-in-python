# Web VPython 3.2
from vpython import sphere, vector, curve, rate, color, canvas, checkbox, acos, dot, pi, graph, gdots, gcurve

title = """&#x2022; Based on the original <a href="https://github.com/ckoerber/perihelion-mercury/blob/master/py-scripts/base_solution.py">base_solution.py</a> code
&#x2022; See also his <a href="https://www.ckoerber.com/media/professional/CKoerber-APS-April-2019.pdf">accompanying slides</a>
&#x2022; Refactored by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> in <a href="https://github.com/zhendrikse/science/blob/main/relativity/code/perihelion_mercury.py">perihelion_mercury.py</a>
&#x2022; Values are computed using the <a href="https://nssdc.gsfc.nasa.gov/planetary/factsheet">NASA fact sheet</a>

"""

animation = canvas(title=title, forward=vector(0, .5, -0.85), background=color.gray(0.075), center=vector(0, -1, 0), range=7)
sphere(pos=vector(0, 0, 0), texture="https://i.imgur.com/1nVWbbd.jpg", radius=40, shininess=0, opacity=0.5)

rM0 = 4.60  # Initial radius of Mercury orbit, in units of R0
vM0 = 5.10e-1  # Initial orbital speed of Mercury, in units of R0/T0
c_a = 9.90e-1  # Base acceleration of Mercury, in units of R0**3/T0**2
sun_schwarzschild_radius = 2.95e-7  # Schwarzschild radius of Sun,in units of R0
rL2 = 8.19e-7  # Specific angular momentum, in units of R0**2

# Initialize distance and velocity vectors of Mercury (at perihelion)
initial_position = vector(0, rM0, 0)
initial_velocity = vector(vM0, 0, 0)

sun = sphere(pos=vector(0, 0, 0), radius=1.5, texture="https://i.imgur.com/yoEzbtg.jpg")
sun.velocity = vector(0, 0, 0)

class Mercury:
    def __init__(self, position=initial_position, velocity=initial_velocity):
        self._mercurius = sphere(pos=position, radius=0.5, texture="https://i.imgur.com/SLgVbwD.jpeg")
        self._velocity = velocity
        self._trajectory = curve(radius=0.01, color=color.yellow)
        self._alpha = 1.e6
        self._beta = 1.e5

    def update_by(self, dt):
        current_pos = self._mercurius.pos

        self._trajectory.append(pos=current_pos)
        old_position_vector_magnitude_squared = (current_pos.mag * current_pos.mag)

        # Compute the factor coming from General Relativity
        fact = 1 + self._alpha * sun_schwarzschild_radius / current_pos.mag + self._beta * rL2 / old_position_vector_magnitude_squared

        acceleration_magnitude = c_a * fact / old_position_vector_magnitude_squared
        acceleration_vector = - acceleration_magnitude * (current_pos / current_pos.mag)

        self._velocity += acceleration_vector * dt
        self._mercurius.pos += self._velocity * dt

    # Strength of 1/r**3 term
    def set_alpha(self, event):
        self._alpha = 1.e6 if event.value else 0

    # Strength of 1/r**4 term
    def set_beta(self, event):
        self._beta = 1.e5 if event.value else 0

    def pos(self):
        return self._mercurius.pos


mercurius = Mercury()

animation.append_to_caption("\n")
_ = checkbox(text="Alpha term ", bind=mercurius.set_alpha, checked=True)
_ = checkbox(text="Beta term ", bind=mercurius.set_beta, checked=True)
animation.append_to_caption("\n")

def angle_between(v1, v2):
    """Compute angle between two vectors. Result is in degrees."""
    return acos( dot(v1, v2) / (v1.mag * v2.mag) ) * 180. / pi

max_turns=10
graph_ = graph(title="Perihelion growth", background=color.black, xtitle="Number of turns", ytitle="Angle between perihelions (degrees)", xmin=2, xmax=max_turns, ymin=0, ymax=90)
dots_ = gdots(color=color.green)
curve_ = gcurve(color=color.cyan)

# Define run parameters
dt = 2. * vM0 / c_a / 20  # Time step
time = 0  # Current simulation time
turns = 0
vec_r_last = initial_position      # Previous position of Mercury
perihelion_list = list()       # List of perihelion locations
sum_angle  = 0.           # Angle between first and last perihelion
while turns < max_turns:
    vec_r_before_last = vec_r_last
    vec_r_last        = vector(mercurius.pos())
    rate(200)
    mercurius.update_by(dt)
    # Check if just past perihelion
    if vec_r_before_last.mag > vec_r_last.mag < mercurius.pos().mag:
        turns = turns+1
        perihelion_list.append(vec_r_last)
        if turns > 1:
            # Draw location of perihelion
            sphere(color=color.green, radius=0.2, pos=vec_r_last)
            sum_angle += angle_between(perihelion_list[-2], perihelion_list[-1])
            dots_.plot(turns, angle_between(perihelion_list[-2], perihelion_list[-1]))
            curve_.plot(turns, sum_angle)
