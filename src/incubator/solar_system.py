# https://github.com/tinchit0/SolarSystem/blob/master/SolarSystem.py

from vpython import *
from random import random
from itertools import combinations

G = 6.67384e-11
UA = 1.495978707e11
mu = G * 1.989e30
dt = 10000

#w = window(width=1000, height=800, menus=False)
disp = canvas(x=5, y=5, width=800, height=600, forward=vector(0, 3, 1), range=1.5 * UA, title='Celestial Mechanics Simulator')


class Planet(sphere):
    List = []

    def __init__(self, *args, **keywords):
        if 'name' in keywords:
            self.name = keywords['name']
            del keywords['name']
        else:
            self.name = 'Unknown'
        if 'mass' in keywords:
            self.mass = keywords['mass']
            del keywords['mass']
        else:
            self.mass = 5.98e24
        if 'virtual_radius' in keywords:
            self.virtual_radius = keywords['virtual_radius']
            del keywords['virtual_radius']
        else:
            self.virtual_radius = 5e9
        if 'real_radius' in keywords:
            self.real_radius = keywords['real_radius']
            del keywords['real_radius']
        else:
            self.real_radius = 6.37e6
        keywords['make_trail'] = True
        keywords['retain'] = 2000
        super(Planet, self).__init__(*args, **keywords)
        self.radius = self.virtual_radius
        self.p = vector(0, 0, 0)
        Planet.List.append(self)

    def set_planet(self, mass, eccentricity, major_semiaxis):
        self.mass = mass
        self.eccentricity = eccentricity
        self.major_semiaxis = major_semiaxis
        self.aphelion = (1 + self.eccentricity) * self.major_semiaxis
        self.pos = rotate(vector(self.aphelion, 0, 0), angle=2 * pi * random(), axis=vector(0, 0, 1))
        speed = sqrt(2 * mu * (1 / self.aphelion - 1 / (2 * self.major_semiaxis)))
        v = speed * cross(self.pos, vector(0, 0, 1)) / self.aphelion
        self.p = v * self.mass


def show_solar_system(event):
    global SolarSystemObjects, CurrentPlanets, Asteroid_Belt, SSOCheckBoxes
    if event.checked:
        for planet_ in SolarSystemObjects:
            planet_.visible = True
            if planet_.name != "Asteroid belt":
                if TrailsCheckBox.checked:
                    planet_.make_trail = True
                if planet_ not in CurrentPlanets:
                    CurrentPlanets.append(planet_)
            checkbox = SSOCheckBoxes[planet_.name]
            checkbox.checked = True
            checkbox.disabled = True
    else:
        for planet_ in SolarSystemObjects:
            if planet_ in CurrentPlanets:
                planet_.make_trail = False
                planet_.visible = False
                CurrentPlanets.pop(CurrentPlanets.index(planet_))
            else:
                planet_.visible = False
            checkbox = SSOCheckBoxes[planet_.name]
            checkbox.checked = False
            checkbox.disabled = False


def change_radius(evt):
    for planet_ in Planet.List:
        planet_.radius = planet_.real_radius if RadiusCheckBox.checked else planet_.virtual_radius


show_planet_trails = True
def change_trails(event):
    global show_planet_trails
    if event.checked:
        for a_planet in CurrentPlanets:
            a_planet.make_trail = True
    else:
        for a_planet in CurrentPlanets:
            a_planet.make_trail = False
            a_planet.clear_trail()


def set_simulation_speed(evt):
    global dt
    dt = speed_slider.value


## Creating Planets #############################
def CreatePlanet(evt):
    global CreateButton
    CreateButton.disabled = True
    #CreateButton.Unbind(wx.EVT_BUTTON)
    disp.bind('mousedown', Preparados)


