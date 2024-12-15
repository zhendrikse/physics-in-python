##
# Original: https://github.com/Physics-Morris/Physics-Vpython/blob/master/1_Moving_Wedge.py
# See also: https://github.com/zhendrikse/physics-in-python/
#

from vpython import radians, tan, sin,cos, mag, vec, canvas, button, winput, vertex, color, quad, triangle, textures, gdots, graph, rate, box, sphere
from toolbox.wedge import Wedge
from toolbox.timer import PhysTimer

ball_mass, grav_constant, theta, friction_constant = 1.0, 9.8, 45, 0.0

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
    plot_ball_velocity_x.delete()
    plot_wedge_velocity_x.delete()
    # m_p.delete()
    # M_p.delete()
    plot_energy_total.delete()
    plot_energy_ball.delete()
    plot_energy_wedge.delete()

    wedge.with_new_parameters(theta_tmp, friction_tmp, M_tmp, m_tmp)   
    ball.v = vec(0, 0, 0)
    ball.pos = vec(1.5/sin(radians(theta_tmp)), 10, 5)
    ball.a = wedge.acceleration_ball()

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
    wedge.with_new_parameters(theta_tmp, friction_tmp, M_tmp, m_tmp)    
    ball.pos.x = 1.5/sin(radians(theta_tmp))
    ball.a = wedge.acceleration_ball()

set_scene()

running = False
wedge = Wedge()
timer = PhysTimer(0, -12)

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
            a=wedge.acceleration_ball(), 
            texture=textures.wood)

g1 = graph(title='<b>Velocity (x direction), ball=red, wedge=green</b>', 
           xtitle='<b>time</b>', ytitle='<b>P</b>', 
           align='left', width=500, height=300)

g2 = graph(title='<b>Energy, ball=blue, wedge=red, total=green<b>', xtitle='<b>time</b>', 
           ytitle='<b>E</b>', align='left', width=500, height=300)

plot_ball_velocity_x = gdots(graph=g1, color=color.red)
plot_wedge_velocity_x = gdots(graph=g1, color=color.green)
plot_energy_ball = gdots(graph=g2, color=color.blue)
plot_energy_wedge = gdots(graph=g2, color=color.red)
plot_energy_total = gdots(graph=g2, color=color.green)

def ball_on_ramp():
    return ball.pos.y >= ball.radius+floor.size.y / 2

dt = 0.01
t = 0
while True:
    rate(1/dt)
    timer.update(t)
    running = running if ball.pos.x < 50 else False

    if running:
        ball.v += ball.a * dt
        ball.pos += ball.v * dt
        wedge.update(dt)

        if not ball_on_ramp():
            ball.a = vec(0, 0, 0)
            wedge.zero_acceleration()

            ball.v = vec(mag(ball.v), 0, 0)
            ball.up = vec(0, 1, 0)
            ball.pos += ball.v * dt

            wedge.update(dt)


        if wedge_mass_input_field.number == None: tmp_M = wedge.mass
        else: tmp_M = wedge_mass_input_field.number
        if ball_mass_input_field.number == None: tmp_m = ball_mass
        else: tmp_m = ball_mass_input_field.number

        plot_ball_velocity_x.plot(pos=(t, ball.v.x))
        plot_wedge_velocity_x.plot(pos=(t, wedge.velocity))

        K = 0.5*tmp_m*(ball.v.x**2 + ball.v.y**2) + wedge.kinetic_energy
        U = tmp_m*grav_constant*(ball.pos.y - (ball.radius+floor.size.y/2))

        plot_energy_ball.plot(pos=(t, K))
        plot_energy_wedge.plot(pos=(t, U))
        plot_energy_total.plot(pos=(t, K+U))

        t += dt