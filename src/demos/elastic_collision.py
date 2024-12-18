#
# Refactored from Dot Physics
# - https://www.youtube.com/watch?v=g_p-5YfUSnw&t=11s 
# - https://trinket.io/glowscript/c71888ae4a
#

from vpython import vector, color, rate
from toolbox.ball import Ball


def main():
    sphere_a = Ball(0.1, vector(-.2, .02, 0), vector(.2, 0, 0), 0.05, color.yellow, make_trail=True)
    sphere_b = Ball(0.1, vector(.2, .0, 0), vector(0, 0, 0), 0.05, color.cyan, make_trail=True)

    print("initial momentum = " + str(sphere_a.momentum + sphere_b.momentum) + " kg*m/s")
    print("initial kinetic energy = " + str(sphere_a.kinetic_energy + sphere_b.kinetic_energy) + " Joules")

    dt = 0.01
    for timestep in range(0, 300):
        rate(100)  # not do any more than 100 loops per second
        force_ba = sphere_a.force_between(sphere_b)
        sphere_a.move(force_ba, dt)
        sphere_b.move(-force_ba, dt)

    print("final momentum = " + str(sphere_a.momentum + sphere_b.momentum) + " kg*m/s")
    print("final kinetic energy = " + str(sphere_a.kinetic_energy + sphere_b.kinetic_energy) + " Joules")


if __name__ == "__main__":
    main()
