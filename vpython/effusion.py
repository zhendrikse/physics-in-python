#Web VPython 3.2

from vpython import canvas, vector, box, color, cylinder, cos, sin, rate, simple_sphere, pi, random, mag2, dot, mag, sqrt

title="""&#x2022; Based on <a href="https://www.glowscript.org/#/user/Brady888/folder/MyPrograms/program/effusion/">this code</a>
&#x2022; See also his <a href="https://www.youtube.com/watch?v=yOiRSSWBVz4">accompanying video</a>

"""

N = 250
m1, size = 4E-3 / 6E23, 31E-12 * 10  # He atom are 10 times bigger for easier collision but not too big for accuracy
m2 = 222E-3 / 6E23

P = 10  # atm
one_third = 1 / 3.
L = ((24.4E-3 / P / 6E23) * 2 * N) ** one_third / 2 + size  # 2L is the cubic container's original length, width, and height
k, T = 1.38E-23, 298.0  # Boltzmann Constant and initial temperature
t, dt = 0, 8E-13
vrms = sqrt(2 * k * 1.5 * T / m1)  # the initial root-mean-square velocity
vrms2 = sqrt(2 * k * 1.5 * T / m2)
box_is_open = 0  # stage number

hole_radius = 3 * size  # the size of the hole


def keyinput(event):
    global box_is_open, t
    next_stage = event.key

    if next_stage == 'o':
        print("open")
        box_is_open = True
        t = 0


# initialization
scene = canvas(width=600, height=600, background=color.gray(0.075), align='left')
scene.bind('keydown', keyinput)
container = box(length=2 * L, height=2 * L, width=2 * L, opacity=0.2, color=color.yellow, pos=vector(-(L + size), 0, 0))

container2 = box(length=2 * L, height=2 * L, width=2 * L, opacity=0.2, color=color.blue, pos=vector(L + size, 0, 0))

a1 = cylinder(pos=vector(0, 0, 0), color=color.black, radius=hole_radius, axis = 0.05 * vector(L, 0, 0))


def af_col_v(M1, M2, v1, v2, x1, x2):
    v1_prime = v1 + 2 * M2 / (M1 + M2) * dot((v2 - v1), (x1 - x2)) / mag2(x1 - x2) * (x1 - x2)
    v2_prime = v2 + 2 * M1 / (M1 + M2) * dot((v1 - v2), (x2 - x1)) / mag2(x2 - x1) * (x2 - x1)
    return v1_prime, v2_prime


#effusion_time = 0

