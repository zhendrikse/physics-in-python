#Web VPython 3.2

from vpython import log, canvas, rate, curve, vector, color, cross, quad, vertex, sqrt, pow, checkbox, slider
import random

title = """&#x2022; Based on <a href="https://github.com/ragnraok/RandomFractalTerrain-Vpython">RandomFractalTerrain-Vpython</a>
&#x2022; Refactored and extended by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in <a href="https://github.com/zhendrikse/science/blob/main/mathematics/code/fractal_terrain.py">fractal_terrain.py</a>
&#x2022; Click to regenerate a new terrain

"""

display = canvas(range=350, width=600, height=600, title=title, background=color.gray(0.075), forward=vector(-40, -122, -83), center=vector(-18, -110, 10))


class Diamond:
    """
    a -- b -- c
    |    |    |
    d -- e -- f
    |    |    |
    g -- h -- i
    """

    def __init__(self, x, y, span, height, random_value):
        half = span >> 1
        self.a = vector(x, y, height[y][x])
        self.c = vector(x + span, y, height[y][x + span])
        self.g = vector(x, y + span, height[y + span][x])
        self.i = vector(x + span, y + span, height[y + span][x + span])

        average_height = .25 * (self.a.z + self.c.z + self.g.z + self.i.z)
        self.e = vector(x + half, y + half, average_height + random_value)

    def center_point(self):
        return self.e


class Square:
    """
    a -- b -- c
    |    |    |
    d -- e -- f
    |    |    |
    g -- h -- i
    """

    def __init__(self, x, y, span, height):
        self.half = half = span >> 1
        self.a = vector(x, y, height[y][x])
        self.b = vector(x + half, y, height[y][x + half])
        self.c = vector(x + span, y, height[y][x + span])
        self.d = vector(x, y + half, height[y + half][x])
        self.e = vector(x + half, y + half, height[y + half][x + half])
        self.f = vector(x + span, y + half, height[y + half][x + span])
        self.g = vector(x, y + span, height[y + span][x])
        self.h = vector(x + half, y + span, height[y + span][x + half])
        self.i = vector(x + span, y + span, height[y + span][x + span])

    def set_random_heights(self, random_values, terrain_size, height):
        x, y = self.a.x, self.a.y
        half = self.half
        above_b = vector(x + half, y - half >= 0 and y - half or terrain_size - half, 0)
        left_d = vector(x - half >= 0 and x - half or terrain_size - half, y + half, 0)
        right_f = vector(x + half * 3 <= terrain_size and x + half * 3 or half, y + half, 0)
        below_h = vector(x + half, y + half * 3 <= terrain_size and y + half * 3 or half, 0)

        # the four diamonds
        self._set_height_for_square(height, random_values[0], self.a, self.e, self.g, left_d, self.d)
        self._set_height_for_square(height, random_values[1], self.a, self.e, self.c, above_b, self.b)
        self._set_height_for_square(height, random_values[2], self.c, self.e, self.i, right_f, self.f)
        self._set_height_for_square(height, random_values[3], self.g, self.e, self.i, below_h, self.h)

    def _set_height_for_square(self, height, random_value, a, b, c, d, center_point):
        tmp = [height[int(point.y)][int(point.x)] for point in [a, b, c, d]]
        average = sum(tmp) / len(tmp)
        center_point.z = average + random_value
        height[int(center_point.y)][int(center_point.x)] = center_point.z


