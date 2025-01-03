# GlowScript 2.6 VPython

from vpython import *

# ------------------------------------------------------------------------------
# Space (Scene) ----------------------------------------------------------------
simscene = canvas(title='(h = 60s) Three-Body Problem: Sun, Earth, Moon',
                  width=1200, height=500, align="left",
                  center=vec(1e11, 0, 0), forward=vec(0, 0, -1))
simscene.camera.pos = vec(1.52507e11, 0, 0)

# Add instructions below the display
s = "<b>Fly through the scene:</b><br>"
s += "To zoom in and out use the mouse scrollwheel.<br>"
s += "Left mouse click to show/delete the trail.<br>"
simscene.caption = s

# ------------------------------------------------------------------------------
# Constants --------------------------------------------------------------------
G = 6.67e-11  # gravitational constant

# units for distance - m
# units for mass - kg
# units for velocity - m/s

radS = 695.7e6  # Sun
mS = 1.989e30

radE = 6.371e6  # Earth
mE = 5.97e24

radM = 1.738e6  # Moon
mM = 7.34e22

distSE = 1.521e11  # the distance between the sun and the earth
distEM = 4.07e8  # the distance between the earth and the moon
distSM = distSE + distEM  # the distance between the sun and the moon

# ------------------------------------------------------------------------------
# Initial conditions -----------------------------------------------------------
# Lunar eclipse
x_i = 0  # Sun's initial coordinates
y_i = 0

x_j = distSE  # Earth's initial coordinates   // Aphelion
y_j = 0

x_k = distSM  # Moon's initial coordinates    // Apogee
y_k = 0

vx_i = 0
vy_i = 0  # Sun's initial velocity

vx_j = 0
vy_j = 29.3e3  # Earth's initial velocity in the aphelion

vx_k = 0
vy_k = 30.3e3  # Moon's initial velcoity in the apogee

# ------------------------------------------------------------------------------
# Bodies -----------------------------------------------------------------------
sun = sphere(radius=radS, pos=vec(0, 0, 0), color=color.yellow)

earth = sphere(radius=radE, pos=vec(1.521e11, 0, 0), texture=textures.earth,
               make_trail=True, trai_radius=-150)

moon = sphere(radius=radM, pos=vec(distSM, 0, 0), color=color.red,
              make_trail=True, trai_radius=-500)
# texture = textures.rough

simscene.camera.follow(earth)


def change():
    if earth.make_trail == True and moon.make_trail == True:
        earth.make_trail = False
        moon.make_trail = False
    else:
        earth.make_trail = True
        moon.make_trail = True


simscene.bind('click', change)


# ------------------------------------------------------------------------------
# Acceleration functions -------------------------------------------------------
def acc_fun_i_x(x_i, y_i, x_j, y_j, x_k, y_k):  # Sun

    term_1 = (mE * G * (x_j - x_i)) / (sqrt((x_j - x_i) ** 2 + (y_j - y_i) ** 2)) ** 3
    term_2 = (mM * G * (x_k - x_i)) / (sqrt((x_k - x_i) ** 2 + (y_k - y_i) ** 2)) ** 3

    return term_1 + term_2


def acc_fun_i_y(x_i, y_i, x_j, y_j, x_k, y_k):  # Sun

    term_1 = (mE * G * (y_j - y_i)) / (sqrt((x_j - x_i) ** 2 + (y_j - y_i) ** 2)) ** 3
    term_2 = (mM * G * (y_k - y_i)) / (sqrt((x_k - x_i) ** 2 + (y_k - y_i) ** 2)) ** 3

    return term_1 + term_2


def acc_fun_j_x(x_i, y_i, x_j, y_j, x_k, y_k):  # Earth

    term_1 = (mS * G * (x_i - x_j)) / (sqrt((x_i - x_j) ** 2 + (y_i - y_j) ** 2)) ** 3
    term_2 = (mM * G * (x_k - x_j)) / (sqrt((x_k - x_j) ** 2 + (y_k - y_j) ** 2)) ** 3

    return term_1 + term_2


