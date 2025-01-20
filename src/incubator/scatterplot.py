from vpython import *
import numpy

SIZE = 10

#
# https://www.researchgate.net/publication/253329352_Python_Data_Plotting_and_Visualisation_Extravaganza
#
class PointCloud(object):
    def __init__(self):
        self.iterator = None
        self.balls = numpy.zeros([SIZE] * 3, dtype=object)

        for x in range(SIZE):
            for y in range(SIZE):
                 for z in range(SIZE):
                    coords = vec(x, y, z)
                    new_sphere = sphere(pos=coords, radius=0.25, color=coords / (SIZE - 1))
                    self.balls[x, y, z] = new_sphere

    def update_balls(self):
        for x in range(SIZE):
            for y in range(SIZE):
                for z in range(SIZE):
                    offset = numpy.random.normal(loc=0.0, scale=0.01, size=3) * 5
                    pos = self.balls[x, y, z].pos
                    self.balls[x, y, z].pos = pos + vec(offset[0], offset[1], offset[2])


    def run(self):
        for i in range(10000):
            self.update_balls()

point_cloud = PointCloud()
point_cloud.run()

while True:
    rate(30)
