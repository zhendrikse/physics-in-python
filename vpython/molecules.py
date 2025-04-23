#Web VPython 3.2

from vpython import canvas, vec, color, slider, wtext, radians, sin, cos, sphere, curve, rate, sqrt, radio

title="""&#x2022; Based on <a href="https://glowscript.org/#/user/priisdk/folder/molecules/">this original code and idea</a>
&#x2022; Refactored by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a>

"""

animation = canvas(title=title, background=vec(0.3, 0.2, 0.25),
                forward=vec(10, -8, 5), center=vec(0, 0, 0))#, ambient=color.gray(0.25))

class Atom:
    def __init__(self, radius, colour, position=vec(0, 0, 0)):
        self._sphere = sphere(pos=position, radius=radius, color=colour)
        self._radius = radius

    def hide(self):
        self._sphere.visible = False

    def show(self):
        self._sphere.visible = True

    def scale_by(self, scale_factor):
        self._sphere.radius = self._radius * scale_factor

    def pos(self):
        return self._sphere.pos

class Bond:
    def __init__(self, radius, from_, to_):
        self._bond = curve(pos=[from_, to_], radius=radius, color=color.gray(0.5))

    def hide(self):
        self._bond.visible = False

    def show(self):
        self._bond.visible = True

class Molecule:
    def __init__(self):
        self._atoms = []
        self._bonds = []

    def scale_atomic_radius_by(self, scale):
        for atom in self._atoms:
            atom.scale_by(scale)

    def show(self):
        for atom in self._atoms:
            atom.show()
        for bond in self._bonds:
            bond.show()

    def hide(self):
        for atom in self._atoms:
            atom.hide()
        for bond in self._bonds:
            bond.hide()

class Ammonia(Molecule):
    def __init__(self, bond_radius=0.1, hydrogen_radius = 0.53, nitrogen_radius = 0.65):
        Molecule.__init__(self)

        r0 = 2
        phi = radians(107)
        zN = sqrt((1 + 2 * cos(phi)) / (1 - cos(phi)) / 2) * r0

        positions = [vec(r0, 0, -zN / 2)]
        positions += [vec(-r0 / 2, sqrt(3) * r0 / 2, -zN / 2)]
        positions += [vec(-r0 / 2, -sqrt(3) * r0 / 2, -zN / 2)]
        for position in positions:
            self._atoms.append(Atom(hydrogen_radius, color.white, position))

        position = vec(0, 0, zN / 2)
        for hydrogen in self._atoms:
            self._bonds.append(Bond(bond_radius, position, hydrogen.pos()))

        self._atoms.append(Atom(nitrogen_radius, color.blue, position))


class Methane(Molecule):
    def __init__(self, carbon_radius = 0.25, hydrogen_radius = 0.2, bond_radius=0.05):
        Molecule.__init__(self)
        sin_phi = 1 / 3
        cos_phi = 2 * sqrt(2) / 3

        positions = [vec(0, 1, 0)]
        positions += [vec(cos_phi, -sin_phi, 0)]
        positions += [vec(-cos_phi / 2, -sin_phi,  sqrt(3) / 2 * cos_phi)]
        positions += [vec(-cos_phi / 2, -sin_phi, -sqrt(3) / 2 * cos_phi)]
        for position in positions:
            self._atoms.append(Atom(hydrogen_radius, color.white, position))

        position = vec(0, 0, 0)
        for hydrogen in self._atoms:
            self._bonds.append(Bond(bond_radius, position, hydrogen.pos()))

        self._atoms.append(Atom(carbon_radius, color.black, position))


class Water(Molecule):
    def __init__(self, oxygen_radius = 0.3, hydrogen_radius = 0.2, bond_radius=0.05):
        Molecule.__init__(self)

        phi_hydrogen = radians(104.5) / 2
        sin_phi = sin(phi_hydrogen)
        cos_phi = cos(phi_hydrogen)

        positions = [vec(0, cos_phi, sin_phi), vec(0, cos_phi, -sin_phi)]
        for position in positions:
            self._atoms.append(Atom(hydrogen_radius, color.red, position))

        position = vec(0, 0, 0)
        for hydrogen in self._atoms:
            self._bonds.append(Bond(bond_radius, position, hydrogen.pos()))

        self._atoms.append(Atom(oxygen_radius, color.blue, position))

class Ethanol(Molecule):
    def __init__(self, carbon_radius=0.25, oxygen_radius=0.3, hydrogen_radius=0.2, bond_radius=0.05):
        Molecule.__init__(self)

        hydrogen_positions = [vec(1, -1/2, -1/2), vec(1, -1/2, 1/2)]
        hydrogen_positions += [vec(-1.25, 1/2, -1/2), vec(-1.25, 1/2, 1/2)]
        hydrogen_positions += [vec(-1.1, -1/2, 0), vec(1.75, 0.75, 0)]
        for position in hydrogen_positions:
            self._atoms.append(Atom(hydrogen_radius, color.white, position))

        carbon_positions = [vec(1/2, 0, 0), vec(-1/2, 0, 0)]
        for position in carbon_positions:
            self._atoms.append(Atom(carbon_radius, color.black, position))
        self._bonds.append(Bond(bond_radius, carbon_positions[1], carbon_positions[0]))

        for i in range(len(hydrogen_positions) - 1):
            carbon_position = carbon_positions[0] if i == 0 or i == 1 else carbon_positions[1]
            self._bonds.append(Bond(bond_radius, carbon_position, hydrogen_positions[i]))

        oxygen_position = vec(1, 1, 0)
        self._atoms.append(Atom(oxygen_radius, color.red, oxygen_position))

        self._bonds.append(Bond(bond_radius, hydrogen_positions[5], oxygen_position))
        self._bonds.append(Bond(bond_radius, carbon_positions[0], oxygen_position))