def acc_fun_j_y(x_i, y_i, x_j, y_j, x_k, y_k):  # Earth

    term_1 = (mS * G * (y_i - y_j)) / (sqrt((x_i - x_j) ** 2 + (y_i - y_j) ** 2)) ** 3
    term_2 = (mM * G * (y_k - y_j)) / (sqrt((x_k - x_j) ** 2 + (y_k - y_j) ** 2)) ** 3

    return term_1 + term_2


def acc_fun_k_x(x_i, y_i, x_j, y_j, x_k, y_k):  # Moon

    term_1 = (mS * G * (x_i - x_k)) / (sqrt((x_i - x_k) ** 2 + (y_i - y_k) ** 2)) ** 3
    term_2 = (mE * G * (x_j - x_k)) / (sqrt((x_j - x_k) ** 2 + (y_j - y_k) ** 2)) ** 3

    return term_1 + term_2


def acc_fun_k_y(x_i, y_i, x_j, y_j, x_k, y_k):  # Moon

    term_1 = (mS * G * (y_i - y_k)) / (sqrt((x_i - x_k) ** 2 + (y_i - y_k) ** 2)) ** 3
    term_2 = (mE * G * (y_j - y_k)) / (sqrt((x_j - x_k) ** 2 + (y_j - y_k) ** 2)) ** 3

    return term_1 + term_2


# ------------------------------------------------------------------------------
# Time step (units for time - s (seconds))
h = 60  # 1 day = 86 400s // 1 h = 3600s  // 1 min = 60s // 1s

s = 0
T = 31557600  # In astronomy, the Julian year is a unit of time;
# it is defined as 365.25 days of exactly 86400 seconds (SI base unit),
# totalling exactly 31557600 seconds in the Julian astronomical year.

earthList = []
moonList = []

