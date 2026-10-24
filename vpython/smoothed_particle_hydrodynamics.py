#Web VPython 3.2
from vpython import sqrt, simple_sphere, color, vec, rate, canvas, label, cylinder, slider, mag, dot

title="""&#x2022; Original <a href="https://github.com/AlexandreSajus/Python-Fluid-Simulation">Python-Fluid-Simulation</a> code by <a href="https://github.com/AlexandreSajus">Alexandre Sajus</a>
&#x2022; Ported to <a href="https://vpython.org">VPython</a> by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a>, see <a href="https://github.com/zhendrikse/science/blob/main/fluids/code/smoothed_particle_hydrodynamics.py">smoothed_particle_hydrodynamics.py</a>

"""

# Simulation parameters
N = 300  # Number of particles
SIM_W = 0.5  # Simulation space width
BOTTOM = 0  # Simulation space ground
DAM = -0.3  # Position of the dam, simulation space is between -0.5 and 0.5
DAM_BREAK = 250  # Number of frames before the dam breaks

# Physics parameters
G = 0.02 * 0.25  # Acceleration of gravity
SPACING = 0.08  # Spacing between particles, used to calculate pressure
K = SPACING / 1000.0  # Pressure factor
K_NEAR = K * 10  # Near pressure factor, pressure when particles are close to each other
# Default density, will be compared to local density to calculate pressure
REST_DENSITY = 3.0
# Neighbour radius, if the distance between two particles is less than R, they are neighbours
R = SPACING * 1.25
SIGMA = 0.2  # Viscosity factor
MAX_VEL = 2.0  # Maximum velocity of particles, used to avoid instability
# Wall constraints factor, how much the particle is pushed away from the simulation walls
WALL_DAMP = 0.05
VEL_DAMP = 0.5  # Velocity reduction factor when particles are going above MAX_VEL


class Particle:
    def __init__(self, x_pos: float, y_pos: float):
        self._position = vec(x_pos, y_pos, 0)
        self._previous_position = vec(x_pos, y_pos, 0)
        self._visual_position = vec(x_pos, y_pos, 0)
        self._rho = 0.0
        self._rho_near = 0.0
        self._press = 0.0
        self._press_near = 0.0
        self._neighbors = []
        self._velocity = vec(0, 0, 0)
        self._force = vec(0, -G, 0)

    def calculate_neighbor_pressure(self):
        pressure = vec(0, 0, 0)
        for neighbor in self._neighbors:
            particle_to_neighbor = neighbor.position() - self._position
            distance = mag(particle_to_neighbor)
            normal_distance = 1 - distance / R
            normal_distance_squared = normal_distance * normal_distance
            normal_distance_cubed = normal_distance_squared * normal_distance

            total_pressure = (self._press + neighbor._press) * normal_distance_squared + (self._press_near + neighbor._press_near) * normal_distance_cubed

            pressure_vector = particle_to_neighbor * total_pressure / distance
            neighbor._force += pressure_vector
            pressure += pressure_vector
        self._force -= pressure

    def update_state(self, dam: bool):
        self._previous_position = vec(self._position)

        # Apply force using Newton's second law and Euler integration with mass = 1 and dt = 1
        self._velocity += self._force

        # Move particle according to its velocity using Euler integration with dt = 1
        self._position += self._velocity

        # Set visual position. Visual position is the one shown on the screen
        # It is used to avoid unstable particles to be shown
        self._visual_position = vec(self._position)

        # Reset force
        self._force = vec(0, -G, 0)

        # Define velocity using Euler integration with dt = 1
        self._velocity = self._position - self._previous_position

        # Calculate velocity
        velocity = mag(self._velocity)

        # Reduces the velocity if it is too high
        if velocity > MAX_VEL:
            self._velocity *= VEL_DAMP

        # Wall constraints, if a particle is out of bounds, create a spring force to bring it back
        if self._position.x < -SIM_W:
            self._force.x -= (self._position.x - -SIM_W) * WALL_DAMP
            self._visual_position.x = -SIM_W

        # Same thing as a wall constraint but for the dam that will move from dam to SIM_W
        if dam and self._position.x > DAM:
            self._force.x -= (self._position.x - DAM) * WALL_DAMP

        # Same thing for the right wall
        if self._position.x > SIM_W:
            self._force.x -= (self._position.x - SIM_W) * WALL_DAMP
            self._visual_position.x = SIM_W

        # Same thing but for the floor
        if self._position.y < BOTTOM:
            # We use SIM_W instead of BOTTOM here because otherwise particles are too low
            self._force.y -= (self._position.y - SIM_W) * WALL_DAMP
            self._visual_position.y = BOTTOM

        # Reset density
        self._rho = 0.0
        self._rho_near = 0.0

        # Reset neighbors
        self._neighbors = []

    def calculate_pressure(self):
        self._press = K * (self._rho - REST_DENSITY)
        self._press_near = K_NEAR * self._rho_near

    def calculate_viscosity_force(self):
        for neighbor in self._neighbors:
            particle_to_neighbor = neighbor.position() - self._position
            distance = sqrt(dot(particle_to_neighbor, particle_to_neighbor))
            normal_p_to_n = particle_to_neighbor / distance

            relative_distance = distance / R
            velocity_difference = dot(self._velocity - neighbor.velocity(), normal_p_to_n)
            if velocity_difference > 0:
                viscosity_force = (1 - relative_distance) * SIGMA * velocity_difference * normal_p_to_n
                self._velocity -= viscosity_force * 0.5
                neighbor._velocity += viscosity_force * 0.5

    def position(self):
        return self._position

    def velocity(self):
        return self._velocity


