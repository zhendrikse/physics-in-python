#Web VPython 3.2

from vpython import canvas, color, sqrt, pi, graph, gvbars, gcurve, cylinder, textures, sphere, vec, simple_sphere, combin, rate, random, slider, box, exp

title = """&#x2022; <a href="https://github.com/zhendrikse/science/blob/main/mathematics/code/galton_board.py">galton_board.py</a> by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a>
&#x2022; The <span style="color: green">green histogram</span> depicts the binomial distribution
&#x2022; The <span style="color: red">red curve</span> represents the Gaussian/normal distribution.

"""

display = canvas(title=title, width=600, height=800, background=color.gray(0.075), center=vec(0, -17, 0), range=15)
num_nails = 10
num_balls = 200


def normal_distribution(x, mu, sigma):
    return 1 / sqrt(2 * pi * sigma * sigma) * exp(-1 * (x - mu) * (x - mu) / (2 * sigma * sigma))


distribution_graph = graph(title="Distribution", background=color.black, width=600)
distribution = gvbars(color=color.yellow, delta=.75)


class GaltonBoard:
    def __init__(self):
        box(pos=vec(0, -17, -.75), width=1, height=num_balls * .185, length=2 * (num_nails + 1.25),
            texture=textures.wood, shininess=0)
        cylinder(pos=vec(- 1 - num_nails, 1, 0), axis=vec(0, -.18 * num_balls, 0), radius=.2,
                 texture=textures.wood)
        cylinder(pos=vec(num_nails + 1, 1, 0), axis=vec(0, -.18 * num_balls, 0), radius=.2,
                 texture=textures.wood)
        cylinder(pos=vec(-num_nails - 1, -.175 * num_balls, 0), axis=vec(22, 0, 0), radius=.2, texture=textures.wood)
        cylinder(pos=vec(-num_nails - 1, 1, 0), axis=vec(22, 0, 0), radius=.2, texture=textures.wood)
        for i in range(0, num_nails):
            cylinder(pos=2 * vec(i + .5 - num_nails / 2, -5, 0), axis=vec(0, -.125 * num_balls, 0), radius=.2,
                     texture=textures.wood)
            for j in range(-i, i + 1, 2):
                sphere(pos=vec(j, -i, 0), radius=.2, color=color.gray(0.75))


frames_per_second = 200
def modify_animiation_speed(event):
    global frames_per_second
    frames_per_second = event.value


display.append_to_caption("\nAnimation speed")
_ = slider(min=50, max=500, value=frames_per_second, bind=modify_animiation_speed)
display.append_to_caption("\n\n")

binomial = gvbars(color=color.green, delta=.25)
num_nails_plus_1 = num_nails + 1
for x in range(1, num_nails_plus_1):
    binomial.plot(pos=(x, num_balls * combin(num_nails_plus_1, x) * .5 ** num_nails_plus_1))

gauss = gcurve(color=color.red)
for x in range(num_nails_plus_1 * 10):
    gauss.plot(.1 * x, num_balls * normal_distribution(.1 * x, .5 * num_nails_plus_1, sqrt(num_nails_plus_1 * .5 * .5)))

#MathJax.Hub.Queue(["Typeset", MathJax.Hub])

galton_board = GaltonBoard()
bins = [0 for _ in range(num_nails_plus_1)]
dy = -0.04
for _ in range(num_balls):
    ball = simple_sphere(pos=vec(0, 1, 0), make_trail=False, color=color.yellow, radius=.3)
    dx = 0
    for step_count in range(1, 25 * (num_nails + 1) + 1):
        rate(frames_per_second)
        ball.pos += vec(dx, dy, 0)
        if step_count % 25 == 0:
            dx = dy if random() <= .5 else -dy

    bins[(int(ball.pos.x) + num_nails) // 2] += 1
    ball.pos.y = bins[(int(ball.pos.x) + num_nails) // 2] / 2 - num_balls * .175

    for x in range(len(bins)):
        distribution.plot(pos=(x + 1, bins[x]))

