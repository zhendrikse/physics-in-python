##
# Original: https://github.com/Physics-Morris/Physics-Vpython/blob/master/1_Moving_Wedge.py
# See also: https://github.com/zhendrikse/physics-in-python/
#

from vpython import canvas, box, vec, cos, sin, sphere, radians, random, winput, color, button, graph, rate, gdots, degrees, diff_angle

# initial perimeter setting
theta, v0, elasticity, g = 1, 100, 1, 98

# scene setting
def set_scene():
    global scene
    scene = canvas(width=1000, height=600, background=vec(0, 0.6, 0.6), align='left', range=200)
    floor = box(pos=vec(0, 0, 0), size=vec(1000, 1, 1000), color=color.blue)
    building1 = box(pos=vec(100, 50, 0), length=10, height=100, width=10, color=color.cyan, 
                    up=vec(0,1,0))
    scene.camera.pos = vec(0, 60, 200)

class Building:
    def __init__(self, mass=45, pos=vec(-100, 50.5, 0), length=20, height=100, width=50, color=color.orange, up=vec(0,1,0,), v=vec(0, 0, 0), w=0):
        self._building = box(mass=mass, pos=pos, length=length, height=height, width=width, color=color, up=up, v=v, w=w)

    def _angular_acceleration(self):
        center = self._building.pos.x
        r = abs(-110 - self._building.pos.x)
        I = (self._building.mass * (20 * 20 + 100 *100) / 12 + self._building.mass * (10 * 10 + 50 * 50))
        if -100-center <= 10:
            return self._building.mass * g * r / I
        elif -100-center > 10:
            return -self._building.mass * g * r / I
        else:
            return 0
    
    def rotate(self, angle, origin, axis):
        self._building.rotate(origin=origin, axis=axis, angle=angle)

    def update(self, dt):
        self._building.w += self._angular_acceleration() * dt
        dtheta = -self._building.w * dt

        rotate_max = degrees(diff_angle(vec(0,1,0), self._building.up))

        # prevent over turn
        if dtheta > rotate_max:
            dtheta = rotate_max
        
        # when the block hit the ground
        if self._building.pos.y <= 10.5:
            self._building.w = 0
            # building.pos = vec(-160, 10.5, 0)
            self._building.up = vec(-1, 0, 0)
            dtheta = 0

        if self._building.pos.x > -100:
            # building.pos = vec(-100, 50.5, 0) 
            self._building.up = vec(0, 1, 0)
            self._building.w = 0
            dtheta = 0

        self.rotate(origin=vec(-110, 0, 0), axis=vec(0, 0, 1), angle=dtheta)

    def mass(self):
        return self._building.mass
    
    def velocity(self):
        return self._building.v

class Ball:
    def __init__(self, mass=10, pos=vec(100, 105, 0), radius=5, color=vec(random(), random(), random()), v=vec(-v0*cos(radians(theta)), v0*sin(radians(theta)), 0), a=vec(0, -g, 0)):
        self._ball = sphere(mass=mass, pos=pos, radius=radius, color=color, v=v, a=a)

    def hits_ground(self):
        return self._ball.pos.y <= 5.5  and self._ball.pos.x >= -85

    def hits_building(self, building):
        return self._ball.pos.x <= -85 and self._ball.pos.x <= 0 and self._ball.pos.y <= 100 and self._ball.pos.x >= -115 and building._building.up == vec(0, 1, 0)

    def bounce_on_ground(self, dt):
        self._ball.v.y *= -elasticity
        self.move(dt)

        # if the velocity is too slow, stay on the ground
        if self._ball.v.y <= 0.1:
            self._ball.pos.y = 5.5

    def _collision(self, mass_building, velocity_building):
        momentum_ball = self._ball.mass * self._ball.v.x
        momentum_building = mass_building * velocity_building
        velocity_difference = velocity_building - self._ball.v.x
        total_momentum = momentum_ball + momentum_building
        total_mass = self._ball.mass + mass_building
        speed_ball = (total_momentum + elasticity * mass_building * velocity_difference) / total_mass
        speed_building = (total_momentum - elasticity * self._ball.mass * velocity_difference) / total_mass
        return speed_ball, speed_building

    def collides_with_buildiing(self, building, dt):
        velocity_ball, velocity_building = self._collision(building._building.mass, building._building.v.x)

        # motion of ball
        self._ball.v.x = velocity_ball
        self.move(dt)

        # motion of block
        angular_velocity = velocity_building / (self._ball.pos.y - 0.5)
        building._building.w = angular_velocity
        dtheta = -building._building.w * dt
        building.rotate(origin=vec(-110, 0, 0), axis=vec(0, 0, 1), angle=dtheta)

    def move(self, dt):
        self._ball.v += self._ball.a * dt
        self._ball.pos += self._ball.v * dt

set_scene()

building2 = Building()

ball = [] # for each shot a new ball
ball_counter = 0
def create_ball():
    global ball_counter
    new_ball = Ball()
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
            ball[j]._ball.visible = False
        ball[:] = []
    building2._building.pos = vec(-100, 50.5, 0) 
    building2._building.up=vec(0, 1, 0)
    building2._building.v=vec(0, 0, 0)
    building2._building.w=0
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

g1 = graph(title='<b>Angular Velocity (for block)</b>', 
           xtitle='<b>time</b>', ytitle='<b>Angular Velocity</b>', align='right', 
           width=500, height=300)

w = gdots(graph=g1)

t, dt = 0, 0.01
while True:
    rate(1/dt)
    for j in range(len(ball)):

        if ball[j].hits_ground():
            ball[j].bounce_on_ground(dt)

        elif ball[j].hits_building(building2):
            ball[j].collides_with_buildiing(building2, dt)
        
        else:
            ball[j].move(dt)
            building2.update(dt)            

    t += dt
    w.plot(pos=(t, building2._building.w))
            
