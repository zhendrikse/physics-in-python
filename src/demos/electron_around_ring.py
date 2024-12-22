from vpython import vec, rate, vector, scene

from toolbox.charge import Electron
from toolbox.charged_ring import ChargedRing

#
# Original: https://bphilhour.trinket.io/physics-through-glowscript-an-introductory-course#/1-introduction-objects-parameters-and-the-3d-environment/optional-scale-models
#

print(
    "If it isn't doing anything interesting, either wait or run again to randomize start position. Two-finger drag to change perspective.")

radius = 0.5e-10
ring = ChargedRing(radius=radius)
electron = Electron(position=vec(0, 0, radius) + 1.5 * radius * vector.random(), radius=radius / 20, make_trail=True,
                    retain=150)

def on_key_press(event):
    if event.key == 's':
        ring.show_field(x_range=range(-18, 18, 8),
                        y_range=range(-9, 9, 4),
                        z_range=range(-18, 18, 8))

scene.bind('keydown', on_key_press)

dt = 1e-18  # time step
while True:
    rate(100)
    E = ring.field_at(electron.position)
    F = electron.coulomb_force_in(E)
    electron.update(F, dt)
