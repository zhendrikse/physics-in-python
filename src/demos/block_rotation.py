# Morris H. 12/7

from vpython import canvas, vec, sphere, box, sin, cos, radians, random, color, winput, button, graph, gdots, rate, degrees, diff_angle
from toolbox.ball import Ball
from toolbox.building import Building
from toolbox.timer import PhysTimer

# initial perimeter setting
theta, v0, e = 45, 100, 0.9

# scene setting
def set_scene():
    global scene
    scene = canvas(width=1000, height=600, background=vec(0, 0.6, 0.6), align='left', range=200)
    floor = box(pos=vec(0, 0, 0), size=vec(1000, 1, 1000), color=color.blue)
    shooting_tower = box(pos=vec(100, 50, 0), size=vec(10, 100, 10), color=color.cyan, up=vec(0,1,0))
    scene.camera.pos = vec(0, 60, 200)

set_scene()

ball = [] # enable mutlple shots
ball_counter = 0
def gen_ball(velocity):
    global ball_counter
    a = Ball(mass=1, position=vec(100, 105, 0), radius=5, color=vec(random(), random(), random()), velocity=velocity, elasticity=e)
    ball.append(a)
    ball_counter += 1

# set theta
def set_theta(t):
    global e, v0, theta
    e, v0, theta = test_none(ipt_e.number, ipt_v0.number, ipt_theta.number)
    return 0
    
# set v0
def set_v0(v):
    global e, v0, theta
    e, v0, theta = test_none(ipt_e.number, ipt_v0.number, ipt_theta.number)
    return 0

# shoot
def shoot():
    gen_ball(v0 * vec(-cos(radians(theta)), sin(radians(theta)), 0))

# set e
def set_e(g):
    global e, v0, theta
    e, v0, theta = test_none(ipt_e.number, ipt_v0.number, ipt_theta.number)
    return 0


building = Building()
gen_ball(v0 * vec(-cos(radians(theta)), sin(radians(theta)), 0))

# clean all ball
def clc_ball():
    global t
    # print(len(ball))
    if len(ball) != 0:
        for j in range(len(ball)):
            ball[j]._ball.visible = False
        ball[:] = []
    building._building.pos = vec(-100, 50.5, 0) 
    building._building.up=vec(0, 1, 0)
    building._building.velocity=vec(0, 0, 0)
    building._building.w=0
    w.delete()
    t = 0

def test_none(e_tmp, v0_tmp, theta_tmp):
    if e_tmp == None: e_ans = e 
    elif (e_tmp > 1 or e_tmp < 0): e_ans = e
    else: e_ans = e_tmp

    if v0_tmp == None: v0_ans = v0
    else: v0_ans = v0_tmp

    if theta_tmp == None: theta_ans = theta
    else: theta_ans = theta_tmp

    return e_ans, v0_ans, theta_ans

scene.append_to_caption('0 < e <= 1: ')
ipt_e = winput(bind=set_e, type='numeric')
scene.append_to_caption(' \n\n\n')

scene.append_to_caption('      Angle: ')
ipt_theta = winput(bind=set_theta, type='numeric')
scene.append_to_caption(' (Degree)\n\n\n')

scene.append_to_caption('      V0:')
ipt_v0 = winput(bind=set_v0, type='numeric')
scene.append_to_caption('                                    ')

b1 = button(text="Shoot", bind=shoot, 
            background=color.purple)

b2 = button(text="Restart", bind=clc_ball, 
            background=color.purple)

scene.append_to_caption('\n\n')

scene.append_to_caption('<i>\n\n(Please press enter after setting each parameter, otherwise \n it will run on default parameter)</i>')

# determine the boundary of block
# def boundary():
    # b1 = -85 - y*sin(theta)

g1 = graph(title='<b>Angular Velocity (for block)</b>', 
           xtitle='<b>time</b>', ytitle='<b>Angular Velocity</b>', align='right', 
           width=500, height=300)

w = gdots(graph=g1)

t, dt = 0, 0.01
timer = PhysTimer(0, -25)
while True:
    rate(1/dt)
    timer.update(t)
    for j in range(len(ball)):

        if ball[j].is_on_ground() and ball[j].position.x >= -85:
            ball[j].bounce_from_ground(dt)

        elif ball[j].hits_building(building._building):
            building.collide_with(ball[j], dt)
            ball[j].collide_with(building)
            ball[j].move(vec(0, -98, 0) * ball[j].mass, dt)

        else:
            # motion when in the air
            ball[j].move(vec(0, -98, 0) * ball[j].mass, dt)
            building.update(dt)

    t += dt
    w.plot(pos=(t, building._building.w))



            
