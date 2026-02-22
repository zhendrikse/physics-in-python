#Web VPython 3.2
from vpython import pi, sphere, vector, norm, acos, color, rate, vec, canvas, sin, cos, arange, atan2, sqrt, box, checkbox, slider, label, mag, local_light

title="""&#x2022; Original <a href="https://github.com/lukekulik/solar-system">solar system</a> by <a href="https://github.com/lukekulik/">Luke Kulik</a>
&#x2022; Updated by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> in <a href="https://github.com/zhendrikse/science/blob/main/astrophysics/code/solar_system.py">solar_system.py</a>

&#x2022; Fast and accurate representation of all of the planets and bigger moons using Keplerian elements in 3D
  &#x2022; Includes tilt, spin and tidal locking of applicable moons e.g. Earth’s moon
&#x2022; Showing 'real time' data on velocity and position of any selected planet
&#x2022; Click on any planet for more information, click on sun to zoom in.

"""

display = canvas(title=title, width=600, height=400, forward=vec(0.55, -.5, -.7), range=1e9)#, background=color.black)
display.lights = []
display.ambient = color.gray(0.4)
display.fov = 0.8
lamp = local_light(pos=vec(0, 0, 0), color=color.white)

n = 10000  # number of orbit coordinates generated (affects temporal accuracy - dt(real)=365.25*86400/n (in seconds))
scale_up = 2000  # scaling factor for planets and moons radii
dt = 1  # initial time step
ship_mode = False
rate_ = 40

#################
# P L A N E T S #
#################

mercury = {'a': 57909050.,
           'e': 0.205630,
           'inclination': 7 * pi / 180.,
           'right_ascension': 0.8436854966,
           'mean_anomaly': 3.0507657193,
           'radius': 2439.7,
           'tilt': 0.1 * pi / 180.,
           'spin': 2 * pi / 4222.6,
           'material': "https://www.hendrikse.name/science/astrophysics/images/textures/mercury.png",
           'name': "Mercury"}

venus = {'a': 108208000.,
         'e': 0.0067,
         'inclination': 3.39 * pi / 180.,
         'right_ascension': 1.3381895772,
         'mean_anomaly': 0.8746717546,
         'radius': 6051.8,
         'tilt': 177 * pi / 180.,
         'spin': -2 * pi / 2802.,
         'material': "https://www.hendrikse.name/science/astrophysics/images/textures/venus.png",
         'name': "Venus"}

earth = {'a': 149598261.,
         'e': 0.01671123,
         'inclination': 0.,
         'right_ascension': 0.,
         'mean_anomaly': 6.2398515744,
         'radius': 6378.,
         'tilt': 23 * pi / 180.,
         'spin': 2 * pi / 24.,
         'material': "https://www.hendrikse.name/science/astrophysics/images/textures/earth.png",
         'name': "Earth"}

mars = {'a': 227939100.,
        'e': 0.093315,
        'inclination': 1.85 * pi / 180.,
        'right_ascension': 0.8676591934,
        'mean_anomaly': 0.3378329113,
        'radius': 3393.5,
        'tilt': 25 * pi / 180.,
        'spin': 2 * pi / 24.66,
        'material': "https://www.hendrikse.name/science/astrophysics/images/textures/mars.png",
        'name': "Mars"}

jupiter = {'a': 778547200.,
           'e': 0.048775,
           'inclination': 1.31 * pi / 180.,
           'right_ascension': 1.7504400393,
           'mean_anomaly': 0.3284360586,
           'radius': 71400.,
           'tilt': 3 * pi / 180.,
           'spin': 2 * pi / 9.93,
           'material': "https://www.hendrikse.name/science/astrophysics/images/textures/jupiter.png",
           'name': "Jupiter"}

saturn = {'a': 1433449370.,
          'e': 0.055723219,
          'inclination': 2.49 * pi / 180.,
          'right_ascension': 1.98,
          'mean_anomaly': 5.5911055356,
          'radius': 60000.,
          'tilt': 27 * pi / 180.,
          'spin': 2 * pi / 10.66,
          'material': "https://www.hendrikse.name/science/astrophysics/images/textures/saturn.png",
          'name': "Saturn"}

