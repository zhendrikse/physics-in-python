#Web VPython 3.2
from vpython import ellipsoid, vec, vector, mag, rate, sign, sqrt, text, box, canvas, color
from random import uniform

title = """Splatting raindrops 

&#x2022; Original version written by Lenore Horner, 2009
&#x2022; Refactored by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a>
&#x2022; Reset the scene by reloading the browser. 
&#x2022; Click mouse button to start

"""

animation = canvas(title=title)

toggle = 0  # 0 makes all drops the same mass; 1 makes all drops the same density

class Raindrop:
    def __init__(self, cloud_size, drop_size, cloud_height):
        self._droplet = ellipsoid(length=drop_size, width=drop_size, height=drop_size, color=color.cyan)
        self._velocity = vec(0, 0, 0)
        self._acceleration = vec(0, 0, 0)
        self._droplet.pos = vector(uniform(-cloud_size, cloud_size), cloud_height, uniform(-cloud_size, cloud_size))
        self._cloud_height = cloud_height

    def overlaps_with(self, other):
        return mag(self._droplet.pos - other._droplet.pos) < (self._droplet.length + other._droplet.length) / 2.0

    def modify_position(self, new_position):
        self._droplet.pos = new_position

    def _has_hit_the_ground(self):
        return self._droplet.pos.y < -self._cloud_height + self._droplet.height + 0.5

    def _fall_down(self, dt):
        constant = .5

        self._velocity.y = self._velocity.y + self._acceleration.y * dt
        volume = self._droplet.width ** 2 * self._droplet.height
        accel = sign(
            self._velocity.y) * constant * self._droplet.width ** 2 * self._velocity.y ** 2 / (
                    volume) ** toggle
        self._acceleration.y = -9.8 - accel

    def _splat(self):
        if self._droplet.height > 0.09:  # only worry about drops that haven't already gone splat
            self._velocity.y = 0  # drops stop
            # drops flatten on surface
            self._droplet.height = 0.09
            self._droplet.length = self._droplet.width = self._droplet.width ** 1.5
            self._droplet.pos.y = -self._cloud_height + 0.5

    def fall(self, dt):
        self._droplet.pos += self._velocity * dt
        if self._has_hit_the_ground():
            self._splat()
        else:
            self._fall_down(dt)

class Cloud:
    def __init__(self, size, height=10, raindrops_amount=200, max_dropsize=1):
        self._raindrops = []
        self._height = height
        for i in range(raindrops_amount):  # create drops of various sizes at rest at common height
            self._raindrops += [Raindrop(cloud_size=size, drop_size=uniform(0.1, max_dropsize), cloud_height=height)]
            self._check_for_overlap(i, size)

    def _check_for_overlap(self, i, size):
        # make sure drops don't overlap; including making sure changed location doesn't overlap one that was clear before
        check = -1
        while check < 0:
            check = 0
            for j in range(i):
                if self._raindrops[i].overlaps_with(self._raindrops[j]):
                    check = check - 1
            if check < 0:
                new_position = vector(uniform(-size, size), self._height, uniform(-size, size))
                self._raindrops[i].modify_position(new_position)

    def let_it_rain(self, dt):
        for raindrop in self._raindrops:
            raindrop.fall(dt)

dropheight = 10
worldsize = sqrt(200) * 2
max_dropsize = 1

floor = box(length=worldsize, height=0.5, width=worldsize, pos=vec(0, -dropheight, 0), color=color.green)
cloud = Cloud(worldsize / 2.0 - max_dropsize)

pop_up = text(pos=vec(-worldsize/2+2, 0, 0), text="Click mouse to start", height=2, color=color.yellow, billboard=True)
animation.waitfor("click")
pop_up.visible = False

delta_t = 0.01
while 1:
    rate(1 / delta_t)
    cloud.let_it_rain(delta_t)