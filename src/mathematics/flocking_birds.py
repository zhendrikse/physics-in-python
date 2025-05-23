from vpython import canvas, color, arrow, vector, vec, slider, rate
from itertools import combinations

title="""Flock of Birds

&#x2022; Original version created by B. Philhour 10/9/17 
&#x2022; Inspired by Gary Flake's <a href="https://www.amazon.com/Computational-Beauty-Nature-Explorations-Adaptation/dp/0262561271">Computational Beauty of Nature</a>
&#x2022; 1998 MIT Press ISBN-13 978-0-262-56127-3
&#x2022; Maintained by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>

"""

animation = canvas(width=600, height=450, background=color.black, title=title)  # , fov=10)

spread = 3  # initial physical radius of entire flock
speed = 6  # initial horizontal speed
size = 1  # length of bird vector


class Bird:
    def __init__(self, velocity, size=1):
        pos = spread * vector.random()
        self._bird = arrow(pos=pos, axis=size * velocity.norm(), color=color.yellow)
        self._velocity = velocity
        self._position = pos

    def update(self, acceleration, dt):
        self._velocity += acceleration * dt
        self._position += self._velocity * dt
        self._bird.axis = size * self._velocity.norm()
        self.render()

    def position(self):
        return self._position

    def velocity(self):
        return self._velocity

    def render(self):
        self._bird.pos = self._position

    def distance_to(self, other_bird):
        return other_bird.position() - self.position()

class Flock:
    def __init__(self, bird_count, random_weight=0.1, center_weight=0.1, direction_weight=0.05, avoid_weight=0.5):
        self._birds = []
        self._bird_count = bird_count
        self._random_weight = random_weight
        self._center_weight = center_weight
        self._direction_weight = direction_weight
        self._avoid_weight = avoid_weight

        for _ in range(bird_count):
            velocity = vec(speed, 0, 0) + speed * vector.random()
            self._birds += [Bird(velocity)]

    def update(self, dt):
        # compute average position and direction
        center = vec(0, 0, 0)
        direction = vec(0, 0, 0)
        for bird in self._birds:
            center += bird.position()
            direction += bird.velocity()
        center /= self._bird_count
        direction /= self._bird_count

        # avoid nearest birds (A BETTER VERSION WOULD ANTICIPATE COLLISIONS)
        avoid = [vector(0, 0, 0)] * self._bird_count
        for i, j in combinations(range(self._bird_count), 2):
            separation_dist = self._birds[i].distance_to(self._birds[j])
            if separation_dist.mag < 5 * size:
                avoid[i] -= separation_dist / separation_dist.mag2
                avoid[j] += separation_dist / separation_dist.mag2

        for count in range(self._bird_count):
            acceleration = self._random_weight * vector.random()
            acceleration += self._center_weight * (center - self._birds[count].position())
            acceleration += self._direction_weight * (direction - self._birds[count].velocity())
            acceleration += self._avoid_weight * (avoid[count].norm() - self._birds[count].position())
            self._birds[count].update(acceleration, dt)

    def set_center_weight(self, value):
        self._center_weight = value

    def set_direction_weight(self, value):
      self._direction_weight = value

    def set_avoid_weight(self, value):
      self._avoid_weight = value

    def set_random_weight(self, new_random_weight):
        self._random_weight = new_random_weight

    def center_weight(self):
        return self._center_weight

    def direction_weight(self):
        return self._direction_weight

    def avoid_weight(self):
        return self._avoid_weight

    def random_weight(self):
        return self._random_weight

flock = Flock(250)

def avoid_bird():
  flock.set_avoid_weight(avoid_weight_slider.value)

def direction_bird():
    flock.set_direction_weight(direction_weight_slider.value)

def center_bird():
    flock.set_center_weight(center_weight_slider.value)

def on_random_weight_slider():
    flock.set_random_weight(random_weight_slider.value)

animation.append_to_caption("\nRandom behavior\n")
random_weight_slider = slider(bind=on_random_weight_slider, min=0.0, max=50.0, value=flock.random_weight())
animation.append_to_caption("\n\nCentering behavior\n")
center_weight_slider = slider(bind=center_bird, min=0.0, max=2.0, value=flock.center_weight())
animation.append_to_caption("\n\nDirection behavior\n")
direction_weight_slider = slider(bind=direction_bird, min=0.0, max=2.0, value=flock.direction_weight())
animation.append_to_caption("\n\nAvoidance behavior\n")
avoid_weight_slider = slider(bind = avoid_bird, min = 0.0, max = 2.0, value=flock.avoid_weight())

# make a button for startling the birds
# def startle():
#     nonlocal bird, N
#     for i in range(N):
#       bird[i].vel = 2 * speed * vector.random()
#
# scene.append_to_caption('\n\n')
# button( bind=startle, text='Startle' )

# set up the time step interval
dt = 0.02
while True:
    flock.update(dt)
    rate(1 / dt)
    # scene.center = center
