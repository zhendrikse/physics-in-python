from vpython import radians, tan, sin,cos, exp, vec, canvas, button, winput, vertex, color, quad, triangle, textures, gdots, graph, rate, box, sphere
from dataclasses import dataclass

ball_mass, grav_constant, theta, friction_constant = 1.0, 9.8, 45, 0.0

@dataclass
class Accelerations:
    acceleration_ball_x: float = 0.0
    acceleration_ball_y: float = 0.0
    acceleration_wedge_x: float = 0.0

class Wedge:
    def __init__(self, mass=3.0):
        self._mass = mass

        accelerations = self.calculate_accelerations(theta, friction_constant, mass, ball_mass)
        A = vertex(pos=vec(0, 0, 0), color=color.orange, v=vec(0, 0, 0), a=vec(accelerations.acceleration_wedge_x, 0, 0))
        B = vertex(pos=vec(10/tan(radians(theta)), 0, 0), color=color.purple, v=vec(0, 0, 0), a=vec(accelerations.acceleration_wedge_x, 0, 0))
        C = vertex(pos=vec(10/tan(radians(theta)), 0, 10), color=color.green, v=vec(0, 0, 0), a=vec(accelerations.acceleration_wedge_x, 0, 0))
        D = vertex(pos=vec(0, 0, 10), color=color.blue, v=vec(0, 0, 0), a=vec(accelerations.acceleration_wedge_x, 0, 0))
        E = vertex(pos=vec(0, 10, 10), color=color.cyan, v=vec(0, 0, 0), a=vec(accelerations.acceleration_wedge_x, 0, 0))
        F = vertex(pos=vec(0, 10, 0), color=color.red, v=vec(0, 0, 0), a=vec(accelerations.acceleration_wedge_x, 0, 0))

        self._apex = [A, B, C, D, E, F]

        T1 = triangle(v0=E, v1=D, v2=C)
        T2 = triangle(v0=F, v1=A, v2=B)
        Q1 = quad(v0=F, v1=E, v2=D, v3=A)
        Q2 = quad(v0=F, v1=E, v2=C, v3=B)
        Q3 = quad(v0=A, v1=B, v2=C, v3=D)

    def update(self, dt):
        for i in range(0, len(self._apex)):
            self._apex[i].v.x += self._apex[i].a.x * dt
            self._apex[i].pos.x += self._apex[i].v.x * dt

    def zero_acceleration(self):
        for i in range(0, len(self._apex)):
            self._apex[i].a.x = 0

    def calculate_accelerations(self, theta, friction, mass_wedge, mass_ball):
        theta = radians(theta)
        total_mass = mass_ball + mass_wedge
        if friction >= tan(theta):
            # too much friction to get the ball moving!
            acceleration_ball, acceleration_wedge, acceleration_ball_x, acceleration_ball_y, acceleration_wedge_x = 0.0, 0.0, 0.0, 0.0, 0.0
        else:
            acceleration_ball = grav_constant/(mass_wedge * (cos(theta)**2 + friction*sin(theta)*cos(theta))/(total_mass)/(sin(theta) - friction*cos(theta))+ sin(theta))
            acceleration_wedge = mass_ball * cos(theta) / (total_mass) * acceleration_ball

            acceleration_ball_x = acceleration_ball * cos(theta) - acceleration_wedge
            acceleration_ball_y = -acceleration_ball * sin(theta)
            acceleration_wedge_x = -acceleration_wedge

        return Accelerations(acceleration_ball_x, acceleration_ball_y, acceleration_wedge_x)
        
    def with_new_parameters(self, theta, accelerations):
        self._apex[0].pos, self._apex[1].pos, self._apex[2].pos, self._apex[3].pos, self._apex[4].pos, self._apex[5].pos = vec(0, 0, 0), vec(10/tan(radians(theta)), 0, 0), vec(10/tan(radians(theta)), 0, 10), vec(0, 0, 10), vec(0, 10, 10), vec(0, 10, 0)
        self._apex[0].v,   self._apex[1].v,   self._apex[2].v,   self._apex[3].v,   self._apex[4].v,   self._apex[5].v = vec(0,0,0), vec(0,0,0), vec(0,0,0), vec(0,0,0), vec(0,0,0), vec(0,0,0)

        for i in range(0, len(self._apex)):
            self._apex[i].a.x = accelerations.acceleration_wedge_x
            self._apex[i].v = vec(0, 0, 0)

    @property
    def velocity(self):
        return self._apex[0].v.x # all points of wedge move at equal velocity
    
    @property
    def mass(self):
        return self._mass

def set_scene():
    global scene
    scene = canvas(width=1000, height=300, align='left')
    scene.camera.pos = vec(30, 10, 40)
    scene.camera.axis = vec(-5, -10, -30)

def Run(r):
    global running
    running = not running
    if running: 
        r.text = "Pause"
    else: 
        r.text = "Run"

