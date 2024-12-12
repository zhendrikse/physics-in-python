from vpython import vector, cos, sin, cylinder, sphere, box, color, rate
#
# https://www.leonhostetler.com/blog/newtons-cradle-in-visual-python-201702/
#

# Constants
g = 9.80            # (m/s^2)
L = 10              # Length of the pendulums (m)
initialAngle = 1.2  # In radians
 
 
# Create the pendulum bob and rod
ceiling = box(pos=vector(0, 0, 0), size=vector(20, 1, 4), color=color.green)
pend = sphere(pos=vector(L* sin(initialAngle), -L* cos(initialAngle), 0), radius=1, color=color.yellow)
rod = cylinder(pos=vector(0, 0, 0), axis=vector(pend.pos.x, pend.pos.y, 0), radius=0.1)
pend2 = sphere(pos=vector(-2, -L, 0), radius=1, color=color.red)
rod2 = cylinder(pos=vector(-2, 0, 0), axis=vector(pend2.pos.x+2, pend2.pos.y, 0), radius=0.1)
 
 
def position(right, t):
    """
    Only one of the pendulums is in motion at a given time. This function
    moves the moving pendulum to its new position. We use the equation:
        theta(t) = theta_0*cos(sqrt(g/L)*t)
    """
    theta = initialAngle * cos((g/L)**(1/2)*t)
 
    if right:
        # Update position of bob
        pend.pos = vector(L * sin(theta), -L * cos(theta), 0)  
        # Update rod's position
        rod.axis = vector(pend.pos.x, pend.pos.y, 0)  
        
    else:
        # Update position of bob
        pend2.pos = vector(L * sin(theta) - 2, -L * cos(theta), 0)
        # Update rod's position
        rod2.axis = vector(pend2.pos.x + 2, pend2.pos.y, 0)  
 
    # Once the moving pendulum reaches theta = 0, switch to the other one
    if theta <= 0:
        return False  # Return
    else:
        return True
 
# Increment time
i = 0
right = True  # The right pendulum is the first in motion
while True:
    rate(200)
    right = position(right, i)
    i += 0.01