for i in range(15):

    atoms = []  # list to store atoms
    went_out = []

    for i in range(N):
        atom = simple_sphere(pos=vector(-2 * L * random(), 2 * L * random() - L, 2 * L * random() - L), radius=size, color=vector(1, 0, 0))
        ra = pi * random()
        rb = 2 * pi * random()
        atom.v = vrms * vector(sin(ra) * cos(rb), sin(ra) * sin(rb), cos(ra))  # particle initially same speed but random direction
        atoms.append(atom)
        went_out.append(0)

    atoms2 = []
    went_out2 = []

    for i in range(N):
        atom = simple_sphere(pos=vector(2 * L * random(), 2 * L * random() - L, 2 * L * random() - L), radius=size, color=vector(0, 1, 0))
        ra = pi * random()
        rb = 2 * pi * random()
        atom.v = vrms2 * vector(sin(ra) * cos(rb), sin(ra) * sin(rb), cos(ra))  # particle initially same speed but random direction
        atoms2.append(atom)
        went_out2.append(0)

    go_out = 0
    go_out2 = 0
    t = 0
    box_is_open = False
    period = 0
    tratio = 0

    while go_out < 25:
        t += dt
        rate(100000)
        period += 1
        if period == 10:
            box_is_open = True
            t = 0

        for i in range(N):
            atoms[i].pos += atoms[i].v * dt  # to display atoms at new positions
            atoms2[i].pos += atoms2[i].v * dt

        ### find collisions between pairs of atoms, and handle their collisions
        for i in range(N):
            for j in range(i + 1, N):
                if mag(atoms[i].pos - atoms2[j].pos) <= 2 * size and dot((atoms[i].pos - atoms2[j].pos), (atoms[i].v - atoms2[j].v)) <= 0:
                    atoms[i].v, atoms2[j].v = af_col_v(m1, m2, atoms[i].v, atoms2[j].v, atoms[i].pos, atoms2[j].pos)

                if mag(atoms[i].pos - atoms[j].pos) <= 2 * size and dot((atoms[i].pos - atoms[j].pos), (atoms[i].v - atoms[j].v)) <= 0:
                    atoms[i].v, atoms[j].v = af_col_v(m1, m1, atoms[i].v, atoms[j].v, atoms[i].pos, atoms[j].pos)

                if mag(atoms2[i].pos - atoms2[j].pos) <= 2 * size and dot((atoms2[i].pos - atoms2[j].pos), (atoms2[i].v - atoms2[j].v)) <= 0:
                    atoms2[i].v, atoms2[j].v = af_col_v(m2, m2, atoms2[i].v, atoms2[j].v, atoms2[i].pos, atoms2[j].pos)

        # find collisions between the atoms and the walls, and handle their elastic collisions
        for i in range(N):
            if abs(atoms[i].pos.x) <= 2 * size and mag(atoms[i].pos - vector(-2 * size, 0, 0)) < hole_radius and box_is_open:
                if went_out[i] == 0:
                    go_out += 1
                    went_out[i] = 1
            elif abs(atoms[i].pos.x) <= 2 * size and mag(atoms[i].pos - vector(2 * size, 0, 0)) < hole_radius and box_is_open:
                if went_out[i] == 1:
                    go_out -= 1
                    went_out[i] = 0
            elif (abs(atoms[i].pos.x) >= 2 * L or abs(atoms[i].pos.x) <= 2 * size) and (atoms[i].pos.x + L) * atoms[i].v.x > 0 and went_out[i] == 0:
                atoms[i].v.x = - atoms[i].v.x
            elif (abs(atoms[i].pos.x) >= 2 * L or abs(atoms[i].pos.x) <= 2 * size) and (atoms[i].pos.x - L) * atoms[i].v.x > 0 and went_out[i] == 1:
                atoms[i].v.x = - atoms[i].v.x

            if abs(atoms[i].pos.y) >= L - size and atoms[i].pos.y * atoms[i].v.y > 0:
                atoms[i].v.y = - atoms[i].v.y

            if abs(atoms[i].pos.z) >= L - size and atoms[i].pos.z * atoms[i].v.z > 0:
                atoms[i].v.z = - atoms[i].v.z

            ### atom2
            if abs(atoms2[i].pos.x) <= 2 * size and mag(atoms2[i].pos - vector(2 * size, 0, 0)) < hole_radius and box_is_open:
                if went_out2[i] == 0:
                    go_out2 += 1
                    went_out2[i] = 1
            elif abs(atoms2[i].pos.x) <= 2 * size and mag(atoms2[i].pos - vector(-2 * size, 0, 0)) < hole_radius and box_is_open:
                if went_out2[i] == 1:
                    go_out2 -= 1
                    went_out2[i] = 0

            elif (abs(atoms2[i].pos.x) >= 2 * L or abs(atoms2[i].pos.x) <= 2 * size) and (atoms2[i].pos.x - L) * atoms2[i].v.x > 0 and went_out2[i] == 0:
                atoms2[i].v.x = - atoms2[i].v.x
            elif (abs(atoms2[i].pos.x) >= 2 * L or abs(atoms2[i].pos.x) <= 2 * size) and (atoms2[i].pos.x + L) * atoms2[i].v.x > 0 and went_out2[i] == 1:
                atoms2[i].v.x = - atoms2[i].v.x

            if abs(atoms2[i].pos.y) >= L - size and atoms2[i].pos.y * atoms2[i].v.y > 0:
                atoms2[i].v.y = - atoms2[i].v.y

            if abs(atoms2[i].pos.z) >= L - size and atoms2[i].pos.z * atoms2[i].v.z > 0:
                atoms2[i].v.z = - atoms2[i].v.z

    ratio = go_out2 / go_out
    tratio += ratio
    print(ratio)

    for i in range(N):
        atoms[i].visible = False
        atoms2[i].visible = False
print("average ratio")
print(tratio / 15)

