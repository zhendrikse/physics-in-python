from vpython import canvas, arrow, vec, vector, pi, cos, sin, color, arange, curve, text, box, rate, radians

gmag = 10
g = gmag * vec(0, -1, 0)

pos_init = vec(0, 0, 0)
theta_init = radians(45)
vel_init = 40.0 * vec(cos(theta_init), sin(theta_init), 0)
tracklength = 200

# x_hat = arrow(axis=vec(1, 0, 0), color=color.red)
# y_hat = arrow(axis=vec(0, 1, 0), color=color.green)
# z_hat = arrow(axis=vec(0, 0, 1), color=color.blue)

class Mesh:
    def __init__(self, size=100):
        for x in arange(0, 1 + tracklength, 10):
            curve(pos=[vec(x, 0, 0), vec(x, size, 0)])
            text(text="x", pos=vec(x, 0, 0), color=color.black)
        for y in arange(0, 1 + size, 10):
            curve(pos=[vec(0, y, 0), vec(tracklength, y, 0)])
            text(text="y", pos=vec(0, y, 0), color=color.black)

def Fnet(t, pos, vel, m):
    Fnet = vec(0, 0, 0)
    return Fnet

animation = canvas(fov=1e-14, fullscreen=1, width = 1200, height = 800, range = 40, forward = vector(-0.0, -5, -100.), background=vec(200, 200, 200))

track = box(pos=vec(tracklength / 2, 0, 0), axis=vec(1, 0, 0), length=tracklength, height=.005, width=2, color=color.white)
block_color = color.red

grid = Mesh()
block_mass = 10
block_size = 1
block = box(mass=block_mass, vel=vel_init, pos=pos_init, axis=track.axis,
            length=block_size, height=block_size, width=block_size, color=block_color,
            make_trail=True, interval=1)  # trail_type="points", trail_radius=0.01 )
block.mass = block_mass

animation.camera.follow(block)

t = 0.
counter = 0
count_tick = 300  # for ticks at 1-second intervals
dt = 1. / count_tick

animation.waitfor("click ")
while t < 2 * vel_init.y / gmag:
    rate(100)

    block.acc = Fnet(t, block.pos, block.vel, block.mass) / block.mass
    block.vel += block.acc * dt
    block.pos += block.vel * dt

    t += dt
    counter += 1



