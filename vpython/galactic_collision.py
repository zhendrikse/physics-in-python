# Web VPython 3.2
from vpython import canvas, color, vector, random, simple_sphere, pi, cos, sqrt, log, rate, slider, wtext, sphere

title = """&#x2022; <a href="https://github.com/SamirOmarov/galactic-collision">Original code</a> written by <a href="https://github.com/SamirOmarov/Personal-Website">Samir Omarov</a>
&#x2022; Ported to Glowscript <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in <a href="https://github.com/zhendrikse/science/blob/main/astrophysics/code/galactic_collision.py">galactic_collision.py</a>

"""

display = canvas(background=color.gray(0.075), width=650, range=5, forward=vector(.33, -.36, -.85), title=title, center=vector(-1.5, -.35, -.45))
stars = sphere(pos=vector(0, 0, 0), texture="https://www.hendrikse.name/science/astrophysics/images/textures/universe.jpg", radius=15, shininess=0, opacity=0.5, center=vector(-1.5, -.35, -.45))

# Universal gravitational constant
G = 6.673e-11

# Solar mass in kg (assume average stellar mass)
SOLAR_MASS = 2.000e30

# Precalculated bounds to solar mass
MIN_SOLAR_MASS = SOLAR_MASS * 0.5
MAX_SOLAR_MASS = SOLAR_MASS * 250
AVG_SOLAR_MASS = SOLAR_MASS * 3.0

# Scale distances for galactic scales
DIST_SCALE = 1e20  # 1e20

# Galactic parameters
MAX_ORBITAL_RADIUS = DIST_SCALE * 10
MIN_ORBITAL_RADIUS = DIST_SCALE * 0.15

MILKY_WAY_GALAXY_THICKNESS = DIST_SCALE * 0.9
ANDROMEDA_GALAXY_THICKNESS = DIST_SCALE * 0.2

# Milky Way contains about 300 billion stars
NUM_STARS_MILKY_WAY = 1400
# Andromeda Galaxy contains about 1 trillion (10^12) stars
NUM_STARS_ANDROMEDA = 2800

# Graphical constants
STAR_RADIUS = 0.025


# Limit x between lower and upper
def clamp(x, lower, upper):
    return max(min(x, upper), lower)


# Return the force due to gravity on an object
def gravity(mass1, mass2, radius):
    return G * mass1 * mass2 / radius * radius


# Return the acceleration due to gravity on an object.
def g_accel(mass, radius):
    # Limit minimum radius to avoid flinging out too many particles
    radius = max(radius, MIN_ORBITAL_RADIUS)
    return G * mass / radius / radius


# Calculate acceleration on an object caused by galaxy
def accel(obj, galaxy):
    r_galaxy = galaxy.position() - obj.position()
    # We have a = F / m = G * m_center / r ^2
    return r_galaxy.norm() * g_accel(galaxy.mass(), r_galaxy.mag)


# Box-Muller Transform To Create a Normal Distribution
def normal_distribution(mu, sigma):
    u1 = random()
    u2 = random()
    vt = sqrt(-2 * log(u1)) * cos(2 * pi * u2)
    vt *= sigma + mu
    return vt


class Star:
    def __init__(self, mass, radius, pos, vel, colour):
        self._obj = simple_sphere(pos=pos / DIST_SCALE, radius=radius, color=colour)
        self._mass = mass
        self._velocity = vel
        self._pos = pos

    def position(self):
        return self._pos

    def __str__(self):
        return "Mass: " + str(self._mass) + "\nPos: " + str(self._pos) + \
            "\nVel: " + str(self._velocity)

    def update_by(self, dt, milky_way, andromeda):
        self._velocity += accel(self, milky_way) * dt
        self._velocity += accel(self, andromeda) * dt
        self._pos += self._velocity * dt
        # Externally use scaled version for physics, use normalized version for graphics
        self._obj.pos = self._pos / DIST_SCALE

        mag_difference = milky_way.position().mag - andromeda.position().mag
        if -6 + 18 > mag_difference > -5e+18:
            self._obj.color = vector(1, 0.5, 0)
        # if andromeda.position().mag < 1.1920057081525512e+20:
        #    self._obj.color = vector(1, 0.5, 0)


