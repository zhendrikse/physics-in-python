# Web VPython 3.2

from vpython import box, helix, graph, vec, vector, sin, cos, sqrt, color, canvas, slider, mag, gcurve, rate, button

title = """&#x2022; Based on <a href="https://trinket.io/glowscript/1fe7d9cdd6">this code</a> and <a href="https://www.youtube.com/watch?v=dShtlMl69kY">accompanying video</a>
&#x2022; Refactored by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> to <a href="https://github.com/zhendrikse/science/blob/main/kinematics/code/numerical_methods.py">numerical_methods.py</a>

&#x2022; Comparison of accuracy of numerical methods:
   &#x2022; <span style="color: red">Exact solution (red))</span>
   &#x2022; <span style="color: cyan">Euler&apos;s method (cyan)</span>
   &#x2022; <span style="color: orange">Implicit Euler method (orange)</span> 
   &#x2022; <span style="color: purple">Runge-Kutta 2 (purple)</span>
   &#x2022; <span style="color: green">Runge-Kutta 4 (green)</span>

"""

display = canvas(title=title, width=600, background=color.gray(0.075), range=1.75, forward=vec(-.5, -.1, -.8))

amplitude = .5
phi = 0.0  # Phase angle
spring_rest_length = 1


class Oscillator:
    def __init__(self, block_height, spring_length, mass=3, k=2, colour=vector(0, 1, 1)):
        self._velocity = 0
        self._mass = mass
        self._spring_constant = k
        self._omega = sqrt(k / mass)  # Angular frequency (sqrt(k/m))
        self._clock = 0

        self._block = box(
            pos=vector(amplitude, block_height, 0),
            length=0.3, width=0.3, height=0.3,
            color=colour,
        )

        self._spring = helix(
            pos=vector(self._block.pos.x - spring_length, self._block.pos.y, 0),
            axis=vector(1, 0, 0),
            length=spring_length,
            radius=self._block.width / 3,
            thickness=0.02,
            color=colour
        )

    def _update_spring(self):
        self._spring.axis = self._block.pos - self._spring.pos
        self._spring.length = mag(self._spring.axis)

    def pos(self):
        return self._block.pos

    def _numerical_time_lapse(self, dt, num_method):
        self._block.pos.x, self._velocity = num_method(self._block.pos.x, self._velocity, dt, self._spring_constant,
                                                       self._mass)
        self._update_spring()

    def _exact_time_lapse(self, dt):
        self._clock += dt
        self._block.pos.x = amplitude * cos(self._omega * self._clock + phi)
        self._velocity = -amplitude * self._omega * sin(self._omega * self._clock + phi)
        self._update_spring()

    def time_lapse(self, dt, num_method=None):
        if num_method is None:
            self._exact_time_lapse(dt)
        else:
            self._numerical_time_lapse(dt, num_method)

    def reset(self):
        self._velocity = 0
        self._clock = 0
        self._block.pos.x = amplitude
        self._update_spring()


position_graph = graph(title="Position vs Time", xtitle='Time', ytitle='Pos_x', background=color.black)
exact_curve = gcurve(color=color.red)
euler_curve = gcurve(color=color.cyan)
implicit_curve = gcurve(color=color.orange)
rk2_curve = gcurve(color=color.purple)
rk4_curve = gcurve(color=color.green)

error_graph = graph(title="Errors: Euler [cyan] vs Implicit [orange] vs RK2 [purple] vs RK4 [green]", xtitle='Time',
                    ytitle='Error', background=color.black)
rk4_error = gcurve(color=color.green)
rk2_error = gcurve(color=color.purple)
euler_error = gcurve(color=color.cyan)
implicit_error = gcurve(color=color.orange)

exact_oscillator = Oscillator(1, spring_rest_length + amplitude, colour=color.red)
euler_oscillator = Oscillator(0.5, spring_rest_length + amplitude, colour=color.cyan)
implicit_euler_oscillator = Oscillator(0, spring_rest_length + amplitude, colour=color.orange)
runge_kutta_2_oscillator = Oscillator(-0.5, spring_rest_length + amplitude, colour=color.purple)
runge_kutta_4_oscillator = Oscillator(-1, spring_rest_length + amplitude, colour=color.green)


