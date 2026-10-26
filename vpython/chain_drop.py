#Web VPython 3.2

title = """ 
&#x2022; Based on original by <a href="https://trinket.io/glowscript/bbe791bbfe7d">Rhett Allain</a>
&#x2022; Belongs to <a href="https://www.youtube.com/watch?v=vXp1hW_t-bo">this video</a> 
&#x2022; Refactored by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> to <a href="https://github.com/zhendrikse/science/blob/main/kinematics/code/chain_drop.py">chain_drop.py</a>

"""

from vpython import canvas, color, vector, sphere, vec, rate, mag, text

animation = canvas(title=title, color=color.gray(0.075), center=vec(.031, -0.58, -0.19), forward=vec(-0.32, -0.7, -0.64), range=1)

gravitational_force_vector = vector(0, -9.8, 0)

class Chain:
    def __init__(self, amount_hanging_over_edge = 0.2):
        self._balls = []
        total_spring_constant = 300 
        self._total_amount_balls = 20
        self._individual_spring_constant = total_spring_constant / self._total_amount_balls  
        self._mass = 0.1
        self._length = 1
        self._inter_ball_chain_length = self._length / (self._total_amount_balls - 1)

        rt = vector(0, 0, 0)
        while rt.x > -(self._length - amount_hanging_over_edge):
            rt += vector(-self._inter_ball_chain_length, 0, 0)
        
        rt += vector(self._inter_ball_chain_length, 0, 0)
        while rt.x <= 0:
            self._balls += [sphere(pos=rt, radius=self.ball_radius(), m=self._mass / self._total_amount_balls, p = vector(0, 0, 0), on=True)]
            rt += vector(self._inter_ball_chain_length, 0, 0)

        self._balls[-1].on = False # on = True indicates ball is on table
        
        rt += vector(-self._inter_ball_chain_length, 0, 0)
        while rt.y > -amount_hanging_over_edge:
            rt += vector(0, -self._inter_ball_chain_length, 0)
            self._balls = self._balls + [sphere(pos=rt, radius=self.ball_radius(), m=self._mass / self._total_amount_balls, p = vector(0, 0, 0), on=False)]

    def total_balls(self):
        return self._total_amount_balls

    def ball_radius(self):
        return self._length / 50

    def length(self):
        return self._length
    
    def update(self, dt):
        self._update_forces()
        for ball in self._balls:
            ball.p = ball.p + ball.F * dt
            ball.pos = ball.pos + ball.p * dt / ball.m

    def _update_forces(self):
        position_right_ball = self._balls[1].pos - self._balls[0].pos
        position_left_ball = self._balls[-2].pos - self._balls[-1].pos

        self._balls[0].F = self._individual_spring_constant*(mag(position_right_ball)
                                                       -self._inter_ball_chain_length)*norm(position_right_ball)+self._balls[0].m*gravitational_force_vector
        self._balls[-1].F = self._individual_spring_constant*(mag(position_left_ball)
                                                        -self._inter_ball_chain_length)*norm(position_left_ball)+self._balls[-1].m*gravitational_force_vector

        for i in range(1, self._total_amount_balls - 1):
            position_left_ball = self._balls[i - 1].pos - self._balls[i].pos
            position_right_ball = self._balls[i + 1].pos - self._balls[i].pos
            
            force_to_left = self._individual_spring_constant * (mag(position_left_ball) - self._inter_ball_chain_length) * norm(position_left_ball)
            force_to_right = self._individual_spring_constant * (mag(position_right_ball) - self._inter_ball_chain_length) * norm(position_right_ball)
            gravitational_force = self._balls[i].m * gravitational_force_vector

            self._balls[i].F = force_to_left + force_to_right + gravitational_force

        
        #test for pivot
        for ball in self._balls:
            position_vector = vector(0, 0, 0)
            if 0 > ball.pos.y > -self._inter_ball_chain_length/2 > ball.pos.x:
                position_vector = vector(0, -ball.pos.y, 0)
            if 0 > ball.pos.x > -self._inter_ball_chain_length/2 > ball.pos.y:
                position_vector = vector(-ball.pos.x, 0, 0)
            if 0 > ball.pos.x > -self._inter_ball_chain_length/2 and 0 > ball.pos.y > -self._inter_ball_chain_length / 2:
                position_vector = vector(-ball.pos.x, -ball.pos.y, 0)
            ball.F += (self.total_balls() / 2) * self._individual_spring_constant * position_vector

amount_hanging_over_edge = 0.2
chain  = Chain(amount_hanging_over_edge)

table_length = 1
table_height = 0.1
table  = box(pos=vector(-table_length/2-.01, -table_height/2-.01,0), size=vector(table_length, table_height, 3 * table_height), opacity=0.3)

corner = sphere(pos=vector(0,chain.length() / 10,0), radius=chain.ball_radius() / 2, color=color.yellow)
le     = sphere(pos=vector(-(chain.length() - amount_hanging_over_edge), chain.length() / 10,0),radius=chain.ball_radius() / 2, color=color.magenta)
be     = sphere(pos=vector(chain.length() / 10,-amount_hanging_over_edge, 0),radius=chain.ball_radius() / 2, color=color.cyan)

t = 0
dt = 0.0001
#balls[-1].p = balls[-1].m*vector(0.1,0,0)
#pivot = vector(-inter_ball_chain_length/2,-inter_ball_chain_length/2,0)
popup = text(text="Click mouse to start", pos=vec(-1.5, -2, 0), billboard=True, color=color.yellow, height=.25)
animation.waitfor('click')
popup.visible = False
while t < 1:
    rate(1000)
    chain.update(dt)
    t += dt
