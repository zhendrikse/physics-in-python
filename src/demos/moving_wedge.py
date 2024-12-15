from vpython import radians, tan, sin,cos, exp, vec, canvas, button, winput, vertex, color, quad, triangle, textures, gdots, graph, rate, box, sphere
from dataclasses import dataclass

wedge_mass, ball_mass, grav_constant, theta, friction_constant = 3.0, 1.0, 9.8, 45, 0.0

@dataclass
class Accelerations:
    acceleration_ball_x: float = 0.0
    acceleration_ball_y: float = 0.0
    acceleration_wedge_x: float = 0.0

def calculate_accelerations(theta, friction, mass_wedge, mass_ball):
    theta = radians(theta)
    total_mass = mass_ball + mass_wedge
    if friction >= tan(theta):
        # too much friction to get the ball moving!
        acceleration_ball, acceleration_wedge, acceleration_ball_x, acceleration_ball_y, acceleration_wedge_x = 0.0, 0.0, 0.0, 0.0, 0.0
    else:
        acceleration_ball = grav_constant/(mass_wedge*(cos(theta)**2 + friction*sin(theta)*cos(theta))/(total_mass)/(sin(theta) - friction*cos(theta))+ sin(theta))
        acceleration_wedge = mass_ball * cos(theta) / (total_mass) * acceleration_ball

        acceleration_ball_x = acceleration_ball * cos(theta) - acceleration_wedge
        acceleration_ball_y = -acceleration_ball * sin(theta)
        acceleration_wedge_x = -acceleration_wedge

    return Accelerations(acceleration_ball_x, acceleration_ball_y, acceleration_wedge_x)

accelerations = calculate_accelerations(theta, friction_constant, wedge_mass, ball_mass)

def set_scene():
    global scene
    scene = canvas(width=1000, height=300, align='left')
    scene.camera.pos = vec(30, 10, 40)
    scene.camera.axis = vec(-5, -10, -30)

set_scene()

running = False

def Run(r):
    global running
    running = not running
    if running: 
        r.text = "Pause"
    else: 
        r.text = "Run"

def restart():
    theta_tmp, friction_tmp, M_tmp, m_tmp = s1.number, s2.number, s0.number, s3.number
    if theta_tmp == None: theta_tmp = theta
    if friction_tmp == None: friction_tmp = friction_constant
    if M_tmp == None: M_tmp = wedge_mass
    if m_tmp == None: m_tmp = ball_mass

    global running
    global t 
    running = False
    b1.text = "Run"
    t = 0
    m_v.delete()
    M_v.delete()
    # m_p.delete()
    # M_p.delete()
    total_E.delete()
    m_E.delete()
    M_E.delete()
    A.pos, B.pos, C.pos, D.pos, E.pos, F.pos = vec(0, 0, 0), vec(10/tan(radians(theta_tmp)), 0, 0), vec(10/tan(radians(theta_tmp)), 0, 10), vec(0, 0, 10), vec(0, 10, 10), vec(0, 10, 0)
    A.v, B.v, C.v, D.v, E.v, F.v = vec(0,0,0), vec(0,0,0), vec(0,0,0), vec(0,0,0), vec(0,0,0), vec(0,0,0)
    apex = [A, B, C, D, E, F]
    acclerations = calculate_accelerations(theta_tmp, friction_tmp, M_tmp, m_tmp)

    for i in range(0,len(apex)):
        apex[i].v.x, apex[i].a.x = 0, acclerations.acceleration_wedge_x
    ball.v, ball.pos, ball.a.x, ball.a.y = vec(0,0,0), vec(1.5/sin(radians(theta_tmp)), 10, 5), acclerations.acceleration_ball_x, acclerations.acceleration_ball_y


def set_theta():
    theta_tmp, friction_tmp, M_tmp, m_tmp = s1.number, s2.number, s0.number, s3.number
    if theta_tmp == None: theta_tmp = theta
    if friction_tmp == None: friction_tmp = friction_constant
    if M_tmp == None: M_tmp = wedge_mass
    if m_tmp == None: m_tmp = ball_mass
    if theta_tmp > 80 or theta_tmp < 10: theta_tmp = theta
    acclerations = calculate_accelerations(theta_tmp, friction_tmp, M_tmp, m_tmp)

    for i in range(1,3):
        apex[i].pos.x = 10/tan(radians(theta_tmp))

    for i in range(0,6):
        apex[i].a.x = acclerations.acceleration_wedge_x

    ball.pos.x = 1.5/sin(radians(theta_tmp))
    ball.a.x, ball.a.y = acclerations.acceleration_ball_x, acclerations.acceleration_ball_y

def set_friction():
    theta_tmp, friction_tmp, M_tmp, m_tmp = s1.number, s2.number, s0.number, s3.number
    if theta_tmp == None: theta_tmp = theta
    if friction_tmp == None: friction_tmp = friction_constant
    if M_tmp == None: M_tmp = wedge_mass
    if m_tmp == None: m_tmp = ball_mass

    acclerations = calculate_accelerations(theta_tmp, friction_tmp, M_tmp, m_tmp)

    for i in range(0,6):
        apex[i].a.x = acclerations.acceleration_wedge_x

    ball.a.x, ball.a.y = acclerations.acceleration_ball_x, acclerations.acceleration_ball_y


def set_mass():
    theta_tmp, friction_tmp, M_tmp, m_tmp = s1.number, s2.number, s0.number, s3.number
    if theta_tmp == None: theta_tmp = theta
    if friction_tmp == None: friction_tmp = friction_constant
    if M_tmp == None: M_tmp = wedge_mass
    if m_tmp == None: m_tmp = ball_mass

    acclerations = calculate_accelerations(theta_tmp, friction_tmp, M_tmp, m_tmp)

    for i in range(0,6):
        apex[i].a.x = acclerations.acceleration_wedge_x

    ball.a.x, ball.a.y = acclerations.acceleration_ball_x, acclerations.acceleration_ball_y

