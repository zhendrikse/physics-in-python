from vpython import *

title = """<b>Not</b> to scale Earth-Sun-Moon simulator
It does not include gravitational physics or Newtonian analysis &mdash; just circular motion

&#x2022; Based on the <a href="https://trinket.io/embed/glowscript/575a4ed5d362597041cd6f84">Sun-Earth-Moon model by B. Philhour</a>
&#x2022; Modified by Rob Salgado to model the sunshine seen by the United Kingdom
&#x2022; Updated by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a>
&#x2022; Maintained in the <a href="https://github.com/zhendrikse/physics-in-python/">Physics in Python</a> GitHub repository

&#x2022; The red arrow points "upward from the UK" (at 52 degrees latitude [from the equator])
&#x2022; The cyan arrow is the rotational axis of the earth, tilted at 23 degrees from vertical
&#x2022; The yellow arrow points from the earth to the sun.

"""

simulation_speed = 0.5

# constants - use these to change the scale and initial positions of everything
# the basic issue here is that realistic size scales would be impossible to see,
# so we choose unrealistic values for ease of visualization
sun_radius = 0.2  # note: real value would be 696,000 km, a good choice for sim is 0.1
earth_radius = sun_radius * 0.5  # note: real value would be sunRadius * 0.01, a good choice for sim is * 0.5
moon_radius = earth_radius * 0.27  # note: real value would be earthRadius * 0.27, this is fine for sim
astronomical_unit = 4.0  # note: real value would be 150,000,000 km, a good choice for sim is 4.0
earth_angle = 0  # this is the angle in degrees representing the Earth's year-long motion around the Sun - so use 0 to 360 (default 0)
moon_angle = 0  # this is an angle in degrees representing the Moon's month-long motion around the Earth - so use 0 to 360 (default 0)
earth_moon_distance = earth_radius * 6  # note that the real value would be earthRadius * 60, a good choice for sim is 6
earth_orbit_rate = 1  # the Earth orbits the Sun at about 1 degree per day
moon_orbit_rate = 13  # the Moon orbits the Earth at about 13 degrees per day

sun = sphere(radius=sun_radius, opacity=0.7, emissive=True, texture="http://i.imgur.com/yoEzbtg.jpg")
earth = sphere(radius=earth_radius, texture=textures.earth, flipx=False, shininess=0.9)
moon = sphere(radius=moon_radius, texture="http://i.imgur.com/YPg4RPU.jpg", flipx=True, flipy=True, shininess=0.9)

# stopped working
# let's allow the user to change the camera view point
def changeView():  # define a new function by name
    chosenObject = scene.mouse.pick()  # find out which object the user clicked on
    if chosenObject is not None:  # if it is a real object that they clicked on ...
        scene.camera.follow(chosenObject)  # .. then have the camera follow that object

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
scene.camera.follow(sun)  # have the camera default to centering on the sun
scene.bind("mousedown", changeView)  # allow mouse clicks to call the changeView function

# place a few sources of light at the same position as the Sun to illuminate the Earth and Moon objects
sunlight = local_light(pos=vec(0, 0, 0), color=color.white)
more_sunlight = local_light(pos=vec(0, 0, 0), color=color.white)  # I found adding two lights was about right

class EarthArrows:
    def __init__(self, scale=0.5, radius_earth=earth_radius, latitude=52, tilt=23):
        self._scale = scale

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
        self._from_uk_up_arrow.rotate(angle=rotation_angle, axis=vec(sin(radians(tilt)), cos(radians(tilt)), 0))
        self._earth_sun_arrow.axis = -norm(position)

    def sun_energy_transfer(self):
        ## arrows are unit-vectors (times scale factor), so dot product is cos(angle between)
        dot_product = dot(self._from_uk_up_arrow.axis, self._earth_sun_arrow.axis)
        # During nighttime, there is no energy transfer, so set to zero during the night
        energy_transfer = 0 if dot_product <= 0 else dot_product / self._scale
        return energy_transfer

earth_arrows = EarthArrows(latitude=52) # UK latitude, -38 for melbourne
simulation_speed = min(simulation_speed, 1 / 24.)  ###RS
program_speed = simulation_speed  # default setting

# def set_speed():
#     global program_speed
#     program_speed = $("#speed_slider").slider("value")
#
# # stopped working
# # make a place for the animation speed adjuster slider to appear on the scene
# $('<div id="speed_slider"></div>').appendTo(scene.caption).css(width="750px")
#
# # stopped working
# # create and define the actual animation speed adjuster slider
# $(
#
#
# def():
#     $("#speed_slider").slider(value=0.02, step=0.0005, min=0, max=0.05, range="min", slide=set_speed, change=set_speed)
#
# )

list_of_months = ['January', 'February', 'March', 'April',
                  'May', 'June', 'July', 'August',
                  'September', 'October', 'November', 'December']
graph_height = 70
graph_width = 480
new_graph_interval = 30
alignment = graph(width=graph_width, height=graph_height, title="Sunlight in " + list_of_months[0],
                  xmax=new_graph_interval, ymin=-0.1, ymax=1)  # xmax=365
alignment_graph = gcurve(graph=alignment, interval=1)

# below is the main loop of the program - everything above is "setup" and now we are in the main "loop" where all the action occurs
month_counter = 0
hours_counter = 0
accum = 0
while -earth_angle <= 365:  # stop after one year

    rate(100)  # this limits the animation rate so that it won't depend on computer/browser processor speed
    hours_counter += 1

    # update the position of the Earth and Moon by using basic circle trigonometry
    earth.pos = astronomical_unit * vec(cos(radians(earth_angle)), 0, sin(radians(earth_angle)))
    moon.pos = earth.pos + earth_moon_distance * vec(cos(radians(moon_angle)), 0, sin(radians(moon_angle)))

    earth_arrows.update(earth.pos, radians(program_speed * 365))
    sun_energy_transfer = earth_arrows.sun_energy_transfer()
    alignment_graph.plot(-earth_angle, sun_energy_transfer)
    accum += sun_energy_transfer

    if -earth_angle > (month_counter + 1) * new_graph_interval:  # new month, new graph
        month_counter += 1
        print(list_of_months[month_counter], "\t accum=", accum, " from days=", round(hours_counter / 24),
              "accum/hours=", accum / hours_counter)
        alignment = graph(title="Sunlight in " + list_of_months[month_counter], width=graph_width, height=graph_height,
                          xmin=month_counter * new_graph_interval, xmax=(month_counter + 1) * new_graph_interval,
                          ymin=-0.1,
                          ymax=1)  # xmax=365
        alignment_graph = gcurve(graph=alignment, interval=1)

    # Calculate the amount by which the position of the Earth and Moon change each loop cycle
    earth_angle -= earth_orbit_rate * program_speed  # -= means subtract the following  - we subtract to make counterclockwise orbits seen from above
    moon_angle -= moon_orbit_rate * program_speed

    # Because the Earth and Moon to rotate on their own axis - to flip one of them, make the middle entry in the axis vector (-1)
    # Rotate the earth 365 times per year
    earth.rotate(angle=radians(program_speed * 365), axis=vec(sin(radians(tilt)), cos(radians(tilt)), 0))

    # The moon is in tidal lock so always shows the same face to Earth
    moon.rotate(angle=radians(program_speed * moon_orbit_rate), axis=vec(0, 1, 0))
    # Rotate the Sun with a period of about 22 days
    sun.rotate(angle=radians(program_speed * 16), axis=vec(0, 1, 0))

print(list_of_months[month_counter], "\t accum=", accum, " from days=", round(hours_counter) / 24, "accum/hours=",
      accum / hours_counter)
