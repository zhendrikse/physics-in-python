from vpython import vec, color, pi, rate, scene, curve

from toolbox.wave import ElectromagneticWave

scene.ambient = vec(.4, .4, .4)

waves_separation = 4.
step_range = 20
omega = 0.1
wavelength = step_range
k = 2 * pi / wavelength

color_scheme = 0

# sine = curve(pos=positions)
waves = []
for z in range(-2, 3, 1):
  waves += [ElectromagneticWave(position=vec(0, 0, z * waves_separation))]
waves += [ElectromagneticWave(position=vec(0, waves_separation, 0))]
waves += [ElectromagneticWave(position=vec(0, -waves_separation, 0))]

height = waves_separation / 2.0
faraday_loop = curve(
  pos=[vec(-1, -height, 0), vec(-1, height, 0), vec(1, height, 0), vec(1, -height, 0), vec(-1, -height, 0)],
  color=color.yellow)
ampere_loop = curve(
  pos=[vec(-1, 0, -height), vec(-1, 0, height), vec(1, 0, height), vec(1, 0, -height), vec(-1, 0, -height)],
  color=color.magenta)

dt = 0.05
t = 0
while True:
  rate(1 / dt)

  for wave in waves:
    t += dt
    wave.update(t)
