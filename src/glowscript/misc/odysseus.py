# Web VPython 3.2

from vpython import *

title = """Odysseus

&#x2022; <a href="https://glowscript.org/#/user/X9Z3/folder/X9Z3Publications/program/Odysseus">Original version</a> created by Maximillian DeMarr
&#x2022; Maintained by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>
&#x2022; Pan around by holding shift, left-clicking, and dragging.
&#x2022; Reset the scene by reloading the browser. 
&#x2022; Click mouse button to pause

"""
animation = canvas(width=1300, height=600, title=title, autoscale=False)

body_color = vec(230, 184, 99) / 255
brown_color = vec(122, 90, 37) / 255
iron_color = vec(66, 64, 61) / 255
bow_color = vec(252, 163, 28) / 255


class Odysseus:
    def __init__(self, position=vec(0, 0, 0)):
        self._position = position
        self._head(position)
        self._torso(position)
        self._left_arm(position)
        self._right_arm(position)
        self._left_leg(position)
        self._right_leg(position)

    def _head(self, position):
        sphere(pos=position + vector(0, 1.5, 0), color=body_color, size=.4 * vector(2, 2, 1))
        sphere(pos=position + vector(0, 1, 0), color=body_color, size=.2 * vector(2, 2, 1))

    def _left_leg(self, position):
        cylinder(pos=position + vec(0.183159, -1.09949, 0), color=body_color, size=vec(1.4, 0.6, 0.6),
                 axis=vec(1.0209, -1.12299, 0))  # Thigh
        sphere(pos=position + vec(1.1, -2.12063, 0), color=body_color, size=vec(0.6, 0.6, 0.6),
               axis=vec(0.440081, -0.512465, 0))  # Knee (near thigh)
        sphere(pos=position + vec(1.14938, -2.19989, 0), color=body_color, size=vec(0.53, 0.53, 0.53),
               axis=vec(0.440081, -0.512465, 0))  # Knee (near shin)
        cylinder(pos=position + vec(1.14389, -2.15271, 0), color=body_color, size=vec(1.2, 0.4, 0.4),
                 axis=vec(0.349075, -1.31097, 0))  # Shin

        sphere(pos=position + vec(1.45596, -3.31786, 0), color=body_color, size=vec(0.4, 0.4, 0.4),
               axis=vec(0.440081, -0.512465, 0))  # Ankle
        sphere(pos=position + vec(1.5014, -3.51345, 0), color=body_color, size=vec(0.4, 0.4, 0.3),
               axis=vec(0.440081, -0.512465, 0))  # Heel
        sphere(pos=position + vec(1.70688, -3.59053, 0), color=body_color, size=vec(0.8, 0.2, 0.4),
               axis=vec(1.35176, -0.0875508, 0))  # Foot

    def _right_leg(self, position):
        cylinder(pos=position + vec(-0.229185, -1.11047, 0), color=body_color, size=vec(1.4, 0.6, 0.6),
                 axis=vec(-0.427335, -1.16334, 0))  # Thigh
        sphere(pos=position + vec(-0.730757, -2.44792, 0), color=body_color, size=vec(0.6, 0.6, 0.6),
               axis=vec(0.440081, -0.512465, 0))  # Knee (near thigh)
        sphere(pos=position + vec(-0.805473, -2.60348, 0), color=body_color, size=vec(0.51, 0.51, 0.51),
               axis=vec(0.440081, -0.512465, 0))  # Knee (near shin)
        cylinder(pos=position + vec(-0.806256, -2.66083, 0), color=body_color, size=vec(1.2, 0.4, 0.4),
                 axis=vec(-0.321837, -3.26105, 0))  # Shin

        sphere(pos=position + vec(-0.922794, -3.87687, 0), color=body_color, size=vec(0.4, 0.4, 0.4),
               axis=vec(0.440081, -0.512465, 0))  # Ankle
        s1 = sphere(pos=position + vec(-0.976689, -4.02122, 0), color=body_color, size=vec(0.4, 0.4, 0.3),
                    axis=vec(0.220041, -0.512465, 0))  # Heel
        s2 = sphere(pos=position + vec(-1.22013, -4.10062, 0), color=body_color, size=vec(0.8, 0.2, 0.4),
                    axis=vec(-1.33548, -0.419258, 0))  # Foot
        s1.rotate(axis=vec(0, 1, 0), angle=pi / 3, origin=position + vec(-0.972794, -3.87687, 0))
        s2.rotate(axis=vec(0, 1, 0), angle=pi / 3, origin=position + vec(-0.972794, -3.87687, 0))

    def _torso(self, position):
        sphere(pos=position + vec(-0.41933, 0.54241, 0), color=body_color, size=vec(0.943888, 0.315041, 0.335041),
               axis=vec(-0.315041, 0.943888, 0))  # Latissimus Dorsi right
        sphere(pos=position + vec(0.41933, 0.54241, 0), color=body_color, size=vec(0.943888, 0.315041, 0.335041),
               axis=vec(0.315041, 0.943888, 0))  # Latissimus Dorsi left

        cylinder(pos=position + vec(0, -1, 0), color=body_color, size=vec(2, 1, 0.7), axis=vec(0, 1, 0),
                 texture={'file': textures.wood_old}, shininess=0)  # Chest/Stomach
        cone(pos=position + vec(0.1231916, -1.69299, 0), color=body_color, size=vec(2, 2, 1.1),
             axis=vec(-0.1347874, 1.28713, 0), radius=3,
             texture={'file': textures.wood_old}, shininess=0)  # Waist

    def _left_arm(self, position):
        sphere(pos=position + vec(0.440306, 0.930325, 0), color=body_color, size=vec(0.49, 0.28, 0.4))  # Shoulder
        cylinder(pos=position + vec(0.517094, 0.833352, 0), color=body_color, size=vec(1.2, 0.3, 0.3),
                 axis=vec(1.8, -0.0215945, 0))  # Bicep skeletal
        sphere(pos=position + vec(1.1068, 0.835039, 0), color=body_color, size=vec(1, 0.4, 0.3),
               axis=vec(1.8, -0.0215945, 0))  # Bicep muscular
        sphere(pos=position + vec(1.717094, 0.8147575, 0), color=body_color, size=vec(0.3, 0.3, 0.3),
               axis=vec(1, 0, 0))  # Bicep/Forearm joint
        cylinder(pos=position + vec(1.71878, 0.826082, 0), color=body_color, size=vec(1.1, 0.3, 0.3),
                 axis=vec(1.51893, 0.179873, 0))  # Forearm
        sphere(pos=position + vec(2.80094, 0.959798, 0), color=body_color, size=vec(0.3, 0.3, 0.3),
               axis=vec(1, 0, 0))  # Wrist

        sphere(pos=position + vec(3.0124, 0.980891, 0), color=body_color, size=vec(0.5, 0.28, 0.19),
               axis=vec(1, 0, 0))  # Hand

    def _right_arm(self, position):
        sphere(pos=position + vec(-0.557351, 0.968201, 0), color=body_color, size=vec(0.49, 0.28, 0.4),
               axis=vec(-1.6466, 0.281491, 0))  # Shoulder
        cylinder(pos=position + vec(-0.519632, 0.912688, 0), color=body_color, size=vec(1.2, 0.3, 0.3),
                 axis=vec(-1.14586, 0.203013, 0))  # Bicep skeletal
        sphere(pos=position + vec(-1.14798, 1.00883, 0), color=body_color, size=vec(1, 0.4, 0.3),
               axis=vec(-1.14586, 0.203013, 0))  # Bicep muscular
        sphere(pos=position + vec(-1.7308, 1.11911, 0), color=body_color, size=vec(0.27, 0.28, 0.28),
               axis=vec(1, 0, 0))  # Bicep/Forearm joint
        cylinder(pos=position + vec(-1.7024, 1.11155, 0), color=body_color, size=vec(1.2, 0.3, 0.3),
                 axis=vec(1.07406, 0.313257, 0.313257))  # Forearm
        sphere(pos=position + vec(-0.6175994, 1.424807, 0.313257), color=body_color, size=vec(0.3, 0.3, 0.3),
               axis=vec(1, 0, 0))  # Wrist

        sphere(pos=position + vec(-0.408753, 1.47742, 0.408753), color=body_color, size=vec(0.5, 0.28, 0.19),
               axis=vec(1, 0, 0))  # Hand

    def position(self):
        return self._position


