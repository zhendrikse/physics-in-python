#Web VPython 3.2

from vpython import sphere, cos, sin, textures, color, radians, vec, arrow, norm, dot, canvas, slider, checkbox, local_light, graph, gcurve, rate

title = """<b>Not</b> to scale Earth-Sun-Moon simulator
It does not include gravitational physics or Newtonian analysis &mdash; just circular motion

&#x2022; Based on the <a href="https://trinket.io/embed/glowscript/575a4ed5d362597041cd6f84">Sun-Earth-Moon model by B. Philhour</a>
&#x2022; Modified by <a href="https://www.glowscript.org/#/user/Rob_Salgado/folder/My_Programs/program/SunshineOnTheEarth">Rob Salgado</a> to model the sunshine seen by the United Kingdom
&#x2022; Refactored by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>

&#x2022; The red arrow points "upward from the UK" (at 52 degrees latitude [from the equator])
&#x2022; The cyan arrow is the rotational axis of the earth, tilted at 23 degrees from vertical
&#x2022; The yellow arrow points from the earth to the sun
&#x2022; Click on sun or earth to change the camera perspective

"""

list_of_months = ['January', 'February', 'March', 'April',
                  'May', 'June', 'July', 'August',
                  'September', 'October', 'November', 'December']

# Real astronomical unit would be 150,000,000 km, a good choice for sim is 4.0
astronomical_unit = 4.0
# the earth orbits the Sun at about 1 degree per day
earth_orbit_rate = 1
# the moon orbits the Earth at about 13 degrees per day
moon_orbit_rate = 13

animation = canvas(title=title, height=300, width=1200, range=astronomical_unit / 4., fov=radians(10))

class EarthArrows:
    def __init__(self, radius_earth, axis_earth, scale=0.5, latitude=52):
        self._scale = scale
        self._earth_axis = axis_earth
        axis = scale * vec(sin(radians(0 - (90 - latitude))), cos(radians(0 - (90 - latitude))), 0)
        self._from_uk_up_arrow = arrow(shaftwidth=radius_earth / 5., axis=axis, color=color.red)
        # UK-arrow faces the sun (axisE points away from the sun)... in January
        self._from_uk_up_arrow.rotate(angle=radians(90), axis=vec(0, 1, 0))  # start at midnight
        # unit-vector on earth pointing to the sun
        self._earth_sun_arrow = arrow(shaftwidth=radius_earth / 3, color=color.yellow)

        self._earth_axis_arrow = arrow(shaftwidth=radius_earth / 5, axis=axis_earth * scale, color=color.cyan)

    def update(self, position, rotation_angle):
        self._earth_axis_arrow.pos = position
        self._earth_sun_arrow.pos = position
        self._from_uk_up_arrow.pos = position
        self._from_uk_up_arrow.rotate(angle=rotation_angle, axis=self._earth_axis)
        self._earth_sun_arrow.axis = -norm(position)

    def sun_energy_transfer(self):
        ## arrows are unit-vectors (times scale factor), so dot product is cos(angle between)
        dot_product = dot(self._from_uk_up_arrow.axis, self._earth_sun_arrow.axis)
        # During nighttime, there is no energy transfer, so set to zero during the night
        energy_transfer = 0 if dot_product <= 0 else dot_product / self._scale
        return energy_transfer

    def show(self):
        self._earth_axis_arrow.visible = True
        self._from_uk_up_arrow.visible = True
        self._earth_sun_arrow.visible = True

    def hide(self):
        self._earth_axis_arrow.visible = False
        self._from_uk_up_arrow.visible = False
        self._earth_sun_arrow.visible = False

