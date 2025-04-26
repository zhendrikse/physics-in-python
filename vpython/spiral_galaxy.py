# Web VPython 3.2
from vpython import *

title = """&#x2022; Original <a href="https://gist.github.com/rlvaugh/a49bf875890581f338a000c2b5c3a2bb">galaxy_3d_Medium.py</a> by <a href="https://towardsdatascience.com/author/lee_vaughan/">Lee Vaughan</a>
&#x2022; The (theory behind the) code is thoroughly explained in his <a href="https://towardsdatascience.com/create-3-d-galactic-art-with-matplotlib-a7534148a319/">accompanying article</a>
&#x2022; Ported to <a href="https://vpython.org">VPython</a> by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> in <a href="https://github.com/zhendrikse/science/blob/main/astrophysics/code/spiral_galaxy.py">spiral_galaxy.py</a>

"""

from random import randint, uniform, random

# Set the radius of the galactic disc (scaling factor):
SCALE = 500  # Use range of 200 - 700.


def build_spiral_stars(b, r, rot_fac, fuz_fac):
    """Return list of (x,y,z) points for a logarithmic spiral.

    b = constant for spiral direction and "openess"
    r = scale factor (galactic disc radius)
    rot_fac = factor to rotate each spiral arm
    fuz_fac = random shift in star position in arm, applied to 'fuzz' variable
    """
    fuzz = int(0.030 * abs(r))  # Scalable initial amount to shift locations.
    num_stars = 1000
    spiral_stars = []
    for i in range(0, num_stars):
        theta = radians(i)
        x = r * exp(b * theta) * cos(theta - pi * rot_fac) - randint(-fuzz, fuzz) * fuz_fac
        y = r * exp(b * theta) * sin(theta - pi * rot_fac) - randint(-fuzz, fuzz) * fuz_fac
        z = uniform((-SCALE / (SCALE * 3)), (SCALE / (SCALE * 3)))
        spiral_stars.append(vec(x, y, z))
    return spiral_stars


# Assign scale factor, rotation factor and fuzz factor for spiral arms.
# Each arm is a pair: leading arm + trailing arm:
arms_info = [(SCALE, 2, 1.5), (SCALE, 1.91, 1.5),
             (-SCALE, 2, 1.5), (-SCALE, -2.09, 1.5),
             (-SCALE, 0.5, 1.5), (-SCALE, 0.4, 1.5),
             (-SCALE, -0.5, 1.5), (-SCALE, -0.6, 1.5)]


def build_spiral_arms(b, arms_info):
    """Return lists of point coordinates for galactic spiral arms.

    b = constant for spiral direction and "openess"
    arms_info = list of scale, rotation, and fuzz factors
    """
    leading_arms = []
    trailing_arms = []
    for i, arm_info in enumerate(arms_info):
        arm = build_spiral_stars(b=b,
                                 r=arm_info[0],
                                 rot_fac=arm_info[1],
                                 fuz_fac=arm_info[2])
        if i % 2 != 0:
            leading_arms.extend(arm)
        else:
            trailing_arms.extend(arm)
    return leading_arms, trailing_arms


# Box-Muller transform to create a normal distribution
def gauss(mu, sigma):
    u1 = random()
    u2 = random()
    vt = sqrt(-2 * log(u1)) * cos(2 * pi * u2)
    vt *= sigma + mu
    return vt


def spherical_coordinates(num_pts, radius):
    """Return list of uniformly distributed points in a sphere."""
    position_list = []
    for _ in range(num_pts):
        position = radius * vector(gauss(0, 1), gauss(0, 1), gauss(0, 1))
        # position.z *= 0.02  # Reduce z range for matplotlib default z-scale.
        position_list.append(position)
    return position_list


def build_core_stars(scale_factor):
    """Return lists of point coordinates for galactic core stars."""
    core_radius = scale_factor / 15
    num_rim_stars = 3000
    outer_stars = spherical_coordinates(num_rim_stars, core_radius)
    inner_stars = spherical_coordinates(int(num_rim_stars / 4), core_radius / 2.5)
    return outer_stars + inner_stars


def haze(scale_factor, r_mult, z_mult, density):
    """Generate uniform random (x,y,z) points within a disc for 2-D display.

    scale_factor = galactic disc radius
    r_mult = scalar for radius of disc
    z_mult = scalar for z values
    density = multiplier to vary the number of stars posted
    """
    haze_coordinates = []
    for _ in range(0, scale_factor * density):
        n = random()
        theta = uniform(0, 2 * pi)
        x = round(sqrt(n) * cos(theta) * scale_factor) / r_mult
        y = round(sqrt(n) * sin(theta) * scale_factor) / r_mult
        z = uniform(-1, 1) * z_mult
        haze_coordinates.append(vec(x, y, z))
    return haze_coordinates


# Create lists of star positions for galaxy:
leading_arm, trailing_arm = build_spiral_arms(b=-0.3, arms_info=arms_info)
core = build_core_stars(SCALE)
inner_haze = haze(SCALE, r_mult=2, z_mult=0.5, density=5)
outer_haze = haze(SCALE, r_mult=1, z_mult=0.3, density=5)

display = canvas(background=color.gray(0.075), center=vec(0, -80, -80), range=SCALE, forward=vec(0, .75, -.7),
                 title=title)

def colorAt(position):
    distance = position.mag
    t = min(distance / SCALE, 1.0)  # 0 at center, 1 at border
    return color.hsv_to_rgb(vec(0.65 - 0.5 * t, 1.0, 0.6)) # from yellow (t=0) to blue (t=1)

leading_arm_stars = [simple_sphere(pos=position, color=colorAt(position), radius=5) for position in leading_arm]
trailing_arm_stars = [simple_sphere(pos=position, color=colorAt(position), radius=2) for position in trailing_arm]
core_stars = [simple_sphere(pos=position, color=colorAt(position), radius=1) for position in core]
inner_haze_stars = [simple_sphere(pos=position, color=colorAt(position), radius=1) for position in inner_haze]
outer_haze_stars = [simple_sphere(pos=position, color=colorAt(position), radius=1) for position in outer_haze]


while True:
    rate(10)
