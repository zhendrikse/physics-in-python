##
# Original: https://github.com/Physics-Morris/Physics-Vpython/blob/master/1_Moving_Wedge.py
# See also: https://github.com/zhendrikse/physics-in-python/
#

from vpython import canvas, box, vec, cos, sin, sphere, radians, random, winput, color, button, graph, rate, gdots, degrees, diff_angle

# initial perimeter setting
m, M, theta, v0, elasticity, g = 1, 10, 45, 100, 1, 98

# scene setting
def set_scene():
    global scene
    scene = canvas(width=1000, height=600, background=vec(0, 0.6, 0.6), align='left', range=200)
    floor = box(pos=vec(0, 0, 0), size=vec(1000, 1, 1000), color=color.blue)
    building1 = box(pos=vec(100, 50, 0), length=10, height=100, width=10, color=color.cyan, 
                    up=vec(0,1,0))
    scene.camera.pos = vec(0, 60, 200)

set_scene()
building2 = box(pos=vec(-100, 50.5, 0), length=20, height=100, width=50, color=color.orange, 
    up=vec(0,1,0,), v=vec(0, 0, 0), w=0)


ball = [] # for each shot a new ball
ball_counter = 0
def create_ball():
    global ball_counter
    new_ball = sphere(pos=vec(100, 105, 0), radius=5, color=vec(random(), random(), random()), 
               v=vec(-v0*cos(radians(theta)), v0*sin(radians(theta)), 0), a=vec(0, -g, 0))
    ball.append(new_ball)
    ball_counter += 1
create_ball()

def set_theta(t):
    global elasticity, v0, theta
    elasticity, v0, theta = get_input_parameters(elasticity_input_field.number, velocity_input_field.number, theta_input_field.number)
    return 0
    
def set_start_velocity(v):
    global elasticity, v0, theta
    elasticity, v0, theta = get_input_parameters(elasticity_input_field.number, velocity_input_field.number, theta_input_field.number)
    return 0

def shoot():
    create_ball()
    # ball[i].v = vec(-v0*cos(radians(theta)), 
    #                   v0*sin(radians(theta)), 0)

def set_ball_elasticity(g):
    global elasticity, v0, theta
    elasticity, v0, theta = get_input_parameters(elasticity_input_field.number, velocity_input_field.number, theta_input_field.number)
    return 0

def clear_all_balls():
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

def get_input_parameters(e_tmp, v0_tmp, theta_tmp):
    if e_tmp == None: e_ans = elasticity 
    elif (e_tmp > 1 or e_tmp < 0): e_ans = elasticity
    else: e_ans = e_tmp

    if v0_tmp == None: v0_ans = v0
    else: v0_ans = v0_tmp

    if theta_tmp == None: theta_ans = theta
    else: theta_ans = theta_tmp

    return e_ans, v0_ans, theta_ans

# create widgets
scene.append_to_caption('      0 < elasticity < 1: ')
elasticity_input_field = winput(bind=set_ball_elasticity, type='numeric')
scene.append_to_caption(' \n\n\n')

scene.append_to_caption('      Angle: ')
theta_input_field = winput(bind=set_theta, type='numeric')
scene.append_to_caption(' (Degree)\n\n\n')

scene.append_to_caption('      Velocity:')
velocity_input_field = winput(bind=set_start_velocity, type='numeric')
scene.append_to_caption('                                    ')

b1 = button(text="Shoot", bind=shoot, 
            background=color.purple)

b2 = button(text="Restart", bind=clear_all_balls, 
            background=color.purple)

scene.append_to_caption('\n\n')

scene.append_to_caption('<i>\n\n(Please press enter after setting each parameter, otherwise \n it will run on default parameter)</i>')


def collide(mass_ball, mass_building, velocity_ball, velocity_building):
    momentum_ball = mass_ball * velocity_ball
    momentum_building = mass_building * velocity_building
    velocity_difference = velocity_building - velocity_ball
    total_momentum = momentum_ball + momentum_building
    total_mass = mass_ball + mass_building
    speed_ball = (total_momentum + elasticity * mass_building * velocity_difference) / total_mass
    speed_building = (total_momentum - elasticity * mass_ball * velocity_difference) / total_mass
    return speed_ball, speed_building

def angular_acceleration():
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

def ball_hits_ground(ball_position):
    return ball_position.y <= 5.5  and ball_position.x >= -85

def ball_hits_building(ball_position, building):
    return ball_position.x <= -85 and ball_position.x <= 0 and ball_position.y <= 100 and ball_position.x >= -115 and building.up == vec(0, 1, 0)

def bounce_on_ground(ball, dt):
    ball.v.y *= -elasticity
    move_ball(ball, dt)

    # if the velocity is too slow, stay on the ground
    if ball.v.y <= 0.1:
        ball.pos.y = 5.5

def collide_with_buildiing(ball, building, dt):
    velocity_ball, velocity_building = collide(m, M, ball.v.x, building.v.x)

    # motion of ball
    ball.v.x = velocity_ball
    move_ball(ball, dt)

    # motion of block
    building.w = angular_v(velocity_building, ball.pos.y-0.5)
    dtheta = -building.w * dt
    building.rotate(origin=vec(-110, 0, 0), axis=vec(0, 0, 1), angle=dtheta)

def move_ball(ball, dt):
    ball.v += ball.a * dt
    ball.pos += ball.v * dt

def update_building(building, dt):
    building.w += angular_acceleration()*dt
    dtheta = -building.w * dt

    rotate_max = degrees(diff_angle(vec(0,1,0), building.up))

    # prevent over turn
    if dtheta > rotate_max:
        dtheta = rotate_max
    
    # when the block hit the ground
    if building.pos.y <= 10.5:
        building.w = 0
        # building2.pos = vec(-160, 10.5, 0)
        building.up = vec(-1, 0, 0)
        dtheta = 0

    if building.pos.x > -100:
        # building2.pos = vec(-100, 50.5, 0) 
        building.up = vec(0, 1, 0)
        building.w = 0
        dtheta = 0

    building.rotate(origin=vec(-110, 0, 0), axis=vec(0, 0, 1), angle=dtheta)

t, dt = 0, 0.01
while True:
    rate(1/dt)
    for j in range(len(ball)):

        if ball_hits_ground(ball[j].pos):
            bounce_on_ground(ball[j], dt)

        elif ball_hits_building(ball[j].pos, building2):
            collide_with_buildiing(ball[j], building2, dt)
        else:
            move_ball(ball[j], dt)
            update_building(building2, dt)            

    t += dt
    w.plot(pos=(t, building2.w))
            
