#Web VPython 3.2
from random import uniform
from vpython import box, sphere, simple_sphere, color, vec, vector, pi, mag, mag2, norm, rate, sqrt, proj, curve, canvas

title = "&#x2022; The original <a href=\"https://github.com/dzirbel/brownian-motion/blob/master/main.py\">main.py</a> "
title += "was written by Jackson Bahr and Dominic Zirbel for \n   <a href=\"https://matterandinteractions.org/\">Matter and Interactions</a> "
title += "I at Carnegie Mellon University, Fall 2013.\n"
title += "&#x2022; Repaired and refactored by <a href=\"https://github.com/zhendrikse/\">Zeger Hendrikse</a> "
title += "in <a href=\"https://github.com/zhendrikse/science/blob/main/thermodynamics/code/brownian_motion.py\">brownian_motion.py</a>\n\n"

display = canvas(title=title, width=600, height=600, background=color.gray(0.075), forward=vec(-.1, -.6, -.8), center=vec(0, -5, 0))

BOX_SIZE = 5e2  # distance from the origin to the edges of the box, in meters
PARTICLES = 200  # the number of particles in the simulation
dt = .25  # the timestep between ticks in seconds - smaller for more accuracy, larger to run more quickly
SLEEP = .001  # amount of time to spend idle each tick (if running in demo mode), in seconds
NUM_SIMS = 250  # the number of times to run the simulation (starting over each time)
SIM_TIME = 100  # how long each simulation should run, in seconds of simulation-time
DEMO = True  # toggle running the demo (show the window, run only one simulation)
P2P = True  # toggle whether particles collide with other particles (as opposed to colliding only with the mass)
# if this is true, particles are allowed to spawn while intersecting with other particles

d2 = False  # set to true to simulate in 2 dimensions (all z-fields are 0)
d1 = False  # set to true to simulate in 1 dimension (all y- and z-fields are 0)

display.visible = False
#display.fullscreen = True
display.visible = DEMO

if DEMO:
    box_bottom = box(pos=vec(0, -BOX_SIZE, 0), length=2 * BOX_SIZE, width=2 * BOX_SIZE, height=0.01, color=color.cyan,
                     opacity=0.2)
    box_top = box(pos=vec(0, BOX_SIZE, 0), length=2 * BOX_SIZE, width=2 * BOX_SIZE, height=0.01, color=color.cyan,
                  opacity=0.2)
    box_left = box(pos=vec(-BOX_SIZE, 0, 0), length=0.01, width=2 * BOX_SIZE, height=2 * BOX_SIZE, color=color.cyan,
                   opacity=0.2)
    box_right = box(pos=vec(BOX_SIZE, 0, 0), length=0.01, width=2 * BOX_SIZE, height=2 * BOX_SIZE, color=color.cyan,
                    opacity=0.2)
    box_back = box(pos=vec(0, 0, -BOX_SIZE), length=2 * BOX_SIZE, width=0.01, height=2 * BOX_SIZE, color=color.cyan,
                   opacity=0.2)


class Body:
    def __init__(self, pos=vector(0, 0, 0), radius=0, velocity=vector(0, 0, 0), colour=color.white, opacity=1):
        #sphere.__init__(self, color=color, radius=radius, pos=pos)
        self._sphere = simple_sphere(pos=pos, color=colour, radius=radius) if opacity == 1 else sphere(pos=pos, color=colour, radius=radius, opacity=opacity)
        self._radius = radius
        self._velocity = velocity

    def volume(self):
        return 4 / 3 * pi * self._radius * self._radius * self._radius

    def mass(self):
        return self.volume()  # uniform density of 1 kg/m^3

    def pos(self):
        return self._sphere.pos

    def set_pos(self, pos):
        self._sphere.pos = pos

    def radius(self):
        return self._radius

    def collide_edge(self):
        if abs(self.pos().x) > BOX_SIZE:
            self._sphere.pos.x *= -1
        if abs(self.pos().y) > BOX_SIZE:
            self._sphere.pos.y *= -1
        if abs(self.pos().z) > BOX_SIZE:
            self._sphere.pos.z *= -1

    def tick(self, objects, start, dt):
        self._sphere.pos += self._velocity * dt
        self.collide_edge()

        other_particles = range(PARTICLES + 1 - start) if P2P else range(PARTICLES, PARTICLES + 1)
        for i in other_particles:
            o = objects[PARTICLES - i]

            # determine whether the two objects are colliding, using mag2 for performance
            tot_radius = self.radius() + o.radius()
            intersect_amount = tot_radius * tot_radius - mag2(self.pos() - o.pos())
            if intersect_amount > 1e-3:
                # the amount of overlap between the two colliding objects
                intersect_amount = tot_radius - mag(self.pos() - o.pos())
                # the vector from self to o
                r = o.pos() - self.pos()

                # adjust the objects so they are no longer intersecting
                # if the radii of the objects are the same (i.e. two Particles)
                #  collided, each is adjusted by the same amount
                # otherwise, the larger object (i.e. the Mass) is held not
                #  adjusted, and the smaller object (i.e. the Particle) is moved
                #  to the edge of the larger object
                # this is done to preserve the position of the Mass, which is
                #  what we are attempting to measure
                self_adjust = .5
                o_adjust = .5

                if self.radius() > o.radius():
                    self_adjust = 0
                    o_adjust = 1
                elif self.radius() < o.radius():
                    self_adjust = 1
                    o_adjust = 0

                self.set_pos(self.pos() -  norm(r) * self_adjust * intersect_amount)
                o.set_pos(o.pos() + norm(r) * o_adjust * intersect_amount)

                # switch into the frame of reference of the other object
                frame = vector(o._velocity)

                self._velocity -= frame
                o._velocity -= frame

                p = proj(self._velocity, r)

                # calculate the new velocities for the two objects
                total_mass = self.mass() + o.mass()
                self._velocity = (self._velocity - p) + (p * (self.mass() - o.mass()) / total_mass)
                o._velocity = p * ((2 * self.mass()) / total_mass)

                # switch back into the original frame of reference
                self._velocity += frame
                o._velocity += frame


