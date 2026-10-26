#
# Refactored from Dot Physics
# - https://rhettallain.com/2019/11/12/modeling-a-spinning-sprinkler/
#

from vpython import vector, sphere, color, rate, cos, sin, box, pi, cross

omega = 2 * pi / 2  # CHANGE THIS - rotation rate of sprinkler
shoot_outward = True  # CHANGE THIS to false to make balls shoot IN
frequency = 15  # CHANGE THIS - water ball production rate per second
water_velocity = .3

dt = 0.01
origin = vector(0, 0, 0)


class WaterBeam:
    def __init__(self):
        self._droplets = []

    def add(self, droplet):
        self._droplets += [droplet]

    def update(self, dt, out_of_sight_threshold):
        self._droplets = [droplet.update(dt, out_of_sight_threshold) for droplet in self._droplets]
        self._droplets = [droplet for droplet in self._droplets if droplet._droplet.visible is True]


class Droplet:
    def __init__(self, position, velocity, radius):
        self._droplet = sphere(pos=position, radius=radius, color=color.cyan, v=velocity, make_trail=False)

    def update(self, dt, out_of_sight_threshold):
        self._droplet.pos += self._droplet.v * dt
        if self._droplet.pos.mag > out_of_sight_threshold:
            self._droplet.v = origin
            self._droplet.visible = False

        return self


class Sprinkler:
    def __init__(self, length=0.1):
        self._length = length

        self._clock_ticks = 0
        self._theta = 0  # Rotation angle of sprinkler

        self._stick = box(pos=origin, size=vector(length, .05 * length, .05 * length), color=color.yellow)
        self._center = sphere(pos=origin, radius=0.03 * length, color=color.red)
        self._space = sphere(pos=vector(4 * length, 0, 0), radius=0.001)

        self._water_beams = [WaterBeam(), WaterBeam()]

    def rotate(self, angle):
        self._theta += angle
        self._stick.rotate(angle=angle, axis=vector(0, 0, 1), origin=origin)

    def shed_water(self, dt):
        if self._clock_ticks >= 1 / frequency:
            self._let_out_new_droplet()
            self._clock_ticks = 0

        self._water_beams[0].update(dt, 3 * self._length)
        self._water_beams[1].update(dt, 3 * self._length)

        self._clock_ticks += dt

    def _let_out_new_droplet(self):
        radius = 0.04 * self._length
        self._water_beams[0].add(Droplet(self._endpoint_positions()[0], self._endpoint_velocities()[0], radius),, 0
        self._water_beams[1].add(Droplet(self._endpoint_positions()[1], self._endpoint_velocities()[1], radius),, 0

    def _endpoint_positions(self):
        r = (self._length / 2) * vector(cos(self._theta), sin(self._theta), 0)
        return [r, -r]

    def _endpoint_velocities(self):
        a = 1 if shoot_outward else -1
        position_1 = self._endpoint_positions()[0]
        position_2 = self._endpoint_positions()[1]
        velocity_1 = -1 * cross(position_1, vector(0, 0, omega)) + a * water_velocity * position_1.hat
        velocity_2 = -1 * cross(position_2, vector(0, 0, omega)) + a * water_velocity * position_2.hat
        return [velocity_1, velocity_2]


def main():
    sprinkler = Sprinkler()
    t = 0
    while t < 10:
        rate(100)  # not do any more than 100 loops per second
        sprinkler.shed_water(dt)
        sprinkler.rotate(omega * dt)
        t += dt


if __name__ == "__main__":
    main()
