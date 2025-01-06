# https://github.com/tinchit0/SolarSystem/blob/master/SolarSystem.py

from vpython import *
from random import random
from itertools import combinations

G = 6.67384e-11
UA = 1.495978707e11
mu = G * 1.989e30
dt = 10000

#w = window(width=1000, height=800, menus=False)
disp = canvas(x=5, y=5, width=600, height=750, forward=vector(0, 3, 1), range=1.5 * UA, title='Celestial Mechanics Simulator')


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

    def SetPlanet(self, mass, excentricity, major_semiaxis):
        self.mass = mass
        self.excentricity = excentricity
        self.major_semiaxis = major_semiaxis
        self.aphelion = (1 + self.excentricity) * self.major_semiaxis
        self.pos = rotate(vector(self.aphelion, 0, 0), angle=2 * pi * random(), axis=vector(0, 0, 1))
        speed = sqrt(2 * mu * (1 / self.aphelion - 1 / (2 * self.major_semiaxis)))
        v = speed * cross(self.pos, vector(0, 0, 1)) / self.aphelion
        self.p = v * self.mass


def ShowSolarSystem(event):
    global SolarSystemObjects, CurrentPlanets, Asteroid_Belt, SSOCheckBoxes
    if event.checked:
        for planet in SolarSystemObjects:
            planet.visible = True
            if planet.name != "Asteroid belt":
                if TrailsCheckBox.GetValue():
                    planet.make_trail = True
                if planet not in CurrentPlanets:
                    CurrentPlanets.append(planet)
            checkbox = SSOCheckBoxes[planet.name]
            checkbox.SetValue(True)
            checkbox.Enable(False)
    else:
        newplanetlist = []
        for planet in SolarSystemObjects:
            if planet in CurrentPlanets:
                planet.make_trail = False
                planet.visible = False
                CurrentPlanets.pop(CurrentPlanets.index(planet))
            else:
                planet.visible = False
            checkbox = SSOCheckBoxes[planet.name]
            checkbox.SetValue(False)
            checkbox.Enable(True)


def ChangeRadius(evt):
    if RadiusCheckBox.GetValue():
        for planet in Planet.List:
            planet.radius = planet.real_radius
    else:
        for planet in Planet.List:
            planet.radius = planet.virtual_radius


show_planet_trails = True
def ChangeTrails(event):
    global show_planet_trails
    if event.checked:
        for a_planet in CurrentPlanets:
            a_planet.make_trail = True
    else:
        for a_planet in CurrentPlanets:
            a_planet.make_trail = False


def set_simulation_speed(evt):
    global dt
    dt = speed_slider.value


## Creating Planets #############################
def CreatePlanet(evt):
    global CreateButton
    CreateButton.Enable(False)
    CreateButton.Unbind(wx.EVT_BUTTON)
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


def MovePlanet(evt):
    global MoveButton
    MoveButton.SetLabel("Stop")
    MoveButton.Bind(wx.EVT_BUTTON, StopMoving)
    disp.bind('mousedown', PickPlanet)


def PickPlanet(evt):
    global drag_pos
    planet = evt.pick
    drag_pos = planet.pos
    disp.bind('mousemove', MovingPlanet, planet)
    disp.bind('mouseup', DropPlanet)


def MovingPlanet(evt, obj):
    global drag_pos
    new_pos = disp.mouse.project(normal=(0, 0, 1))
    if new_pos != drag_pos:
        obj.pos += new_pos - drag_pos
        drag_pos = new_pos


def DropPlanet(evt):
    disp.unbind('mousemove', MovingPlanet)
    disp.unbind('mouseup', DropPlanet)


def StopMoving(evt):
    MoveButton.SetLabel("Move planets")
    MoveButton.Bind(wx.EVT_BUTTON, MovePlanet)
    disp.unbind('mousedown', PickPlanet)


#################################################

def ShowPlanet(event):
    planet_name = event.text
    global SolarSystemObjects, SSOCheckBoxes
    if event.checked:
        planet.visible = True
        if planet_name != 'Asteroid belt':
            CurrentPlanets.append(planet)
            if show_planet_trails:
                planet.make_trail = True
    else:
        planet.visible = False
        if planet_name != 'Asteroid belt':
            CurrentPlanets.pop(CurrentPlanets.index(planet))
            planet.make_trail = False


