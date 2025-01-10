# ------------------------------------------------------------------------------
#
#  This is a simulation of the rotation of a book about its center of mass.
#  The angular velocity vector is evolved in time using Euler's equations
#  for zero torque.  The motion is most interesting when the angular
#  velocity vector is almost, but not exactly, aligned with the principal
#  axis that has the intermediate principal moment (i.e. not the biggest
#  or smallest lambda).  I have set up the default initial conditions to
#  correspond to that situation.  You can verify that this simulation is
#  accurate by trying it with a book!
#
#  The top three sliders in the control panel allow you to adjust the
#  components of the initial angular velocity.
#
#  The bottom slider controls the speed of the animation.
#
#  Owen Long, University of California Riverside
#  February 2013
#
# ------------------------------------------------------------------------------
from __future__ import division, print_function
from vpython import *

scene.title = 'Rigid body rotations simulator'
scene.height = 500
scene.width = 800
scene.center = vector(0, 0, 0)

omegamax = 2.0

# initial values for components of angular velocity vector in body frame.
omega1_0 = omegamax
omega2_0 = 0.005
omega3_0 = 0.000

omega_b = vector(omega1_0, omega2_0, omega3_0)

# start out with body frame and space frame lined up.
omega_s = vector(omega_b)

# setval = 0

paused = 0
slider_max = 100
speed = 50
speed_max = 100

# define the geometry of the rigid object (a physics book)

book_l = 1.5  # length along 1 axis
book_h = 2.0  # length along 2 axis
book_w = 0.3  # length along 3 axis

len1 = book_l
len2 = book_h
len3 = book_w

bookoffset = -2.0
vecoffset = 2.0

# frame_book = frame( pos=vector(bookoffset,0,0) )
#
# book = box(frame=frame_book, pos=vector(0,0,0),
#            height=book_h, length=book_l, width=book_w,
#            color=color.red)
#
# physics_text = text( frame=frame_book, pos=vector(0, 0+book_h/4, book_w/2), \
#                      text="Physics", align='center', height=0.2, depth=0.0001, color=(1,1,0) )
#
# book_text = text( frame=frame_book, pos=vector(0, 0+book_h/9, book_w/2), \
#                      text="Book", align='center', height=0.2, depth=0.0001, color=(1,1,0) )
#

book = box(pos=vector(0, 0, 0),
           height=book_h, length=book_l, width=book_w,
           color=color.red)

physics_text = text(pos=vector(0, 0 + book_h / 4, book_w / 2),
                    text="Physics", align='center', height=0.2, depth=0.0001, color=vector(1, 1, 0))

book_text = text(pos=vector(0, 0 + book_h / 9, book_w / 2),
                 text="Book", align='center', height=0.2, depth=0.0001, color=vector(1, 1, 0))

# define space frame unit vectors

x_hat = vector(1, 0, 0)
y_hat = vector(0, 1, 0)
z_hat = vector(0, 0, 1)

# initialize body frame unit vectors to initially point along space frame unit vectors

e1 = vector(x_hat.x, x_hat.y, x_hat.z)
e2 = vector(x_hat.x, x_hat.y, x_hat.z)
e3 = vector(x_hat.x, x_hat.y, x_hat.z)

label_e1 = label(text='1', opacity=False, box=False, line=False)
label_e2 = label(text='2', opacity=False, box=False, line=False)
label_e3 = label(text='3', opacity=False, box=False, line=False)

mass = 4.0

# compute principal moments of inertia for the book

lambda1 = (mass / 12.0) * (len2 * len2 + len3 * len3)
lambda2 = (mass / 12.0) * (len3 * len3 + len1 * len1)
lambda3 = (mass / 12.0) * (len1 * len1 + len2 * len2)

print('lambda1 = %.2f, lambda2 = %.2f, lambda3 = %.2f' % (lambda1, lambda2, lambda3))

# arrows to indicate body frame unit vectors in the display

arrow_e1 = arrow(pos=vector(vecoffset, 0, 0), axis=e1, color=vector(1, 1, 1), shaftwidth=0.005)
arrow_e2 = arrow(pos=vector(vecoffset, 0, 0), axis=e2, color=vector(1, 1, 1), shaftwidth=0.005)
arrow_e3 = arrow(pos=vector(vecoffset, 0, 0), axis=e3, color=vector(1, 1, 1), shaftwidth=0.005)

# angular momentum vector in the body and space frame

angular_momentum_b = vector(lambda1 * omega_b.x, lambda2 * omega_b.y, lambda3 * omega_b.z)
angular_momentum_s = angular_momentum_b.x * e1 + angular_momentum_b.y * e2 + angular_momentum_b.z * e3

# arrows for angular momentum and angular velocity vectors

arrow_L = arrow(pos=vector(vecoffset, 0, 0), axis=angular_momentum_s, color=vector(0, 0, 1), shaftwidth=0.005)
arrow_omega = arrow(pos=vector(vecoffset, 0, 0), axis=omega_s, color=vector(0, 1, 0), shaftwidth=0.005)

label_L = text(pos=vector(vecoffset, -1.1 * vecoffset, 0), text="Angular Momentum (L)", align='center', height=0.20,
               depth=0.01, color=vector(0, 0, 1))
label_omega = text(pos=vector(vecoffset, -1.3 * vecoffset, 0), text="Angular velocity (Omega)", align='center',
                   height=0.20, depth=0.01, color=vector(0, 1, 0))

##---------------------------------------------------------------------

# This section has all of the control stuff.
# The buttons are self explanatory.
# The top three sliders are for the initial values for the components of the
#    angular velocity vector.
# The bottom slider controls how fast the animation goes.

