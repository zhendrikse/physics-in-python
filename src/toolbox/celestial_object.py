from vpython import sphere, mag, norm, textures, color, vector, sqrt

G = 6.67e-11
EARTH_RADIUS = 6.356e6
EARTH_MASS = 5.97e24

MOON_MASS = 7.37e22
MOON_RADIUS = 1.737e6

EARTH_MOON_DISTANCE = 384.4e6
MOON_VELOCITY = sqrt(G * EARTH_MASS / EARTH_MOON_DISTANCE) * vector(0, 1, 0)
EARTH_VELOCITY = -MOON_MASS * MOON_VELOCITY / EARTH_MASS

EROS_RADIUS = 16.8e3 / 2
EROS_MASS = ME = 6.7e15


class CelestialObject:

    def __init__(self, mass, position=vector(0, 0, 0), velocity=vector(0, 0, 0), radius=10.0, color=color.yellow,
                 texture=None, shininess=0.6):
        self._body = sphere(mass=mass, pos=position, velocity=velocity, radius=radius, color=color, texture=texture,
                            shininess=shininess, make_trail=True)

    def distance_to(self, other):
        return other.position - self.position

    def force_on(self, other_object, from_distance):
        r_squared = mag(from_distance) * mag(from_distance)
        force_magnitude = G * self.mass * other_object.mass / r_squared
        force_vector = force_magnitude * norm(from_distance)
        return force_vector

    def force_between(self, other_object):
        radius = self.distance_to(other_object)
        force_magnitude = G * self.mass * other_object.mass / mag(radius)**2
        force_vector = force_magnitude * norm(radius)
        return force_vector

    def rotate(self, angle, origin=vector(0, 0, 0), axis=vector(0, 1, 0)):
        self._body.rotate(origin=origin, axis=axis, angle=angle)

    def move(self, force, dt):
        self._body.velocity += force / self.mass * dt
        self._body.pos += self.velocity * dt

    @property
    def momentum(self):
        return self.mass * self.velocity

    @property
    def position(self):
        return self._body.pos

    @property
    def mass(self):
        return self._body.mass

    @property
    def velocity(self):
        return self._body.velocity


class Earth(CelestialObject):
    def __init__(self, position=vector(0, 0, 0), velocity=EARTH_VELOCITY, shininess=0.6):
        super().__init__(mass=EARTH_MASS, position=position, velocity=velocity, radius=EARTH_RADIUS,
                         texture=textures.earth, shininess=shininess)


class Moon(CelestialObject):
    def __init__(self, position=vector(EARTH_MOON_DISTANCE, 0, 0), velocity=MOON_VELOCITY, shininess=0.6):
        super().__init__(mass=MOON_MASS, position=position, velocity=velocity, radius=MOON_RADIUS, shininess=shininess,
                         texture={ 'file': "http://i.imgur.com/YPg4RPU.jpg"})


class Eros(CelestialObject):
    def __init__(self, position=vector(0, 0, 0), velocity=EARTH_VELOCITY, shininess=0.6):
        super().__init__(mass=EROS_MASS, position=position, velocity=velocity, radius=EROS_RADIUS, shininess=shininess,
                         texture=textures.stucco)
