from vpython import *

"""
Interactive Superposition of Coherent Sources (ver 2/16/2004)
Rob Salgado (salgado@physics.syr.edu)
"""
### ver 2/16/2004   tested on Windows 2000
###                 with Python-2.3.3.exe and VPython-2003-10-05.exe
###                 Navigation needs work. The mouse should be able to
###                    drag each of the three points along the xz-plane.
###                    The relation between the dragged point and mouse
###                    cursor look unnatural.

# phase=arange(0,1,.1)
# print len(phase)
# sinphase=sin(phase)
# print phase, sinphase
# eqn =raw_input('formula')
# x=arange(0,10,0.1)
# c=curve(x=x,y=eval(eqn))

scene.autoscale = 0
scene.range = (12, 12, 12)
scene.title = "Wave Superposition"

t = 0

amplitude_a = 1
wavenumber_k_a = 2. * pi / 5
omega_a = 1
phase_a = 0

wavelength = 2. * pi / wavenumber_k_a

Ax0 = 0
Ay0 = 0
Ax1 = 10
Ay1 = 0
Adx = Ax1 - Ax0
Ady = Ay1 - Ay0
a_value_range = arange(0, sqrt(Adx * Adx + Ady * Ady) + 0.01, 0.01)

curve_vectors_a=[]
for value in a_value_range:
    Ax = Ax0 + Adx * value / a_value_range[-1]
    Ay = Ay0 + Ady * value / a_value_range[-1]
    curve_vectors_a += [vector(Ax, amplitude_a * sin(wavenumber_k_a * value - omega_a * t + phase_a), Ay)]

# curve_vectors_a=[]
# for i in range(len(Ax)):
#     curve_vectors_a += [vector(Ax[i], amplitude_a * sin(wavenumber_k_a * Ar[i] - omega_a * t + phase_a), Ay[i])]

#Ac = curve(x=Ax, z=Ay, y=amplitude * sin(Ak * Ar - Aw * t + Ap), color=color.cyan, radius=0.2)
Ac = curve(curve_vectors_a, color=color.cyan, radius=0.2)
sphere_wave_a_0 = sphere(pos=vector(Ax0, 0, Ay0), radius=0.1, color=color.cyan)
sphere_wave_a_1 = sphere(pos=vector(Ax1, 0, Ay1), radius=0.1, color=color.cyan)

Alabel = label(pos=vector(Ax0, 0, Ay0), text="{:4.2f}".format(a_value_range[-1]), color=color.cyan, yoffset=-60, opacity=0)

source_arrow = arrow(pos=sphere_wave_a_0.pos, axis=vector(0, curve_vectors_a[0].y, 0), color=color.cyan)
target_arrow = arrow(pos=sphere_wave_a_1.pos, axis=vector(0, curve_vectors_a[-1].y, 0), color=color.cyan)

amplitude_b = 1
wave_number_k_b = wavenumber_k_a
omega_b = 1
phase_b = 0

Bx0 = 0
By0 = 0
Bx1 = 10
By1 = 0
Bdx = Bx1 - Bx0
Bdy = By1 - By0
b_value_range = arange(0, sqrt(Bdx * Bdx + Bdy * Bdy) + 0.01, 0.01)
#
# Bx = Bx0 + Bdx * Br / Br[-1]
# By = By0 + Bdy * Br / Br[-1]

curve_vectors_b=[]
for value in b_value_range:
    Bx = Bx0 + Bdx * value / b_value_range[-1]
    By = By0 + Bdy * value / b_value_range[-1]
    curve_vectors_b += [vector(Bx, amplitude_b * sin(wave_number_k_b * value - omega_b * t + phase_b), By)]

#
# curve_vectors_b = []
# for i in range(len(Br)):
#     curve_vectors_b += [vector(Bx[i], amplitude_b * sin(wave_number_k_b * Br[i] - omega_b * t + phase_b), By[i])]

#Bc = curve(x=Bx, z=By, y=amplitude_b * sin(Bk * Br - Bw * t + Bp), color=color.green, radius=0.2)
Bc = curve(curve_vectors_b, color=color.green, radius=0.2)
sphere_wave_b_0 = sphere(pos=vector(Bx0, 0, By0), radius=0.1, color=color.green)
sphere_wave_b_1 = sphere(pos=vector(Bx1, 0, By1), radius=0.1, color=color.green)

# Blabel = label(pos=vector(Bx0, 0, By0), text="Br=%4.2f" % (Br[-1]), color=color.green, yoffset=-100, opacity=0)
#
Bsource = arrow(pos=sphere_wave_b_0.pos, axis=vector(0, curve_vectors_b[0].y, 0), color=color.green)
Btarget = arrow(pos=sphere_wave_b_1.pos, axis=vector(0, curve_vectors_b[0].y, 0), color=color.green)

Xtarget = arrow(pos=sphere_wave_b_1.pos, axis=vector(0, curve_vectors_a[-1].y + curve_vectors_b[-1].y, 0), color=color.magenta)
#
# Xlabeld = label(pos=Bs1.pos, text="delta_r=%4.2f" % (Br[-1] - Ar[-1]), color=color.magenta, xoffset=-30, yoffset=100,
#                 opacity=0)
# Xlabell = label(pos=Bs1.pos, text="lambda=%4.2f" % wavelength, color=color.magenta, xoffset=-30, yoffset=60, opacity=0)
# Xlabelr = label(pos=Bs1.pos, text="ratio=%4.2f" % ((Br[-1] - Ar[-1]) / wavelength), color=color.magenta, xoffset=-30,
#                 yoffset=-60, opacity=0)

n = None
drag = 0