def restart():
    theta_tmp, friction_tmp, M_tmp, m_tmp = theta_input_field.number, friction_input_field.number, wedge_mass_input_field.number, ball_mass_input_field.number
    if theta_tmp == None: theta_tmp = theta
    if friction_tmp == None: friction_tmp = friction_constant
    if M_tmp == None: M_tmp = wedge.mass
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

    accelerations = wedge.calculate_accelerations(theta_tmp, friction_tmp, M_tmp, m_tmp)
    wedge.with_new_parameters(theta_tmp, accelerations)   
    ball.v, ball.pos, ball.a.x, ball.a.y = vec(0,0,0), vec(1.5/sin(radians(theta_tmp)), 10, 5), accelerations.acceleration_ball_x, accelerations.acceleration_ball_y

def get_parameter_values():
    theta_tmp, friction_tmp, M_tmp, m_tmp = theta_input_field.number, friction_input_field.number, wedge_mass_input_field.number, ball_mass_input_field.number
    if theta_tmp == None: theta_tmp = theta
    if friction_tmp == None: friction_tmp = friction_constant
    if M_tmp == None: M_tmp = wedge.mass
    if m_tmp == None: m_tmp = ball_mass
    if theta_tmp > 80 or theta_tmp < 10: theta_tmp = theta
    return theta_tmp, friction_tmp, M_tmp, m_tmp

def new_parameter_value():
    theta_tmp, friction_tmp, M_tmp, m_tmp = get_parameter_values()
    accelerations = wedge.calculate_accelerations(theta_tmp, friction_tmp, M_tmp, m_tmp)
    wedge.with_new_parameters(theta_tmp, accelerations)    
    ball.pos.x = 1.5/sin(radians(theta_tmp))
    ball.a.x, ball.a.y = accelerations.acceleration_ball_x, accelerations.acceleration_ball_y

set_scene()

running = False
wedge = Wedge()

scene.append_to_caption('      ')
b1 = button(text="Run", bind=Run, background=color.cyan)

scene.append_to_caption('      ')
b2 = button(text="Restart", bind=restart, background=color.cyan)

scene.append_to_caption('\n\nM =     ')
wedge_mass_input_field = winput(bind=new_parameter_value, type='numeric')

scene.append_to_caption('\n\nm =     ')
ball_mass_input_field = winput(bind=new_parameter_value, type='numeric')

scene.append_to_caption('\n\nAngle of wedge(10~80):')
theta_input_field = winput(bind=new_parameter_value, type='numeric')

scene.append_to_caption(' Degree\n')

scene.append_to_caption('\n\nCoefficient of friction on the slope: ')      
friction_input_field = winput(bind=new_parameter_value, type='numeric')

scene.append_to_caption('<i>\n\n(Please press enter after setting each parameter, otherwise \n it will run on default parameter)</i>')
scene.append_to_caption('\n\n\n\n\n')


floor = box(pos=vec(0,0,0), size=vec(300, 1, 30), color=color.blue, v=vec(0, 0, 0), 
            a=vec(0, 0, 0))

ball = sphere(pos=vec(1.5/sin(radians(theta)), 10, 5), radius=1.5, v=vec(0, 0, 0),
            a=vec(wedge.calculate_accelerations(theta, friction_constant, wedge.mass, ball_mass).acceleration_ball_x, wedge.calculate_accelerations(theta, friction_constant, wedge.mass, ball_mass).acceleration_ball_y, 0), 
            texture=textures.wood)

g1 = graph(title='<b>Velocity (x direction), ball=red, wedge=green</b>', 
           xtitle='<b>time</b>', ytitle='<b>P</b>', 
           align='left', width=500, height=300)

g2 = graph(title='<b>Energy, ball=blue, wedge=red, total=green<b>', xtitle='<b>time</b>', 
           ytitle='<b>E</b>', align='left', width=500, height=300)

m_v = gdots(graph=g1, color=color.red)
M_v = gdots(graph=g1, color=color.green)


m_E = gdots(graph=g2, color=color.blue)
M_E = gdots(graph=g2, color=color.red)
total_E = gdots(graph=g2, color=color.green)

def ball_on_ramp():
    return ball.pos.y >= ball.radius+floor.size.y / 2

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

        wedge.update(dt)

        if not ball_on_ramp():
            ball.v.x = (ball.v.x**2 + ball.v.y**2)**0.5
            ball.a.x, ball.a.y, ball.v.y = 0, 0, 0
            ball.up = vec(0, 1, 0)
            ball.pos.x += ball.v.x * dt

            wedge.zero_acceleration()
            wedge.update(dt)


        if wedge_mass_input_field.number == None: tmp_M = wedge.mass
        else: tmp_M = wedge_mass_input_field.number
        if ball_mass_input_field.number == None: tmp_m = ball_mass
        else: tmp_m = ball_mass_input_field.number

        if ball_on_ramp():
            p = ball.v.x * tmp_m + wedge.velocity * tmp_M
            m_v.plot(pos=(t, ball.v.x))
            M_v.plot(pos=(t, wedge.velocity))

            # m_p.plot(pos=(t, m * ball.v.x))
            # M_p.plot(pos=(t, s0.value * A.v.x))

        K = 0.5*tmp_m*(ball.v.x**2 + ball.v.y**2) + 0.5*tmp_M* wedge.velocity **2
        U = tmp_m*grav_constant*(ball.pos.y - (ball.radius+floor.size.y/2))

        m_E.plot(pos=(t, K))
        M_E.plot(pos=(t, U))
        total_E.plot(pos=(t, K+U))

        t += dt