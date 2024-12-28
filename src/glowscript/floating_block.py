#
# Refactored from
# https://github.com/gcschmit/vpython-physics/blob/master/buoyancy/buoyancy.py
#

from vpython import rate, scene, box, color, vector, graph, gcurve

def submerged_volume(object, fluid):
    topOfFluid = fluid.pos.y + fluid.size.y/2
    topOfObject = object.pos.y + object.size.y/2
    bottomOfObject = object.pos.y - object.size.y/2
    
    if topOfObject <= topOfFluid:
        heightSubmerged = object.size.y
    elif bottomOfObject >= topOfFluid:
        heightSubmerged = 0
    else:
        heightSubmerged = (topOfFluid - bottomOfObject)
        
    return (object.size.x * heightSubmerged * object.size.z)

scene.title = "Buoyancy"
scene.background = color.black

fluid = box(size = vector(2, 2, 0.75), color = color.green, opacity = 0.3, density=1000)
floating_object = box(pos = vector(0, 0, 0), v = vector(0, 0, 0), color = color.red, density = 500, size = vector(0.4, 0.4, 0.1))

graphs = graph(title="Buyoancy")
buoyance_curve = gcurve(color=color.magenta)
drag_force_curve = gcurve(color=color.blue)

dragCoefficient = vector(0, -5.0, 0)
g = vector(0, -9.8, 0)

t = 0 
dt = 0.001
while t < 20 and floating_object.pos.y > (fluid.pos.y - fluid.size.y/2) : 
    rate(2/dt)
    
    mass = floating_object.density * floating_object.size.x * floating_object.size.y * floating_object.size.z
    
    net_force =gravitational_force = mass * g
    drag_force = dragCoefficient * floating_object.v.y
    buoyance_force = fluid.density * -g * submerged_volume(floating_object, fluid)    

    net_force = buoyance_force + gravitational_force + drag_force
    acceleration = net_force / mass
    floating_object.v += + acceleration * dt
    floating_object.pos += floating_object.v * dt

    buoyance_curve.plot(t, buoyance_force.y)
    drag_force_curve.plot(t, drag_force.y) 

    t += dt
    