uranus = {'a': 2876679082.,
          'e': 0.044405586,
          'inclination': 0.77 * pi / 180.,
          'right_ascension': 1.2908891856,
          'mean_anomaly': 2.4950479462,
          'radius': 25600.,
          'tilt': 98 * pi / 180.,
          'spin': -2 * pi / 17.24,
          'material': "https://www.hendrikse.name/science/astrophysics/images/textures/uranus.png",
          'name': "Uranus"}

neptune = {'a': 4503443661.,
           'e': 0.011214269,
           'inclination': 1.77 * pi / 180.,
           'right_ascension': 2.3001058656,
           'mean_anomaly': 4.6734206826,
           'radius': 24300.,
           'tilt': 30 * pi / 180.,
           'spin': 2 * pi / 16.11,
           'material': "https://www.hendrikse.name/science/astrophysics/images/textures/neptune.png",
           'name': "Neptune"}

#############
# M O O N S #
#############

ScaleMoon = 300  # scaling factor for semi major axes of some moons

# moons have arbitrary scale factors applied to semi major axis and radius to make them properly visible

# dictionaries with moon parameters (lengths in km, inclinations w.r.t. plane of the ecliptic, spin in rad/h, \
# planet numbers from 0, tidal lock - 0/1, only including moons with radius > 500km,):

luna = {'a': 384399 * 50.,
        'e': 0.0549,
        'inclination': (-23.4 + 5.145) * pi / 180.,
        'right_ascension': -pi / 2.,
        'mean_anomaly': 0.,
        'radius': 1737.1,
        'tilt': 0.02691995838,
        'spin': 2 * pi / 708.7341666667,
        'material': "https://www.hendrikse.name/science/astrophysics/images/textures/earth_moon.jpg",
        'period': 27.321,
        'planet_name': "Earth",
        'planet_num': 2,
        'name': "Luna",
        'tidal_lock': 1}

phobos = {'a': 9376 * 1000,
          'e': 0.0151,
          'inclination': 0,
          'right_ascension': -pi / 2,
          'mean_anomaly': 0.,
          'radius': 11.2667 * 10,
          'tilt': 0.,
          'spin': 0,
          'material': "https://www.hendrikse.name/science/astrophysics/images/textures/moon.png",
          'period': 0.31891023,
          'planet_name': "Mars",
          'planet_num': 3,
          'name': "Phobos",
          'tidal_lock': 1}

deimos = {'a': 23463.2 * 650.,
          'e': 0.00033,
          'inclination': 0,
          'right_ascension': -pi / 2,
          'mean_anomaly': 0.,
          'radius': 10. * 10,
          'tilt': 0.,
          'spin': 0,
          'material': "https://www.hendrikse.name/science/astrophysics/images/textures/moon.png",
          'period': 1.263,
          'planet_name': "Mars",
          'planet_num': 3,
          'name': "Deimos",
          'tidal_lock': 1}

callisto = {'a': 1882700 * ScaleMoon / 2,
            'e': 0.0074,
            'inclination': 0.003351032164,
            'right_ascension': 0.,
            'mean_anomaly': 0.,
            'radius': 2410.3,
            'tilt': 0.,
            'spin': 0,
            'material': "https://www.hendrikse.name/science/astrophysics/images/textures/moon.png",
            'period': 16.689,
            'planet_name': "Jupiter",
            'planet_num': 4,
            'name': "Callisto",
            'tidal_lock': 1}

europa = {'a': 670900 * ScaleMoon,
          'e': 0.009,
          'inclination': 0.008203047484,
          'right_ascension': 0.,
          'mean_anomaly': 0.,
          'radius': 1560.8,
          'tilt': 0.,
          'spin': 0,
          'material': "https://www.hendrikse.name/science/astrophysics/images/textures/moon.png",
          'period': 12.689,
          'planet_name': "Jupiter",
          'planet_num': 4,
          'name': "Europa",
          'tidal_lock': 1}

ganymede = {'a': 1070400 * ScaleMoon,
            'e': 0.0013,
            'inclination': 0.003490658504,
            'right_ascension': 0.,
            'mean_anomaly': 0.,
            'radius': 2634.1,
            'tilt': 0.,
            'spin': 0,
            'material': "https://www.hendrikse.name/science/astrophysics/images/textures/moon.png",
            'period': 10.689,
            'planet_name': "Jupiter",
            'planet_num': 4,
            'name': "Ganymede",
            'tidal_lock': 1}