def start(xmin: float, xmax: float, ymin: float, space: float, count: int):
    """
    Creates a rectangle of particles within xmin, xmax and ymin
    We start by creating a particle at (xmin, ymin)
    and then add particles until we reach count particles.
    Particles are represented by their position [x, y]

    Args:
        xmin (float): x min bound of the rectangle
        xmax (float): x max bound of the rectangle
        ymin (float): y min bound of the rectangle
        space (float): space between particles
        count (int): number of particles

    Returns:
        list: list of Particle objects
    """
    result = []
    x_pos, y_pos = xmin, ymin
    for _ in range(count):
        result.append(Particle(x_pos, y_pos))
        x_pos += space
        if x_pos > xmax:
            x_pos = xmin
            y_pos += space
    return result


def calculate_density(particles: list[Particle]):
    """
    Calculates density of particles
        Density is calculated by summing the relative distance of neighboring particles
        We distinguish density and near density to avoid particles to collide with each other
        which creates instability

    Args:
        particles (list[Particle]): list of particles
    """
    for i, particle_1 in enumerate(particles):
        density = 0.0
        density_near = 0.0
        # Density is calculated by summing the relative distance of neighboring particles
        for j in range(i + 1, len(particles)):
            particle_2 = particles[j]
            distance = mag(particle_1.position() - particle_2.position())
            if distance < R:
                # normal distance is between 0 and 1
                normal_distance = 1 - distance / R
                normal_distance_squared = normal_distance * normal_distance
                normal_distance_cubed = normal_distance_squared * normal_distance

                density += normal_distance_squared
                density_near += normal_distance_cubed

                particle_2._rho += normal_distance_squared
                particle_2._rho_near += normal_distance_cubed

                particle_1._neighbors.append(particle_2)
        particle_1._rho += density
        particle_1._rho_near += density_near


def update(particles: list[Particle], dam: bool):
    # Update the state of the particles (apply forces, reset values, etc.)
    for particle in particles:
        particle.update_state(dam)

    calculate_density(particles)

    for particle in particles:
        particle.calculate_pressure()
        particle.calculate_neighbor_pressure()
        particle.calculate_viscosity_force()


display = canvas(title=title, width=600, height=300, color=color.gray(0.075), range=.5, center=vec(0, .35, 0))

water = start(-SIM_W, DAM, BOTTOM, 0.03, N)
droplets = []
for particle_ in water:
    droplets.append(simple_sphere(color=vec(0.1, 0.2, 1.0), pos=particle_.position(), radius=0.03, shininess=0))

clock = label(pos=vec(0, .75, 0), text="Breaking dam in 0:00", box=False, color=color.yellow)
cylinder(pos=vec(-.75, -.1, 0), color=color.orange, axis=vec(1.5, 0, 0), radius=0.02)
wall = cylinder(pos=vec(-.05, -.1, 0), color=color.orange, axis=vec(0, .4, 0), radius=0.02)

def modify_droplet_radius(event):
    for droplet in droplets:
        droplet.radius = event.value

display.append_to_caption("\nDroplet radius")
_ = slider(min=.01, max=.05, value=0.03, bind=modify_droplet_radius)

step = 0
dam_built = True
frame_rate = 25
while True:
    clock.text = "Breaking dam in {:1.2f}".format((DAM_BREAK - step) / frame_rate)
    rate(frame_rate)
    if step == DAM_BREAK:
        clock.visible = False
        dam_built = False
        wall.pos.y += .4

    update(water, dam_built)
    for i, droplet in enumerate(droplets):
        droplet.pos = vec(water[i]._position)

    step += 1