def Preparados(evt):
    global NewPlanet, v
    global CreateButton, NewPlanet, MassTC, RRTC, VRTC
    posicion_inicial = evt.project(normal=(0, 0, 1))
    mass = float(MassTC.GetValue())
    real_radius = float(RRTC.GetValue())
    virtual_radius = float(VRTC.GetValue())
    NewPlanet = Planet(pos=posicion_inicial, mass=mass, real_radius=real_radius, virtual_radius=virtual_radius,
                       color=(1, 0, 1))
    v = arrow(pos=NewPlanet.pos, axis=(0, 0, 0))
    disp.bind('mousemove', Listos)
    disp.bind('mouseup', YA)


def Listos(evt):
    global v
    new_pos = evt.project(normal=(0, 0, 1))
    v.axis = new_pos - v.pos


def YA(evt):
    global v, NewPlanet, TrailsCheckBox, CurrentPlanets
    v.visible = False
    NewPlanet.p = NewPlanet.mass * v.axis * 3e-7
    if not TrailsCheckBox.GetValue():
        NewPlanet.make_trail = False
    CurrentPlanets.append(NewPlanet)
    CreateButton.Enable(True)
    CreateButton.Bind(wx.EVT_BUTTON, CreatePlanet)
    disp.unbind('mousedown', Preparados)
    disp.unbind('mousemove', Listos)
    disp.unbind('mouseup', YA)


#################################################


# Ship Launching ################################
HoldShip = 0


def CreateShip(evt):
    global Ship, HoldShip, Earth, ShipButton, desv
    ShipButton.Bind(wx.EVT_BUTTON, StopShip)
    ShipButton.SetLabel("Stop")
    direccion_arbitraria = vector(random(), random(), random())
    desv = direccion_arbitraria / mag(direccion_arbitraria) * Earth.radius
    posicion_inicial = Earth.pos + desv
    Ship = Planet(name='Ship', mass=1000, pos=posicion_inicial, color=color.green, virtual_radius=4e9)
    HoldShip = 1
    Ship.p = Earth.p / Earth.mass * Ship.mass
    disp.bind('mousedown', GrabArrow)


def GrabArrow(evt):
    drag_pos = evt.project(normal=(0, 0, 1))
    v = arrow(pos=drag_pos, axis=(0, 0, 0))
    disp.bind('mousemove', DragArrow, v)
    disp.bind('mouseup', DropArrow, v)


def DragArrow(evt, obj):
    new_pos = disp.mouse.project(normal=(0, 0, 1))
    obj.axis = new_pos - obj.pos


def DropArrow(evt, obj):
    global CurrentPlanets, Ship, HoldShip
    deltav = obj.axis * 1e-7
    print("Burn: ", deltav)
    Ship.p += deltav * Ship.mass
    obj.visible = False
    if HoldShip:
        CurrentPlanets.append(Ship)
        HoldShip = 0
    disp.unbind('mousemove', DragArrow)
    disp.unbind('mouseup', DropArrow)


def StopShip(evt):
    ShipButton.Bind(wx.EVT_BUTTON, CreateShip)
    ShipButton.SetLabel("New Ship")
    disp.unbind('mousedown', GrabArrow)


#################################################

# Move planets ##################################
drag_pos = None  # no object picked yet


def move_planet(evt):
    global MoveButton
    MoveButton.text="Stop"
    MoveButton.bind=stop_moving
    disp.bind('mousedown', pick_planet)


def pick_planet(evt):
    global drag_pos
    planet = evt.pick
    drag_pos = planet.pos
    disp.bind('mousemove', moving_planet, planet)
    disp.bind('mouseup', drop_planet)


def moving_planet(evt, obj):
    global drag_pos
    new_pos = disp.mouse.project(normal=(0, 0, 1))
    if new_pos != drag_pos:
        obj.pos += new_pos - drag_pos
        drag_pos = new_pos


def drop_planet(evt):
    disp.unbind('mousemove', moving_planet)
    disp.unbind('mouseup', drop_planet)


def stop_moving(evt):
    MoveButton.text="Move planets"
    MoveButton.bind=move_planet
    disp.unbind('mousedown', pick_planet)


#################################################

