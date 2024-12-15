from vpython import vec, vertex, radians, tan, color, quad, triangle, cos, sin, atan
 
grav_constant = 9.8

class Wedge:
    
    def __init__(self, mass=3.0, ball_mass=1.0, theta=45, friction_constant=0.0):
        self._mass = mass
        self._theta = radians(theta)
        self._ball_mass = ball_mass
        self._friction = friction_constant

        A = vertex(pos=vec(0, 0, 0), color=color.orange, v=vec(0, 0, 0), a=vec(self._acceleration_x(), 0, 0))
        B = vertex(pos=vec(10/tan(radians(theta)), 0, 0), color=color.purple, v=vec(0, 0, 0), a=vec(self._acceleration_x(), 0, 0))
        C = vertex(pos=vec(10/tan(radians(theta)), 0, 10), color=color.green, v=vec(0, 0, 0), a=vec(self._acceleration_x(), 0, 0))
        D = vertex(pos=vec(0, 0, 10), color=color.blue, v=vec(0, 0, 0), a=vec(self._acceleration_x(), 0, 0))
        E = vertex(pos=vec(0, 10, 10), color=color.cyan, v=vec(0, 0, 0), a=vec(self._acceleration_x(), 0, 0))
        F = vertex(pos=vec(0, 10, 0), color=color.red, v=vec(0, 0, 0), a=vec(self._acceleration_x(), 0, 0))

        self._apex = [A, B, C, D, E, F]

        T1 = triangle(v0=E, v1=D, v2=C)
        T2 = triangle(v0=F, v1=A, v2=B)
        Q1 = quad(v0=F, v1=E, v2=D, v3=A)
        Q2 = quad(v0=F, v1=E, v2=C, v3=B)
        Q3 = quad(v0=A, v1=B, v2=C, v3=D)

    def update(self, dt):
        for i in range(0, len(self._apex)):
            self._apex[i].v += self._apex[i].a * dt
            self._apex[i].pos += self._apex[i].v * dt

    def zero_acceleration(self):
        for i in range(0, len(self._apex)):
            self._apex[i].a = vec(0, 0, 0)

    def acceleration_ball(self): 
        acceleration_ball_x = self._acceleration_ball() * cos(self._theta) + self._acceleration_x()
        acceleration_ball_y = -self._acceleration_ball() * sin(self._theta)

        return vec(acceleration_ball_x, acceleration_ball_y, 0)

    def _acceleration_ball(self):
        theta = self._theta
        total_mass = self._ball_mass + self._mass
        net_mass = self._mass * (cos(theta)*cos(theta) + self._friction*sin(theta)*cos(theta))/(total_mass)/(sin(theta) - self._friction*cos(theta))+ sin(theta)
        return  grav_constant / net_mass

    def _acceleration_x(self):
        total_mass = self._ball_mass + self._mass

        if self._friction >= tan(self._theta):
            return 0.0
        
        force_on_wedge = -self._acceleration_ball() * self._ball_mass * cos(self._theta)
        return force_on_wedge / total_mass 
        
    def with_new_parameters(self, theta, friction, mass_wedge, mass_ball):
        self._friction = friction
        self._ball_mass = mass_ball
        self._mass = mass_wedge
        self._theta = radians(theta)
        self._apex[0].pos, self._apex[1].pos, self._apex[2].pos, self._apex[3].pos, self._apex[4].pos, self._apex[5].pos = vec(0, 0, 0), vec(10/tan(radians(theta)), 0, 0), vec(10/tan(radians(theta)), 0, 10), vec(0, 0, 10), vec(0, 10, 10), vec(0, 10, 0)

        for i in range(0, len(self._apex)):
            self._apex[i].a.x = self._acceleration_x()
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