class SunEarthMoonSystem:
    def __init__(self, simulation_speed=0.5, tilt=23):
        # Real sun radius would be 696,000 km, a good choice for sim is 0.1
        sun_radius = 0.2
        # Real earth radius would be sun radius * 0.01, a good choice for sim is * 0.5
        self._earth_radius = sun_radius * 0.5
        self._earth_axis = vec(sin(radians(tilt)), cos(radians(tilt)), 0)
        # Real moon radius would be earth radius * 0.27, this is fine for sim
        moon_radius = self._earth_radius * 0.27
        self._simulation_speed = min(simulation_speed, 1 / 24.)

        # Angle in degrees representing the Earth's year-long motion around the Sun - so use 0 to 360 (default 0)
        self._earth_angle = 0  #
        # Angle in degrees representing the Moon's month-long motion around the Earth - so use 0 to 360 (default 0)
        self._moon_angle = 0

        self._sun = sphere(radius=sun_radius, opacity=0.7, emissive=True, texture="http://i.imgur.com/yoEzbtg.jpg")
        self._earth = sphere(radius=self._earth_radius, texture=textures.earth, flipx=False, shininess=0.9)
        self._moon = sphere(radius=moon_radius, texture="http://i.imgur.com/YPg4RPU.jpg", flipx=True, flipy=True, shininess=0.9)

        self._earth_arrows = EarthArrows(radius_earth=self._earth_radius, axis_earth=self._earth_axis, latitude=52)  # UK latitude, -38 for melbourne

    def update(self):
        # Real earth moon distance value would be earthRadius * 60, a good choice for sim is 6
        earth_moon_distance = self._earth_radius * 6

        # update the position of the Earth and Moon by using basic circle trigonometry
        self._earth.pos = astronomical_unit * vec(cos(radians(self._earth_angle)), 0, sin(radians(self._earth_angle)))
        self._moon.pos = self._earth.pos + earth_moon_distance * vec(cos(radians(self._moon_angle)), 0, sin(radians(self._moon_angle)))
        self._earth_arrows.update(self._earth.pos, radians(self._simulation_speed * 365))
        self._rotate()

    def _rotate(self):
        # Calculate the amount by which the position of the Earth and Moon change each loop cycle
        self._earth_angle -= earth_orbit_rate * self._simulation_speed  # we subtract to make counterclockwise orbits seen from above
        self._moon_angle -= moon_orbit_rate * self._simulation_speed

        # Because the Earth and Moon to rotate on their own axis - to flip one of them, make the middle entry in the axis vector (-1)
        # Rotate the earth 365 times per year
        self._earth.rotate(angle=radians(self._simulation_speed * 365), axis=self._earth_axis)

        # The moon is in tidal lock so always shows the same face to Earth
        self._moon.rotate(angle=radians(self._simulation_speed * moon_orbit_rate), axis=vec(0, 1, 0))
        # Rotate the Sun with a period of about 22 days
        self._sun.rotate(angle=radians(self._simulation_speed * 16), axis=vec(0, 1, 0))

    def follow_sun(self, camera):
        camera.follow(self._sun)

    def day_count(self):
        return abs(self._earth_angle)

    def show_earth_arrows(self):
        self._earth_arrows.show()

    def hide_earth_arrows(self):
        self._earth_arrows.hide()

    def sun_energy_transfer(self):
        return self._earth_arrows.sun_energy_transfer()

    def simulation_speed(self):
        return self._simulation_speed

    def set_simulation_speed_to(self, value):
        self._simulation_speed = value

def on_mouse_click():
    change_view()

def set_speed():
    sun_earth_moon.set_simulation_speed_to(speed_slider.value)

def change_view():  # define a new function by name
    chosen_object = animation.mouse.pick  # find out which object the user clicked on
    if chosen_object is not None:  # if it is a real object that they clicked on ...
        animation.camera.follow(chosen_object)  # .. then have the camera follow that object

def on_radio_button(event):
    if event.text == 'white background':
        animation.background = color.white if event.checked else color.black
    elif event.text == 'earth arrows':
        sun_earth_moon.show_earth_arrows() if event.checked else sun_earth_moon.hide_earth_arrows()

sun_earth_moon = SunEarthMoonSystem()
animation.append_to_caption("\nAdjust the speed of the simulation using the slider\n")
_ = checkbox(bind=on_radio_button, text='white background', name='background', checked=False)
_ = checkbox(bind=on_radio_button, text='earth arrows', name='arrows', checked=True)
speed_slider = slider(bind=set_speed, value=sun_earth_moon.simulation_speed(), min=0.0, max=1./24.)
animation.append_to_caption("\n\n")


# animation.lights = []    # this gets rid of all the ambient scene lights so that the Sun is the source / the command here blanks an array
sun_earth_moon.follow_sun(animation.camera) # have the camera default to centering on the sun
animation.bind("mousedown", change_view)  # allow mouse clicks to call the changeView function

# place a few sources of light at the same position as the Sun to illuminate the Earth and Moon objects
sunlight = local_light(pos=vec(0, 0, 0), color=color.white)
more_sunlight = local_light(pos=vec(0, 0, 0), color=color.white)  # I found adding two lights was about right


graph_height = 70
graph_width = 480
daylight_graph = graph(width=graph_width, height=graph_height * 4, title="Hours with daylight", xmax=365, ymin=5, ymax=17)
daylight_curve = gcurve(graph=daylight_graph, color=color.red)
equator_curve = gcurve(graph=daylight_graph, color=color.cyan)
_ = [equator_curve.plot(day, 12) for day in range(365)]
energy_curve = gcurve()

new_graph_interval = 30
month_counter = 0
daylight = 0
while sun_earth_moon.day_count() <= 365:  # stop after one year
    rate(100)
    sun_earth_moon.update()

    sun_energy_transfer = sun_earth_moon.sun_energy_transfer()
    energy_curve.plot(sun_earth_moon.day_count(), sun_energy_transfer)

    daylight += sun_energy_transfer
    if sun_energy_transfer == 0 and daylight != 0:
        daylight = daylight * sun_earth_moon.simulation_speed()
        daylight_curve.plot(sun_earth_moon.day_count(), daylight * 35 + 4.25)
        daylight = 0

    if sun_earth_moon.day_count() > month_counter * new_graph_interval:  # new month, new graph
        energy_graph = graph(title="Sunlight in " + list_of_months[month_counter%12], width=graph_width, height=graph_height,
                             xmin=month_counter * new_graph_interval, xmax=(month_counter + 1) * new_graph_interval, ymin=-0.1, ymax=1)
        energy_curve = gcurve(graph=energy_graph, interval=1)
        month_counter += 1




