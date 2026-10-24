# Web VPython 3.2

from vpython import curve, color, vec, canvas, rate, radio

title = """&#x2022; Inspired by <a href="https://isoptera.lcsc.edu/~seth/cs111/project5.pdf">a student assignment</a> by <a href="https://isoptera.lcsc.edu/~seth/">S. Seth Long</a> 
&#x2022; Written by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in <a href="https://github.com/zhendrikse/science/blob/main/mathematics/code/sierpinski.py">sierpinski.py</a>

"""

display = canvas(title=title, width=600, height=600, background=color.gray(0.075), range=1.25)
display.range = 1.4
display.forward = vec(-.8, .22, -.51)
display.center = vec(.07, -.23, -.05)


def colour(vertex_):
    return color.hsv_to_rgb(vec(.25 * (1 + vertex_.y), 1, 1))


def sierpinski_pyramid(vertices, level):
    if level == 0:
        pyramid(vertices)
    else:
        midpoints = [
            (vertices[0] + vertices[4]) / 2,
            (vertices[1] + vertices[4]) / 2,
            (vertices[2] + vertices[4]) / 2,
            (vertices[3] + vertices[4]) / 2,
            (vertices[0] + vertices[1]) / 2,
            (vertices[1] + vertices[2]) / 2,
            (vertices[2] + vertices[3]) / 2,
            (vertices[3] + vertices[0]) / 2,
            (vertices[2] + vertices[0]) / 2,
        ]

        sierpinski_pyramid([vertices[0], midpoints[4], midpoints[8], midpoints[7], midpoints[0]], level - 1)
        sierpinski_pyramid([midpoints[4], vertices[1], midpoints[5], midpoints[8], midpoints[1]], level - 1)
        sierpinski_pyramid([midpoints[8], midpoints[5], vertices[2], midpoints[6], midpoints[2]], level - 1)
        sierpinski_pyramid([midpoints[7], midpoints[8], midpoints[6], vertices[3], midpoints[3]], level - 1)
        sierpinski_pyramid([midpoints[0], midpoints[1], midpoints[2], midpoints[3], vertices[4]], level - 1)


def sierpinski_tetrahedron(vertices, level):
    if level == 0:
        tetrahedron(vertices)
    else:
        midpoints = [
            (vertices[0] + vertices[1]) / 2,
            (vertices[1] + vertices[2]) / 2,
            (vertices[2] + vertices[0]) / 2,
            (vertices[0] + vertices[3]) / 2,
            (vertices[1] + vertices[3]) / 2,
            (vertices[2] + vertices[3]) / 2
        ]

        sierpinski_tetrahedron([vertices[0], midpoints[0], midpoints[2], midpoints[3]], level - 1)
        sierpinski_tetrahedron([midpoints[0], vertices[1], midpoints[1], midpoints[4]], level - 1)
        sierpinski_tetrahedron([midpoints[2], midpoints[1], vertices[2], midpoints[5]], level - 1)
        sierpinski_tetrahedron([midpoints[3], midpoints[4], midpoints[5], vertices[3]], level - 1)


def tetrahedron(vertices):
    curve(pos=[vertices[0], vertices[1]], color=colour(vertices[0]), radius=0.0055)
    curve(pos=[vertices[0], vertices[2]], color=colour(vertices[0]), radius=0.0055)
    curve(pos=[vertices[0], vertices[3]], color=colour(vertices[0]), radius=0.0055)
    curve(pos=[vertices[1], vertices[2], vertices[3], vertices[1]], color=colour(vertices[0]), radius=0.0055)


def pyramid(vertices):
    curve(pos=[vertices[0], vertices[4]], color=colour(vertices[0]), radius=0.0055)
    curve(pos=[vertices[1], vertices[4]], color=colour(vertices[0]), radius=0.0055)
    curve(pos=[vertices[2], vertices[4]], color=colour(vertices[0]), radius=0.0055)
    curve(pos=[vertices[3], vertices[4]], color=colour(vertices[0]), radius=0.0055)
    curve(pos=[vertices[0], vertices[1], vertices[2], vertices[3], vertices[0]], color=colour(vertices[0]),
          radius=0.0055)


initial_tetrahedron = [
    vec(0, 1, 0),
    vec(-1, -1, -1),
    vec(1, -1, -1),
    vec(0, -1, 1)
]

initial_pyramid = [
    vec(-1, -1, -1),
    vec(1, -1, -1),
    vec(1, -1, 1),
    vec(-1, -1, 1),
    vec(0, 1, 0)
]


def clear_canvas():
    for obj in display.objects:
        obj.visible = False


def toggle_pyramids(event):
    clear_canvas()
    if event.name == "tetrahedron":
        sierpinski_tetrahedron(initial_tetrahedron, 5)
        pyramid_radio.checked = False
        display.range = 1.25
        display.forward = forward = vec(-.4, .25, -.85)
        display.center = vec(.07, -.23, -.05)
    else:
        sierpinski_pyramid(initial_pyramid, 5)
        tetrahedron_radio.checked = False
        display.range = 1.4
        display.forward = vec(-.8, .22, -.51)
        display.center = vec(.07, -.23, -.05)


display.append_to_caption("\n")
pyramid_radio = radio(text="Pyramids ", checked=True, name="pyramids", bind=toggle_pyramids)
tetrahedron_radio = radio(text="Tetrahedron ", checked=False, name="tetrahedron", bind=toggle_pyramids)

sierpinski_pyramid(initial_pyramid, 5)

while True:
    rate(1)


