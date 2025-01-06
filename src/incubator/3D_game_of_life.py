from vpython import *
# https://github.com/johann2357/conways-game-of-life

class Matrix:
    def __init__(self, rows, columns, side):
        self.rows = rows
        self.columns = columns
        self.side = side
        self.alive = color.white
        self.dead = color.black
        self.data = []
        x = self.rows * self.side * -1
        y = self.columns * self.side * -1
        z = 0
        for i in range(0, self.rows):
            self.data.append([])
            for j in range(0, self.columns):
                d = dict(pos=(x+i*self.side, y+j*self.side, z),
                         length=self.side,
                         height=self.side,
                         width=self.side,
                         color=self.dead,
                         opacity=0)
                self.data[i].append(box(**d))
    def set_alive(self, row, column):
        self.data[row][column].color = self.alive
        self.data[row][column].opacity = 1
    def random_matrix(self):
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                if randint(0,19)%3:
                    self.set_alive(i, j)
    def update_box(self, r, c):
        if c == 0:
            left_c = self.columns - 1
        else:
            left_c = c - 1
        if c == self.columns - 1:
            right_c = 0
        else:
            right_c = c + 1
        if r == 0:
            top_r = self.rows - 1
        else:
            top_r = r - 1
        if r == self.rows - 1:
            bottom_r = 0
        else:
            bottom_r = r + 1
        neighbours = 0
        if self.data[top_r][left_c].color == self.alive:
            neighbours += 1
        if self.data[top_r][c].color == self.alive:
            neighbours += 1
        if self.data[top_r][right_c].color == self.alive:
            neighbours += 1
        if self.data[r][left_c].color == self.alive:
            neighbours += 1
        if self.data[r][right_c].color == self.alive:
            neighbours += 1
        if self.data[bottom_r][left_c].color == self.alive:
            neighbours += 1
        if self.data[bottom_r][c].color == self.alive:
            neighbours += 1
        if self.data[bottom_r][right_c].color == self.alive:
            neighbours += 1
        if self.data[r][c].color == self.alive:
            if neighbours < 2 or neighbours > 3:
                return self.dead
            else:
                return self.alive
        else:
            if neighbours == 3:
                return self.alive
            else:
                return self.dead
    def update(self):
        changes = []
        for i in range(0, self.rows):
            changes.append([])
            for j in range(0, self.columns):
                changes[i].append(self.update_box(i, j))
        rate(1.0)
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                if changes[i][j] == self.alive:
                    self.data[i][j].opacity = 1
                else:
                    self.data[i][j].opacity = 0
                self.data[i][j].color = changes[i][j]
        return True
    def run(self):
        while True:
            if self.update():
                print (".")
        return


def main():
    r = 66
    c = 66
    s = 7
    test = Matrix(rows=r, columns=c, side=s)
    test.random_matrix()
    test.run()

if __name__ == "__main__":
    main()