class LacticAcid(Molecule):
    def __init__(self, carbon_radius=0.25, oxygen_radius=0.3, hydrogen_radius=0.2, bond_radius=0.05):
        Molecule.__init__(self)
        sqrt3=sqrt(3)
        sqrt3h=sqrt3/2
        sin_phi=1/3
        cos_phi=2*sqrt(2)/3

        carbon_positions = [vec(-1, 0, 0), vec(0 ,0, 0), vec(sin_phi, -cos_phi / 2, -sqrt3h * cos_phi)]
        for position in carbon_positions:
            self._atoms.append(Atom(carbon_radius, color.black, position))

        hydrogen_positions = [vec(-1 - sin_phi, -cos_phi, 0), vec(-1 - sin_phi, cos_phi / 2,sqrt3h * cos_phi)]
        hydrogen_positions += [vec(-1 - sin_phi,cos_phi / 2, -sqrt3h * cos_phi), vec(sin_phi, -cos_phi / 2, 0 + sqrt3h * cos_phi)]
        hydrogen_positions += [vec(1.25 + sin_phi,-0.5 - cos_phi / 2, -1.25 - sqrt3h * cos_phi)] #Denne her sidder på O[1]
        hydrogen_positions += [vec(0.75 - sin_phi, 1 + cos_phi / 2, +sqrt3h * cos_phi)] # Denne her sidder på det ensomme O-atom O[0]
        for position in hydrogen_positions:
            self._atoms.append(Atom(hydrogen_radius, color.white, position))

        oxygen_positions = [vec(0.75, 1, 0)]
        oxygen_positions += [vec(1.25, -0.5, -1.25)]
        oxygen_positions += [vec(0.25, -1.25, -1.25)] # Double bond is located here
        for position in oxygen_positions:
            self._atoms.append(Atom(oxygen_radius, color.red, position))

        self._bonds.append(Bond(bond_radius, carbon_positions[1], hydrogen_positions[3]))
        self._bonds.append(Bond(bond_radius, carbon_positions[1], oxygen_positions[0]))
        self._bonds.append(Bond(bond_radius, carbon_positions[2], oxygen_positions[1]))
        self._bonds.append(Bond(2.5 * bond_radius, carbon_positions[2], oxygen_positions[2]))
        self._bonds.append(Bond(bond_radius, oxygen_positions[1], hydrogen_positions[4]))
        self._bonds.append(Bond(bond_radius, carbon_positions[2], oxygen_positions[1]))
        self._bonds.append(Bond(bond_radius, hydrogen_positions[5], oxygen_positions[0]))
        self._bonds.append(Bond(bond_radius, carbon_positions[0], hydrogen_positions[0]))
        self._bonds.append(Bond(bond_radius, carbon_positions[0], hydrogen_positions[1]))
        self._bonds.append(Bond(bond_radius, carbon_positions[0], hydrogen_positions[2]))
        self._bonds.append(Bond(bond_radius, carbon_positions[0], carbon_positions[1]))
        self._bonds.append(Bond(bond_radius, carbon_positions[1], carbon_positions[2]))

class RadioButton:
    def __init__(self, button_, molecule_):
        self._button = button_
        self._molecule = molecule_

    def uncheck(self):
        self._button.checked = False

    def push(self, button_name):
        self._molecule.show()

    def check(self):
        self._button.checked = True

    def name(self):
        return self._button.name

class RadioButtons:
    def __init__(self):
        self._radio_buttons = []
        self._selected_button = None

    def add(self, button_, molecule_):
        self._radio_buttons.append(RadioButton(button_, molecule_))

        if (len(self._radio_buttons) % 5) == 0:
            animation.append_to_caption("\n\n")

        if (len(self._radio_buttons)) == 1:
            self._radio_buttons[0].check()
            self._selected_button = self._radio_buttons[0]

    def _uncheck_buttons_except(self, button_name):
        for button_ in self._radio_buttons:
            if button_.name() != button_name: button_.uncheck()

    def _get_button_by(self, button_name):
        for button_ in self._radio_buttons:
            if button_.name() == button_name: return button_

    def toggle(self, button_name):
        self._uncheck_buttons_except(button_name)
        self._selected_button = self._get_button_by(button_name)
        self._selected_button.push(button_name)

    def get_selected_button_name(self):
        return self._selected_button.name()

molecules = {"Water": Water(), "Methane": Methane(), "Ammonia": Ammonia(), "Ethanol": Ethanol(), "Lactic acid": LacticAcid()}

for molecule in molecules.values():
    molecule.hide()

molecules["Water"].show()

################
# GUI controls #
################

def toggle(event):
    for molecule_ in molecules.values():
        molecule_.hide()
    radio_buttons.toggle(event.name)

def on_radius_change(s):
    wt.text = 'Atomic radius scale factor: {:1.2f}'.format(s.value)
    for molecule_ in molecules.values():
        molecule_.scale_atomic_radius_by(radius_slider.value)

radio_buttons = RadioButtons()
for name in molecules.keys():
    radio_buttons.add(radio(bind=toggle, text=name + " ", name=name), molecules[name])

animation.append_to_caption("\n\n")
radius_slider = slider(min=0.5, max=3, value=1, bind=on_radius_change)
wt = wtext(text=' Atomic radius scale factor: {:1.2f}'.format(radius_slider.value))

while True:
    rate(10)