#c = controls(x=0, y=500, width=200, height=250, range=80)


def set_pause(val):
    global paused
    paused = val
    print('set paused to %d' % (val))


def set_omega1_0():
    global omega1_0
    omega1_0 = slider_omega1_0.value * (omegamax / slider_max)
    print('omega1_0 set to %.3f' % omega1_0)
    if paused == 1:
       reset()


def set_omega2_0():
    global omega2_0
    omega2_0 = slider_omega2_0.value * (omegamax / slider_max)
    print('omega2_0 set to %.3f' % omega2_0)
    if paused == 1:
        reset()


def set_omega3_0():
    global omega3_0
    omega3_0 = slider_omega3_0.value * (omegamax / slider_max)
    print('omega3_0 set to %.3f' % omega3_0)
    if paused == 1:
        reset()


def set_speed():
    global speed
    speed = slider_speed.value * (speed_max / slider_max)
    print('set speed to %.1f' % speed)


def reset():
    global omega_s, omega_b
    global arrow_omega, arrow_L, arrow_e1, arrow_e2, arrow_e3
    # global frame_book
    global e1, e2, e3
    global label_e1, label_e2, label_e3
    omega_s = vector(omega1_0, omega2_0, omega3_0)
    omega_b = omega_s
    arrow_e1.axis = x_hat;
    arrow_e2.axis = y_hat;
    arrow_e3.axis = z_hat;
    e1 = x_hat;
    e2 = y_hat;
    e3 = z_hat;
    angmom_b = vector(lambda1 * omega_b.x, lambda2 * omega_b.y, lambda3 * omega_b.z)
    angmom_s = angmom_b.x * e1 + angmom_b.y * e2 + angmom_b.z * e3
    arrow_L.axis = angmom_s
    arrow_omega.axis = omega_s
    # frame_book.axis = vector(1, 0, 0)
    # frame_book.up = vector(0, 1, 0)
    label_e1.pos = e1 + vector(vecoffset, 0, 0)
    label_e2.pos = e2 + vector(vecoffset, 0, 0)
    label_e3.pos = e3 + vector(vecoffset, 0, 0)

    print(omega_s)


scene.append_to_caption("\n")
button_pause = button(height=20, width=40, text='Pause', bind=lambda: set_pause(1))
button_resume = button(height=20, width=40, text='Resume', bind=lambda: set_pause(0))
button_reset = button(height=20, width=40, text='Reset', bind=reset)

scene.append_to_caption("\n")
slider_omega1_0 = slider(text="Omega 1", bind=set_omega1_0, max=slider_max, value = omega1_0 * slider_max / omegamax)#, width=5, length=50, axis=vec(1, 0, 0))
slider_omega2_0 = slider(text="Omega 2", bind=set_omega2_0, max=slider_max, value = omega2_0 * slider_max / omegamax)#, width=5, length=50, axis=vec(1, 0, 0))
slider_omega3_0 = slider(text="Omega 3", bind=set_omega3_0, max=slider_max, value = omega3_0 * slider_max / omegamax)#, width=5, length=50, axis=vec(1, 0, 0))
scene.append_to_caption("\n")
slider_speed = slider(text="Speed", bind=set_speed, max=slider_max, value = speed * slider_max / speed_max)#, width=5, length=50, axis=vec(1, 0, 0),)

##---------------------------------------------------------------------


t = 0.
count = 1

while t < 1500:

    dt = 0.000003 * speed

    rate(30000)

    if paused == 1:
        print('pause requested')
        while paused == 1:
            rate(50)

    t = t + dt

    # This line is where all the physics is!!!  The Euler Equations for zero torque.
    # Note that this is computed in the body frame.

    omega_b_dot = vector(((lambda2 - lambda3) / lambda1) * omega_b.y * omega_b.z,
                         ((lambda3 - lambda1) / lambda2) * omega_b.y * omega_b.x,
                         ((lambda1 - lambda2) / lambda3) * omega_b.x * omega_b.y)

    omega_b = omega_b + dt * omega_b_dot

    # Translate the omega vector from the body frame to the space frame.
    # The geometry of the drawing in the graphics screen is all done in the space frame.

    omega_s = omega_b.x * e1 + omega_b.y * e2 + omega_b.z * e3

    # evolve the position of the unit vectors for the body frame.

    newe1 = rotate(e1, angle=dt * mag(omega_s), axis=omega_s);
    newe2 = rotate(e2, angle=dt * mag(omega_s), axis=omega_s);
    newe3 = rotate(e3, angle=dt * mag(omega_s), axis=omega_s);

    e1 = newe1
    e2 = newe2
    e3 = newe3

    arrow_e1.axis = e1
    arrow_e2.axis = e2
    arrow_e3.axis = e3

    label_e1.pos = e1 + vector(vecoffset, 0, 0)
    label_e2.pos = e2 + vector(vecoffset, 0, 0)
    label_e3.pos = e3 + vector(vecoffset, 0, 0)

    # evolve the orientation of the book

    book.rotate(axis=omega_s, angle=dt * mag(omega_s))

    # update the angular momentum vector

    angular_momentum_b = vector(lambda1 * omega_b.x, lambda2 * omega_b.y, lambda3 * omega_b.z)
    angular_momentum_s = angular_momentum_b.x * e1 + angular_momentum_b.y * e2 + angular_momentum_b.z * e3

    arrow_L.axis = angular_momentum_s
    arrow_omega.axis = omega_s

    #scene.autoscale = 0

    count = count + 1

#  if ( count % 10000 == 0 ) :
#     print( 'e1 = ')
#     print( e1 )
