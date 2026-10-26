# Morris 2019/11/21

from vpython import vertex, color, quad, vec, canvas, helix, box, button, random, gcurve, winput, wtext, graph, rate
from dataclasses import dataclass
from ..toolbox.ball import Ball
from ..toolbox.spring import Spring

k, m = 1, 5
# critical, under, over = 2*m*(k/m)**0.5, 0.2, 10
gamma = 2*(m*k)**0.5


############################################################################################

animation = canvas(width=1000, height=600, background=vec(0, 0.6, 0.6), align='left')
animation.camera.pos = vec(-35, 80, 90)
animation.camera.axis = vec(25, -60, -90)

############################################################################################

# box()
# scene.caption = "\\(m\\dfrac {d^{2}x}{dt^{2}}+\\gamma \\dfrac {dx}{dt}+kx = 0\\)"

# MathJax.Hub.Queue(["Typeset",MathJax.Hub])

############################################################################################
 
A = vertex(pos=vec(50, 45, 17), color=color.green, opacity=0.2)
B = vertex(pos=vec(50, 45, -17), color=color.green, opacity=0.2)
D = vertex(pos=vec(-50, 45, 17), color=color.green, opacity=0.2)
C = vertex(pos=vec(-50, 45, -17), color=color.green, opacity=0.2)

E = vertex(pos=vec(50, -35, 17), color=color.green, opacity=0.2)
F = vertex(pos=vec(50, -35, -17), color=color.green, opacity=0.2)
H = vertex(pos=vec(-50, -35, 17), color=color.green, opacity=0.2)
G = vertex(pos=vec(-50, -35, -17), color=color.green, opacity=0.2)

# S1 = quad(v0=E, v1=F, v2=G, v3=H)
# S2 = quad(v0=A, v1=B, v2=E, v3=H)
# S3 = quad(v0=B, v1=C, v2=F, v3=E)
# S4 = quad(v0=C, v1=D, v2=G, v3=F)
# S5 = quad(v0=D, v1=A, v2=H, v3=G)


############################################################################################
block = []
balls = [] # Every restart a new ball

ball = Ball(mass=m, position=vec(0, 33, 0), velocity=vec(0, 0, 0), radius=3)


spring = helix(pos=vec(0, 33, 0), axis=vec(0, 37, 0), radius=3, coil=30,
                v=vec(0, 0, 0), a=vec(0, -35*k/m, 0))

a = box(pos=vec(0, 35, 0), size=vec(7, 7, 7), color=color.red, v=vec(0, 0, 0), a=vec(0, -35*k/m, 0))

block.append(a)

water = box(pos=vec(0, 2, 0), size=vec(100, 74, 34), color=vec(0, 0, 1), opacity=0.2)
celling = box(pos=vec(0, 70, 0), size=vec(100, 2, 34), color=vec(0.3, 0.3, 0.3))



############################################################################################

@dataclass
class InputParameters:
    spring_constant:float = k 
    mass: float = m
    gamma: float = gamma

    @staticmethod
    def obtain(input_k, input_m, input_gamma):
        spring_constant = k if input_k is None else input_k
        mass = m if input_m is None else input_m
        gamma_value = gamma if input_gamma is None else gamma
        return InputParameters(spring_constant, mass, gamma_value)
    
    def as_tuplet(self):
        return self.spring_constant, self.mass, self.gamma

running = False

def Run(r):
    global running
    running = not running
    r.text = "Pause" if running else "Run"

restart_counter = 0
curves = [] # Every restart a new curve
def Restart():
    global running, t, restart_counter
    k0, m0, gamma0 = InputParameters.obtain(input_spring_constant.number, input_mass.number, input_gamma.number).as_tuplet()

    running = False
    b1.text = 'Run'
    t = 0
    restart_counter += 1
    x, y, z = random(), random(), random()
    yt_idx = gcurve(graph=g1, color=vec(x, y, z))
    curves.append(yt_idx)

    block.append(box(pos=vec(0, 35, 0), size=vec(7, 7, 7), color=vec(x, y, z), v=vec(0, 0, 0), a=vec(0, -35*k0/m0, 0)))
    block[restart_counter-1].visible = False

    spring.pos = vec(0, 33, 0)
    spring.v = vec(0, 0, 0)
    spring.atom = vec(0, -35 * k0 / m0, 0)
    spring.axis = vec(0, 37, 0)

def set_spring_constant():
    k0, m0, gamma0 = InputParameters.obtain(input_spring_constant.number, input_mass.number, input_gamma.number).as_tuplet()
    update_critical_text_value(k0, m0, gamma0)

def set_mass():
    k0, m0, gamma0 = InputParameters.obtain(input_spring_constant.number, input_mass.number, input_gamma.number).as_tuplet()
    update_critical_text_value(k0, m0, gamma0)

def set_gamma():
    k0, m0, gamma0 = InputParameters.obtain(input_spring_constant.number, input_mass.number, input_gamma.number).as_tuplet()
    update_critical_text_value(k0, m0, gamma0)

def update_critical_text_value(k_tmp, m_tmp, gamma_tmp):
    k0, m0, gamma0 = InputParameters.obtain(input_spring_constant.number, input_mass.number, input_gamma.number).as_tuplet()
    txt1.text = 2 * (k0 * m0)**0.5

############################################################################################

animation.append_to_caption('      ')
b1 = button(text="Run", bind=Run, background=color.cyan)

animation.append_to_caption('      ')
b2 = button(text="Restart", bind=Restart, background=color.cyan)

animation.append_to_caption('\n\n      k =     ')
input_spring_constant = winput(bind=set_spring_constant, type='numeric')

animation.append_to_caption('\n\n      m =     ')
input_mass = winput(bind=set_mass, type='numeric')

animation.append_to_caption('\n\n      &Gamma; =     ')
input_gamma = winput(bind=set_gamma, type='numeric')

animation.append_to_caption('\n\n      (for critical damping &Gamma; = ')
txt1 = wtext(text=2*(k*m)**0.5)
animation.append_to_caption(')')

animation.append_to_caption('<i>\n\n(Please press enter after setting each parameter to confirm the setting,\n otherwise it will run on default parameter)</i>')

############################################################################################
g1 = graph(title='Position', xtitle='t', ytitle='position', align='right', width=500, height=300)

yt_idx = gcurve(graph=g1, color=color.red)
curves.append(yt_idx)
############################################################################################

dt = 0.01
t = 0

while True:

    if running:
        k0, m0, gamma0 = InputParameters.obtain(input_spring_constant.number, input_mass.number, input_gamma.number).as_tuplet()

        rate(300)
        block[restart_counter].atom.y = -k0 * block[restart_counter].pos.y / m0 - block[restart_counter].v.y * gamma0 / m0
        block[restart_counter].v.y += block[restart_counter].atom.y * dt
        block[restart_counter].pos.y += block[restart_counter].v.y * dt

        spring.atom.y = -k0 * spring.pos.y / m0 - spring.v.y * gamma0 / m0

        spring.v.y += spring.atom.y * dt
        spring.pos.y += spring.v.y*dt
        spring.axis.y -= spring.v.y*dt

        curves[restart_counter].plot(pos=(t, block[restart_counter].pos.y))

        t += dt