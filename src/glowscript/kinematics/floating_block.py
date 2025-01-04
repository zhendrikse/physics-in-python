#Web VPython 3.2

from vpython import rate, scene, box, color, vector, graph, gcurve

title = """Floating block

&#x2022; Based on original <a href="https://github.com/gcschmit/vpython-physics/blob/master/buoyancy/buoyancy.py">buoyancy.py</a>
&#x2022; Maintained by <a href="https://github.com/zhendrikse/">Zeger Hendrikse</a> in this <a href="https://github.com/zhendrikse/physics-in-python/">GitHub repository</a>

"""

def submerged_volume(object, fluid):
    top_of_fluid = fluid.pos.y + fluid.size.y/2
    top_of_object = object.pos.y + object.size.y/2
    bottom_of_object = object.pos.y - object.size.y/2
    
    if top_of_object <= top_of_fluid:
        height_submerged = object.size.y
    elif bottom_of_object >= top_of_fluid:
        height_submerged = 0
    else:
        height_submerged = (top_of_fluid - bottom_of_object)
        
    return object.size.x * height_submerged * object.size.z

scene.title = title
scene.background = color.black
scene.forward= vector(-0.52, -0.67, -0.52)
scene.range= 2.


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
    rate(1/dt)
    
    mass = floating_object.density * floating_object.size.x * floating_object.size.y * floating_object.size.z
    
    gravitational_force = mass * g
    drag_force = dragCoefficient * floating_object.v.y
    buoyance_force = fluid.density * -g * submerged_volume(floating_object, fluid)    

    net_force = buoyance_force + gravitational_force + drag_force
    acceleration = net_force / mass
    floating_object.v += + acceleration * dt
    floating_object.pos += floating_object.v * dt

    buoyance_curve.plot(t, buoyance_force.y)
    drag_force_curve.plot(t, drag_force.y) 

    t += dt


print("scene.center=", scene.center)
print("scene.forward=", scene.forward)
print("scene.range=", scene.range)