### SETUP ELEMENTS FOR GRAPHING, SIMULATION, VISUALIZATION, TIMING
# ------------------------------------------------------------------------

from vpython import scene, color, box, vector,sqrt, rate, curve

from toolbox.physics_timer import PhysTimer
from toolbox.physics_axis import PhysAxis

# Set window title
scene.title = "Length Contraction"

# Make scene background black
scene.background=color.black

# Define scene objects
track = box(pos =vector(0,-1.5,0), size=vector(10,.1,.1),color = color.green) # units are in meters
car = box(size=vector(1 ,1, 1), color = color.yellow) # units are in meters

# Define axis that marks the track with a specified number of tick marks
axis = PhysAxis(track, 11, startPos=vector(-5, -2, 0))

# Set up trail to mark the car's trajectory
trail = curve(color = color.yellow, radius = 0.1) # units are in meters

# Set timer in top right of screen (units are in meters)
timerDisplay = PhysTimer(4, 4.5, useScientific=True)


### SETUP PARAMETERS AND INITIAL CONDITIONS
# ----------------------------------------------------------------------------------------

# Define parameters
c = 3e8 # speed of light in m/s

car.m = 1.0 # mass of car in kg
car.pos = vector(0,0,0) # initial position of the car in(x, y, z) form, units are in meters
car.v = vector(2.9e7, 0, 0) # initial velocity of car in (vx, vy, vz) form, units are in m/s

# calculate the Lorentz factors based on the car's velocity in each direction
lorentzFactors = (1 / (sqrt(1 - (car.v.x**2 / c**2))), 
      1 / (sqrt(1 - (car.v.y**2 / c**2))),
      1 / (sqrt(1 - (car.v.z**2 / c**2))))

# adjust the size of the car to account for length contraction
car.size = vector(car.size.x / lorentzFactors[0], 
      car.size.y / lorentzFactors[1], 
      car.size.z / lorentzFactors[2]) 


# Define time parameters
t=0 # starting time
deltat = 1e-11  # time step units are s


### CALCULATION LOOP; perform physics updates and drawing
# ------------------------------------------------------------------------------------

# while the car's x-position is between -4.5 m and 4.5 m
while -4.5 < car.pos.x < 4.5:
 
    # Required to make animation visible / refresh smoothly (keeps program from running faster
    #    than 1000 frames/s)
    rate(1000)    

    # Compute Net Force 
    Fnet = vector(0,0,0) 

    # Newton's 2nd Law 
    car.v = car.v + Fnet/car.m * deltat

    # Position update 
    car.pos = car.pos + car.v*deltat

    # Update timer, graph, and trail
    timerDisplay.update(t)

    # Time update 
    t = t + deltat
    
### OUTPUT
# --------------------------------------------------------------------------------------

# Print the final time and the car's size
print(t)
print(car.size)