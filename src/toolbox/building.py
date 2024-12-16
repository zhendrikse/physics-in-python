from vpython import box, vec, color, degrees, diff_angle

g = 98

class Building:
    def __init__(self, mass=45, pos=vec(-100, 50.5, 0), length=20, height=100, width=50, color=color.orange, up=vec(0,1,0,), v=vec(0, 0, 0), w=0):
        self._building = box(mass=mass, pos=pos, length=length, height=height, width=width, color=color, up=up, v=v, w=w)
        self._position_in_rest = pos

    def _angular_acceleration(self):
        if self._position_in_rest.x - self.position().x <= 0:
            return 0 #self._building.mass * g * r / I

        r = abs(-self._position_in_rest.x - self.length() / 2 - self._building.pos.x)
        length_squared = self._building.length * self._building.length
        height_squared = self._building.height * self._building.height
        width_squared = self._building.width * self._building.width
        I = (self._building.mass * (length_squared + height_squared) / 12 + self._building.mass * (10 * 10 + width_squared))
        
        return -self._building.mass * g * r / I
    
    def rotate(self, angle, origin, axis):
        self._building.rotate(origin=origin, axis=axis, angle=angle)

    def _hits_ground(self):
        return self._building.pos.y - self.length() / 2 <= 0.5
    
    def update(self, dt):
        self._building.w += self._angular_acceleration() * dt
        dtheta = -self._building.w * dt

        rotate_max = degrees(diff_angle(vec(0,1,0), self._building.up))
        # prevent over turn
        if dtheta > rotate_max:
            dtheta = rotate_max
        
        # when the block hit the ground
        if self._hits_ground():
            self._building.w = 0
            dtheta = 0
            # building.pos = vec(-160, 10.5, 0)
            self._building.up = vec(-1, 0, 0)

        self.rotate(origin=vec(self._position_in_rest.x - self.length() / 2, 0, 0), axis=vec(0, 0, 1), angle=dtheta)

    def mass(self):
        return self._building.mass
    
    def velocity(self):
        return self._building.v

    def height(self):
        return self._building.height
    
    def position(self):
        return self._building.pos
    
    def length(self):
        return self._building.length