io = {'a': 421800 * ScaleMoon * 1.5,
      'e': 0.0041,
      'inclination': 0.03857177647,
      'right_ascension': 0.,
      'mean_anomaly': 0.,
      'radius': 1821.6,
      'tilt': 0.,
      'spin': 0,
      'material': "https://www.hendrikse.name/science/astrophysics/images/textures/moon.png",
      'period': 6.689,
      'planet_name': "Jupiter",
      'planet_num': 4,
      'name': "Io",
      'tidal_lock': 1}

dione = {'a': 377396 * 3 * ScaleMoon,
         'e': 0.0022,
         'inclination': 0,
         'right_ascension': -pi / 2.,
         'mean_anomaly': 0.,
         'radius': 561.4 * 3,
         'tilt': 0.,
         'spin': 0,
         'material': "https://www.hendrikse.name/science/astrophysics/images/textures/moon.png",
         'period': 7.689,
         'planet_name': "Saturn",
         'planet_num': 5,
         'name': "Dione",
         'tidal_lock': 1}

enceladus = {'a': 237948 * 3 * ScaleMoon,
             'e': 0.0047,
             'inclination': 0,
             'right_ascension': -pi / 2.,
             'mean_anomaly': 0.,
             'radius': 252.1 * 3,
             'tilt': 0.,
             'spin': 0,
             'material': "https://www.hendrikse.name/science/astrophysics/images/textures/moon.png",
             'period': 16.689,
             'planet_name': "Saturn",
             'planet_num': 5,
             'name': "Enceladus",
             'tidal_lock': 1}

tethys = {'a': 294619 * 3 * ScaleMoon,
          'e': 0.,
          'inclination': 0,
          'right_ascension': -pi / 2.,
          'mean_anomaly': 0.,
          'radius': 531.1 * 3,
          'tilt': 0.,
          'spin': 0,
          'material': "https://www.hendrikse.name/science/astrophysics/images/textures/moon.png",
          'period': 1.689,
          'planet_name': "Saturn",
          'planet_num': 5,
          'name': "Tethys",
          'tidal_lock': 1}

titan = {'a': 1221870 * ScaleMoon,
         'e': 0.0288,
         'inclination': 0,
         'right_ascension': -pi / 2.,
         'mean_anomaly': 0.,
         'radius': 2576.,
         'tilt': 0.,
         'spin': 0,
         'material': "https://www.hendrikse.name/science/astrophysics/images/textures/moon.png",
         'period': 61.689,
         'planet_name': "Saturn",
         'planet_num': 5,
         'name': "Titan",
         'tidal_lock': 1}

ariel = {'a': 191020 * ScaleMoon,
         'e': 0.0012,
         'inclination': 0,
         'right_ascension': -pi / 2.,
         'mean_anomaly': 0.,
         'radius': 578.9,
         'tilt': 0.,
         'spin': 0,
         'material': "https://www.hendrikse.name/science/astrophysics/images/textures/moon.png",
         'period': 16.689,
         'planet_name': "Uranus",
         'planet_num': 6,
         'name': "Ariel",
         'tidal_lock': 1}

oberon = {'a': 583520 * ScaleMoon,
          'e': 0.0014,
          'inclination': 0.,
          'right_ascension': -pi / 2.,
          'mean_anomaly': 0.,
          'radius': 761.4,
          'tilt': 0.,
          'spin': 0,
          'material': "https://www.hendrikse.name/science/astrophysics/images/textures/moon.png",
          'period': 6.689,
          'planet_name': "Uranus",
          'planet_num': 6,
          'name': "Oberon",
          'tidal_lock': 1}

titania = {'a': 435910 * ScaleMoon,
           'e': 0.0011,
           'inclination': 0,
           'right_ascension': -pi / 2.,
           'mean_anomaly': 0.,
           'radius': 788.4,
           'tilt': 0.,
           'spin': 0,
           'material': "https://www.hendrikse.name/science/astrophysics/images/textures/moon.png",
           'period': 1.689,
           'planet_name': "Uranus",
           'planet_num': 6,
           'name': "Titania",
           'tidal_lock': 1}

umbriel = {'a': 266000 * ScaleMoon,
           'e': 0.0039,
           'inclination': 0,
           'right_ascension': -pi / 2.,
           'mean_anomaly': 0.,
           'radius': 584.7,
           'tilt': 0.,
           'spin': 0,
           'material': "https://www.hendrikse.name/science/astrophysics/images/textures/moon.png",
           'period': 24.689,
           'planet_name': "Uranus",
           'planet_num': 6,
           'name': "Umbriel",
           'tidal_lock': 1}

