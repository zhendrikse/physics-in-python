from vpython import *

print("Two-finger swipe to zoom; two-finger click & drag to move camera.")
print("Wait for the ball to drop! Grab it afterwards...")

X = 5
Y = 3
Z = 5
space = 1
offset = vec(-(X - 1) * space / 2.0, -(Y - 1) * space / 2.0, -(Z - 1) * space / 2.0)
N = 4 * X * Y * Z + 1
print("N = " + N + " - alter X,Y,Z for better performance.")

ball = []
ballMass = 0.020  # kg
bond = []
bondStiffness = 4000  # N/m

drag = 8.0  # Ns^2/m^2

for i in range(X):
    for j in range(Y):
        for k in range(Z):

            index = i + j * X + k * X * Y

            gridpoint = vec(i * space, j * space, k * space)
            ball[index] = sphere(pos=offset + gridpoint, radius=space / 10)
            ball[index].velocity = vec(0, 0, 0)
            ball[index].force = vec(0, 0, 0)

            if (i < X - 1):
                bond[index] = helix(pos=ball[index].pos, axis=vec(space, 0, 0), radius=space / 20, color=color.white,
                                    coils=6, thickness=space / 100)

            if (j < Y - 1):
                bond[X * Y * Z + index] = helix(pos=ball[index].pos, axis=vec(0, space, 0), radius=space / 20,
                                                color=color.yellow, coils=6, tichkness=space / 100)

            if (k < Z - 1):
                bond[2 * X * Y * Z + index] = helix(pos=ball[index].pos, axis=vec(0, 0, space), radius=space / 20,
                                                    color=color.green, coils=6, tichkness=space / 100)

bigBall = sphere(pos=vec(random() - 0.5, 2 * space * Y, random() - 0.5), radius=space * 2, color=color.red)
bigBall.velocity = vec(0, 0, 0)
bigMass = 10.0  # kg
g = 10  # N/kg

time = 0
dt = 0.0002

animation.range = X * space / 2.0

pull = False
chosenObject = None

animation.bind("mousedown", down)
animation.bind("mousemove", move)
animation.bind("mouseup", up)


def down():
    nonlocal pull, chosenObject
    chosenObject = animation.mouse.pick()
    chosenObject.pos = animation.mouse.pos
    pull = True


def move():
    nonlocal pull, chosenObject
    if (pull == True):  # mouse button is down
        chosenObject.pos = animation.mouse.pos


def up():
    nonlocal pull, chosenObject
    chosenObject = None
    pull = False


while (True):

    rate(1 / dt)
    time = time + dt

    bigBall.force = vec(0, -bigMass * g, 0)
    bigBall.force = bigBall.force - drag * bigBall.velocity

    for i in range(X):
        for j in range(Y):
            for k in range(Z):

                index = i + j * X + k * X * Y

                ball[index].force = -drag * ball[index].velocity

                if (i > 0):
                    leftBall = ball[(i - 1) + j * X + k * X * Y]
                    separation = leftBall.pos - ball[index].pos
                    ball[index].force = ball[index].force + bondStiffness * (separation - space * separation.norm())

                if (i < X - 1):
                    rightBall = ball[(i + 1) + j * X + k * X * Y]
                    separation = rightBall.pos - ball[index].pos
                    ball[index].force = ball[index].force + bondStiffness * (separation - space * separation.norm())

                if (j > 0):
                    belowBall = ball[i + (j - 1) * X + k * X * Y]
                    separation = belowBall.pos - ball[index].pos
                    ball[index].force = ball[index].force + bondStiffness * (separation - space * separation.norm())

                if (j < Y - 1):
                    aboveBall = ball[i + (j + 1) * X + k * X * Y]
                    separation = aboveBall.pos - ball[index].pos
                    ball[index].force = ball[index].force + bondStiffness * (separation - space * separation.norm())

                if (k > 0):
                    toBall = ball[i + j * X + (k - 1) * X * Y]
                    separation = toBall.pos - ball[index].pos
                    ball[index].force = ball[index].force + bondStiffness * (separation - space * separation.norm())

                if (k < Z - 1):
                    froBall = ball[i + j * X + (k + 1) * X * Y]
                    separation = froBall.pos - ball[index].pos
                    ball[index].force = ball[index].force + bondStiffness * (separation - space * separation.norm())

                separation = ball[index].pos - bigBall.pos
                contactDistance = bigBall.radius + 2 * ball[index].radius
                if (separation.mag < contactDistance):
                    ball[index].force = ball[index].force - bondStiffness * (
                                separation - contactDistance * separation.norm())
                    bigBall.force = bigBall.force + bondStiffness * (
                                separation - contactDistance * separation.norm())  # 3rd Law

    if (pull):
        chosenObject.force = vec(0, 0, 0)
        chosenObject.velocity = vec(0, 0, 0)

    for i in range(X):
        for j in range(Y):
            for k in range(Z):

                index = i + j * X + k * X * Y

                ball[index].velocity = ball[index].velocity + (ball[index].force / ballMass) * dt
                ball[index].pos = ball[index].pos + ball[index].velocity * dt

                if (i < X - 1):
                    bond[index].axis = ball[(i + 1) + j * X + k * X * Y].pos - ball[index].pos
                    bond[index].pos = ball[index].pos

                if (j < Y - 1):
                    bond[X * Y * Z + index].axis = ball[i + (j + 1) * X + k * X * Y].pos - ball[index].pos
                    bond[X * Y * Z + index].pos = ball[index].pos

                if (k < Z - 1):
                    bond[2 * X * Y * Z + index].axis = ball[i + j * X + (k + 1) * X * Y].pos - ball[index].pos
                    bond[2 * X * Y * Z + index].pos = ball[index].pos

    bigBall.velocity = bigBall.velocity + (bigBall.force / bigMass) * dt
    bigBall.pos = bigBall.pos + bigBall.velocity * dt





