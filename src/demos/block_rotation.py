##
# Original: https://github.com/Physics-Morris/Physics-Vpython/blob/master/3_Block_Rotation.py
# See also: https://github.com/zhendrikse/physics-in-python/
#

from vpython import canvas, box, vec, cos, sin, sphere, radians, random, winput, color, button, graph, rate, gdots, degrees, diff_angle
# Morris H. 12/7

from vpython import *


# initial perimeter setting
m, M, theta, v0, e, g = 1, 10, 45, 100, 1, 98


# scene setting
def set_scene():
    global scene
    scene = canvas(width=1000, height=600, background=vec(0, 0.6, 0.6), align='left', range=200)
    floor = box(pos=vec(0, 0, 0), size=vec(1000, 1, 1000), color=color.blue)
    building1 = box(pos=vec(100, 50, 0), size=vec(10, 100, 10), color=color.cyan, 
                    up=vec(0,1,0))
    scene.camera.pos = vec(0, 60, 200)

set_scene()
building2 = box(pos=vec(-100, 50.5, 0), size=vec(20, 100, 50), color=color.orange, 
    up=vec(0,1,0,), v=vec(0, 0, 0), w=0)


# generate ball
ball = []
i = 0
def gen_ball():
    global i
    a = sphere(pos=vec(100, 105, 0), radius=5, color=vec(random(), random(), random()), 
               v=vec(-v0*cos(radians(theta)), v0*sin(radians(theta)), 0), a=vec(0, -g, 0))
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
            ball[j].visible = False
        ball[:] = []
    building2.pos = vec(-100, 50.5, 0) 
    building2.up=vec(0, 1, 0)
    building2.v=vec(0, 0, 0)
    building2.w=0
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

# calculate angular acc
def angular_acc():
    center = building2.pos.x
    r = abs(-110-building2.pos.x)
    I = (M*(20**2+100**2)/12 + M*(10**2+50**2))
    if -100-center <= 10:
        return M*g*r/I
    elif -100-center > 10:
        return -M*g*r/I
    else:
        return 0

def angular_v(vx, r):
    return vx/r


# plot
g1 = graph(title='<b>Angular Velocity (for block)</b>', 
           xtitle='<b>time</b>', ytitle='<b>Angular Velocity</b>', align='right', 
           width=500, height=300)

w = gdots(graph=g1)

t, dt = 0, 0.01
while True:
    rate(1/dt)
    for j in range(len(ball)):

        # motion when hit thte ground
        if ball[j].pos.y <= 5.5  and ball[j].pos.x >= -85:
            ball[j].v.y *= -e
            ball[j].v += ball[j].a*dt
            ball[j].pos += ball[j].v*dt

            # if the velocity is too slow, stay on the ground
            if ball[j].v.y <= 0.1:
                ball[j].pos.y = 5.5

        # motion when hit the block
        elif ball[j].pos.x <= -85 and ball[j].v.x <= 0 and ball[j].pos.y <= 100 and ball[j].pos.x >= -115 and building2.up == vec(0, 1, 0):
            
            v1f, v2f = collide(m, M, ball[j].v.x, building2.v.x)

            # motion of ball
            ball[j].v.x = v1f
            ball[j].v += ball[j].a*dt
            ball[j].pos += ball[j].v*dt

            # motion of block
            building2.w = angular_v(v2f, ball[j].pos.y-0.5)
            dtheta = -building2.w*dt
            building2.rotate(origin=vec(-110, 0, 0), axis=vec(0, 0, 1), 
                             angle=dtheta)
            

        
        # motion when in the air
        else:
            ball[j].v += ball[j].a*dt
            ball[j].pos += ball[j].v*dt

            
            building2.w += angular_acc()*dt
            dtheta = -building2.w*dt

            rotate_max = degrees(diff_angle(vec(0,1,0), building2.up))

            # prevent over turn
            if dtheta > rotate_max:
                dtheta = rotate_max
            
            # when the block hit the ground
            if building2.pos.y <= 10.5:
                building2.w = 0
                # building2.pos = vec(-160, 10.5, 0)
                building2.up = vec(-1, 0, 0)
                dtheta = 0

            if building2.pos.x > -100:
                # building2.pos = vec(-100, 50.5, 0) 
                building2.up = vec(0, 1, 0)
                building2.w = 0
                dtheta = 0

            building2.rotate(origin=vec(-110, 0, 0), axis=vec(0, 0, 1), 
                             angle=dtheta)

    t += dt

    # plot
    w.plot(pos=(t, building2.w))



            