# scene.forward=vector([0.021853,-0.923144,-0.383834])
while 1:
    rate(40)
    #    print scene.center, scene.forward, scene.range
    t += 0.1

    vectors_a = []
    for i in range(len(a_value_range)):
        vectors_a += [vector(0, amplitude_a * sin(wavenumber_k_a * a_value_range[i] - omega_a * t + phase_a), 0)]
        current_pos = Ac.point(i)["pos"]
        new_pos = vec(current_pos.x, amplitude_a * sin(wavenumber_k_a * a_value_range[i] - omega_a * t + phase_a), current_pos.z)
        Ac.modify(i, pos=new_pos)
    #Ac.y = amplitude_a * sin(wavenumber_k_a * Ar - omega_a * t + phase_a)
    source_arrow.axis = vectors_a[0]
    target_arrow.axis = vectors_a[-1]

    vectors_b = []
    for i in range(len(b_value_range)):
        vectors_b += [vector(0, amplitude_b * sin(wave_number_k_b * b_value_range[i] - omega_b * t + phase_b), 0)]
        current_pos = Bc.point(i)["pos"]
        new_pos = vec(current_pos.x, amplitude_b * sin(wave_number_k_b * b_value_range[i] - omega_b * t + phase_b), current_pos.z)
        Bc.modify(i, pos=new_pos)
    #Bc.y = amplitude_b * sin(wave_number_k_b * Br - omega_b * t + phase_b)
    Bsource.axis = vectors_b[0]
    Btarget.axis = vectors_b[-1]

    Xtarget.axis = vectors_a[-1] + vectors_b[-1]

    # if scene.mouse.clicked:
    #     m = scene.mouse.getclick()
    #     newPick = scene.mouse.pick
    #
    #     if newPick == As0:
    #         print(" A")
    #     elif newPick == Bs0:
    #         print(" B")
    #     elif newPick == Bs1:
    #         print(" X")
    #     else:
    #         print(" none")
    #         # scene.center=(As0.pos+Bs0.pos+As1.pos+Bs1.pos)/4.
    #         # scene.center=scene.mouse.pos
    #
    #     print
    #     newPick
    #     if m.click == "none":
    #         drag = 0;
    #         print
    #         drag
    #         scene.mouse.getclick()
    #         scene.center = scene.mouse.pos
    #     elif m.click == "left":
    #         n = newPick
    #         drag = 1;
    #         print
    #         drag

    # if drag == 1:
    #     # print "Drag ",
    #     # print scene.mouse.button
    #     if not n is None:
    #         n.pos[0] = scene.mouse.pos[0]
    #         n.pos[2] = scene.mouse.pos[2]
    #
    #         newpos = n.pos
    #         if n == As0:
    #             Ax0 = newpos[0]
    #             Ay0 = newpos[2]
    #             As0.pos = vector([Ax0, 0, Ay0])
    #
    #         elif n == Bs0:
    #             Bx0 = newpos[0]
    #             By0 = newpos[2]
    #             Bs0.pos = vector([Bx0, 0, By0])
    #         elif n == Bs1:
    #             Ax1 = newpos[0]
    #             Ay1 = newpos[2]
    #             Bx1 = newpos[0]
    #             By1 = newpos[2]
    #             As1.pos = vector([Ax1, 0, Ay1])
    #             Bs1.pos = vector([Bx1, 0, By1])
    #
    #         else:
    #             print
    #             "none"
    #
    #         Adx = Ax1 - Ax0
    #         Ady = Ay1 - Ay0
    #         Ar = arange(0, sqrt(Adx * Adx + Ady * Ady) + 0.01, 0.01)
    #         Alabel.pos = vector([Ax0, 0, Ay0])
    #         Alabel.text = "Ar=%4.2f" % (Ar[-1])
    #
    #         Ax = Ax0 + Adx * Ar / Ar[-1]
    #         Ay = Ay0 + Ady * Ar / Ar[-1]
    #         Aold = Ac
    #         Ac = curve(x=Ax, z=Ay, y=amplitude_a * sin(wavenumber_k_a * Ar - omega_a * t + phase_a), color=color.cyan, radius=.2)
    #         Aold.visible = 0
    #
    #         source_arrow.pos = vector([Ax0, 0, Ay0])
    #         target_arrow.pos = vector([Ax1, 0, Ay1])
    #
    #         Bdx = Bx1 - Bx0
    #         Bdy = By1 - By0
    #         Br = arange(0, sqrt(Bdx * Bdx + Bdy * Bdy) + 0.01, 0.01)
    #         Blabel.pos = vector([Bx0, 0, By0])
    #         Blabel.text = "Br=%4.2f" % (Br[-1])
    #
    #         Bx = Bx0 + Bdx * Br / Br[-1]
    #         By = By0 + Bdy * Br / Br[-1]
    #         Bold = Bc
    #         Bc = curve(x=Bx, z=By, y=amplitude_b * sin(wave_number_k_b * Br - omega_b * t + phase_b), color=color.green, radius=.2)
    #         Bold.visible = 0
    #
    #         Bsource.pos = vector([Bx0, 0, By0])
    #         Btarget.pos = vector([Bx1, 0, By1])
    #
    #         Xtarget.pos = vector([Bx1, 0, By1])
    #         Xlabeld.pos = Bs1.pos
    #         Xlabeld.text = "delta_r=%4.2f" % (Br[-1] - Ar[-1])
    #         Xlabell.pos = Bs1.pos
    #         Xlabell.text = "lambda=%4.2f" % wavelength
    #         Xlabelr.pos = Bs1.pos
    #         Xlabelr.text = "ratio=%4.2f" % ((Br[-1] - Ar[-1]) / wavelength)