class Particle(Body):
    RADIUS = 10  # radius of each Particle, in meters
    MAX_SPEED = 100  # the maximum magnitude of the velocity of a Particle when it is created, in meters/second
    MIN_SPEED = 15  # the minimum magnitude of the velocity of a Particle when it is created, in meters/second

    def __init__(self, objects):
        Body.__init__(self, pos=vector(0, 0, 0), radius=Particle.RADIUS, velocity=vector(0, 0, 0), colour=color.yellow)
        self.generate_velocity()
        self.generate_position(objects)

    def generate_velocity(self):
        velocity = uniform(Particle.MIN_SPEED, Particle.MAX_SPEED) * norm(
            vector(uniform(-1, 1),
                   0 if d1 else uniform(-1, 1),
                   0 if d2 or d1 else uniform(-1, 1)))

        self._velocity = velocity

    def generate_position(self, objects):
        other_particles = range(len(objects)) if P2P else range(len(objects) - 1, len(objects))
        candidate = vector(0, 0, 0)
        found_candidate = False
        while not found_candidate:
            candidate = vector(uniform(-BOX_SIZE, BOX_SIZE),
                               0 if d1 else uniform(-BOX_SIZE, BOX_SIZE),
                               0 if d1 or d2 else uniform(-BOX_SIZE, BOX_SIZE))

            for i in other_particles:
                o = objects[len(objects) - i - 1]
                if mag(candidate - o.pos()) <= o.radius() + Particle.RADIUS:
                    break
                else:
                    found_candidate = True
        self.set_pos(candidate)


class Mass(Body):
    RADIUS = 100  # radius of the Mass, in meters

    def __init__(self):
        Body.__init__(self, pos=vector(0, 0, 0), radius=Mass.RADIUS, velocity=vector(0, 0, 0), colour=color.blue, opacity=.4)
        self._trace = curve(color=color.red)

    def collide_edge(self):
        if self.pos().x + self.radius() > BOX_SIZE or self.pos().x - self._radius < -BOX_SIZE:
            self.pos().x = BOX_SIZE - self.radius() if self.pos().x > 0 else -BOX_SIZE + self.radius()
            self._velocity.x *= -1
        if self.pos().y + self.radius() > BOX_SIZE or self.pos().y - self._radius < -BOX_SIZE:
            self.pos().y = BOX_SIZE - self.radius() if self.pos().y > 0 else -BOX_SIZE + self.radius()
            self._velocity.y *= -1
        if self.pos().z + self.radius() > BOX_SIZE or self.pos().z - self._radius < -BOX_SIZE:
            self.pos().z = BOX_SIZE - self.radius() if self.pos().z > 0 else -BOX_SIZE + self.radius()
            self._velocity.z *= -1

    def tick(self, objects, start, dt):
        Body.tick(self, objects, start, dt)
        self._trace.append(self.pos())


def run_sim(total_time=-1):
    objects = list()
    mass = Mass()
    objects.append(mass)
    for _ in range(PARTICLES):
        objects.append(Particle(objects))

    t = 0
    while total_time < 0 or t < total_time:
        for i in range(len(objects)):
            objects[i].tick(objects, i + 1, dt)

        t += dt
        rate(400)

    return mag(mass._sphere.pos)


if DEMO:
    run_sim()
else:
    distances = list()
    for i in range(NUM_SIMS):
        print("running simulation " + str(i + 1) + "/" + str(NUM_SIMS))
        distances.append(run_sim(SIM_TIME))

    avg = 0

    for d in distances:
        avg += d
    avg /= len(distances)

    sd = 0
    for d in distances:
        sd += (d - avg) ** 2
    sd /= len(distances)
    sd = sqrt(sd)

    #
    # This writes the output to file
    #
    # datetime = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
    # filename = "data/data-" + str(datetime) + ".txt"
    # f = open(filename, 'w')
    # f.write("Brownian Motion Simulation\n")
    # f.write(datetime + "\n\n")
    # f.write("Simulation Parameters:\n")
    # f.write("   times run: " + str(NUM_SIMS) + "\n")
    # f.write("   number of particles: " + str(PARTICLES) + "\n")
    # f.write("   simulation time (s): " + str(SIM_TIME) + "\n")
    # f.write("   dt (s): " + str(dt) + "\n")
    # f.write("   box size (m): " + str(BOX_SIZE) + "\n")
    # f.write("   mass radius: " + str(Mass.RADIUS) + "\n")
    # f.write("   particle radius: " + str(Particle.RADIUS) + "\n")
    # f.write("   particle speed interval: [" + str(Particle.MIN_SPEED) + "," + str(Particle.MAX_SPEED) + "]\n")
    # f.write("\n")
    # f.write("Average displacement: " + str(avg) + "\n")
    # f.write("Standard deviation: " + str(sd) + "\n\n")
    # f.write("Displacement data:\n")

    # for d in distances:
    #     f.write(str(d) + "\n")
    #
    # f.close()
    #
    # print
    # "Output written to " + filename
