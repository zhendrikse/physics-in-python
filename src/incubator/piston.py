from vpython import *

# B. Philhour

num = 350  # number of molecules / atoms
crest = 0.99  # coefficient of restitution

# create container # T stands for Tube
Tlength = 0.15  # size scale of system in meters
Tradius = Tlength / 10
tube = cylinder(radius=Tradius + Tlength / 200, axis=vec(0, Tlength, 0), pos=vec(0, -Tlength / 2, 0), opacity=0.2)

# create lid # L stands for Lid
Llength = Tlength / 40
Lradius = Tradius
lid = cylinder(radius=Lradius, axis=vec(0, Llength, 0), pos=vec(0, Tlength / 2, 0), color=color.cyan)
amplitude = 3 * Llength
freq = 4000

# create molecules / atoms
atoms = [None for i in range(num)]
speed = 550  # initial speeds in m/s

atomR = Tlength / 200  # visual radius of atoms
sizeMult = 1.0  # multiply above for actual radius in particle-particle collisions

for i in range(num):
    atoms[i] = sphere(radius=atomR)
    atoms[i].pos.y = (Tlength / 2) - Tlength * random()
    angle = 2 * pi * random()
    atoms[i].pos.x = Tradius * cos(angle) * random()
    atoms[i].pos.z = Tradius * sin(angle) * random()
    atoms[i].mass = 0.1  # in kg
    atoms[i].vel = speed * vector.random()

c = curve()
graphAxis = curve(color=color.red)
graphLabel = label(text='Density', box=False, height=11)

def flipRunning():
    global running
    if (running == True):
        running = False
        pause.text = 'Resume'
    else:
        running = True
        pause.text = 'Pause'


running = True
pause = button(text='Pause', bind=flipRunning)

def setFrequency():
    global freq
    freq = freqSlider.value


scene.append_to_caption('\n\nPiston frequency\n')
freqSlider = slider(min=0, max=30000, value=4000, bind=setFrequency)


def setAmplitude():
    global amplitude
    amplitude = amplitudeSlider.value


scene.append_to_caption('\n\nPiston amplitude\n')
amplitudeSlider = slider(min=0, max=4 * Llength, value=2 * Llength, bind=setAmplitude)

dt = 2e-6
time = 0

scene.append_to_caption('\n\nGraph bins\n')
binSlider = slider(min=2, max=100, value=50, bind=bin)


# def bin():
#     numBins = int(binSlider.value)


scene.range = 25 * Llength

freqText = label(text='Freq: ' + str(freq) + " Hz", pos=vec(3 * Tradius, Tradius, 0), box=False, align='left')
ampText = label(text='Amplitude: ' + str(amplitude * 100) + ' cm', pos=vec(3 * Tradius, -Tradius, 0), box=False,
                align='left')

while True:

    rate(1 / dt)

    if not running: continue

    freqText.text = 'Freq: ' + str(freq) + ' Hz'
    ampText.text = 'Amplitude: ' + str(round(1000 * amplitude) / 10) + ' cm'

    lid.pos.y = (Tlength / 2 - Llength - amplitude) + amplitude * sin(2 * pi * time * freq)
    lid.vel = vec(0, 2 * pi * freq * amplitude * cos(2 * pi * time * freq), 0)

    for i in arange(num):
        atoms[i].hasCollided = False

    for i in arange(num):

        # check for collisions and apply laws of physics

        # bottom (just reflect)
        if (atoms[i].pos.y < -(Tlength / 2)):
            atoms[i].vel.y = - crest * atoms[i].vel.y
            atoms[i].pos.y = - Tlength / 2

        # sides (just reflect)
        r = vec(atoms[i].pos.x, 0, atoms[i].pos.z)
        if (r.mag + atomR > Tradius):
            v = vec(atoms[i].vel.x, 0, atoms[i].vel.z)
            theta = acos(r.dot(v) / (r.mag * v.mag))
            atoms[i].vel = crest * atoms[i].vel.rotate(angle=pi - 2 * theta, axis=vec(0, 1, 0))
            atoms[i].pos = (Tradius - atomR) * r.norm() + vec(0, atoms[i].pos.y, 0)

        # lid (treat as elastic with infinite lid mass)
        if (atoms[i].pos.y + atomR > (lid.pos.y - Llength / 2)):
            atoms[i].vel = 2 * lid.vel - atoms[i].vel
            atoms[i].pos.y = lid.pos.y - Llength / 2 - atomR

        # check for collisions with other (equal mass) atoms
        for j in range(num):
            if (j == i or atoms[j].hasCollided == True or atoms[i].hasCollided == True):
                continue
            sep = atoms[i].pos - atoms[j].pos
            if (sep.mag < sizeMult * 2.0 * atomR):  # two atoms overlapping
                v_rel = (atoms[i].vel - atoms[j].vel).dot(sep.norm())
                atoms[i].vel = atoms[i].vel - v_rel * sep.norm()
                atoms[j].vel = atoms[j].vel + v_rel * sep.norm()
                atoms[i].hasCollided = True
                atoms[j].hasCollided = True

    for i in range(num):
        # update positions
        atoms[i].pos = atoms[i].pos + atoms[i].vel * dt

    numBins = int(binSlider.value)
    positionBin = [0 for j in range(numBins)]
    average = 0
    seg = Tlength / numBins
    c.clear()
    for j in range(numBins):
        positionBin[j] = 0
        for i in range(num):
            if (atoms[i].pos.y > ((Tlength / 2) - (j + 1) * seg) and atoms[i].pos.y < ((Tlength / 2) - j * seg)):
                positionBin[j] = positionBin[j] + 1

        average = average + positionBin[j]

    average = average / numBins

    graphAxis.clear()
    graphAxis.append(pos=vec(-3 * Lradius - average / num, Tlength / 2, 0))
    graphAxis.append(pos=vec(-3 * Lradius - average / num, -Tlength / 2, 0))
    graphLabel.pos = vec(-3 * Lradius - average / num, (Tlength / 2) + Llength, 0)

    for j in range(numBins):
        c.append(pos=vec(-3 * Lradius - ((positionBin[j]) / num), (Tlength / 2) - j * seg, 0))

    time = time + dt

