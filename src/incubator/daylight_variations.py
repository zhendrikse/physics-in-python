from vpython import *

latitude = 52  # UK
#  -38 for melbourne
tilt = 23

print("latitude=", latitude, "\ttilt", tilt)

title="""<b>Not</b> to scale Earth-Sun-Moon simulator
It does not include gravitational physics or Newtonian analysis &mdash; just circular motion

&#x2022; Based on the <a href="https://trinket.io/embed/glowscript/575a4ed5d362597041cd6f84">Sun-Earth-Moon model by B. Philhour</a>
&#x2022; Modified by Rob Salgado to model the sunshine seen by the United Kingdom
&#x2022; Updated by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a>
&#x2022; Located in the <a href="https://github.com/zhendrikse/physics-in-python/">Physics in Python GitHub repository</a>

&#x2022; The red arrow points "upward from the UK" (at 52 degrees latitude [from the equator])
&#x2022; The cyan arrow is the rotational axis of the earth, tilted at 23 degrees from vertical
&#x2022; The yellow arrow points from the earth to the sun.
"""

simulation_speed = 0.5
graph_height = 70
graph_width = 480
new_graph_interval = 30
alignment = graph(width=graph_width, height=graph_height, title='sunlight vs t (days)', xmax=new_graph_interval, ymin=-0.1, ymax=1)  # xmax=365
alignmentGraph = gcurve(graph=alignment, interval=1)
t = 0

# constants - use these to change the scale and initial positions of everything
# the basic issue here is that realistic size scales would be impossible to see, 
# so we choose unrealistic values for ease of visualization
sunRadius = 0.2  # note: real value would be 696,000 km, a good choice for sim is 0.1
earthRadius = sunRadius * 0.5  # note: real value would be sunRadius * 0.01, a good choice for sim is * 0.5
moonRadius = earthRadius * 0.27  # note: real value would be earthRadius * 0.27, this is fine for sim
astronomicalUnit = 4.0  # note: real value would be 150,000,000 km, a good choice for sim is 4.0
earthAngle = 0  # this is the angle in degrees representing the Earth's year-long motion around the Sun - so use 0 to 360 (default 0)
moonAngle = 0  # this is an angle in degrees representing the Moon's month-long motion around the Earth - so use 0 to 360 (default 0)
earthMoonDistance = earthRadius * 6  # note that the real value would be earthRadius * 60, a good choice for sim is 6
earthOrbitRate = 1  # the Earth orbits the Sun at about 1 degree per day
moonOrbitRate = 13  # the Moon orbits the Earth at about 13 degrees per day

# set up the scene
# scene.caption.text("Use two-finger swipe to zoom. Use two-finger click/drag to rotate camera.\nClick on an object to change camera focus." +
#                    "\n\nThis simulation is NOT TO ACCURATE SCALE - edit source to play with scale." +
#                    "\n\nUse the slider below to adjust the animation speed or pause the simulation.\n")
# scene.lights = []    # this gets rid of all the ambient scene lights so that the Sun is the source / the command here blanks an array
scene.height = 300
scene.width = 1200  # width in pixels of the display on the screen
# scene.forward = vec(0,-15,0)    # this allows you to change the starting perspective of the camera
scene.range = astronomicalUnit / 4.
scene.fov = radians(10)
scene.title = title

# create the Sun object
sun = sphere(radius=sunRadius, opacity=0.7, emissive=True, texture="http://i.imgur.com/yoEzbtg.jpg")

# place a few sources of light at the same position as the Sun to illuminate the Earth and Moon objects
sunlight = local_light(pos=vec(0, 0, 0), color=color.white)
more_sunlight = local_light(pos=vec(0, 0, 0), color=color.white)  # I found adding two lights was about right

# create the Earth object
earth = sphere(radius=earthRadius, texture=textures.earth, flipx=False, shininess=0.9)

uk_arrow_up = arrow(shaftwidth=earthRadius / 5., axis=vec(sin(radians(0 - (90 - latitude))), cos(radians(0 - (90 - latitude))), 0),
                    color=color.red)
## UK-arrow faces the sun (axisE points away from the sun)... in January
uk_arrow_up.rotate(angle=90 * DEG, axis=vec(0, 1, 0))  # start at midnight
axis_sun_earth = arrow(shaftwidth=earthRadius / 3, color=color.yellow)
axis_earth = arrow(shaftwidth=earthRadius / 5, axis=vec(sin(radians(tilt)), cos(radians(tilt)), 0), color=color.cyan)


