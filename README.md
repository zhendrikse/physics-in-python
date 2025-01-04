# Physics in Python &mdash; introduction

This repository contains physics demos, based on 
[_testable_](https://medium.com/ns-techblog/tdd-or-how-i-learned-to-stop-worrying-and-love-writing-tests-ef7314470305) code! 
The graphics library used is [VPython](https://vpython.org/).

All animations can be viewed on [my glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/) page.

### Repository contents

- [**`src`**](src) &rarr; contains the sources
- [**`test`**](test) &rarr; the tests of the components in the generic toolbox

# Electromagnetism

The code pertaining to the demos in this section is available under the 
[electromagnetism tab](https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/)
on [glowscript.org](https://glowscript.org).

## Electric fields of dipoles and point charges

The following code snippets visualize the electric fields around dipoles and point charges. 
You may zoom in at any particular point by clicking your mouse button.

<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Pointchargefield">
  <img alt="Electric field of point charge" width="45%" height="45%" src="./src/demos/images/point_charge.png" title="Click to animate"/>
</a>
<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Electricdipolefield">
  <img alt="Electric field of a dipole" width="40%" height="40%" src="./src/demos/images/dipole_field.png" title="Click to animate"/>
</a>

- Point charge field action [on Trinket](https://zegerh-6085.trinket.io/sites/point_charge) and
  in action [on glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Pointchargefield)
- Point charge field code base [on Trinket](https://trinket.io/glowscript/96da4eb68335)


- Dipole field in action [on Trinket](https://zegerh-6085.trinket.io/sites/dipole) and
  in action [on glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Electricdipolefield)
- Dipole field code base [on Trinket](https://trinket.io/glowscript/a2b8b655fa07)

## Interactive visualization of electric and magnetic fields

The first dynamic simulation illustrates Faraday's law by visualizing an electric current (of electric charges) running through a wire. 
The second static simulation shows the electric field inside a series of charged rings.

<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Faradayslaw">
  <img alt="Faraday's law" width="45%" height="45%" src="./src/demos/images/faradays_law.png" title="Click to animate"/>
</a>
<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Chargedrings">
  <img alt="Charged rings" width="45%" height="45%" src="./src/demos/images/charged_rings.png" title="Click to animate"/>
</a>

- Faraday's law in action [on Trinket](https://zegerh-6085.trinket.io/sites/faradays_law) and
  in action [on glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Faradayslaw)
- Code base [on Trinket](https://trinket.io/library/trinkets/d3934e117c2e)


- Charged rings in action [on Trinket](https://zegerh-6085.trinket.io/sites/charged_rings) and
  in action [on glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Chargedrings)
- Code base [on Trinket](https://trinket.io/library/trinkets/0a61629dcbdb)

## Electron spinning around a charged ring

The following demos show the movement of an electron in two different electric fields. 

In the first case, an electron is spinning around a charged ring, as opposed to a point-like charged nucleus.
The charge that normally resides in the nucleus is evenly spread out across the ring.

In the second case, the path of an electron is visualized when traversing an electric field 
generated by the two plates of a charged capacitor.

<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Chargedring">
  <img alt="Electron spinning around charged ring" width="45%" height="45%" src="./src/demos/images/electron_and_charged_ring.png" title="Click to animate"/>
</a>
<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Movingcharge">
  <img alt="Particle in electric field" width="45%" height="45%" src="./src/demos/images/particle_in_electric_field.png" title="Click to animate"/>
</a>

- Charged ring in action [on Trinket](https://zegerh-6085.trinket.io/sites/electron_and_charged_ring) 
  and in action [on glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Chargedring)
- Charged ring code base [on Trinket](https://trinket.io/library/trinkets/1983b9c1dc58)


- Charged plates in action [on Trinket](https://zegerh-6085.trinket.io/sites/moving_charge) 
  and in action [on glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Chargedring)
- Charged plates code base [on Trinket](https://trinket.io/glowscript/db4616ccd73c)

## Charged disk and accompanying builder

Two rather simple demos that show the electric field around a disk. The builder allows a step-by-step
set-up of the disk by adding a charged ring at each mouse click.

<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Chargeddisk">
  <img alt="Charged disk" width="40%" height="40%" src="./src/demos/images/charged_disk.png" title="Click to animate"/>
</a>
<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Chargeddiskbuilder">
  <img alt="Charged disk builder" width="50%" height="50%" src="./src/demos/images/charged_disk_builder.png" title="Click to animate"/>
</a>

- Charged disk in action [on Trinket](https://zegerh-6085.trinket.io/sites/charged_disk) 
  and in action [on glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Chargeddisk)
- Charged disk code base [on Trinket](https://trinket.io/library/trinkets/93fcb16edcea)


- Charged disk builder in action [on Trinket](https://zegerh-6085.trinket.io/sites/charged_disk_builder)
  and in action [on glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Chargeddiskbuilder)
- Charged disk builder code base [on Trinket](https://trinket.io/library/trinkets/3456b49e462d)


## Visualization of electromagnetic waves

Both of the two dynamic simulations below visualize the propagation of electromagnetic waves. In the first demo,
the electromagnetic waves emanate from an antenna, in the second they are propagating through a vacuum.

<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Antenna">
  <img alt="Antenna" width="45%" height="45%" src="./src/demos/images/antenna.png" title="Click to animate"/>
</a>
<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Electromagneticwave">
  <img alt="Electromagnetic waves" width="50%" height="50%" src="./src/demos/images/electromagnetic_wave.png" title="Click to animate"/>
</a>

- Antenna in action [on Trinket](https://zegerh-6085.trinket.io/sites/antenna) 
  and in action [on glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Antenna)
- Antenna code base [on Trinket](https://trinket.io/library/trinkets/32ca075649d6)


- Electromagnetic waves in action [on Trinket](https://zegerh-6085.trinket.io/sites/electromagnetic_wave)
  and in action [on glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Electromagneticwave)
- Electromagnetic waves code [on Trinket](https://trinket.io/library/trinkets/b8d62b38e852)

## Symmetry planes within a cubic lattice

This simple visualization allows the viewer to alternate between some planes of symmetry within a cubic crystal.

<a href="https://www.glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Crystalsymmetryplanes ">
  <img alt="Symmetry planes" width="40%" height="40%" src="./src/demos/images/crystal_planes.png" title="Click to animate"/>
</a>

- Code in action [on Trinket](https://zegerh-6085.trinket.io/sites/relativistic_proton) 
  and in action [on glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Crystalsymmetryplanes)
- Code base [on Trinket](https://trinket.io/library/trinkets/78efbf3b2a97)

# Special relativity &mdash; space-time visualizations and more

The code pertaining to the demos in this section is available under the 
[relativity tab](https://glowscript.org/#/user/zeger.hendrikse/folder/Relativity/)
on [glowscript.org](https://glowscript.org).

## Lightcone animation and electric field of a fast moving proton

A three-dimensional lightcone is animated by simultaneously 
sending off both a photon and a spaceship from the origin.

The other code snippet visualizes an electric field of a
fast moving (relativistic) proton.

<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Relativity/program/Lightcone">
  <img alt="Light cone" width="40%" height="40%" src="./src/demos/images/lightcone.png" title="Click to animate"/>
</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Relativity/program/Relativisticproton">
  <img alt="Relativistic proton" width="30%" height="30%" src="./src/demos/images/relativistic_proton.png" title="Click to animate"/>
</a>

- Moving proton in action [on Trinket](https://zegerh-6085.trinket.io/sites/relativistic_proton) 
  and in action [on glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/folder/Relativity/program/Relativisticproton)
- Proton code base [on Trinket](https://trinket.io/library/trinkets/2aaad6e82cc4)


- Lightcone animation [on Trinket](https://zegerh-6085.trinket.io/sites/lightcone) 
  and in action [on glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/folder/Relativity/program/Lightcone)
- Lightcocne code base [on Trinket](https://trinket.io/library/trinkets/2afb9d937b95)

## Galilean transformation of relative motions in Euclidean plane

Before diving into (special) relativity, let's first get acquainted with 
the so-called Galilean transformation.

<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Relativity/program/Glalileantransformation">
  <img alt="Galilean space-time" width="50%" height="50%" src="./src/demos/images/galilean_space_time.png" title="Click to animate"/>
</a>

- Code in action [on Trinket](https://zegerh-6085.trinket.io/sites/galileo_space_time) 
  and in action [on glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/folder/Relativity/program/Glalileantransformation)
- Code base [on Trinket](https://trinket.io/library/trinkets/6499b8e78c27)

# Coming soon: Minkowski space-time

This is currently under construction

# Thermodynamics

The code pertaining to the demos in this section is available under the 
[thermodynamics tab](https://glowscript.org/#/user/zeger.hendrikse/folder/Thermodynamics/)
on [glowscript.org](https://glowscript.org).

## Visualizing a hard sphere gas model

This model represents a Boltzmann gas (consisting of hard spheres) in a box, where 
the velocity distribution of the colliding atoms eventually approaches the calculated 
theoretical velocity distribution.

<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Thermodynamics/program/Hardspheregas">
  <img alt="Hard sphere gas" width="40%" height="40%" src="./src/demos/images/hard_sphere_gas.png" title="Click to animate"/>
</a>

- Code in action [on Trinket](https://zegerh-6085.trinket.io/sites/hard_sphere_gas) 
  and in action [on glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/folder/Thermodynamics/program/Hardspheregas)
- Code base [on Trinket](https://trinket.io/library/trinkets/554248a15bc4)

## Two-dimensional Ising spin model

This demo models the magnetization at various temperatures using a two-dimensional Ising spin lattice.

<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Thermodynamics/program/Isingspin">
  <img alt="Ising spin model" width="40%" height="40%" src="./src/demos/images/ising_spin_model.png" title="Click to animate"/>
</a>

- Ising spin in action [on Trinket](https://zegerh-6085.trinket.io/sites/ising_spin_model) 
  and in action [on glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/folder/Thermodynamics/program/Isingspin)
- Ising spin code base [on Trinket](https://trinket.io/library/trinkets/07404ee90b64)

# Quantum &amp; wave mechanics

The code pertaining to the demos in this section is available under the 
[quantum tab](https://glowscript.org/#/user/zeger.hendrikse/folder/Quantum/)
on [glowscript.org](https://glowscript.org).

## [Doppler effect]()

<a href="https://www.glowscript.org/#/user/zeger.hendrikse/folder/Quantum/program/Dopplereffect">
  <img alt="Doppler effect" width="50%" height="50%" src="./src/demos/images/doppler_effect.png" title="Click to animate"/>
</a>


- Doppler effect in action [on Trinket](https://zegerh-6085.trinket.io/sites/doppler_effect) 
  and in action [on glowscript.org](https://www.glowscript.org/#/user/zeger.hendrikse/folder/Quantum/program/Dopplereffect)
- The code base [on Trinket](https://trinket.io/library/trinkets/9d869c1167ec)

## The quantum harmonic oscillator

The quantum harmonic oscillator is visualized in a semi-classical way below.

<a href="https://www.glowscript.org/#/user/zeger.hendrikse/folder/Quantum/program/Quantumoscillator">
  <img alt="Quantum oscillator" width="50%" height="50%" src="./src/demos/images/quantum_oscillator.png" title="Click to animate"/>
</a>

- Quantum oscillator in action [on Trinket](https://zegerh-6085.trinket.io/sites/quantum_oscillator) 
  and in action [on glowscript.org](https://www.glowscript.org/#/user/zeger.hendrikse/folder/Quantum/program/Quantumoscillator)
- Quantum oscillator code base [on Trinket](https://trinket.io/library/trinkets/555f7535fe74)


# Astrophysics

The code pertaining to the demos in this section is available under the 
[astrophysics tab](https://glowscript.org/#/user/zeger.hendrikse/folder/Astrophysics/)
on [glowscript.org](https://glowscript.org).


##  Kepler's law of equal areas

A dynamic visualization of Kepler's laws.

<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Astrophysics/program/Keplerslaw">
  <img alt="Kepler's laws" width="50%" height="50%" src="./src/demos/images/keplers_law.png" title="Click to animate"/>
</a>

- Code in action [on Trinket](https://zegerh-6085.trinket.io/sites/keplers_law) 
  and in action [on glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/folder/Astrophysics/program/Keplerslaw)
- Code base [on Trinket](https://trinket.io/library/trinkets/11c6cd8b5622)


## Daylight variations &mdash; sun-earth-moon model

A not accurate to scale sun-earth-moon model, but very detailed and instructive nonetheless! It shows the per day
incoming energy from the sun (at a given latitude), as well as the variations in the length of
the days per season. By clicking on the sun or earth, the camera perspective can be changed as well!

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Astrophysics/program/Daylightvariations">
  <img alt="Daylight variations" width="50%" height="50%" src="./src/demos/images/daylight_variations.png" title="Click to animate"/>
</a>

- Code in action [on Trinket](https://zegerh-6085.trinket.io/sites/daylight_variations) 
  and in action [on glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/folder/Astrophysics/program/Daylightvariations)
- Code base [on Trinket](https://trinket.io/library/trinkets/d218d43e551a)

# Kinematics

The code pertaining to the demos in this section is available under the 
[kinematics tab](https://glowscript.org/#/user/zeger.hendrikse/folder/Kinematics/)
on [glowscript.org](https://glowscript.org).

## Fun with springs

The applications of a simple harmonic oscillator are almost endless. 
You may be surprised though to find out what happens when you drop such a simple harmonic oscillator!! 

<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Kinematics/program/Ballonspringdrop">
  <img alt="Ball drop" width="30%" height="30%" src="./src/demos/images/ball_falling_on_spring.png" title="Click to animate"/>
</a>
<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Kinematics/program/Slinkydrop">
  <img alt="Slinky drop" width="50%" height="50%" src="./src/demos/images/slinky_drop.png" title="Click to animate"/>
</a>

- [Drop the ball](https://zegerh-6085.trinket.io/sites/slinkydrop) on Trinket
  or [on glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/folder/Kinematics/program/Ballonspringdrop)
- View the code [on Trinket](https://trinket.io/glowscript/92ffad53ab4d) which is based on the
  original [ball falling on spring](https://www.youtube.com/watch?v=ExxDuRTIe0E) video and the code presented therein


- Observe [the slinky drop](https://zegerh-6085.trinket.io/sites/slinkydrop) on Trinket
  or [on glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/folder/Kinematics/program/Slinkydrop)
- View the slinky drop code [on Trinket](https://trinket.io/library/trinkets/9c6757b113dc), which is
  based on the original [slinky drop](https://rhettallain.com/2019/02/06/modeling-a-falling-slinky/) blog post and [the code presented therein](https://trinket.io/glowscript/e5f14ebee1)

## The _N_-body coupled oscillator

The N-body coupled harmonic oscillator is composed of beads connected by springs.
This coupled harmonic oscillator here lets you play around with an arbitrary 
number of vibrating beads coupled by springs on both sides!

<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Kinematics/program/N-bodycoupledoscillator">
  <img alt="N-body coupled oscillator" width="60%" height="60%" src="./src/demos/images/n_body_coupled_oscillator.png" title="Click to animate"/>
</a>

- N-body coupled oscillator code in action [on Trinket](https://zegerh-6085.trinket.io/sites/n_body_coupled_oscillator) 
  and in action [on glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/folder/Kinematics/program/N-bodycoupledoscillator)
- N-body coupled oscillator code base [on Trinket](https://trinket.io/glowscript/5a852a2b7570)

## Newton&apos;s pendulum 

<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Kinematics/program/Newtonspendulum">
  <img alt="Newton's pendulum" width="50%" height="50%" src="./src/demos/images/newtons_pendulum.png" title="Click to animate"/>
</a>

- Pendulum in action [on Trinket](https://zegerh-6085.trinket.io/sites/newtons_pendulum) 
  and in action [on glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/folder/Kinematics/program/Newtonspendulum)
- Pendulum code base [on Trinket](https://trinket.io/glowscript/1b74de8aeee8)


## [Ball on sliding ramp](https://trinket.io/library/trinkets/0731c4e734f8) and ball hitting block

<a href="https://zegerh-6085.trinket.io/sites/ball_on_sliding_ramp">
  <img alt="Ball on sliding ramp" width="48%" height="48%" src="./src/demos/images/ball_on_sliding_ramp.png" title="Click to animate"/>
</a> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Kinematics/program/Blockrotation">
  <img alt="Block rotation" width="42%" height="42%" src="./src/demos/images/block_rotation.png" title="Click to animate"/>
</a>

- Rotating block in action [on Trinket](https://zegerh-6085.trinket.io/sites/block_rotation) 
  and in action [on glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/folder/Kinematics/program/Blockrotation)
- Rotating block code base [on Trinket](https://trinket.io/library/trinkets/0e414ca766d1)

## Water sprinkler

This is a refactored version of the original idea from [Dot Physics](https://www.youtube.com/channel/UCVxIDFY01y4n_c2lK1TB-KA). 

<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Kinematics/Watersprinkler">
  <img alt="Water sprinkler" width="50%" height="50%" src="https://rhettallain.com/wp-content/uploads/2019/11/sprinkler1.gif" title="Click to animate"/>
</a>

- See the water sprinkler in action [on Trinket](https://zegerh-6085.trinket.io/sites/sprinkler) 
  and on [glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/folder/Kinematics/Watersprinkler)
- Take a look at [the code base](https://trinket.io/glowscript/3ec01917098d), which is 
  based on the original [water sprinkler](https://rhettallain.com/2019/11/12/modeling-a-spinning-sprinkler/) blog post and the code presented therein

# Miscellaneous

## [Floating block](https://trinket.io/library/trinkets/94ed363f8b25)

<a href="https://zegerh-6085.trinket.io/sites/floating_block">
  <img alt="Floating block" width="50%" height="50%" src="./src/demos/images/floating_block.png" title="Click to animate"/>
</a>

## Polar coordinates

An illustration of using polar (spherical) coordinates.

<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/MyPrograms/program/Polarcoordinates">
  <img alt="Polar coordinates" width="60%" height="60%" src="./src/demos/images/polar_coordinates.png" title="Click to animate"/>
</a>

- Polar code in action [on Trinket](https://zegerh-6085.trinket.io/sites/polar_coordinates) 
  and in action [on glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/folder/MyPrograms/program/Polarcoordinates)
- Polar coordinates code base [on Trinket](https://trinket.io/library/trinkets/d7fa526a8ee9)


## Elastic collision

- See [my code in action](https://trinket.io/glowscript/d7600bd4705a) on Trinket
- Based on the original [elastic collision](https://www.youtube.com/watch?v=g_p-5YfUSnw&t=11s) video and the code presented therein

## Chain falling from table

- See [my code in action](https://trinket.io/glowscript/c3e556761469) on Trinket
- Based on the original [chain falling from table](https://www.youtube.com/watch?v=vXp1hW_t-bo) video and the code presented therein

## Three-body problem

- See [my code in action](https://trinket.io/glowscript/42acc05540ae) on Trinket
- Based on the original [three-body problem](https://www.youtube.com/watch?v=Ye2wIV8-SB8) video and the code presented therein

## Earth-moon orbit

- See [my code in action](https://trinket.io/glowscript/42acc05540ae) on Trinket
- Based on the original [earth-moon system](https://www.youtube.com/watch?v=2BisyQhNBFM) video and the code presented therein

# Fun stuff with [VPython](https://vpython.org/) 

## [Rubik's cube](https://trinket.io/library/trinkets/00eb13fbcd14) and  [Turtle graphics robot](https://trinket.io/library/trinkets/31a188264ef1)

<a href="https://zegerh-6085.trinket.io/sites/rubiks_cube">
  <img alt="Rubiks cube" width="45%" height="50%" src="./src/demos/images/rubiks_cube.png" title="Click to animate"/>
</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<a href="https://zegerh-6085.trinket.io/sites/vturtle">
  <img alt="Robot for turtle graphics" width="45%" height="50%" src="./src/demos/images/robot.png" title="Click to animate"/>
</a>

# Acknowledgements

- [Ruth Chabay and Bruce Sherwood](https://www.aapt.org/aboutaapt/Chabay_Sherwood_2014-Halliday-Resnick-Award.cfm)
- [Rhett Allain](https://en.wikipedia.org/wiki/Rhett_Allain)
- [Rob Salgado](https://www.linkedin.com/in/robertobsalgado)

# References

- [MyScript](https://webdemo.myscript.com/): enter text, equations, or diagrams by hand, and effortlessly convert 
  it to MathML, LaTeX, etc.!

- Just for fun: [online electric circuit construction kit](https://phet.colorado.edu/sims/html/circuit-construction-kit-ac/latest/circuit-construction-kit-ac_all.html).
Make sure to check it out, it simply is brilliant.

- [Manim](https://github.com/3b1b/manim), an animation engine for explanatory math videos

## Other VPython resources

- [Physics through Glowscript - An introductory course](https://bphilhour.trinket.io/physics-through-glowscript-an-introductory-course), an excellent tutorial!

- [3D Modeling with VPython](https://rsehosting.reading.ac.uk/courses/py3d-basic/)

- [VPython Applications for Teaching Physics](https://www.visualrelativity.com/vpython/)

- [Programs by Bob Salgado](https://www.glowscript.org/#/user/Rob_Salgado/folder/My_Programs/)

- [VPython Docs](https://www.beautifulmathuncensored.de/static/GlowScript/VPythonDocs/)

- [Glowscript documentation](https://www.glowscript.org/docs/VPythonDocs/index.html)

- [VPython lecture demos](https://lectdemo.github.io/virtual/index.html) (based on deprecated (V)Python versions)
