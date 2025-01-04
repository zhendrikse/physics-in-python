from vpython import *

title = """<b>Not</b> to scale Earth-Sun-Moon simulator
It does not include gravitational physics or Newtonian analysis &mdash; just circular motion

&#x2022; Based on the <a href="https://trinket.io/embed/glowscript/575a4ed5d362597041cd6f84">Sun-Earth-Moon model by B. Philhour</a>
&#x2022; Modified by Rob Salgado to model the sunshine seen by the United Kingdom
&#x2022; Maintained by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>

&#x2022; The red arrow points "upward from the UK" (at 52 degrees latitude [from the equator])
&#x2022; The cyan arrow is the rotational axis of the earth, tilted at 23 degrees from vertical
&#x2022; The yellow arrow points from the earth to the sun
&#x2022; Click on sun or earth to change the camera perspective
&#x2022; Click on space bar to change background color scheme

"""

list_of_months = ['January', 'February', 'March', 'April',
                  'May', 'June', 'July', 'August',
                  'September', 'October', 'November', 'December']

# constants - use these to change the scale and initial positions of everything
# the basic issue here is that realistic size scales would be impossible to see,
# so we choose unrealistic values for ease of visualization
sun_radius = 0.2  # note: real value would be 696,000 km, a good choice for sim is 0.1
earth_radius = sun_radius * 0.5  # note: real value would be sunRadius * 0.01, a good choice for sim is * 0.5
moon_radius = earth_radius * 0.27  # note: real value would be earthRadius * 0.27, this is fine for sim
astronomical_unit = 4.0  # note: real value would be 150,000,000 km, a good choice for sim is 4.0
earth_moon_distance = earth_radius * 6  # note that the real value would be earthRadius * 60, a good choice for sim is 6
earth_orbit_rate = 1  # the Earth orbits the Sun at about 1 degree per day
moon_orbit_rate = 13  # the Moon orbits the Earth at about 13 degrees per day

simulation_speed = 0.5


class SunEarthMoonSystem:
    def __init__(self):

        self._earth_angle = 0  # this is the angle in degrees representing the Earth's year-long motion around the Sun - so use 0 to 360 (default 0)
        self._moon_angle = 0  # this is an angle in degrees representing the Moon's month-long motion around the Earth - so use 0 to 360 (default 0)

        self._sun = sphere(radius=sun_radius, opacity=0.7, emissive=True, texture="http://i.imgur.com/yoEzbtg.jpg")
        self._earth = sphere(radius=earth_radius, texture=textures.earth, flipx=False, shininess=0.9)
        self._moon = sphere(radius=moon_radius, texture="http://i.imgur.com/YPg4RPU.jpg", flipx=True, flipy=True, shininess=0.9)

    def update(self):
        # update the position of the Earth and Moon by using basic circle trigonometry
        self._earth.pos = astronomical_unit * vec(cos(radians(self._earth_angle)), 0, sin(radians(self._earth_angle)))
        self._moon.pos = self._earth.pos + earth_moon_distance * vec(cos(radians(self._moon_angle)), 0, sin(radians(self._moon_angle)))
        earth_arrows.update(self._earth.pos, radians(program_speed * 365))

    def rotate(self, program_speed):
        # Calculate the amount by which the position of the Earth and Moon change each loop cycle
        self._earth_angle -= earth_orbit_rate * program_speed  # -= means subtract the following  - we subtract to make counterclockwise orbits seen from above
        self._moon_angle -= moon_orbit_rate * program_speed

        # Because the Earth and Moon to rotate on their own axis - to flip one of them, make the middle entry in the axis vector (-1)
        # Rotate the earth 365 times per year
        self._earth.rotate(angle=radians(program_speed * 365), axis=earth_arrows.earth_rotation_axis())

        # The moon is in tidal lock so always shows the same face to Earth
        self._moon.rotate(angle=radians(program_speed * moon_orbit_rate), axis=vec(0, 1, 0))
        # Rotate the Sun with a period of about 22 days
        self._sun.rotate(angle=radians(program_speed * 16), axis=vec(0, 1, 0))

    def follow_sun(self, camera):
        camera.follow(self._sun)

    def follow_earth(self, camera):
        camera.follow(self._earth)

    def follow_moon(self, camera):
        camera.follow(self._moon)

    def earth_angle(self):
        return self._earth_angle