# create the Moon
moon = sphere(radius=moonRadius, texture="http://i.imgur.com/YPg4RPU.jpg", flipx=True, flipy=True, shininess=0.9)
scene.camera.follow(sun)  # have the camera default to centering on the sun


# stopped working
# let's allow the user to change the camera view point
def changeView():  # define a new function by name
    chosenObject = scene.mouse.pick()  # find out which object the user clicked on
    if chosenObject is not None:  # if it is a real object that they clicked on ...
        scene.camera.follow(chosenObject)  # .. then have the camera follow that object

scene.bind("mousedown", changeView)  # allow mouse clicks to call the changeView function

# set up a function that interacts with the slider that controls how fast the program animates
simulation_speed = min(simulation_speed, 1 / 24.)  ###RS
programSpeed = simulation_speed  # default setting


# def setspeed():
#     global programSpeed
#     programSpeed = $("#speed_slider").slider("value")
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
#     $("#speed_slider").slider(value=0.02, step=0.0005, min=0, max=0.05, range="min", slide=setspeed, change=setspeed)
#
# )

# below is the main loop of the program - everything above is "setup" and now we are in the main "loop" where all the action occurs
t = 0
tt = 0
accum = 0
while -earthAngle <= 365:  # this will make it NO LONGER loop forever --- IT STOPS AFTER ONE YEAR

    rate(100)  # this limits the animation rate so that it won't depend on computer/browser processor speed

    # update the position of the Earth and Moon by using basic circle trigonometry
    earth.pos = vec(astronomicalUnit * cos(radians(earthAngle)), 0, astronomicalUnit * sin(radians(earthAngle)))
    moon.pos = earth.pos + vec(earthMoonDistance * cos(radians(moonAngle)), 0, earthMoonDistance * sin(radians(moonAngle)))

    ## RS
    tt += 1
    axis_earth.pos = earth.pos
    axis_sun_earth.pos = earth.pos
    uk_arrow_up.pos = earth.pos
    axis_sun_earth.axis = -norm(earth.pos)  # unit-vector on earth pointing to the sun
    uk_arrow_dot_sun_earth_axis = dot(uk_arrow_up.axis, axis_sun_earth.axis)  ## these are unit-vectors (so this is cos(angle between) )
    if uk_arrow_dot_sun_earth_axis > 0:
        alignmentGraph.plot(-earthAngle, uk_arrow_dot_sun_earth_axis)
        accum += uk_arrow_dot_sun_earth_axis
    else:
        alignmentGraph.plot(-earthAngle, 0)  # nighttime... no energy transfer

    if -earthAngle > (t + 1) * new_graph_interval:  # new graph
        t = t + 1
        print("t=", t, "\t accum=", accum, " from tt=", tt, "accum/tt=", accum / tt)
        alignment = graph(width=graph_width, height=graph_height, xmin=t * new_graph_interval, xmax=(t + 1) * new_graph_interval, ymin=-0.1,
                          ymax=1)  # xmax=365
        alignmentGraph = gcurve(graph=alignment, interval=1)
    ## RS

    # Calculate the amount by which the position of the Earth and Moon change each loop cycle
    earthAngle -= earthOrbitRate * programSpeed  # -= means subtract the following  - we subtract to make counterclockwise orbits seen from above
    moonAngle -= moonOrbitRate * programSpeed

    # Because the Earth and Moon to rotate on their own axis - to flip one of them, make the middle entry in the axis vector (-1)
    # Rotate the earth 365 times per year
    uk_arrow_up.rotate(angle=radians(programSpeed * 365), axis=vec(sin(radians(tilt)), cos(radians(tilt)), 0))  
    earth.rotate(angle=radians(programSpeed * 365), axis=vec(sin(radians(tilt)), cos(radians(tilt)), 0))  

    # The moon is in tidal lock so always shows the same face to Earth
    moon.rotate(angle=radians(programSpeed * moonOrbitRate), axis=vec(0, 1, 0))  
    # Rotate the Sun with a period of about 22 days
    sun.rotate(angle=radians(programSpeed * 16), axis=vec(0, 1, 0))  
    

print("t=", t, "\t accum=", accum, " from tt=", tt, "accum/tt=", accum / tt)