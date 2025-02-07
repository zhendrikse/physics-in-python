#########################################################################################
#                                                                                       #
#  Name:                                                                                #
#                                                                                       #
#    Breakout3D.py                                                                      #
#                                                                                       #
#  Description:                                                                         #
#                                                                                       #
#    A 3D version of Breakout (requires red/cyan glasses). Black out the bricks on 4    #
#    walls to win.                                                                      #
#                                                                                       #
#  Options:                                                                             #
#                                                                                       #
#    Change the following variables in the code to modify the game                      #
#                                                                                       #
#    NO_LOSE_MODE = False            #set True to make floor solid (self play mode)     #
#    SHOW_TRAIL   = True             #set True to make ball leave temporary trail       #
#    SHOW_COORDS  = False            #set True to display ball coordinates              #
#                                                                                       #
#  Future:                                                                              #
#                                                                                       #
#    Randomize start velocity on ball launch                                            #
#    Allow above options to be specified on the command line                            #
#    Change velocity vector depending on what part of the paddle is hit.                #
#    Add shadow as training aid                                                         #
#                                                                                       #
#  Audit:                                                                               #
#                                                                                       #
#    2011-09-05  added NO_LOSE_MODE, SHOW_TRAIL & SHOW_COORDS options                   #
#                change ball radius based on z coordinate to improve depth perception   #
#                ball is red if coming at you, green if going away                      #
#    2011-09-04  R J de Graff original code                                             #
#                                                                                       #
#########################################################################################

from vpython import *

#
# https://www.daniweb.com/programming/software-development/code/380901/breakout-3d-sample-vpython-app
#


def SideBrick(bricks, y, z):  # check if a left or right side brick was hit

    halfy = bricks[0].height / 2
    halfz = bricks[0].width / 2

    for brick in bricks:
        if brick.visible:
            if brick.y - halfy <= y <= brick.y + halfy and brick.z - halfz <= z <= brick.z + halfz:
                return True, brick
    return False, ""


def TopBrick(bricks, x, z):  # check if a top brick was hit

    halfx = bricks[0].width / 2
    halfz = bricks[0].length / 2

    for brick in bricks:
        if brick.visible:
            if brick.x - halfx <= x <= brick.x + halfx and brick.z - halfz <= z <= brick.z + halfz:
                return True, brick
    return False, ""


def BackBrick(bricks, x, y):  # check if a back brick was hit

    halfx = bricks[0].length / 2
    halfy = bricks[0].height / 2

    for brick in bricks:
        if brick.visible:
            if brick.x - halfx <= x <= brick.x + halfx and brick.y - halfy <= y <= brick.y + halfy:
                return True, brick
    return False, ""


def UpdateStatus(status, numballs, numbricks):
    status.text = "Balls=%d  Bricks=%d" % (numballs, numbricks)


def Reset(bricks):  # set all bricks visible

    for brick in bricks:
        brick.visible = True
    return len(bricks)


def EmptyBuffer(myscene):  # flush all buffered left clicks

    while myscene.mouse.clicked > 0:
        temp = myscene.mouse.getclick()


NO_LOSE_MODE = False  # set True to make floor solid
SHOW_TRAIL = True  # set True to make ball leave temporary trail
SHOW_COORDS = False  # set True to display ball coordinates

brickLeft = []  # all bricks on the left wall
brickRight = []  # all bricks on the right wall
brickTop = []  # all bricks on the top wall
brickBack = []  # all bricks on the back wall

myscene = canvas(title="3D Breakout", width=1000, height=640, fullscreen=True)
myscene.select()
myscene.autoscale = True
myscene.userzoom = True
myscene.userspin = False
myscene.range = 360
#myscene.cursor.visible = False

myscene.stereo = 'redcyan'  # redblue yellowblue crosseyed passive active

wallLeft = -250  # x coordinate of the left wall
wallRight = 250  # x coordinate of the right wall
wallTop = 150  # y coordinate of the ceiling
wallBottom = -150  # y coordinate of the floor
wallBack = -300  # z coordinate of the back wall
wallFront = 200  # z coordinate of the front wall

brickColor = vec(0.7, 0.7, 1)

for x in range(-200, 201, 100):  # draw the bricks on the top
    for z in range(-260, 141, 100):
        brickTop.append(box(pos=vec(x, wallTop, z), size=vec(95, 0.1, 95), color=brickColor))

for y in range(-120, 121, 60):  # draw the bricks on the left and right
    for z in range(-260, 141, 100):
        brickLeft.append(box(pos=vec(wallLeft, y, z), size=vec(0.1, 55, 95), color=brickColor))
        brickRight.append(box(pos=vec(wallRight, y, z), size=vec(0.1, 55, 95), color=brickColor))

for x in range(-200, 201, 100):  # draw the bricks on the back
    for y in range(-120, 121, 60):
        brickBack.append(box(pos=vec(x, y, wallBack), size=vec(95, 55, 0.1), color=brickColor))