class Galaxy:
    def __init__(self, num_stars, pos, vel, radius, thickness, colour):
        self._pos = pos
        self._mass = 0
        self._velocity = vel
        self._radius = radius
        self._stars = []

        # Gaussian distributions
        sigma_mass = AVG_SOLAR_MASS / 3.0
        masses = []
        for i in range(num_stars):
            masses += [clamp(normal_distribution(mu=AVG_SOLAR_MASS, sigma=sigma_mass), MIN_SOLAR_MASS, MAX_SOLAR_MASS)]

        # Galaxy mass is sum of all stars
        self._mass = sum(masses)

        # Gaussian distribution of positions
        sigma_x = radius * 0.1
        sigma_y = thickness * 0.10
        sigma_z = radius * 0.1

        # Generate list of all positions
        positions = []
        for i in range(num_stars):
            pos = vector(clamp(normal_distribution(mu=0, sigma=sigma_x), -radius, radius),
                         clamp(normal_distribution(mu=0, sigma=sigma_y), -thickness, thickness),
                         clamp(normal_distribution(mu=0, sigma=sigma_z), -radius, radius))

            # Limit radius to avoid particles shooting to nowhere
            if pos.mag < MIN_ORBITAL_RADIUS:
                pos.mag = MIN_ORBITAL_RADIUS

            positions.append(pos)

        # Generate list of all stars
        up = vector(0.0, 1.0, 0.0)
        for i in range(num_stars):
            # Find normalized vector along direction of travel
            absolute_pos = positions[i] + self._pos
            relative_pos = positions[i]
            vec = relative_pos.cross(up).norm()
            relative_vel = vec * self._calc_orbital_velocity(relative_pos.mag)
            absolute_vel = relative_vel + vel

            self._stars.append(Star(mass=masses[i], radius=STAR_RADIUS, pos=absolute_pos, vel=absolute_vel, colour=colour))

    def _calc_orbital_velocity(self, radius_):
        return sqrt(G * self._mass / radius_)

    def update_stars_by(self, dt, other_galaxy):
        for star in self._stars:
            star.update_by(dt, self, other_galaxy)

    def update_by(self, dt, galaxy):
        self._velocity += accel(self, galaxy) * dt
        self._pos += self._velocity * dt

    def position(self):
        return self._pos

    def mass(self):
        return self._mass


milky_way_galaxy = Galaxy(num_stars=NUM_STARS_MILKY_WAY, pos=vector(-5, 0, 0) * DIST_SCALE, vel=vector(0, 0, 0), radius=MAX_ORBITAL_RADIUS, thickness=MILKY_WAY_GALAXY_THICKNESS, colour=vector(0.9, 0.9, 1))
andromeda_galaxy = Galaxy(num_stars=NUM_STARS_ANDROMEDA, pos=vector(3, 0, 0) * DIST_SCALE, vel=vector(0, 3, 0), radius=MAX_ORBITAL_RADIUS, thickness=ANDROMEDA_GALAXY_THICKNESS, colour=vector(0, 0.5, 1))

def set_animation_speed(event):
    global frame_rate
    frame_rate = event.value
    speed_slider_text.text = " = " + str(event.value)


display.append_to_caption("\nAnimation speed")
_ = slider(value=10.0, min=1, max=100, bind=set_animation_speed)
speed_slider_text = wtext(text=" = 10")

# MathJax.Hub.Queue(["Typeset", MathJax.Hub])

delta_t = 1e17
frame_rate = 10
while True:
    rate(frame_rate)

    milky_way_galaxy.update_stars_by(delta_t, andromeda_galaxy)
    andromeda_galaxy.update_stars_by(delta_t, milky_way_galaxy)
    milky_way_galaxy.update_by(delta_t, andromeda_galaxy)
    andromeda_galaxy.update_by(delta_t, milky_way_galaxy)