# Euler Method
def euler_step(position, velocity, dt, spring_constant, mass):
    acceleration = - (spring_constant / mass) * position
    v_new = velocity + acceleration * dt
    x_new = position + velocity * dt

    return x_new, v_new


# Implicit Euler Method
def implicit_euler_step(x, v, dt, k, m):
    A = 1 + (dt ** 2 * k / m)
    B = -dt * k / m

    x_new = (x + dt * v) / A
    v_new = v + dt * (-k / m * x_new)

    return x_new, v_new


# RK2 Method
def rk2_step(x, v, dt, k, m):
    def derivatives(x, v):
        return v, - (k / m) * x

    k1x, k1v = derivatives(x, v)
    k2x, k2v = derivatives(x + dt * k1x, v + dt * k1v)

    x_new = x + (dt / 2) * (k1x + k2x)
    v_new = v + (dt / 2) * (k1v + k2v)

    return x_new, v_new


# RK4 Method
def rk4_step(x, v, dt, k, m):
    def derivatives(x, v):
        return v, - (k / m) * x

    k1x, k1v = derivatives(x, v)
    k2x, k2v = derivatives(x + 0.5 * dt * k1x, v + 0.5 * dt * k1v)
    k3x, k3v = derivatives(x + 0.5 * dt * k2x, v + 0.5 * dt * k2v)
    k4x, k4v = derivatives(x + dt * k3x, v + dt * k3v)

    x_new = x + (dt / 6) * (k1x + 2 * k2x + 2 * k3x + k4x)
    v_new = v + (dt / 6) * (k1v + 2 * k2v + 2 * k3v + k4v)

    return x_new, v_new


# GUI controls
dt = .05
def set_dt(event):
    global dt
    dt = event.value

running = False
def toggle_run(button_):
    global running
    running = not running
    button_.text = "Stop" if running else "Run"


display.append_to_caption("\n")
run_button = button(
    text="Run",
    pos=display.caption_anchor,
    bind=toggle_run,
)

display.append_to_caption(" | Animation speed")
dt_slider = slider(
    bind=set_dt,
    max=0.15,
    min=0.0001,
    step=0.0001,
    value=0.05
)
display.append_to_caption("\n\n")

def run(t=0, frame_rate=60):
    global running
    while t < 25 * frame_rate:
        if not running:
            rate(10)
            continue

        rate(frame_rate)

        exact_oscillator.time_lapse(dt)
        euler_oscillator.time_lapse(dt, euler_step)
        implicit_euler_oscillator.time_lapse(dt, implicit_euler_step)
        runge_kutta_2_oscillator.time_lapse(dt, rk2_step)
        runge_kutta_4_oscillator.time_lapse(dt, rk4_step)

        exact_curve.plot(t, exact_oscillator.pos().x)
        euler_curve.plot(t, euler_oscillator.pos().x)
        implicit_curve.plot(t, implicit_euler_oscillator.pos().x)
        rk2_curve.plot(t, runge_kutta_2_oscillator.pos().x)
        rk4_curve.plot(t, runge_kutta_4_oscillator.pos().x)

        euler_error.plot(t, abs(exact_oscillator.pos().x - euler_oscillator.pos().x))
        implicit_error.plot(t, abs(exact_oscillator.pos().x - implicit_euler_oscillator.pos().x))
        rk4_error.plot(t, abs(exact_oscillator.pos().x - runge_kutta_4_oscillator.pos().x))
        rk2_error.plot(t, abs(exact_oscillator.pos().x - runge_kutta_2_oscillator.pos().x))

        t += 1

def reset():
    exact_oscillator.reset()
    euler_oscillator.reset()
    implicit_euler_oscillator.reset()
    runge_kutta_2_oscillator.reset()
    runge_kutta_4_oscillator.reset()
    display.range = 1.75
    implicit_curve.delete()
    exact_curve.delete()
    euler_curve.delete()
    rk2_curve.delete()
    rk4_curve.delete()
    euler_error.delete()
    implicit_error.delete()
    rk2_error.delete()
    rk4_error.delete()

while True:
    run()
    toggle_run(run_button)
    while not running:
        rate(10)
    reset()