class FractalTerrain:
    def __init__(self, num_grid_lines, smoothness, z_scale):
        self._z_scale = z_scale
        self._smoothness = smoothness
        self._num_grid_lines = num_grid_lines
        self._height = []

    def _iterate(self, smoothness, z_scale):
        count = 0
        iter_num = log(len(self._height) - 1) / log(2)
        while count < iter_num:
            count += 1
            random_value = self._generate_random_num(count, smoothness, z_scale)
            self._diamond(count, random_value)
            self._square(count, smoothness, z_scale)

    def _diamond(self, count, random_value):
        terrain_size = len(self._height) - 1
        num_seg = 1 << (count - 1)
        span = terrain_size // num_seg
        for x in range(0, terrain_size, span):
            for y in range(0, terrain_size, span):
                center_point = Diamond(x, y, span, self._height, random_value).center_point()
                self._height[int(center_point.y)][int(center_point.x)] = center_point.z

    def _square(self, count, smoothness, z_scale):
        terrain_size = len(self._height) - 1
        num_seg = 1 << (count - 1)
        span = terrain_size // num_seg
        for x in range(0, terrain_size, span):
            for y in range(0, terrain_size, span):
                square_ = Square(x, y, span, self._height)
                random_values = []
                for i in range(4):
                    random_values += [self._generate_random_num(count, smoothness, z_scale)]
                square_.set_random_heights(random_values, terrain_size, self._height)

        for y in range(0, terrain_size, span):
            self._height[y][terrain_size] = self._height[y][0]

        for x in range(0, terrain_size, span):
            self._height[terrain_size][x] = self._height[0][x]

    def _generate_random_num(self, count, smoothness, z_scale):
        _reduce = 1
        for i in range(count):
            _reduce *= pow(2, -smoothness)
        return _reduce * random.randint(-z_scale, z_scale)

    def new_terrain(self):
        final_size = 1
        while final_size < self._num_grid_lines:
            final_size <<= 1
        self._height = [[0 for i in range(final_size + 1)] for i in range(final_size + 1)]
        self._iterate(self._smoothness, self._z_scale)
        return self._height

    def z_scale(self):
        return self._z_scale

    def set_smoothness_to(self, event):
        self._smoothness = .5 * event.value + .75

    def set_resolution_to(self, event):
        self._num_grid_lines = event.value

    def set_z_scale_to(self, event):
        self._z_scale = int(event.value)

class SurfacePlot:
    def __init__(self, points, z_scale):
        self._vertices, self._quads = [], []
        self._z_scale = z_scale
        self._create_vertices(points)
        self._create_quads()
        self._make_normals()

    def _create_vertices(self, points):
        for point in points:
            self._vertices.append(vertex(pos=point, normal=vector(0, 1, 0)))
            hue = 1.5 + point.y / self._z_scale
            self._vertices[-1].color = color.hsv_to_rgb(vector(hue, 1., 1.))

    def _create_quad(self, x, y):
        dimension = int(sqrt(len(self._vertices)))
        _neighbor_increment_x, _neighbor_increment_y = 1, 1
        if x == (dimension - 1):
            _neighbor_increment_x = -x
        if y == (dimension - 1):
            _neighbor_increment_y = -y

        v0 = self._get_vertex(x, y, dimension)
        v1 = self._get_vertex(x + _neighbor_increment_x, y, dimension)
        v2 = self._get_vertex(x + _neighbor_increment_x, y + _neighbor_increment_y, dimension)
        v3 = self._get_vertex(x, y + _neighbor_increment_y, dimension)
        self._quads.append(quad(vs=[v0, v1, v2, v3]))

    # Create the quad objects, based on the vertex objects already created.
    def _create_quads(self):
        dimension = int(sqrt(len(self._vertices)))
        for x in range(dimension - 1):
            for y in range(dimension - 1):
                self._create_quad(x, y)

    def _set_vertex_normal_for(self, x, y):
        dimension = int(sqrt(len(self._vertices)))
        _neighbor_increment_x, _neighbor_increment_y = 1, 1
        if x == (dimension - 1):
            _neighbor_increment_x = -x
        if y == (dimension - 1):
            _neighbor_increment_y = -y

        vertex_ = self._get_vertex(x, y, dimension)
        normal_total_ = self._get_vertex(x, y + _neighbor_increment_y, dimension).normal
        normal_total_ += self._get_vertex(x + _neighbor_increment_x, y, dimension).normal
        vec_1 = self._get_vertex(x, y + _neighbor_increment_y, dimension).pos - vertex_.pos
        vec_2 = self._get_vertex(x + _neighbor_increment_x, y, dimension).pos - vertex_.pos
        # """
        # Further work to focus on this area of the normal calculations
        # """
        # vertex_.normal = cross(vec_1, vec_2)
        normal_total_ += cross(vec_1, vec_2)
        vertex_.normal = normal_total_ / 2

    # Set the normal for each vertex to be perpendicular to the lower left corner of the quad.
    # The vectors a and b point to the right and up around a vertex in the xy plane.
    def _make_normals(self):
        dimension = int(sqrt(len(self._vertices)))
        for x in range(dimension):
            for y in range(dimension):
                self._set_vertex_normal_for(x, y)

    def _get_vertex(self, x, y, dimension):
        return self._vertices[x * dimension + y]