triton = {'a': 354759 * ScaleMoon,
          'e': 0.,
          'inclination': 0.,
          'right_ascension': -pi / 2.,
          'mean_anomaly': 0.,
          'radius': 1353.4,
          'tilt': 0.,
          'spin': 0,
          'material': "https://www.hendrikse.name/science/astrophysics/images/textures/moon.png",
          'period': 16.689,
          'planet_name': "Neptune",
          'planet_num': 7,
          'name': "Triton",
          'tidal_lock': 1}

def lin_space(start, stop, num):
    return [x for x in arange(start, stop, (stop - start) / (num - 1))] + [stop]


def orbit(m0, e, a, inclination, ascension, n, acc=1.e-2):
    m = lin_space(m0, 2 * pi + m0, n)
    ecc_anom = m
    ecc_anom_old = [0 for i in range(n)]

    while acc < max([abs(ecc_anom[i] - ecc_anom_old[i]) for i in range(n)]):
        ecc_anom_old = ecc_anom
        for i in range(n):
          ecc_anom[i] -= (ecc_anom[i] - m[i] - e * sin(ecc_anom[i])) / (1. - e * cos(ecc_anom[i]))

    theta = [2. * atan2(sqrt(1. + e) * sin(ecc_anom[i] / 2.), sqrt(1. - e) * cos(ecc_anom[i] / 2.)) for i in range(n)] # true anomaly
    r = [a * (1 - e * cos(ecc_anom[i])) for i in range(n)]  # radius
    theta_asc = [theta[i] - ascension for i in range(n)]

    # conversion to cartesian coordinates:
    x = [r[i] * (cos(ascension) * cos(theta_asc[i]) - sin(ascension) * sin(theta_asc[i]) * cos(inclination)) for i in range(n)]
    z = [r[i] * (sin(ascension) * cos(theta_asc[i]) + cos(ascension) * sin(theta_asc[i]) * cos(inclination)) for i in range(n)]
    y = [r[i] * (sin(theta[i] - ascension) * sin(inclination)) for i in range(n)]

    # returning a vector with the coordinates for one orbital period for a given celestial body
    #print([[x[i], y[i], z[i]] for i in range(n)])
    return [vec(x[i], y[i], z[i]) for i in range(n)]

def planet_init(planet_data, n, scale_factor):  # retrieves data from planet dictionary and creates a planet
    a = planet_data['a']  # semi-major axis
    tilt = planet_data['tilt']
    timescale = (a / earth['a']) ** 1.5  # rotation period w.r.t. Earth
    spin = 365.25 * 24 * planet_data['spin'] / n  # rotation rate

    celestial = sphere(radius=planet_data['radius'] * scale_factor, texture=planet_data['material'], make_trail=True, retain=int(1.5e-9 * a ** 1.55 / dt))
    celestial.rotate(angle=tilt, axis=vec(0, 0, 1))  # tilt the planet

    # create orbit coordinates list for the planet
    coord = orbit(planet_data['mean_anomaly'], planet_data['e'], a, planet_data['inclination'], planet_data['right_ascension'], n)

    return [celestial, coord, timescale, a, tilt, spin]  # return a list with entries used in simulation

def moon_init(moon_data, planets, n, scale_up):  # retrieves data from moon dictionary and creates a moon

    tilt = moon_data['tilt']
    moon_scale = moon_data['period'] / 365.25  # rotation period w.r.t Earth
    spin = 365 * 24 * moon_data['spin'] / n  # rotation rate
    lock = moon_data['tidal_lock']

    celestial = sphere(radius=moon_data['radius'] * scale_up, texture=moon_data['material'])  # create an object using vPython class 'sphere'

    moon_coord = orbit(moon_data['mean_anomaly'], moon_data['e'], moon_data['a'],
                      planets[moon_data['planet_num']][4] + moon_data['inclination'],
                      moon_data['right_ascension'], n)  # create orbit coordinates list for the moon

    planet_coord = planets[moon_data['planet_num']][1]  # retrieve associated planet data
    planet_scale = planets[moon_data['planet_num']][2]  # retrieve associated planet rotation period w.r.t Earth

    # return a list with entries used in simulation
    return [celestial, planet_coord, moon_coord, planet_scale, moon_scale, tilt, spin, lock]