# Runge Kutta 4th order (Motion Loop) ------------------------------------------
while s <= T:
    rate(2000)
    s = s + h

    dx_i_a = h * vx_i
    dy_i_a = h * vy_i
    dx_j_a = h * vx_j
    dy_j_a = h * vy_j
    dx_k_a = h * vx_k
    dy_k_a = h * vy_k

    dvx_i_a = h * acc_fun_i_x(x_i, y_i, x_j, y_j, x_k, y_k)
    dvy_i_a = h * acc_fun_i_y(x_i, y_i, x_j, y_j, x_k, y_k)
    dvx_j_a = h * acc_fun_j_x(x_i, y_i, x_j, y_j, x_k, y_k)
    dvy_j_a = h * acc_fun_j_y(x_i, y_i, x_j, y_j, x_k, y_k)
    dvx_k_a = h * acc_fun_k_x(x_i, y_i, x_j, y_j, x_k, y_k)
    dvy_k_a = h * acc_fun_k_y(x_i, y_i, x_j, y_j, x_k, y_k)

    dx_i_b = h * (vx_i + (dvx_i_a / 2))
    dy_i_b = h * (vy_i + (dvy_i_a / 2))
    dx_j_b = h * (vx_j + (dvx_j_a / 2))
    dy_j_b = h * (vy_j + (dvy_j_a / 2))
    dx_k_b = h * (vx_k + (dvx_k_a / 2))
    dy_k_b = h * (vy_k + (dvy_k_a / 2))

    dvx_i_b = h * acc_fun_i_x(x_i + (dx_i_a / 2), y_i + (dy_i_a / 2),
                              x_j + (dx_j_a / 2), y_j + (dy_i_a / 2),
                              x_k + (dx_k_a / 2), y_k + (dy_k_a / 2))
    dvy_i_b = h * acc_fun_i_y(x_i + (dx_i_a / 2), y_i + (dy_i_a / 2),
                              x_j + (dx_j_a / 2), y_j + (dy_i_a / 2),
                              x_k + (dx_k_a / 2), y_k + (dy_k_a / 2))

    dvx_j_b = h * acc_fun_j_x(x_i + (dx_i_a / 2), y_i + (dy_i_a / 2),
                              x_j + (dx_j_a / 2), y_j + (dy_i_a / 2),
                              x_k + (dx_k_a / 2), y_k + (dy_k_a / 2))
    dvy_j_b = h * acc_fun_j_y(x_i + (dx_i_a / 2), y_i + (dy_i_a / 2),
                              x_j + (dx_j_a / 2), y_j + (dy_i_a / 2),
                              x_k + (dx_k_a / 2), y_k + (dy_k_a / 2))

    dvx_k_b = h * acc_fun_k_x(x_i + (dx_i_a / 2), y_i + (dy_i_a / 2),
                              x_j + (dx_j_a / 2), y_j + (dy_i_a / 2),
                              x_k + (dx_k_a / 2), y_k + (dy_k_a / 2))
    dvy_k_b = h * acc_fun_k_y(x_i + (dx_i_a / 2), y_i + (dy_i_a / 2),
                              x_j + (dx_j_a / 2), y_j + (dy_i_a / 2),
                              x_k + (dx_k_a / 2), y_k + (dy_k_a / 2))

    dx_i_c = h * (vx_i + (dvx_i_b / 2))
    dy_i_c = h * (vy_i + (dvy_i_b / 2))
    dx_j_c = h * (vx_j + (dvx_j_b / 2))
    dy_j_c = h * (vy_j + (dvy_j_b / 2))
    dx_k_c = h * (vx_k + (dvx_k_b / 2))
    dy_k_c = h * (vy_k + (dvy_k_b / 2))

    dvx_i_c = h * acc_fun_i_x(x_i + (dx_i_b / 2), y_i + (dy_i_b / 2),
                              x_j + (dx_j_b / 2), y_j + (dy_i_b / 2),
                              x_k + (dx_k_b / 2), y_k + (dy_k_b / 2))
    dvy_i_c = h * acc_fun_i_y(x_i + (dx_i_b / 2), y_i + (dy_i_b / 2),
                              x_j + (dx_j_b / 2), y_j + (dy_i_b / 2),
                              x_k + (dx_k_b / 2), y_k + (dy_k_b / 2))

    dvx_j_c = h * acc_fun_j_x(x_i + (dx_i_b / 2), y_i + (dy_i_b / 2),
                              x_j + (dx_j_b / 2), y_j + (dy_i_b / 2),
                              x_k + (dx_k_b / 2), y_k + (dy_k_b / 2))
    dvy_j_c = h * acc_fun_j_y(x_i + (dx_i_b / 2), y_i + (dy_i_b / 2),
                              x_j + (dx_j_b / 2), y_j + (dy_i_b / 2),
                              x_k + (dx_k_b / 2), y_k + (dy_k_b / 2))

    dvx_k_c = h * acc_fun_k_x(x_i + (dx_i_b / 2), y_i + (dy_i_b / 2),
                              x_j + (dx_j_b / 2), y_j + (dy_i_b / 2),
                              x_k + (dx_k_b / 2), y_k + (dy_k_b / 2))
    dvy_k_c = h * acc_fun_k_y(x_i + (dx_i_b / 2), y_i + (dy_i_b / 2),
                              x_j + (dx_j_b / 2), y_j + (dy_i_b / 2),
                              x_k + (dx_k_b / 2), y_k + (dy_k_b / 2))

    dx_i_d = h * (vx_i + dvx_i_c)
    dy_i_d = h * (vy_i + dvy_i_c)
    dx_j_d = h * (vx_j + dvx_j_c)
    dy_j_d = h * (vy_j + dvy_j_c)
    dx_k_d = h * (vx_k + dvx_k_c)
    dy_k_d = h * (vy_k + dvy_k_c)

    dvx_i_d = h * acc_fun_i_x(x_i + (dx_i_c / 2), y_i + (dy_i_c / 2),
                              x_j + (dx_j_c / 2), y_j + (dy_i_c / 2),
                              x_k + (dx_k_c / 2), y_k + (dy_k_c / 2))
    dvy_i_d = h * acc_fun_i_y(x_i + (dx_i_c / 2), y_i + (dy_i_c / 2),
                              x_j + (dx_j_c / 2), y_j + (dy_i_c / 2),
                              x_k + (dx_k_c / 2), y_k + (dy_k_c / 2))

    dvx_j_d = h * acc_fun_j_x(x_i + (dx_i_c / 2), y_i + (dy_i_c / 2),
                              x_j + (dx_j_c / 2), y_j + (dy_i_c / 2),
                              x_k + (dx_k_c / 2), y_k + (dy_k_c / 2))
    dvy_j_d = h * acc_fun_j_y(x_i + (dx_i_c / 2), y_i + (dy_i_c / 2),
                              x_j + (dx_j_c / 2), y_j + (dy_i_c / 2),
                              x_k + (dx_k_c / 2), y_k + (dy_k_c / 2))

    dvx_k_d = h * acc_fun_k_x(x_i + (dx_i_c / 2), y_i + (dy_i_c / 2),
                              x_j + (dx_j_c / 2), y_j + (dy_i_c / 2),
                              x_k + (dx_k_c / 2), y_k + (dy_k_c / 2))
    dvy_k_d = h * acc_fun_k_y(x_i + (dx_i_c / 2), y_i + (dy_i_c / 2),
                              x_j + (dx_j_c / 2), y_j + (dy_i_c / 2),
                              x_k + (dx_k_c / 2), y_k + (dy_k_c / 2))

    vx_i = vx_i + (1 / 6) * (dvx_i_a + 2 * dvx_i_b + 2 * dvx_i_c + dvx_i_d)
    vy_i = vy_i + (1 / 6) * (dvy_i_a + 2 * dvy_i_b + 2 * dvy_i_c + dvy_i_d)

    vx_j = vx_j + (1 / 6) * (dvx_j_a + 2 * dvx_j_b + 2 * dvx_j_c + dvx_j_d)
    vy_j = vy_j + (1 / 6) * (dvy_j_a + 2 * dvy_j_b + 2 * dvy_j_c + dvy_j_d)

    vx_k = vx_k + (1 / 6) * (dvx_k_a + 2 * dvx_k_b + 2 * dvx_k_c + dvx_k_d)
    vy_k = vy_k + (1 / 6) * (dvy_k_a + 2 * dvy_k_b + 2 * dvy_k_c + dvy_k_d)

    x_i = x_i + (1 / 6) * (dx_i_a + 2 * dx_i_b + 2 * dx_i_c + dx_i_d)
    y_i = y_i + (1 / 6) * (dy_i_a + 2 * dy_i_b + 2 * dy_i_c + dy_i_d)

    x_j = x_j + (1 / 6) * (dx_j_a + 2 * dx_j_b + 2 * dx_j_c + dx_j_d)
    y_j = y_j + (1 / 6) * (dy_j_a + 2 * dy_j_b + 2 * dy_j_c + dy_j_d)

    x_k = x_k + (1 / 6) * (dx_k_a + 2 * dx_k_b + 2 * dx_k_c + dx_k_d)
    y_k = y_k + (1 / 6) * (dy_k_a + 2 * dy_k_b + 2 * dy_k_c + dy_k_d)

    sun.pos = vec(x_i, y_i, 0)
    earth.pos = vec(x_j, y_j, 0)
    moon.pos = vec(x_k, y_k, 0)

    earthList.append([x_j, y_j])
    moonList.append([x_k, y_k])

