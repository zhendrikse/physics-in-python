from vpython import canvas, cylinder, color, vector, compound, pi, cos, sin, rate, arrow, simple_sphere, mag, cross

title="""&#x2022; <a href="https://trinket.io/glowscript/88ff44297f">Original code</a> by <a href="https://www.youtube.com/@LetsCodePhysics">Let&apos;s code physics</a>
&#x2022; Refactored by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> to <a href="https://github.com/zhendrikse/science/blob/main/kinematics/code/moment_of_inertia.py">moment_of_inertia.py</a>

"""

display = canvas(width=600, height=600, background=color.gray(0.075), title=title, range=2, forward=vector(-.44, -.27, -.85))

class Cylinder:
    def __init__(self, R=1, M=1, z_min=0, z_max=1):
        self._radius, self._mass = R, M
        self._z_min, self._z_max = z_min, z_max
        self._shape = None
        self._omega = 0 * vector(0, 0, 0)
        self._moment_of_inertia = 0

        z = z_min
        atoms = []
        dz = 0.1
        while z <= z_max:
            self._create_ring(atoms, z, R)
            z += dz

        rotation_axis = cylinder(pos=vector(0, 0, -1), axis=vector(0, 0, 1), size=vector(2, 0.05, 0.05))
        self._calculate_moment_of_inertia(atoms)

        # Set a marker to help visualization.
        atoms[-1].color = color.cyan
        self._shape = compound(atoms)

    def _create_ring(self, atoms, ring_center, ring_radius):
        ds = 0.1  # This is a fixed distance between atoms.
        theta = 0
        while theta < 2. * pi:
            pos = vector(ring_radius * cos(theta), ring_radius * sin(theta), ring_center)
            atoms.append(simple_sphere(pos=pos, color=color.red, radius=0.05))
            theta += ds / ring_radius

    def _calculate_moment_of_inertia(self, atoms):
        dm = self._mass / len(atoms)
        for atom in atoms:
            # Add the moment of inertia for this one atom.
            self._moment_of_inertia += dm * (atom.pos.x ** 2 + atom.pos.y ** 2)

        # You can use this printed value to compare against
        # standard formulae from your textbook or the internet.
        # print("moment of inertia=", self._moment_of_inertia, ", or", moi / (M * R ** 2), "MR^2")

    def z_average(self):
        return (self._z_min + self._z_max) / 2

    def radius(self):
        return self._radius

    def update(self, torque, dt):
        # Use update procedure.
        self._omega += torque / self._moment_of_inertia * dt
        self._shape.rotate(angle=mag(self._omega) * dt, axis=self._omega.hat)


class ForceVector:
    def __init__(self, scale_factor = 1):
        self._force_vector = arrow(color=color.cyan)
        self._scale_factor = scale_factor

    def force_at(self, location, z_average, t):
        force = vector(0, cos(t), 0)
        self._force_vector.pos = location + z_average
        self._force_vector.axis = self._scale_factor * force
        return force


cylinder_shape = Cylinder()
force_vector = ForceVector()

dt = 0.05
t = 0
while True:
    rate(10)

    force_location = vector(cylinder_shape.radius(), 0, 0)
    force = force_vector.force_at(force_location, vector(0, 0, cylinder_shape.z_average()), t)
    torque = cross(force_location, force)
    cylinder_shape.update(torque, dt)

    t += dt
