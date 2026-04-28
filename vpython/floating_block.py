# Web VPython 3.2

from vpython import rate, canvas, box, color, vector, graph, gcurve, textures

title = """&#x2022; Based on original <a href="https://github.com/gcschmit/vpython-physics/blob/master/buoyancy/buoyancy.py">buoyancy.py</a>
&#x2022; Refactored by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> to <a href="https://github.com/zhendrikse/science/blob/main/kinematics/code/floating_block.py">floating_block.py</a>

"""

display = canvas(title=title, background=color.gray(0.075), forward=vector(-0.52, -0.67, -0.52), range=2., width=600, height=600)

class WoodenBlock:
    def __init__(self, density=500):
        self._block = box(pos=vector(0, 0, 0), texture=textures.wood, size=vector(0.4, 0.4, 0.1))
        self._density = density
        self._velocity = vector(0, 0, 0)

    def pos(self):
        return self._block.pos

    def buoyancy_force(self, water):
        return water.density() * -g * self._submerged_volume(water)

    def drag_force(self):
        return dragCoefficient * self._velocity.y

    def net_force_in(self, water):
        gravitational_force = self._mass() * g
        return self.buoyancy_force(water) + gravitational_force + self.drag_force()

    def _mass(self):
        return self._density * self._block.size.x * self._block.size.y * self._block.size.z

    def _submerged_volume(self, water: box):
        top_of_fluid = water.pos().y + water.size().y / 2
        top_of_object = self.pos().y + self._block.size.y / 2
        bottom_of_object = self.pos().y - self._block.size.y / 2

        if top_of_object <= top_of_fluid:
            height_submerged = self._block.size.y
        elif bottom_of_object >= top_of_fluid:
            height_submerged = 0
        else:
            height_submerged = (top_of_fluid - bottom_of_object)

        return self._block.size.x * height_submerged * self._block.size.z

    def move_due_to(self, net_force, dt):
        acceleration = net_force / self._mass()
        self._velocity += + acceleration * dt
        self._block.pos += self._velocity * dt

class Liquid:
    def __init__(self, density=1000):
        self._liquid = box(size=vector(2, 2, 0.75), color=color.blue, opacity=0.3)
        self._density = density

    def density(self):
        return self._density

    def size(self):
        return self._liquid.size

    def pos(self):
        return self._liquid.pos


wooden_block = WoodenBlock()
fluid = Liquid()

display.append_to_caption("\n\n")
graphs = graph(title="Buoyancy (magenta) and drag (blue) forces", background=color.black, xtitle="Time", ytitle="Force")
buoyancy_curve = gcurve(color=color.magenta)
drag_force_curve = gcurve(color=color.blue)

dragCoefficient = vector(0, -5.0, 0)
g = vector(0, -9.8, 0)

t = 0
dt = 0.001
while t < 20 and wooden_block.pos().y > (fluid.pos().y - fluid.size().y / 2):
    rate(1 / dt)

    wooden_block.move_due_to(wooden_block.net_force_in(fluid), dt)

    buoyancy_curve.plot(t, wooden_block.buoyancy_force(fluid).y)
    drag_force_curve.plot(t, wooden_block.drag_force().y)

    t += dt
