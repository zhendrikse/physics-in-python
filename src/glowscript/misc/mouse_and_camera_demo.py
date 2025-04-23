from vpython import *

#
# Bruce Sherwood, December 2007
# Updated by Zeger Hendrikse: http://github.com/zhendrikse
#

"""
With left mouse button down,
move left or right to look around.
"""
s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
c = len(s)
R = 5
for n in range(c):
    theta = n * 2 * pi / c - pi / 2
    text(pos=vec(R * cos(theta), 0, R * sin(theta)),
         axis=vec(-sin(theta), 0, cos(theta)),
         text=s[n], height=1, depth=0.5,
         color=color.yellow)
camera = vector(0, 0, 0)  # for generality; need not be at origin

# Place center of scene at a distance R from the camera:
animation.center = camera + vector(0, 0, -R)
# Point the camera:
animation.forward = animation.center - camera
# scene.fov is "field of view" in radians. R times the tangent
#  of half the field of view is half of the width of the scene:
animation.range = R * tan(animation.fov / 2)
animation.userspin = False

lastpos = None

def process_mouse_click(down):
    if down:  # and scene.mouse.pos != lastpos:
        lastpos = animation.mouse.pos
        lastpos.y = 0  # force mouse position to have y=0
        # (lastpos-camera) is a vector parallel to screen.
        # (lastpos-camera) cross norm(forward) is a vector in the +y direction,
        #   and this y component of the cross product is proportional to
        #   how far to the right the mouse is (if mouse is to left, this y
        #   component is negative)
        rotation = cross((lastpos - camera), norm(animation.forward))
        # If the mouse is to the right, y component is positive, and we need to
        #   turn the view toward the right, which means rotating the forward
        #   vector toward the right, about the +y axis, which requires a
        #   negative angle (vice versa if mouse is to the left, in which case
        #   the cross product is in the -y direction. The factor of 1/100 was
        #   chosen experimentally as giving an appropriate sensitivity to how
        #   far to the right (or left) the mouse is. Bigger mouse displacement
        #   makes the rotation faster.
        animation.forward = animation.forward.rotate(angle=-rotation.y / 100, axis=vec(0, 1, 0))
        # Move the center of the scene to be a distance R from the camera,
        #   in the direction of forward.
        animation.center = camera + R * norm(animation.forward)

def on_mouse_up():
    process_mouse_click(False)

def on_mouse_down():
    process_mouse_click(True)

animation.bind('mousedown', on_mouse_down)
animation.bind('mouseup', on_mouse_up)

while 1:
    rate(100)
