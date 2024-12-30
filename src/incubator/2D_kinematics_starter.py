from vpython import scene, arrow, vec, vector, pi, cos, sin, color, arange, curve, text, box, rate


DEG = pi / 180.

#####################################
##
## EDIT KINEMATICS PARAMETERS HERE
##
##
gmag = 10
g = gmag * vec(0, -1, 0)

pos_init = vec(0, 0, 0)
theta_init = 45 * DEG
vel_init = 40.0 * vec(cos(theta_init), sin(theta_init), 0)


def Fnet(t, pos, vel, m):
    Fnet = vec(0, 0, 0)
    return Fnet


#####################################
## GRAPHICS SETUP

scene.width = 1200
scene.height = 800
scene.range = 40
scene.forward = vector(-0.0, -5, -100.)

scene.fullscreen = 1
scene.fov = 1e-14  # pseudo-orthogonal
scene.background = vec(200, 200, 200)

xhat = arrow(axis=vec(1, 0, 0), color=color.red)
yhat = arrow(axis=vec(0, 1, 0), color=color.green)
zhat = arrow(axis=vec(0, 0, 1), color=color.blue)

#####################################
## TRACK SETUP

tracklength = 200
track = box(pos=vec(tracklength / 2, 0, 0), axis=vec(1, 0, 0),
            length=tracklength, height=.005, width=2, color=color.white)

#####################################
## grid
##
for x in arange(0, 1 + tracklength, 10):
    curve(pos=[vec(x, 0, 0), vec(x, 100, 0)])
    text(text="x", pos=vec(x, 0, 0), color=color.black)
for y in arange(0, 1 + 100, 10):
    curve(pos=[vec(0, y, 0), vec(tracklength, y, 0)])
    text(text="y", pos=vec(0, y, 0), color=color.black)

#
# block
#
block_mass = 10
block_size = 1
block_color = color.red

block = box(pos=pos_init, axis=track.axis,
            length=block_size, height=block_size, width=block_size, color=block_color,
            make_trail=True, interval=1)  # trail_type="points", trail_radius=0.01 )
block.mass = block_mass
block.vel = vel_init

scene.camera.follow(block)

# SETUP ANIMATION
#
t = 0.
counter = 0

count_tick = 300  # for ticks at 1-second intervals
dt = 1. / count_tick

scene.waitfor("click ")

print(t, block.pos)
while t < 2 * vel_init.y / gmag:
    rate(100)

    block.acc = Fnet(t, block.pos, block.vel, block.mass) / block.mass
    block.vel += block.acc * dt
    block.pos += block.vel * dt

    t = t + dt
    counter += 1



