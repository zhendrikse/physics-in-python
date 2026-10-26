#Web VPython 3.2
from vpython import box, random, rate, color, vec, slider, canvas, cylinder

title = """&#x2022; <a href="https://github.com/zhendrikse/science/blob/main/mathematics/code/2d_game_of_life.py">2d_game_of_life.py</a> by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> &amp; Rob Westgeest
&#x2022; Developed using the principles of <a href="https://www.hendrikse.name/tdd/">test-driven development (TDD)</a>, see also <a href="https://github.com/zhendrikse/tdd/tree/master/kata-solutions/game-of-life">code with tests</a>

"""

dimension_x = dimension_y = 100
display = canvas(title=title, bacground=color.gray(0.075), width=600, height=600, center=.5 * vec(dimension_x, dimension_y, 0))
MathJax.Hub.Queue(["Typeset", MathJax.Hub])

class Game:
    def __init__(self, cells):
        self._cells = cells

    def next_generation(self):
        new_cells = []
        for row in range(self.height()):
            new_cells.append(self.next_row_generation(row))
        return Game(new_cells)

    def next_row_generation(self, row):
        result = []
        for i in range(self.width()):
            result.append(self.cell_at(row, i).next_generation(self.neighbours_for(row, i)))
        return result

    def neighbours_for(self, row, column):
        neighbours = [
            self.cell_at(row - 1, column - 1),
            self.cell_at(row - 1, column),
            self.cell_at(row - 1, column + 1),
            self.cell_at(row, column - 1),
            self.cell_at(row, column + 1),
            self.cell_at(row + 1, column - 1),
            self.cell_at(row + 1, column),
            self.cell_at(row + 1, column + 1),
        ]
        return without_nones(neighbours)

    def cell_at(self, row, column):
        if column < 0: return None
        if column >= self.width(): return None
        if row < 0: return None
        if row >= self.height(): return None
        return self._cells[row][column]

    def width(self):
        return len(self._cells[0])

    def height(self):
        return len(self._cells)


def without_nones(list_):
    filtered_list = []
    for item in list_:
        if item is not None:
            filtered_list.append(item)
    return filtered_list


class Cell:
    def __init__(self, alive):
        self._alive = alive

    def next_generation(self, neighbours):
        if self.is_alive():
            return self._next_generation_when_alive(neighbours)

        return self._next_generation_when_dead(neighbours)

    def _next_generation_when_dead(self, neighbours):
        return living_cell() if len(living(neighbours)) == 3 else dead_cell()

    def _next_generation_when_alive(self, neighbours):
        return living_cell() if len(living(neighbours)) in {2, 3} else dead_cell()

    def is_alive(self):
        return self._alive


def living(neighbours):
    living_neighbours = []
    for neighbour in neighbours:
        if neighbour.is_alive():
            living_neighbours.append(neighbour)
    return living_neighbours


def dead_cell():
    return Cell(alive=False)


def living_cell():
    return Cell(alive=True)


def create_pixels(dim_x, dim_y):
    pixel_data = []
    for x in range(dim_x):
        row = []
        for y in range(dim_y):
            row.append(box(pos=vec(x, y, 0), shininess=0, visible=False, color=color.yellow))
            cylinder(pos=vec(-.5, y - .5, 0), color=color.gray(.75), radius=.1, axis=dim_x * vec(1, 0, 0))
        pixel_data.append(row)
        cylinder(pos=vec(x - .5, -.5, 0), color=color.gray(.75), radius=.1, axis=dim_y * vec(0, 1, 0))
    cylinder(pos=vec(dim_x - .5, -.5, 0), color=color.gray(.75), radius=.1, axis=dim_y * vec(0, 1, 0))
    cylinder(pos=vec(-.5, dim_y - .5, 0), color=color.gray(.75), radius=.1, axis=dim_x * vec(1, 0, 0))
    return pixel_data


frame_rate = 1
def change_frame_rate(event):
    global  frame_rate
    frame_rate = event.value

display.append_to_caption("\nFrame rate")
_ = slider(min=1, max=100, value=frame_rate, bind=change_frame_rate)

cells = []
for _ in range(dimension_x):
    row = []
    for _ in range(dimension_y):
        row.append(dead_cell() if random() < 0.5 else living_cell())
    cells.append(row)
game = Game(cells)

pixels = create_pixels(dimension_x, dimension_y)
while True:
    rate(frame_rate)
    game = game.next_generation()
    for x in range(len(pixels)):
        for y in range(len(pixels[0])):
            pixels[x][y].visible = game.cell_at(x, y).is_alive()