def ShowPlanet(event):
    planet_name = event.text
    #print(event.text)
    #print(event.checked)
    planet = Earth
    for planet_ in Planet.List:
        if planet_.name == planet_name:
            planet = planet_
    global SolarSystemObjects, SSOCheckBoxes
    if event.checked:
        planet.visible = True
        if planet_name != 'Asteroid belt':
            CurrentPlanets.append(planet)
            if TrailsCheckBox.checked:
                planet.make_trail = True
    else:
        planet.visible = False
        planet.make_trail = False
        if planet_name != 'Asteroid belt':
            CurrentPlanets.pop(CurrentPlanets.index(planet))
            planet.make_trail = False


## Default Objects (Solar System) ###############
# Sun
Sun = Planet(name="Sun", real_radius=6.96e8, virtual_radius=10e9, mass=1.989e30, color=vec(1, 1, 0), texture="https://i.imgur.com/yoEzbtg.jpg")
# Planets
Mercury = Planet(name="Mercury", real_radius=2.4397e6, virtual_radius=2e9, color=vec(0.7, 0.7, 0.7), texture="https://i.imgur.com/SLgVbwD.jpeg")
Mercury.set_planet(mass=3.302e23, major_semiaxis=0.387098 * UA, eccentricity=0.20563069)
Venus = Planet(name="Venus", real_radius=6.0518e6, virtual_radius=5e9, color=vec(1, 0.8, 0), texture="https://i.imgur.com/YuK3CzJ.jpeg")
Venus.set_planet(mass=4.869e24, major_semiaxis=0.723327 * UA, eccentricity=0.00677323)
Earth = Planet(name="Earth", real_radius=6.3710e6, virtual_radius=6e9, texture=textures.earth)
Earth.set_planet(mass=5.98e24, major_semiaxis=149598261e3, eccentricity=0.01671123)
Mars = Planet(name="Mars", real_radius=3.3895e6, virtual_radius=4e9, color=vec(0.8, 0, 0), texture="https://i.imgur.com/Mwsa16j.jpeg")
Mars.set_planet(mass=6.4185e23, major_semiaxis=1.523679 * UA, eccentricity=0.093315)
Jupiter = Planet(name="Jupiter", real_radius=69.911e6, virtual_radius=15e10, color=vec(0.8, 0.6, 0), texture="https://i.imgur.com/KbVscNb.jpeg")
Jupiter.set_planet(mass=1.899e27, major_semiaxis=5.204267 * UA, eccentricity=0.04839266)
Saturn = Planet(name="Saturn", real_radius=58.232e6, virtual_radius=12e10, color=vec(0.6, 0.5, 0), texture="https://i.imgur.com/r9h0U9E.jpeg")
Saturn.set_planet(mass=5.688e26, major_semiaxis=9.5820172 * UA, eccentricity=0.05415060)
Uranus = Planet(name="Uranus", real_radius=25.362e6, virtual_radius=10e10, color=vec(0.6, 0.6, 1), texture="https://i.imgur.com/2kZNvFw.jpeg")
Uranus.set_planet(mass=8.686e25, major_semiaxis=19.22941195 * UA, eccentricity=0.044405586)
Neptune = Planet(name="Neptune", real_radius=24.622e6, virtual_radius=10e10, color=vec(0, 0, 0.8), texture="https://i.imgur.com/lyLpoMk.jpeg")
Neptune.set_planet(mass=1.024e26, major_semiaxis=30.10366151 * UA, eccentricity=0.00858587)

# TODO ASTEROID BELT
# Asteroid_Belt
#Asteroid_Belt = extrusion(pos=Sun.pos, shape=shapes.circle(radius=2.855 * UA, np=64, thickness=0.795 * UA),  color=vec(0.1, 0.15, 0))
#Asteroid_Belt.name = "Asteroid belt"

#SolarSystemObjects = [Mercury, Venus, Earth, Mars, Asteroid_Belt, Jupiter, Saturn, Uranus, Neptune]
SolarSystemObjects = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune]