paddle = box(pos=vec(0, wallBottom, 0), size=vec(90, .1, 90), color=vec(1, 1, 1))

ball = sphere(radius=5.0, make_trail=False)

if SHOW_TRAIL:
    ball.make_trail = True
    ball.trail_type = "curve"
    ball.interval = 10
    ball.retain = 100

ball.mass = 1.0
ball.velocity = vector(0.15, 0.23, 0.27)
ball.visible = False

dt = 1.0  # 0.5 is half normal speed and 2.0 is double normal

numbricks = Reset(brickLeft + brickRight + brickTop + brickBack)
numballs = 3

newball = True
hitfound = False
gameover = False

coords = label(text="", pos=vec(wallLeft + 40, wallBottom + 5, wallFront), height=20, color=vec(.5, .5, .5), box=False)
status = label(text="", pos=vec(0, wallBottom + 5, wallFront), height=20, box=False)

status.text = "Left Click to launch or ESC to exit"

while True:

    rate(400)

    # update paddle position based on mouse position

    mouse_pos = myscene.mouse.pos
    px = min(max(2 * mouse_pos.x, wallLeft + 20), wallRight - 20)
    pz = -min(max(2 * mouse_pos.y, wallBack), wallFront) - 100
    #px = min(max(2 * myscene.mouse.pos[0], wallLeft + 20), wallRight - 20)
    #pz = -min(max(2 * myscene.mouse.pos[1], wallBack), wallFront) - 100
    paddle.pos = vec(px, wallBottom, pz)

    # If waiting to launch a new ball then idle until keypress. We have to poll rather than
    # pause or we won't be able to move the paddle while we wait.

    if gameover:

        if myscene.mouse.clicked > 0:
            numbricks = Reset(brickLeft + brickRight + brickTop + brickBack)
            numballs = 3
            newball = True
            gameover = False
            UpdateStatus(status, numballs, numbricks)

    elif newball:
        pass
        # TODO
        # if myscene.mouse.clicked > 0:
        #     newball = False
        #     paddle.color = vec(1, 1, 1)
        #     ball.pos = paddle.pos
        #     ball.velocity = vector(0.15, 0.23, 0.27)
        #     ball.visible = True
        #     UpdateStatus(status, numballs, numbricks)

    else:

        # calculate new ball position and adjust size based on z position

        ball.pos = ball.pos + ball.velocity * dt
        ball.radius = 4 + (ball.pos.z + 400) / 100.0

        if ball.velocity.z > 0:
            ball.color = (1, 0, 0)
        else:
            ball.color = (0, 1, 0)

        if SHOW_COORDS:
            coords.text = "%4d %4d %4d" % (ball.pos.x, ball.pos.y, ball.pos.z)

        # check for hit on a visible brick

        if ball.pos.x <= wallLeft:
            ball.velocity.x = -ball.velocity.x
            hitfound, brick = SideBrick(brickLeft, ball.y, ball.z)

        if ball.pos.x >= wallRight:
            ball.velocity.x = -ball.velocity.x
            hitfound, brick = SideBrick(brickRight, ball.y, ball.z)

        if ball.pos.z <= wallBack:
            ball.velocity.z = -ball.velocity.z
            hitfound, brick = BackBrick(brickBack, ball.x, ball.y)

        if ball.pos.z >= wallFront:
            ball.velocity.z = -ball.velocity.z

        if ball.pos.y >= wallTop:
            ball.velocity.y = -ball.velocity.y
            hitfound, brick = TopBrick(brickTop, ball.x, ball.z)

        # if hit then clear brick

        if hitfound:
            brick.visible = False
            hitfound = False
            numbricks -= 1
            UpdateStatus(status, numballs, numbricks)

        # check if paddle hit or miss

        if ball.pos.y <= wallBottom and numballs > 0:
            if NO_LOSE_MODE:
                ball.velocity.y = -ball.velocity.y
            else:
                if paddle.pos.x - 45 <= ball.pos.x <= paddle.pos.x + 45 and paddle.pos.z - 45 <= ball.pos.z <= paddle.pos.z + 45 and wallBottom - ball.pos.y <= 1:
                    ball.velocity.y = -ball.velocity.y
                elif wallBottom - ball.y > 50:
                    ball.velocity.y = -ball.velocity.y
                    numballs -= 1
                    newball = (numballs > 0)
                    EmptyBuffer(myscene)
                    paddle.color = (1, 1, 0)
                    ball.visible = False
                    status.text = "Left Click to launch or ESC to exit"

        # check if out of bricks (win) or balls (lose)

        if not gameover and (numbricks == 0 or numballs == 0):
            gameover = True
            EmptyBuffer(myscene)
            if numbricks == 0:
                status.text = "Congratulations - You Win - Left Click for new game or ESC to exit"
            else:
                status.text = "Sorry - You've got no balls - Left Click for new game or ESC to exit"