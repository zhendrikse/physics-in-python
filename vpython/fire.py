#Web VPython 3.2
from vpython import vec, box, rate, canvas, color, random

title = """&#x2022; Based on <a href="https://github.com/beltoforion/recreational_mathematics_with_python/blob/master/Fire/fire.py">fire.py</a> from <a href="https://github.com/beltoforion/recreational_mathematics_with_python">Recreational Mathematics with Python</a>
&#x2022; Ported to <a href="https://vpython.org/">VPython</a> by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in <a href="https://github.com/zhendrikse/science/blob/main/fun/code/fire.py">fire.py</a>

"""

dim_x, dim_y = 100, 70
display = canvas(title=title, range=32, background=color.gray(0.075), width=600, height=400, center=.5 * vec(dim_x, dim_y - 4, 0))
#MathJax.Hub.Queue(["Typeset", MathJax.Hub])

def init():
    cells = [[0. for _ in range(dim_y)] for _ in range(dim_x)]
    for c in range(dim_x):
        cells[c][0] = random()

    # create color palette
    p1, p2, p3 = vec(0,0,0), vec(80, 0, 0), vec(255, 255, 128)
    fire_colors = []
    for i in range(256):
        colour = p1 + (p2 - p1) * i / 128 if i < 128 else p2 + (p3 - p2) * (i - 128) / 128
        fire_colors.append(colour / 255)

    return cells, fire_colors


def update(pixels, cells, fire_colors):
    old = [[cells[r][c] for c in range(dim_y)] for r in range(dim_x)]

    for r in range(0, dim_y - 1):
        for c in range(0, dim_x - 1):
            if r == 0 and 5 < c < dim_x - 5:
                cells[c][r] = cells[c][1] + random() * 0.9
            else:
                intensity = 4.1 + 0.3 * (abs(c - dim_x / 2) / (dim_x / 2))
                cells[c][r] = (old[c - 1][r - 1] + old[c][r - 1] + old[c + 1][r - 1] + old[c][r - 2]) / intensity

            val = min(int(255 * cells[c][r - 1]), 255) * (r > 2)
            pixels[c][r].color  = fire_colors[val]


def main():
    pixels = [[box(pos=vec(r, c, 0), shininess=0) for c in range(dim_y)] for r in range(dim_x)]
    cells, fire_colors = init()

    while True:
        rate(60)
        update(pixels, cells, fire_colors)


if __name__ == "__main__":
    main()