class ContourPlot:
    def __init__(self, points, z_scale):
        num_points = len(points)
        resolution = int(sqrt(num_points))

        # horizontal lines
        horizontal_curves = []
        for i in range(0, num_points, resolution):
            for j in range(resolution - 1):
                horizontal_curves.append(curve(pos=[points[i + j], points[i + j + 1]], radius=.3))
                hue = 1.5 + .5 * (points[i + j].y + points[i + j + 1].y) / z_scale
                horizontal_curves[-1].color = color.hsv_to_rgb(vector(hue, .9, 1.0))

        # vertical lines
        vertical_curves = []
        for i in range(0, resolution):
            for j in range(0, num_points - resolution, resolution):
                if i + j < num_points:  # and i + j + self._size < num_points:
                    vertical_curves.append(curve(pos=[points[i + j], points[i + j + resolution]], radius=.3))
                    hue = 1.5 + .5 * (points[i + j].y + points[i + j + 1].y) / z_scale
                    vertical_curves[-1].color = color.hsv_to_rgb(vector(hue, .9, 1.0))


class Grid:
    def __init__(self, size=200):
        self._size = size
        self._render_as_surface = False
        self._render_as_contour = True

    def render(self, fractal):
        height = fractal.new_terrain()
        resolution = len(height)
        has_height = (height is not None and len(height) != 0)
        points = []
        row_step = col_step = (self._size - (-self._size)) / float(resolution - 1)
        for row in range(resolution):
            for col in range(resolution):
                points.append(vector(self._size - col * col_step, has_height and height[row][col] or 0, self._size - row * row_step))

        if self._render_as_surface:
            _ = SurfacePlot(points, fractal.z_scale())
        if self._render_as_contour:
            _ = ContourPlot(points, fractal.z_scale())

    def set_surface_rendering(self, event):
        self._render_as_surface = event.checked

    def set_contour_rendering(self, event):
        self._render_as_contour = event.checked


fractal_terrain = FractalTerrain(num_grid_lines=60, z_scale=200, smoothness=1)
grid = Grid()

def refresh_screen(evt):
    for obj in display.objects:
        obj.visible = False
        #obj.delete()

    grid.render(fractal_terrain)


display.bind("click", refresh_screen)

_ = checkbox(text="Surface ", bind=grid.set_surface_rendering, checked=False)
_ = checkbox(text="Contour ", bind=grid.set_contour_rendering, checked=True)

display.append_to_caption("\n\nSmoothness")
_ = slider(min=0, max=1, value=.5, bind=fractal_terrain.set_smoothness_to)

display.append_to_caption("\n\nresolution")
_ = slider(min=10, max=120, value=60, bind=fractal_terrain.set_resolution_to)

display.append_to_caption("\n\nHeight scale")
_ = slider(min=100, max=300, value=200, bind=fractal_terrain.set_z_scale_to)

grid.render(fractal_terrain)
while True:
    rate(10)
