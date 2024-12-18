from vpython import vec, vertex, radians, tan, color, quad, triangle, cos, sin, atan
 
grav_constant = 9.8

class Wedge:
    
    def __init__(self, mass=3.0, theta=45, friction_constant=0.0):
        self._mass = mass
        self._theta = radians(theta)
        self._friction = friction_constant
        self._acceleration = vec(0, 0, 0)

        A = vertex(pos=vec(0, 0, 0), color=color.orange, v=vec(0, 0, 0))
        B = vertex(pos=vec(10/tan(radians(theta)), 0, 0), color=color.purple, v=vec(0, 0, 0))
        C = vertex(pos=vec(10/tan(radians(theta)), 0, 10), color=color.green, v=vec(0, 0, 0))
        D = vertex(pos=vec(0, 0, 10), color=color.blue, v=vec(0, 0, 0))
        E = vertex(pos=vec(0, 10, 10), color=color.cyan, v=vec(0, 0, 0))
        F = vertex(pos=vec(0, 10, 0), color=color.red, v=vec(0, 0, 0))

        self._apex = [A, B, C, D, E, F]

        T1 = triangle(v0=E, v1=D, v2=C)
        T2 = triangle(v0=F, v1=A, v2=B)
        Q1 = quad(v0=F, v1=E, v2=D, v3=A)
        Q2 = quad(v0=F, v1=E, v2=C, v3=B)
        Q3 = quad(v0=A, v1=B, v2=C, v3=D)

    def place_ball(self, ball):
        self._acceleration = vec(self._acceleration_x(ball.mass), 0, 0)

    def update(self, dt):
        for i in range(0, len(self._apex)):
            self._apex[i].v += self._acceleration * dt
            self._apex[i].pos += self._apex[i].v * dt

    def zero_acceleration(self):
        self._acceleration = vec(0, 0, 0)

    def force_on(self, ball): 
        acceleration_ball_x = self._acceleration_ball(ball.mass) * cos(self._theta) + self._acceleration_x(ball.mass)
        acceleration_ball_y = -self._acceleration_ball(ball.mass) * sin(self._theta)

        return ball.mass * vec(acceleration_ball_x, acceleration_ball_y, 0)

    def _acceleration_ball(self, ball_mass):
        theta = self._theta
        total_mass = ball_mass + self._mass
        net_mass = self._mass * (cos(theta)*cos(theta) + self._friction*sin(theta)*cos(theta))/(total_mass)/(sin(theta) - self._friction*cos(theta)) + sin(theta)
        return  grav_constant / net_mass

    def _acceleration_x(self, ball_mass):
        total_mass = ball_mass + self._mass

        if self._friction >= tan(self._theta):
            return 0.0
        
        force_on_wedge = -self._acceleration_ball(ball_mass) * ball_mass * cos(self._theta)
        return force_on_wedge / total_mass 
        
    def with_new_parameters(self, theta, friction, mass_wedge, mass_ball):
        self._friction = friction
        ball_mass = mass_ball
        self._mass = mass_wedge
        self._theta = radians(theta)
        self._apex[0].pos, self._apex[1].pos, self._apex[2].pos, self._apex[3].pos, self._apex[4].pos, self._apex[5].pos = vec(0, 0, 0), vec(10/tan(radians(theta)), 0, 0), vec(10/tan(radians(theta)), 0, 10), vec(0, 0, 10), vec(0, 10, 10), vec(0, 10, 0)

        self._acceleration = vec(0, 0, 0)
        for i in range(0, len(self._apex)):
            self._apex[i].v = vec(0, 0, 0)

    @property
    def velocity(self):
        return self._apex[0].v.x # all points of wedge move at equal velocity

    @property
    def kinetic_energy(self):
        return 0.5 * self._mass * self.velocity * self.velocity    
    
    @property
    def mass(self):
        return self._mass