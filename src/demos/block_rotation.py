# Morris H. 12/7

from vpython import canvas, vec, sphere, box, sin, cos, radians, random, color, winput, button, graph, gdots, rate, degrees, diff_angle
from toolbox.ball import Ball
from toolbox.building import Building
from toolbox.timer import PhysTimer

# initial perimeter setting
m, M, theta, v0, e = 1, 10, 45, 100, 0.9


# scene setting
def set_scene():
    global scene
    scene = canvas(width=1000, height=600, background=vec(0, 0.6, 0.6), align='left', range=200)
    floor = box(pos=vec(0, 0, 0), size=vec(1000, 1, 1000), color=color.blue)
    building1 = box(pos=vec(100, 50, 0), size=vec(10, 100, 10), color=color.cyan, 
                    up=vec(0,1,0))
    scene.camera.pos = vec(0, 60, 200)

set_scene()
    
building2 = Building()

# generate ball
ball = []
i = 0
def gen_ball():
    global i
    a = Ball(mass=1, position=vec(100, 105, 0), radius=5, color=vec(random(), random(), random()), 
               velocity=vec(-v0*cos(radians(theta)), v0*sin(radians(theta)), 0), elasticity=e)
    ball.append(a)
    i += 1
gen_ball()

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
    gen_ball()
    # ball[i].v = vec(-v0*cos(radians(theta)), 
    #                   v0*sin(radians(theta)), 0)

# set e
def set_e(g):
    global e, v0, theta
    e, v0, theta = test_none(ipt_e.number, ipt_v0.number, ipt_theta.number)
    return 0

# clean all ball
def clc_ball():
    global t
    # print(len(ball))
    if len(ball) != 0:
        for j in range(len(ball)):
            ball[j]._ball.visible = False
        ball[:] = []
    building2._building.pos = vec(-100, 50.5, 0) 
    building2._building.up=vec(0, 1, 0)
    building2._building.velocity=vec(0, 0, 0)
    building2._building.w=0
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

# create widgets

scene.append_to_caption('      e: ')
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


# calculate collide speed
def collide(m, M, v1, v2):
    v1f = (m*v1 + M*v2 + e*M*(v2 - v1))/(m + M)
    v2f = (m*v1 + M*v2 + e*m*(v1 - v2))/(m + M)
    return v1f, v2f

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

        # motion when hit thte ground
        if ball[j].is_on_ground() and ball[j].position.x >= -85:
            ball[j].bounce_from_ground(dt)

        # motion when hit the block
        elif ball[j].hits_building(building2._building):
            v1f, v2f = collide(ball[j].mass, building2.mass, ball[j].velocity.x, building2._building.velocity.x)

            # motion of ball
            ball[j]._ball.velocity.x = v1f
            ball[j].move(vec(0, -98, 0) * ball[j].mass, dt)

            # motion of block
            radius = ball[j].position.y - 0.5
            angular_velocity = v2f / radius
            building2.update_omega(angular_velocity, dt)
        
        # motion when in the air
        else:
            ball[j].move(vec(0, -98, 0) * ball[j].mass, dt)
            building2.update(dt)


    t += dt

    # plot
    w.plot(pos=(t, building2._building.w))



            