def moon_update(moonlist, t, dt, n):  # function updating the position of moons

    # assign a position from coordinates list - entire row based on time elapsed from the start of the
    # last period (%n), scaled w.r.t. Earth's period added to associated planet position at given time:

    moonlist[0].pos = moonlist[1][(int(-t / moonlist[3])) % n] + moonlist[2][(int(-t / moonlist[4])) % n]
    # first term - associated planet position, second term - moon position

    # tidal locking mechanism (calculates the change in the direction of the velocity vector and
    # rotates the moon accordingly):

    # moon velocity at time t w.r.t. its planet: (based on the change in position)
    vel_vect0 = vector(
        moonlist[2][(int(-(t + dt) / moonlist[4])) % n] - moonlist[2][(int(-(t) / moonlist[4])) % n])

    # moon velocity at time t+1 w.r.t. its planet: (based on the change in position)
    vel_vect1 = vector(
        moonlist[2][(int(-(t + 2 * dt) / moonlist[4])) % n] - moonlist[2][(int(-(t + dt) / moonlist[4])) % n])

    v0n, v1n = norm(vel_vect0), norm(vel_vect1)  # normalize velocity vectors
    cx = v0n.dot(v1n)  # take dot product of velocity vectors
    d1 = acos(cx)  # angle in radians between two moon velocity vectors

    # planet velocity at time t w.r.t. Sun: (based on the change in position)
    vel_vect2 = vector(
        moonlist[1][(int(-(t + dt) / moonlist[3])) % n] - moonlist[1][(int(-(t) / moonlist[3])) % n])

    # planet velocity at time t+1 w.r.t. Sun: (based on the change in position)
    vel_vect3 = vector(
        moonlist[1][(int(-(t + 2 * dt) / moonlist[3])) % n] - moonlist[1][(int(-(t + dt) / moonlist[3])) % n])

    v2n, v3n = norm(vel_vect2), norm(vel_vect3)  # normalize velocity vectors
    cx2 = v2n.dot(v3n)  # take dot product of velocity vectors
    d2 = acos(cx2)  # angle in radians between two planet velocity vectors

    if d2 > 1:  # protection against d2 becoming a large number if planet velocity does not change in given time step
        d2 = 0

    # rotate a moon by the increment corresponding to the time elapsed, around its tilted axis:
    moonlist[0].rotate(angle=(d1 - d2) * moonlist[7], axis=vec(-sin(moonlist[5]), cos(moonlist[5]), 0))

def planet_update(planet_data, t, dt, n):
    # assign a position from coordinates list - entire row based on time elapsed from the start of the
    # last period (%n), scaled w.r.t. Earth's period:
    planet_data[0].pos = planet_data[1][(int(-t / planet_data[2])) % n]

    # rotate a planet by the increment corresponding to the time elapsed, around its tilted axis:
    planet_data[0].rotate(angle=planet_data[5] * dt, axis=vec(-sin(planet_data[4]), cos(planet_data[4]), 0))

def show_planet_info(selected_object):
    global current_planet
    u = 132712440018.1  # Sun gravitational parameter
    err = 1e20  # large number for error comparison in the for loop below
    r0mag = mag(selected_object.pos)  # computing the instantaneous distance from the Sun

    selected_planet = None
    for planet_ in planet_list:
        if (abs(planet_['a'] - r0mag)) < err:
            err = (abs(planet_['a'] - r0mag))  # assign new closest value
            selected_planet = planet_

    # for moon in moon_list:
    #     if (abs(moon['a'] - r0mag)) < err:
    #         err = (abs(moon['a'] - r0mag))  # assign new closest value
    #         selected_planet = moon

    eps = -u / (2 * selected_planet['a'])  # compute specific orbital energy
    v0mag = (2 * (eps + u / r0mag)) ** 0.5  # velocity calculation using specific orbital energy

    popup.visible = True
    # update label text with new data:
    popup.text = str(selected_planet['name']) + \
                 "\nRadius: " + str(selected_planet['radius']) + " km" + \
                 "\nDistance from the Sun: " + str(int(round(r0mag))) + " km (" + str(
        round(r0mag / 149598261, 2)) + " AU)" + \
                 "\nOrbital Velocity: " + str(round(v0mag, 2)) + " km/s" + \
                 "\nTime scale: 1 s =  " + str(round(rate_ * dt * 365.25 * 86400 / (3600. * n), 3)) + "hrs"