# Numeric values for (x,y)
print('Earth - [x_E, y_E] - 1 year')
print(earthList[len(earthList) - 1])
print('\nInitial cooridnates (internet) [', distSE, ',', 0, ']')
print('\nInitial cooridnates after the first iteration')
print(earthList[0])

print('\n\nMoon - [x_M, y_M] - 1 year')
print(moonList[len(moonList) - 1])
print('\nInitial cooridnates (internet) [', distSM, ',', 0, ']')
print('\nInitial cooridnates after the first iteration')
print(moonList[0])

# Plot -------------------------------------------------------------------------
# Earth
eG = graph(width=600, height=600,
           title='<b>Earth\'s position - Plot</b>', title_align='center',
           xtitle='<i>x</i>', ytitle='<i>y</i>', align='right',
           xmax=1.6e11, xmin=-1.6e11)

eP = gcurve(pos=earthList, color=color.blue, width=0.2)  # a graphics curve

# Moon
mG = graph(width=600, height=600,
           title='<b>Moon\'s position - Plot</b>', title_align='center',
           xtitle='<i>x</i>', ytitle='<i>y</i>', align='left',
           xmax=1.6e11, xmin=-1.6e11)
mP = gcurve(pos=moonList, color=color.red, width=0.2)  # a graphics curve