class EarthArrows:
    def __init__(self, scale=0.5, radius_earth=earth_radius, latitude=52, tilt=23):
        self._scale = scale
        self._rotation_axis = vec(sin(radians(tilt)), cos(radians(tilt)), 0)
        axis = scale * vec(sin(radians(0 - (90 - latitude))), cos(radians(0 - (90 - latitude))), 0)
        self._from_uk_up_arrow = arrow(shaftwidth=radius_earth / 5., axis=axis, color=color.red)
        # UK-arrow faces the sun (axisE points away from the sun)... in January
        self._from_uk_up_arrow.rotate(angle=radians(90), axis=vec(0, 1, 0))  # start at midnight
        # unit-vector on earth pointing to the sun
        self._earth_sun_arrow = arrow(shaftwidth=radius_earth / 3, color=color.yellow)

        axis = scale * vec(sin(radians(tilt)), cos(radians(tilt)), 0)
        self._earth_axis_arrow = arrow(shaftwidth=radius_earth / 5, axis=axis, color=color.cyan)

    def update(self, position, rotation_angle):
        self._earth_axis_arrow.pos = position
        self._earth_sun_arrow.pos = position
        self._from_uk_up_arrow.pos = position
        self._from_uk_up_arrow.rotate(angle=rotation_angle, axis=self._rotation_axis)
        self._earth_sun_arrow.axis = -norm(position)

    def sun_energy_transfer(self):
        ## arrows are unit-vectors (times scale factor), so dot product is cos(angle between)
        dot_product = dot(self._from_uk_up_arrow.axis, self._earth_sun_arrow.axis)
        # During nighttime, there is no energy transfer, so set to zero during the night
        energy_transfer = 0 if dot_product <= 0 else dot_product / self._scale
        return energy_transfer

    def earth_rotation_axis(self):
        return self._rotation_axis

def on_mouse_click():
    change_view()

def set_speed():
    global program_speed
    program_speed = speed_slider.value

def change_view():  # define a new function by name
    chosen_object = scene.mouse.pick  # find out which object the user clicked on
    if chosen_object is not None:  # if it is a real object that they clicked on ...
        scene.camera.follow(chosen_object)  # .. then have the camera follow that object

def on_key_down(event):
    if event.key == " ":
        scene.background = color.white if scene.background == color.black else color.black


earth_arrows = EarthArrows(latitude=52) # UK latitude, -38 for melbourne
simulation_speed = min(simulation_speed, 1 / 24.)  ###RS
program_speed = simulation_speed  # default setting
sun_earth_moon = SunEarthMoonSystem()

# set up the scene
# scene.caption.text("Use two-finger swipe to zoom. Use two-finger click/drag to rotate camera.\nClick on an object to change camera focus." +
#                    "\n\nThis simulation is NOT TO ACCURATE SCALE - edit source to play with scale." +
#                    "\n\nUse the slider below to adjust the animation speed or pause the simulation.\n")
# scene.lights = []    # this gets rid of all the ambient scene lights so that the Sun is the source / the command here blanks an array
scene.height = 300
scene.width = 1200  # width in pixels of the display on the screen
# scene.forward = vec(0,-15,0)    # this allows you to change the starting perspective of the camera
scene.range = astronomical_unit / 4.
scene.fov = radians(10)
scene.title = title
sun_earth_moon.follow_sun(scene.camera) # have the camera default to centering on the sun
scene.bind("mousedown", change_view)  # allow mouse clicks to call the changeView function
scene.bind("keydown", on_key_down)
scene.append_to_caption("\nAdjust the speed of the simulation using the slider\n")
speed_slider = slider(bind = set_speed, value = program_speed, min = 0.0, max = 1./24.)

# place a few sources of light at the same position as the Sun to illuminate the Earth and Moon objects
sunlight = local_light(pos=vec(0, 0, 0), color=color.white)
more_sunlight = local_light(pos=vec(0, 0, 0), color=color.white)  # I found adding two lights was about right


graph_height = 70
graph_width = 480
daylight_graph = graph(width=graph_width, height=graph_height * 4, title="Hours with daylight",
                  xmax=365, ymin=8, ymax=16)
daylight_curve = gcurve(graph=daylight_graph, color=color.red)
equator_curve = gcurve(graph=daylight_graph, color=color.cyan)
_ = [equator_curve.plot(day, 12) for day in range(365)]
energy_curve = gcurve()

new_graph_interval = 30
month_counter = 0
daylight = 0
days_counter = 0
while sun_earth_moon.earth_angle() <= 365:  # stop after one year
    rate(100)

    sun_earth_moon.update()
    sun_earth_moon.rotate(program_speed)

    sun_energy_transfer = earth_arrows.sun_energy_transfer()
    daylight += sun_energy_transfer
    if sun_energy_transfer == 0 and daylight != 0:
        days_counter += 1
        daylight = daylight * program_speed
        daylight_curve.plot(days_counter, daylight * 24 + 7.2)
        daylight = 0

    if -sun_earth_moon.earth_angle() > month_counter * new_graph_interval:  # new month, new graph
        energy_graph = graph(title="Sunlight in " + list_of_months[month_counter%12], width=graph_width, height=graph_height,
                             xmin=month_counter * new_graph_interval, xmax=(month_counter + 1) * new_graph_interval,
                             ymin=-0.1,
                             ymax=1)
        energy_curve = gcurve(graph=energy_graph, interval=1)
        month_counter += 1
    energy_curve.plot(-sun_earth_moon.earth_angle(), sun_energy_transfer)



