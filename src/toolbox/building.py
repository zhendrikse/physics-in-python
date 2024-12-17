from vpython import box, vec, color, degrees, diff_angle

g = 98

class Building:
    def __init__(self, mass=10, position=vec(-100, 50.5, 0), length=20, height=100, width=50, color=color.orange, up=vec(0, 1, 0), velocity=vec(0, 0, 0), w=0):
        self._building = box(mass=mass, pos=position, length=length, height=height, width=width, color=color, up=up, velocity=velocity, w=w)
        self._position_in_rest = position
 
    def _angular_acceleration(self):
        center = self._building.pos.x
        r = abs(-110 - self._building.pos.x)
        # I_block = m / 12 * (H * H + L * L), see https://kids.kiddle.co/Moment_of_inertia
        I = self.mass / 12 * (self.H * self.H + self.L * self.L)
        if -self.H - center > 10:
            return -g * r / I # backward_rotation
        elif -self.H - center <= 10:
            return g * r / I # forward rotation
        else:
            return 0
        
    def collide_with(self, ball):
        # sets angular velocity omega after collision with ball
        velocity = (ball.mass * ball.velocity.x + self.mass * self.velocity.x + ball.elasticity * ball.mass * (ball.velocity.x - self.velocity.x))/(ball.mass + self.mass)
        radius = ball.position.y - 0.5
        omega = velocity / radius
        self._building.w = omega
    
    def update(self, dt):
        self._building.w += self._angular_acceleration() * dt
        dtheta = -self._building.w * dt

        rotate_max = degrees(diff_angle(vec(0, 1, 0), self._building.up))

        # prevent over turn
        if dtheta > rotate_max:
            dtheta = rotate_max
        
        # when the block hit the ground
        if self._building.pos.y <= self.L / 2 +.5:
            self._building.w = 0
            # self._building.pos = vec(-160, 10.5, 0)
            self._building.up = vec(-1, 0, 0)
            dtheta = 0

        # disable forward rotation
        if self._building.pos.x > self._position_in_rest.x:
            # self._building.pos = vec(-100, 50.5, 0) 
            self._building.up = vec(0, 1, 0)
            self._building.w = 0
            dtheta = 0

        self.rotate(dtheta) 

    def rotate(self, dtheta):    
        self._building.rotate(origin=vec(-self.L / 2 - self.H, 0, 0), axis=vec(0, 0, 1), angle=dtheta)
       
    @property
    def mass(self):
        return self._building.mass
    
    @property
    def velocity(self):
        return self._building.velocity

    @property
    def H(self):
        return self._building.height
    
    @property
    def position(self):
        return self._building.pos
    
    @property
    def L(self):
        return self._building.length
    
    @property
    def omega(self):
        return self._building.w

    @property 
    def W(self):
        return self._building.width