## Default Objects (Solar System) ###############
# Sun
Sun = Planet(name="Sun", real_radius=6.96e8, virtual_radius=10e9, mass=1.989e30, color=vec(1, 1, 0))
# Planets
Mercury = Planet(name="Mercury", real_radius=2.4397e6, virtual_radius=2e9, color=vec(0.7, 0.7, 0.7))
Mercury.SetPlanet(mass=3.302e23, major_semiaxis=0.387098 * UA, excentricity=0.20563069)
Venus = Planet(name="Venus", real_radius=6.0518e6, virtual_radius=5e9, color=vec(1, 0.8, 0))
Venus.SetPlanet(mass=4.869e24, major_semiaxis=0.723327 * UA, excentricity=0.00677323)
Earth = Planet(name="Earth", real_radius=6.3710e6, virtual_radius=6e9, material=textures.earth)
Earth.SetPlanet(mass=5.98e24, major_semiaxis=149598261e3, excentricity=0.01671123)
Mars = Planet(name="Mars", real_radius=3.3895e6, virtual_radius=4e9, color=vec(0.8, 0, 0))
Mars.SetPlanet(mass=6.4185e23, major_semiaxis=1.523679 * UA, excentricity=0.093315)
Jupiter = Planet(name="Jupiter", real_radius=69.911e6, virtual_radius=15e10, color=vec(0.8, 0.6, 0))
Jupiter.SetPlanet(mass=1.899e27, major_semiaxis=5.204267 * UA, excentricity=0.04839266)
Saturn = Planet(name="Saturn", real_radius=58.232e6, virtual_radius=12e10, color=vec(0.6, 0.5, 0))
Saturn.SetPlanet(mass=5.688e26, major_semiaxis=9.5820172 * UA, excentricity=0.05415060)
Uranus = Planet(name="Uranus", real_radius=25.362e6, virtual_radius=10e10, color=vec(0.6, 0.6, 1))
Uranus.SetPlanet(mass=8.686e25, major_semiaxis=19.22941195 * UA, excentricity=0.044405586)
Neptune = Planet(name="Neptune", real_radius=24.622e6, virtual_radius=10e10, color=vec(0, 0, 0.8))
Neptune.SetPlanet(mass=1.024e26, major_semiaxis=30.10366151 * UA, excentricity=0.00858587)

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
#
# MoveButton = wx.Button(p, label="Move planets", pos=(650, 90))
# MoveButton.Bind(wx.EVT_BUTTON, MovePlanet)

# ShipButton = wx.Button(p, label="New ship", pos=(750, 90))
# ShipButton.Bind(wx.EVT_BUTTON, CreateShip)
#
# OptionsText = wx.StaticText(p, label='Options:', pos=(650, 140))
# RadiusCheckBox = wx.CheckBox(p, label='Use real radius of planets', pos=(650, 170))
# RadiusCheckBox.Bind(wx.EVT_CHECKBOX, ChangeRadius)
# RadiusCheckBox.SetValue(False)

TrailsCheckBox = checkbox(text="View planet trails", checked=True, bind=ChangeTrails)
# TrailsCheckBox = wx.CheckBox(p, label='View planet trails', pos=(650, 200))
# TrailsCheckBox.Bind(wx.EVT_CHECKBOX, ChangeTrails)
# TrailsCheckBox.SetValue(True)

_ = checkbox(bind=ShowSolarSystem, text="Show solar system")
# SSCheckBox = wx.CheckBox(p, label='Show Solar System', pos=(650, 230))
# SSCheckBox.Bind(wx.EVT_CHECKBOX, ShowSolarSystem)

SSOCheckBoxes = {}
ShowPlanetFunctions = {}
for i in range(len(SolarSystemObjects)):
    planet = SolarSystemObjects[i]
    SSOCheckBoxes[planet.name] = checkbox(text=planet.name, bind=ShowPlanet)
# SSOCheckBoxes = {}
# ShowPlanetFunctions = {}
# for i in range(len(SolarSystemObjects)):
#     planet = SolarSystemObjects[i]
#     SSOCheckBoxes[planet.name] = wx.CheckBox(p, label=planet.name, pos=(650 + 30, 260 + 30 * i))
#     exec
#     "SSOCheckBoxes[planet.name].Bind(wx.EVT_CHECKBOX,lambda evt: ShowPlanet(evt,SolarSystemObjects[" + str(i) + "]))"
# SSOCheckBoxes['Earth'].SetValue(True)
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
# CreateButton = wx.Button(p, label="Create a planet", pos=(850, 700))
# CreateButton.Bind(wx.EVT_BUTTON, CreatePlanet)

# Simulation
while True:
    rate(200)

    # gravitational effect
    for planet1, planet2 in combinations(CurrentPlanets, 2):
        dist = planet1.pos - planet2.pos
        #if mag(dist) != 0:
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