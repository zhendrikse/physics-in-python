#Web VPython 3.2

from vpython import canvas, vec, color, rate, box

title = """&#x2022; Based on <a href="https://github.com/jeffvun/fractals/blob/main/MengerSponge.py">MengerSponge.py</a> code 
&#x2022; Modified by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in <a href="https://github.com/zhendrikse/science/blob/main/mathematics/code/menger_sponge.py">menger_sponge.py</a>

"""

final_size = 200
display = canvas(background=color.gray(0.075), width=600, height=600, forward=vec(-.56, -.51, -.64),
                 center=vec(0, -40, 0), range=final_size, title=title)

def menger_sponge(pos, size, depth):
    if depth == 0:
        box(pos=pos, length=size, height=size, width=size, color=color.hsv_to_rgb(vec(.215 + pos.y / 600, 1, 1)))
    else:
        # Divide the box into 27 smaller cubes
        new_size = size / 3
        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    if abs(x) + abs(y) + abs(z) > 1:
                        new_pos = vec(pos.x + x * new_size, pos.y + y * new_size, pos.z + z * new_size)
                        menger_sponge(new_pos, new_size, depth - 1)


# Generate the Menger sponge
menger_sponge(pos=vec(0, 0, 0), size=final_size, depth=4)

while True:
    rate(1)