def zoom_in_on(selected_object):
    # Clicked on sun? => We assume the user wants to zoom in
    target = selected_object.pos
    step = (target - display.center) / 20.0
    for _ in arange(1, 20, 1):
        rate(20)
        display.center += step
        display.range /= 1.037  # (1.037**19=1.99)

def select(selected_object):
    if selected_object is None:
        popup.visible = False
        return

    if selected_object is sun:
        popup.visible = False
        zoom_in_on(selected_object)
        return

    r0mag = mag(selected_object.pos)
    if r0mag > 1:
        display.center = selected_object.pos
        show_planet_info(selected_object)  # planet label update


# initializing unique (one-off) bodies:
sun = sphere(radius=695500 * 40, texture="https://www.hendrikse.name/science/astrophysics/images/textures/sun.jpg", emissive=True)  # radius in km
sun2 = sphere(radius=695500 * 40, texture="https://www.hendrikse.name/science/astrophysics/images/textures/sun3.png", opacity=0.7, visible=False)  # applying Sun spots
#stars = sphere(radius=30066790000, texture="https://www.hendrikse.name/science/astrophysics/images/textures/starX.png", emissive=True, opacity=0.5)  # constructing a stellar sphere
#stars = sphere(radius=30066790000, texture="https://www.hendrikse.name/science/astrophysics/images/textures/starX.png")  # constructing a stellar sphere


planet_list = [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

moon_list = [luna, phobos, deimos, callisto, europa, ganymede, io, dione, enceladus, tethys, titan, ariel, oberon,
             titania, umbriel, triton]

planets = []
for planet in planet_list:
    planets.append(planet_init(planet, n, scale_up))

moons = []
for moon in moon_list:
    moons.append(moon_init(moon, planets, n, scale_up))

saturn_ring = box(length=planets[5][0].radius + 180000 * scale_up, height=1,
                   width=planets[5][0].radius + 180000 * scale_up, texture="https://www.hendrikse.name/science/astrophysics/images/textures/saturn_ring.jpg")
saturn_ring.rotate(angle=saturn['tilt'], axis=vec(0, 0, 1))  # tilt corresponding to planet tilt

uranus_ring = box(length=planets[6][0].radius + 70000 * scale_up, height=1,
                   width=planets[6][0].radius + 70000 * scale_up, texture="https://www.hendrikse.name/science/astrophysics/images/textures/uranus_ring.jpg")
uranus_ring.rotate(angle=uranus['tilt'], axis=vec(0, 0, 1))  # tilt corresponding to planet tilt

def toggle_planet_trails(event):
    for planet_ in planets:
        planet_[0].clear_trail()
        planet_[0].make_trail = event.checked

def change_speed(event):
    global dt
    dt = event.value

def toggle_sun_texture(event):
    if event.checked:
        sun.texture = "https://www.hendrikse.name/science/astrophysics/images/textures/sun.jpg"
        sun2.visible = False
    else:
        sun2.visible = True
        sun.texture = "https://www.hendrikse.name/science/astrophysics/images/textures/sun.png"

_ = checkbox(text="Planet trails ", bind=toggle_planet_trails, checked=True)
_ = checkbox(text="Sun texture", bind=toggle_sun_texture, checked=True)

display.append_to_caption("\n\nAnimation speed:")
_ = slider(min=0.01, max=10, value=1, bind=change_speed)

# planet/spaceship label definition:
popup = label(visible=False, box=False, xoffset=-49, yoffset=50, font='sans', opacity=0.4)

current_planet = sun # dummy value, popup is not visible from the start anyhow
def on_mouse_click():
    global current_planet
    current_planet = display.mouse.pick
    select(current_planet)

display.bind('click', on_mouse_click)

t = 0  # time counter
while True:
    for planet in planets:
        planet_update(planet, t, dt, n)
    for moon in moons:  # moons coordinates update
        moon_update(moon, t, dt, n)

    saturn_ring.pos = planets[5][0].pos  # saturn's rings coordinates update
    uranus_ring.pos = planets[6][0].pos  # uranus rings coordinates update

    popup.pos = popup.pos if current_planet is None else current_planet.pos

    rate(rate_)
    t += dt
    if t >= 1e20:  # orbital reset, to prevent the counter from going to infinity
        t = 0
        # for planet in planets:  # removing the trail of all the planets
        #     planet[0].trail.append(pos=planet[1][:, 0], retain=0)