scene.append_to_caption('      ')
b1 = button(text="Run", bind=Run, background=color.cyan)

scene.append_to_caption('      ')
b2 = button(text="Restart", bind=restart, background=color.cyan)

scene.append_to_caption('\n\nM =     ')
s0 = winput(bind=set_mass, type='numeric')

scene.append_to_caption('\n\nm =     ')
s3 = winput(bind=set_mass, type='numeric')

scene.append_to_caption('\n\nAngle of wedge(10~80):')
s1 = winput(bind=set_theta, type='numeric')

scene.append_to_caption(' Degree\n')

scene.append_to_caption('\n\nCoefficient of friction on the slope: ')      
s2 = winput(bind=set_friction, type='numeric')

scene.append_to_caption('<i>\n\n(Please press enter after setting each parameter, otherwise \n it will run on default parameter)</i>')
scene.append_to_caption('\n\n\n\n\n')

def set_wedge():

    A = vertex(pos=vec(0, 0, 0), color=color.orange, v=vec(0, 0, 0), a=vec(accelerations.acceleration_wedge_x, 0, 0))
    B = vertex(pos=vec(10/tan(radians(theta)), 0, 0), color=color.purple, v=vec(0, 0, 0), a=vec(accelerations.acceleration_wedge_x, 0, 0))
    C = vertex(pos=vec(10/tan(radians(theta)), 0, 10), color=color.green, v=vec(0, 0, 0), a=vec(accelerations.acceleration_wedge_x, 0, 0))
    D = vertex(pos=vec(0, 0, 10), color=color.blue, v=vec(0, 0, 0), a=vec(accelerations.acceleration_wedge_x, 0, 0))
    E = vertex(pos=vec(0, 10, 10), color=color.cyan, v=vec(0, 0, 0), a=vec(accelerations.acceleration_wedge_x, 0, 0))
    F = vertex(pos=vec(0, 10, 0), color=color.red, v=vec(0, 0, 0), a=vec(accelerations.acceleration_wedge_x, 0, 0))

    apex = [A, B, C, D, E, F]

    T1 = triangle(v0=E, v1=D, v2=C)
    T2 = triangle(v0=F, v1=A, v2=B)
    Q1 = quad(v0=F, v1=E, v2=D, v3=A)
    Q2 = quad(v0=F, v1=E, v2=C, v3=B)
    Q3 = quad(v0=A, v1=B, v2=C, v3=D)

    return A, B, C, D, E, F

A, B, C, D, E, F = set_wedge()
apex = [A, B, C, D, E, F]

floor = box(pos=vec(0,0,0), size=vec(300, 1, 30), color=color.blue, v=vec(0, 0, 0), 
            a=vec(0, 0, 0))

ball = sphere(pos=vec(1.5/sin(radians(theta)), 10, 5), radius=1.5, v=vec(0, 0, 0),

            a=vec(accelerations.acceleration_ball_x, accelerations.acceleration_ball_y, 0), texture=textures.wood)

g1 = graph(title='<b>Velocity (x direction)</b>', 
           xtitle='<b>time</b>', ytitle='<b>P</b>', 
           align='left', width=500, height=300)

g2 = graph(title='<b>Energy<b>', xtitle='<b>time</b>', 
           ytitle='<b>E</b>', align='left', width=500, height=300)

m_v = gdots(graph=g1, color=color.red)
M_v = gdots(graph=g1, color=color.green)


m_E = gdots(graph=g2, color=color.blue)
M_E = gdots(graph=g2, color=color.red)
total_E = gdots(graph=g2, color=color.green)

dt = 0.01
t = 0
while True:
    rate(1/dt)
  
    if ball.pos.x > 50:
        running = False

    if running:
        ball.v.x += ball.a.x * dt
        ball.pos.x += ball.v.x * dt
        ball.v.y += ball.a.y * dt
        ball.pos.y += ball.v.y * dt

        for i in range(0,6):
            apex[i].v.x += apex[i].a.x * dt
            apex[i].pos.x += apex[i].v.x * dt

        if ball.pos.y <= ball.radius+floor.size.y/2:
            ball.v.x = (ball.v.x**2 + ball.v.y**2)**0.5
            ball.a.x, ball.a.y, ball.v.y = 0, 0, 0
            ball.up = vec(0, 1, 0)
            ball.pos.x += ball.v.x * dt

            for i in range(0,6):
                apex[i].a.x = 0
                apex[i].pos.x += apex[i].v.x * dt



        if s0.number == None: tmp_M = wedge_mass
        else: tmp_M = s0.number
        if s3.number == None: tmp_m = ball_mass
        else: tmp_m = s3.number

        if ball.pos.y >= ball.radius+floor.size.y/2:
            p = ball.v.x * tmp_m + A.v.x * tmp_M
            m_v.plot(pos=(t, ball.v.x))
            M_v.plot(pos=(t, A.v.x))

            # m_p.plot(pos=(t, m * ball.v.x))

            # M_p.plot(pos=(t, s0.value * A.v.x))

        K = 0.5*tmp_m*(ball.v.x**2 + ball.v.y**2) + 0.5*tmp_M*A.v.x**2
        U = tmp_m*grav_constant*(ball.pos.y - (ball.radius+floor.size.y/2))

        m_E.plot(pos=(t, K))
        M_E.plot(pos=(t, U))
        total_E.plot(pos=(t, K+U))

        t += dt