### doppler-Wavefront.py
### Doppler Effect for Sound (requires VPython)
### Rob Salgado
### salgado@physics.syr.edu     http://physics.syr.edu/~salgado/
###
### v0.5  2007-02-27 tested on Windows XP/TabletPC
###         with Python-2.3.4.exe and VPython-2003-10-15.exe
###
### Updated by Zeger Hendrikse: https://github.com/zhendrikse/physics-in-python/
###

from vpython import *

velocity_source = 0.20  # velocity of the source
velocity_receiver = -0.30  # velocity of the receiver
velocity_wind = 0.10  # velocity of the wind

scene = canvas(x=0, y=0, height=700, width=700)
scene.autoscale = 0

source = sphere(radius=0.2, pos=vector(0, 0, 0), vel=vector(velocity_source, 0, 0), color=color.red)
receiver = sphere(radius=0.2, pos=vector(3, 0, 0), vel=vector(velocity_receiver, 0, 0), color=color.green)


def source_receiver_distance():
    return receiver.pos.x - source.pos.x


def sign_of_source_receiver_distance():
    if source_receiver_distance == 0:
        return 0
    elif source_receiver_distance == abs(source_receiver_distance()):
        return 1
    else:
        return -1


source_receiver_distance_sign = sign_of_source_receiver_distance()

wind_velocity_vector = vector(velocity_wind, 0, 0)

nudge = vector(0, 6, 0)
nudgev = vector(0, 0.5, 0)

velocity_source_arrow = arrow(pos=source.pos + nudge, axis=5 * vector(velocity_source, 0, 0), fixedwidth=1,
                              shaftwidth=0.1, color=source.color)
velocity_receiver_arrow = arrow(pos=receiver.pos + nudge - nudgev, axis=5 * vector(velocity_receiver, 0, 0),
                                fixedwidth=1, shaftwidth=0.1,
                                color=receiver.color)
velocity_wind_arrow = None
if velocity_wind != 0:
    velocity_wind_arrow = arrow(pos=nudge + 2 * vector(0, 1, 0), axis=5 * vector(velocity_wind, 0, 0), fixedwidth=1,
                                shaftwidth=0.1,
                                color=color.cyan)

source_label_text = "velocity=" + str(velocity_source)
velocity_source_label = label(pos=velocity_source_arrow.pos + nudge, text=source_label_text, color=source.color, box=1)
receiver_label_text = "velocity=" + str(velocity_receiver)
velocity_receiver_label = label(pos=velocity_receiver_arrow.pos - nudgev, text=receiver_label_text, color=receiver.color)

if velocity_wind != 0:
    wind_label_text = "wind speed = " + str(velocity_wind)
    velocity_wind_label = label(pos=velocity_wind_arrow.pos + vector(0, 1, 0), text=wind_label_text,
                                color=velocity_wind_arrow.color)

tmax = 12.0
dt = 0.005
twopi = 2 * pi
N = 32

ball = []
ball0flag = []
source_label = []
received_label = []


def new_wave(t):
    ball0flag.append(0)
    sphere(radius=0.05, pos=source.pos, color=vec(.5, 0, 0))
    sphere(radius=0.05, pos=receiver.pos, color=vec(0, .5, 0))

    for j in range(0, N):
        theta = twopi * j / float(N)
        ball.append(sphere(radius=0.1, pos=source.pos, vel=vector(cos(theta), sin(theta), 0)))

    source_label_text = "time = " + str(round(t, 2))
    source_label.append(label(pos=ball[int(N * (len(ball0flag) - 1) + 3 * N / 4)].pos, text=source_label_text,
                              color=source.color, linecolor=source.color))


def meeting(t):
    global source_receiver_distance_sign
    label_text = "time = " + str(round(t, 2))
    label(pos=source.pos + nudge - nudgev / 2.0, text=label_text,
          color=color.white, linecolor=color.white)
    print(label_text)
    source_receiver_distance_sign = 2


def on_mouse_click():
    # newPick = scene.mouse(pick=sphere)
    newPick = scene.mouse.project(normal=vec(0, 1, 0), point=vec(0, 2, 0))
    if not newPick is None:
        #temp_color = newPick.color
        #newPick.color = color.yellow
        # pick_r=newPick.x*4.
        # string= "r=%7.5f" % pick_r
        # label(pos=newPick.pos,text=string,xoffset=-5,yoffset=5)

        target = newPick
        step = (target - scene.center) / 20.
        for i in arange(1, 20, 1):
            rate(10)
            scene.center += step
            scene.range /= 1.037  # (1.037**19=1.99)
        #newPick.color = temp_color


scene.bind('click', on_mouse_click)

# Now... WHEN AN OBJECT IS PICKED,
# TRANSLATE THE scene.center TO THE OBJECT'S POSITION, THEN ZOOM
while True:
    rate(100)
    print("successive wavefronts received at time...")
    new_wave(0)
    told = 0
    # clock=label()
    for t in arange(0, tmax + dt, dt):
        rate(100)

        #    clock.text="%f" % (t%1.0)
        if t % 1.0 < told % 1.0:
            print("t=" + str(round(t, 2)) + ", len=" + str(len(ball)))
            new_wave(t)

        told = t

        if source_receiver_distance_sign == 0:
            if abs(source_receiver_distance()) > 0: meeting(t)
        elif source_receiver_distance_sign == 1:
            if source_receiver_distance() <= 0: meeting(t)
        elif source_receiver_distance_sign == -1:
            if source_receiver_distance() >= 0: meeting(t)

        for i in arange(len(ball)):
            ball[i].pos += (ball[i].vel + wind_velocity_vector) * dt
        source.pos += source.vel * dt
        receiver.pos += receiver.vel * dt

        velocity_source_arrow.pos = source.pos + nudge
        velocity_receiver_arrow.pos = receiver.pos + nudge - nudgev

        velocity_source_label.pos = velocity_source_arrow.pos + nudgev
        velocity_receiver_label.pos = velocity_receiver_arrow.pos - nudgev

        for j in arange(len(ball0flag)):
            source_label[j].pos = ball[int(N * j + 3 * N / 4)].pos
            if ball0flag[j] == 0 and((source.pos.x <= receiver.pos.x <= ball[N * j].pos.x) or (source.pos.x >= receiver.pos.x > ball[int(N * j + N / 2)].pos.x)):
                ball0flag[j] = 1
                print("t=" + str(round(t, 2)))
                new_label_text = "t=" + str(round(t, 2))
                received_label.append(label(pos=ball[int(N * j + (N - 3))].pos, text=new_label_text,
                                            color=receiver.color, linecolor=receiver.color))
            elif ball0flag[j] == 1:
                received_label[j].pos = ball[N * j + (N - 3)].pos