CurrentPlanets = [Sun, Earth]
for planet in Planet.List:
    if planet not in CurrentPlanets:
        planet.make_trail = False
        planet.visible = False

# TODO ASTEROID BELT
# Asteroid_Belt.visible = False


# TODO USER INTERACTION
# p = w.panel
disp.append_to_caption("\nSimulation speed\n")
speed_slider = slider(bind=set_simulation_speed, min=-50000, max=200000, value=dt)
disp.append_to_caption("\n\n")
MoveButton = button(text="Move planets", name="MoveButton", bind=move_planet)

ShipButton = button(text="New ship",bind=CreateShip)

OptionsText = wtext(text='\n\nOptions:')
disp.append_to_caption("\n")
RadiusCheckBox = checkbox(text='Use real radius of planets', checked=False, bind=change_radius)

TrailsCheckBox = checkbox(text="View planet trails", checked=True, bind=change_trails)

disp.append_to_caption("\n\n")
_ = checkbox(bind=show_solar_system, text="Show solar system")


SSOCheckBoxes = {}
ShowPlanetFunctions = {}
for i in range(len(SolarSystemObjects)):
    planet = SolarSystemObjects[i]
    disp.append_to_caption("\n\t")
    SSOCheckBoxes[planet.name] = checkbox(text=planet.name, bind=ShowPlanet)
# SSOCheckBoxes = {}
# ShowPlanetFunctions = {}
# for i in range(len(SolarSystemObjects)):
#     planet = SolarSystemObjects[i]
#     SSOCheckBoxes[planet.name] = wx.CheckBox(p, label=planet.name, pos=(650 + 30, 260 + 30 * i))
#     exec
#     "SSOCheckBoxes[planet.name].Bind(wx.EVT_CHECKBOX,lambda evt: ShowPlanet(evt,SolarSystemObjects[" + str(i) + "]))"
SSOCheckBoxes['Earth'].checked = True
#
# wx.StaticText(p, label="Add new planet:", pos=(650, 550))
# wx.StaticLine(p, size=(200, 2), pos=(750, 557))
# wx.StaticText(p, label="Mass:", pos=(650 + 30, 550 + 30 * 1))
# MassTC = wx.TextCtrl(p, value='5.98e24', pos=(650 + 150, 550 + 30 * 1), size=(100, 20))
# wx.StaticText(p, label="Real radius:", pos=(650 + 30, 550 + 30 * 2))
# RRTC = wx.TextCtrl(p, value='6.37e6', pos=(650 + 150, 550 + 30 * 2), size=(100, 20))
# wx.StaticText(p, label="Real radius:", pos=(650 + 30, 550 + 30 * 2))
# RRTC = wx.TextCtrl(p, value='6.37e6', pos=(650 + 150, 550 + 30 * 2), size=(100, 20))
# wx.StaticText(p, label="Virtual radius:", pos=(650 + 30, 550 + 30 * 3))
# VRTC = wx.TextCtrl(p, value='6e9', pos=(650 + 150, 550 + 30 * 3), size=(100, 20))
#
disp.append_to_caption("\n\n")
CreateButton = button(text="Create a planet", bind=CreatePlanet)

# Simulation
while True:
    rate(200)

    # gravitational effect
    for planet1, planet2 in combinations(CurrentPlanets, 2):
        dist = planet1.pos - planet2.pos
        if mag(dist) != 0:
            force = -G * planet1.mass * planet2.mass * dist / mag(dist) ** 3
            planet1.p = planet1.p + force * dt
            planet2.p = planet2.p - force * dt

    # movement
    for planet in CurrentPlanets:
        planet.pos = planet.pos + planet.p / planet.mass * dt
        if mag(planet.pos) > 50 * UA:
            planet.visible = False
            planet.make_trail = False
            CurrentPlanets.pop(CurrentPlanets.index(planet))
            print( "Planet %s abandoned the Solar System" % planet.name)

    # hold ship if not lauched yet
    if HoldShip:
        Ship.pos = Earth.pos + desv
        Ship.p = Earth.p / Earth.mass * Ship.mass