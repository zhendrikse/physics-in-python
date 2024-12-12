from vpython import vector, cos, sin, cylinder, sphere, box, color, rate, scene
#
# https://www.leonhostetler.com/blog/newtons-cradle-in-visual-python-201702/
#
#
# https://www.leonhostetler.com/blog/newtons-cradle-in-visual-python-201702/
#

# Constants
g = 9.80            # (m/s^2)
L = 10              # Length of the pendulums (m)
theta_0 = 1.2       # In radians
        
#scene = canvas(width=400, height=300, align='top')
scene.caption = "\\( \\theta(t)=\\theta_0 \\cos \\bigg( \\sqrt{  \\dfrac {g} {L}} t \\bigg) \\)"
MathJax.Hub.Queue(["Typeset", MathJax.Hub])
 
# Create the pendulum bob and rod
ceiling = box(pos=vector(-4, 0, 0), size=vector(20, 1, 4), color=color.green)

balls = [sphere(pos=vector(0*-2 +L* sin(theta_0), -L* cos(theta_0), 0), radius=1, color=color.yellow)]
rods = [cylinder(pos=vector(0*-2, 0, 0), axis=vector(balls[0].pos.x, balls[0].pos.y, 0), radius=0.1)]

for i in range(1, 5):
  balls.append(sphere(pos=vector(i*-2, -L, 0), radius=1, color=color.red))
  rods.append(cylinder(pos=vector(i*-2, 0, 0), axis=vector(balls[i].pos.x+i*2,balls[i].pos.y, 0), radius=0.1))
  
  
def position(right, t):
    """
    Only one of the pendulums is in motion at a given time. This function
    moves the moving pendulum to its new position. We use the equation:
        theta(t) = theta_0*cos(sqrt(g/L)*t)
    """
    theta = theta_0 * cos(sqrt(g/L) * t)
 
    if right:
        # Update position of bob
        balls[0].pos = vector(L * sin(theta), -L * cos(theta), 0)
        balls[0].color = color.yellow
        balls[4].color = color.red
        # Update rod's position
        rods[0].axis = vector(balls[0].pos.x, balls[0].pos.y, 0)  
        
    else:
        # Update position of bob
        balls[4].pos = vector(L * sin(theta) - 4 * 2, -L * cos(theta), 0)
        balls[0].color = color.red
        balls[4].color = color.yellow
        # Update rod's posistion
        rods[4].axis = vector(balls[4].pos.x + 4 * 2, balls[4].pos.y, 0)  
 
    # Once the moving pendulum reaches theta = 0, switch to the other one
    if theta <= 0:
        return False  # Return
    else:
        return True
 
t = 0
dt = 0.01
right = True  # The right pendulum is the first in motion
while True:
    rate(200)
    right = position(right, t)
    t += dt