class Bow:
    def __init__(self, position):
        bpath = paths.arc(angle1=pi / 3, angle2=2.9 * pi / 3)
        bow = extrusion(shape=shapes.circle(radius=0.08, np=60, pos=[4, 0]), path=bpath, color=bow_color)
        bow.rotate(axis=vec(1, 0, 1.1), angle=pi / 2, origin=vec(0, 0, 0))
        bow.rotate(axis=vec(0, 1, 0), angle=-2.2 * pi / 3, origin=vec(0, 0, 0))
        bow.pos = position + vec(1.5124, 0.980891, 0.15)


class Axes:
    def __init__(self, position):
        hpath = paths.arc(angle1=2 * pi / 3, angle2=pi / 3)
        wedge = extrusion(shape=shapes.circle(radius=1.3, np=60, angle1=radians(10), angle2=radians(-10), pos=[-2, 0]),
                          path=hpath, color=iron_color)
        mount1 = cylinder(pos=vec(0, 0.25, 0), axis=vec(3, 0.8, 0), radius=0.1, length=1, color=brown_color)
        mount2 = cylinder(pos=vec(0, -0.25, 0), axis=vec(3, -0.8, 0), radius=0.1, length=1, color=brown_color)
        wedge.rotate(axis=vec(0, 0, 1), angle=pi / 2, origin=vec(0, 0, 0))
        wedge.rotate(axis=vec(0, 1, 0), angle=-pi / 2, origin=vec(0, 0, 0))
        wedge.pos = vec(1.41, 0.0129647, 0)
        shaft = cylinder(pos=vec(0, -4, 0), axis=vec(0, 1, 0), radius=0.14, length=4.4, color=brown_color)

        axes = [compound([wedge, mount1, mount2, shaft], pos=vec(0.52, -1.5, 0)) for _ in range(12)]
        for axe in axes:
            axe.rotate(axis=vec(0, 1, 0), angle=-pi / 2, origin=vec(1, 0, 0))

        axes[0].pos = vec(10, 0, 0, )
        axes[1].pos = vec(11, 0, -1.1)
        axes[2].pos = vec(12, 0, 0, )
        axes[3].pos = vec(13, 0, -1.1)
        axes[4].pos = vec(14, 0, 0, )
        axes[5].pos = vec(15, 0, -1.1)
        axes[6].pos = vec(16, 0, 0, )
        axes[7].pos = vec(17, 0, -1.1)
        axes[8].pos = vec(18, 0, 0, )
        axes[9].pos = vec(19, 0, -1.1)
        axes[10].pos = vec(20, 0, 0, )
        axes[11].pos = vec(21, 0, -1.1)

        _ = compound(axes, pos=position)


axes = Axes(vec(15.5, 0, 0.4))
odysseus = Odysseus(vec(-15, 0, 0))
his_bow = Bow(odysseus.position())
his_arrow = arrow(pos=odysseus.position() + vec(-0.408753, 1.47742, 0.408753), axis=vec(4, 0, 0), color=color.yellow,
                  shaftwidth=0.05, round=True, emissive=True)

running = True


def on_mouse_click(r):  # Pauses the sim.
    global running
    running = not running


animation.bind("mousedown", on_mouse_click)

last_pos = vec(0, 0, 0)
dt = 0.01
t = 0
while True:
    rate(30)
    if not running:
        continue
    if t > 1:
        his_arrow.pos += vec(0.1, 0, 0)
    t += dt
#    myevt = animation.waitfor('click')
#    mpos = animation.mouse.project( normal=vec(0,0,1), point=vec(0,2,0))
#    print_options(clear=True)
#    sphere(pos=mpos, radius=0.05, color=color.green)
#    print("Pos:", last_pos)
#    print("Axis:", mpos-last_pos)
#    a.pos=last_pos
#    a.axis=mpos-last_pos
#    last_pos = mpos