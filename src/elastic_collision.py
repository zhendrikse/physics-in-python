#
# Refactored from Dot Physics
# - https://www.youtube.com/watch?v=g_p-5YfUSnw&t=11s 
# - https://trinket.io/glowscript/c71888ae4a
#

from vpython import vector, color, rate
from ball import Ball     

def main():
    sphere_A = Ball(0.1, vector(-.2, .02 ,0), vector(.2, 0 ,0), 0.05, color.yellow)
    sphere_B = Ball(0.1, vector( .2, .0,  0), vector( 0, 0 ,0), 0.05, color.cyan)

    print("initial momentum = " + str(sphere_A.momentum() + sphere_B.momentum()) + " kg*m/s")
    print("initial kinetic energy = " + str(sphere_A.kinetic_energy() + sphere_B.kinetic_energy()) + " Joules")

    dt = 0.01
    for timestep in range(0, 300):
      rate(100) #  not do any more than 100 loops per second
      force_BA = sphere_A.force_between(sphere_B)
      sphere_A.update(dt, force_BA)
      sphere_B.update(dt, -force_BA)

    print("final momentum = " + str(sphere_A.momentum() + sphere_B.momentum()) + " kg*m/s")
    print("final kinetic energy = " + str(sphere_A.kinetic_energy() + sphere_B.kinetic_energy()) + " Joules")

if __name__=="__main__":
    main()
