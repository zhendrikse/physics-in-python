<blockquote>
The feeling of awed wonder that science can give us is one of the highest experiences 
of which the human psyche is capable. It is a deep aesthetic passion to rank with the 
finest that music and poetry can deliver. &mdash;
Richard Dawkins in Unweaving the Rainbow, 1998.
</blockquote>

<p><br clear="all"/></p>

## Contents

[Astrophysics](#astrophysics) &mdash; [Electromagnetism](#electromagnetism) &mdash;
[Kinematics](#kinematics) &mdash; [Mathematics](#mathematics), with references to my 
separate [Math Art Gallery](geometry.html) &mdash; [Nature models](#nature) &mdash;
[Quantum and particle physics](#quantum) &mdash; [Special relativity](#relativity) &mdash;
[Thermodynamics](#thermodynamics) &mdash;[Waves](#waves) &mdash; [Fun stuff](#fun), 
references &amp; acknowledgements.


<a name="astrophysics"></a>
# Astrophysics

The code pertaining to the demos in this section is also available under the 
[astrophysics tab](https://glowscript.org/#/user/zeger.hendrikse/folder/Astrophysics/)
on [glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/).

### Daylight variations &mdash; sun-earth-moon model
<hr/>

<figure style="float: center; text-align: center;">
  <a href="glowscript/Daylightvariations.html">
    <img alt="Daylight variations" width="100%" height="100%" src="./images/daylight_variations.png" title="Click to animate"/>
  </a>
  <figcaption>A not accurate to scale sun-earth-moon model, but very detailed and instructive!
  It&apos;s main goal is visualizing the change in day length during the course of a year.</figcaption>
</figure>

<p><br clear="all"/></p>

###  Kepler's law &amp; the three-body problem
<hr/>

<figure style="float: left; width: 50%; text-align: center">
  <a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Astrophysics/program/Keplerslaw">
    <img alt="Kepler's laws" src="./images/keplers_law.png" title="Click to animate"/>
  </a>
  <figcaption><a href="https://en.wikipedia.org/wiki/Kepler%27s_laws_of_planetary_motion">Kepler&apos;s laws</a>
    of planetary motion: "I believe the geometric proportion served the creator as an idea when He 
    introduced the continuous generation of similar objects from similar objects" &mdash; Johannes Kepler.
  </figcaption>
</figure>
<figure style="float: right; width: 50%; text-align: center">
  <a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Astrophysics/program/Threebody">
    <img alt="Three body problem" src="./images/three_body.png" title="Click to animate"/>
  </a>
  <figcaption>The well-known <a href="https://en.wikipedia.org/wiki/Three-body_problem">three-body problem</a>.</figcaption>
</figure>

<p><br clear="all"/></p>

<a name="mathematics"></a>
# Mathematics

<p></p>
<blockquote>
Mathematics directs the flow of the universe, lurks behind its shapes and curves, 
holds the reins of everything from tiny atoms to the biggest stars. &mdash; Edward Frenkel
</blockquote>

<p></p>

The code pertaining to the demos in this section is available under the 
[mathematics tab](https://glowscript.org/#/user/zeger.hendrikse/folder/Math/)
on [glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/).

### Dynamic 3D-plots of multivariate and complex functions
<hr/>

<figure style="float: left; width: 50%; text-align: center">
  <a href="glowscript/NumpyMatplot3D.html">
    <img alt="Multivariate functions" src="./images/3d_plot.png" title="Click to animate"/>
  </a>&nbsp;&nbsp;&nbsp;
  <figcaption>Plotting <a href="https://en.wikipedia.org/wiki/Function_of_several_real_variables">multivariate functions</a> $F(x, y)$.</figcaption>
</figure>
<figure style="float: right; width: 50%; text-align: center">
  <a href="glowscript/Complexfunctionplot.html">
    <img alt="Complex functions" src="./images/complex_function_plot.png" title="Click to animate"/>
  </a>
  <figcaption>Plotting <a href="https://en.wikipedia.org/wiki/Complex_analysis">complex functions</a> $F(z)$.</figcaption>
</figure>

<p><br clear="all"></p>

<details>
  <summary><a>&dArr; Python code snippets with which to generate the plots &uArr;</a></summary>

The formula for the above image is given by:

$$\psi(x, y, t) = \sin\left(\sqrt{x^2+y^2}\right)$$

<p>The following Python code was used to plot the graph belonging to this multivariate function:<br/></p>

<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">def</span> <span class="nf">sine_sqrt</span><span class="p">():</span>
    <span class="n">resolution</span> <span class="o">=</span> <span class="mi">50</span>
    <span class="n">x</span> <span class="o">=</span> <span class="n">y</span> <span class="o">=</span> <span class="n">np</span><span class="p">.</span><span class="n">linspace</span><span class="p">(</span><span class="o">-</span><span class="mi">2</span> <span class="o">*</span> <span class="n">pi</span><span class="p">,</span> <span class="mi">2</span> <span class="o">*</span> <span class="n">pi</span><span class="p">,</span> <span class="n">resolution</span><span class="p">)</span>
    <span class="n">xx</span><span class="p">,</span> <span class="n">yy</span> <span class="o">=</span> <span class="n">np</span><span class="p">.</span><span class="n">meshgrid</span><span class="p">(</span><span class="n">x</span><span class="p">,</span> <span class="n">y</span><span class="p">)</span>
    <span class="n">x_2_plus_y_2</span> <span class="o">=</span> <span class="n">xx</span><span class="p">.</span><span class="n">multiply</span><span class="p">(</span><span class="n">xx</span><span class="p">).</span><span class="n">add</span><span class="p">(</span><span class="n">yy</span><span class="p">.</span><span class="n">multiply</span><span class="p">(</span><span class="n">yy</span><span class="p">))</span>
    <span class="n">zz</span> <span class="o">=</span> <span class="n">np</span><span class="p">.</span><span class="n">sin</span><span class="p">(</span><span class="n">np</span><span class="p">.</span><span class="n">sqrt</span><span class="p">(</span><span class="n">x_2_plus_y_2</span><span class="p">)).</span><span class="n">multiply</span><span class="p">(</span><span class="mi">5</span><span class="p">)</span>

    <span class="k">return</span> <span class="n">xx</span><span class="p">,</span> <span class="n">yy</span><span class="p">,</span> <span class="n">zz</span>

<span class="n">xx</span><span class="p">,</span> <span class="n">yy</span><span class="p">,</span> <span class="n">zz</span> <span class="o">=</span> <span class="n">sine_sqrt</span><span class="p">()</span>
<span class="n">plot</span> <span class="o">=</span> <span class="n">Plot3D</span><span class="p">(</span><span class="n">xx</span><span class="p">,</span> <span class="n">yy</span><span class="p">,</span> <span class="n">zz</span><span class="p">)</span>
</code></pre></div></div>


<p>The 
<a href="https://matplotlib.org/stable/gallery/mplot3d/surface3d_radial.html#sphx-glr-gallery-mplot3d-surface3d-radial-py">mexican hat</a> 
is most easily obtained by using polar coordinates:</p>

$$\begin{pmatrix} x \\ y \\ z \end{pmatrix}=\begin{pmatrix} r\cos(\phi) \\ \sin(\phi)) \\ (r^2 - 1)^2 \end{pmatrix}$$

<p><br/>This leads to the following Python code<br/></p>


<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">def</span> <span class="nf">mexican_hat</span><span class="p">():</span>
    <span class="n">r</span> <span class="o">=</span> <span class="n">np</span><span class="p">.</span><span class="n">linspace</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="mf">1.25</span><span class="p">,</span> <span class="mi">50</span><span class="p">)</span>
    <span class="n">p</span> <span class="o">=</span> <span class="n">np</span><span class="p">.</span><span class="n">linspace</span><span class="p">(</span><span class="o">-</span><span class="n">pi</span><span class="p">,</span> <span class="mf">1.05</span> <span class="o">*</span> <span class="n">pi</span><span class="p">,</span> <span class="mi">50</span><span class="p">)</span>
    <span class="n">R</span><span class="p">,</span> <span class="n">P</span> <span class="o">=</span> <span class="n">np</span><span class="p">.</span><span class="n">meshgrid</span><span class="p">(</span><span class="n">r</span><span class="p">,</span> <span class="n">p</span><span class="p">)</span>
    <span class="n">Z</span> <span class="o">=</span> <span class="n">R</span><span class="p">.</span><span class="n">multiply</span><span class="p">(</span><span class="n">R</span><span class="p">).</span><span class="n">subtract</span><span class="p">(</span><span class="mi">1</span><span class="p">).</span><span class="n">multiply</span><span class="p">(</span><span class="n">R</span><span class="p">.</span><span class="n">multiply</span><span class="p">(</span><span class="n">R</span><span class="p">).</span><span class="n">subtract</span><span class="p">(</span><span class="mi">1</span><span class="p">))</span>
    <span class="n">X</span><span class="p">,</span> <span class="n">Y</span> <span class="o">=</span> <span class="n">np</span><span class="p">.</span><span class="n">cos</span><span class="p">(</span><span class="n">P</span><span class="p">).</span><span class="n">multiply</span><span class="p">(</span><span class="n">R</span><span class="p">),</span> <span class="n">np</span><span class="p">.</span><span class="n">sin</span><span class="p">(</span><span class="n">P</span><span class="p">).</span><span class="n">multiply</span><span class="p">(</span><span class="n">R</span><span class="p">)</span>
    <span class="k">return</span> <span class="n">X</span><span class="p">,</span> <span class="n">Y</span><span class="p">,</span> <span class="n">Z</span>

<span class="n">xx</span><span class="p">,</span> <span class="n">yy</span><span class="p">,</span> <span class="n">zz</span> <span class="o">=</span> <span class="n">mexican_hat</span><span class="p">()</span>
<span class="n">plot</span> <span class="o">=</span> <span class="n">Plot3D</span><span class="p">(</span><span class="n">xx</span><span class="p">,</span> <span class="n">yy</span><span class="p">,</span> <span class="n">zz</span><span class="p">)</span>
</code></pre></div></div>


<p>Similarly, many different geometric shapes such as a <a href="https://www.mattiagiuri.com/2020/11/20/plotting-a-torus-with-python/">torus</a> 
can be generated (select the torus from the drop-down menu in the application):</p>

$$\begin{pmatrix} x \\ y \\ z\end{pmatrix}=\begin{pmatrix} (c + a \cos(v))\cdot\cos(u) \\ (c + a \cos(v))\cdot\sin(u) \\ a \sin(v) \end{pmatrix}$$

<p><br/>This leads to the following Python code<br/></p>

<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">def</span> <span class="nf">torus</span><span class="p">():</span>
    <span class="n">c</span> <span class="o">=</span> <span class="mi">3</span>
    <span class="n">a</span> <span class="o">=</span> <span class="mi">1</span>
    <span class="n">xx</span> <span class="o">=</span> <span class="n">yy</span> <span class="o">=</span> <span class="n">np</span><span class="p">.</span><span class="n">linspace</span><span class="p">(</span><span class="o">-</span><span class="n">pi</span><span class="p">,</span> <span class="mf">1.05</span> <span class="o">*</span> <span class="n">pi</span><span class="p">,</span> <span class="mi">75</span><span class="p">)</span>
    <span class="n">U</span><span class="p">,</span> <span class="n">V</span> <span class="o">=</span> <span class="n">np</span><span class="p">.</span><span class="n">meshgrid</span><span class="p">(</span><span class="n">xx</span><span class="p">,</span> <span class="n">yy</span><span class="p">)</span>
    <span class="n">X</span> <span class="o">=</span> <span class="p">(</span><span class="n">np</span><span class="p">.</span><span class="n">cos</span><span class="p">(</span><span class="n">V</span><span class="p">).</span><span class="n">multiply</span><span class="p">(</span><span class="n">a</span><span class="p">).</span><span class="n">add</span><span class="p">(</span><span class="n">c</span><span class="p">)).</span><span class="n">multiply</span><span class="p">(</span><span class="n">np</span><span class="p">.</span><span class="n">cos</span><span class="p">(</span><span class="n">U</span><span class="p">))</span>
    <span class="n">Y</span> <span class="o">=</span> <span class="p">(</span><span class="n">np</span><span class="p">.</span><span class="n">cos</span><span class="p">(</span><span class="n">V</span><span class="p">).</span><span class="n">multiply</span><span class="p">(</span><span class="n">a</span><span class="p">).</span><span class="n">add</span><span class="p">(</span><span class="n">c</span><span class="p">)).</span><span class="n">multiply</span><span class="p">(</span><span class="n">np</span><span class="p">.</span><span class="n">sin</span><span class="p">(</span><span class="n">U</span><span class="p">))</span>
    <span class="n">Z</span> <span class="o">=</span> <span class="n">np</span><span class="p">.</span><span class="n">sin</span><span class="p">(</span><span class="n">V</span><span class="p">).</span><span class="n">multiply</span><span class="p">(</span><span class="n">a</span><span class="p">)</span>
    <span class="k">return</span> <span class="n">X</span><span class="p">,</span> <span class="n">Y</span><span class="p">,</span> <span class="n">Z</span>

<span class="n">xx</span><span class="p">,</span> <span class="n">yy</span><span class="p">,</span> <span class="n">zz</span> <span class="o">=</span> <span class="n">torus</span><span class="p">()</span>
<span class="n">plot</span> <span class="o">=</span> <span class="n">Plot3D</span><span class="p">(</span><span class="n">xx</span><span class="p">,</span> <span class="n">yy</span><span class="p">,</span> <span class="n">zz</span><span class="p">)</span>
</code></pre></div></div>

</details>

<p></p>

### Polar coordinates &amp; [geometrical shapes](geometry.html)
<hr/>

<figure style="float: left; width: 50%; text-align: center">
  <a href="https://glowscript.org/#/user/zeger.hendrikse/folder/MyPrograms/program/Polarcoordinates">
    <img alt="Polar coordinates" src="./images/polar_coordinates.png" title="Click to animate"/>
  </a>
  <figcaption>Polar coordinates frequently simplify the tackling of rotationally symmetric problems.</figcaption>
</figure>
<figure style="float: right; width: 50%; text-align: center">
  <a href="glowscript/AtomicOrbitals.html">
    <img alt="Twisted torus" src="./images/twisted_torus.png" title="Click to animate"/>
  </a>
  <figcaption>A twisted torus. For more geometrical shapes like this, 
  visit my <a href="geometry.html">Math Art gallery</a>.</figcaption>
</figure>

<p><br clear="all"/></p>


<a name="nature"></a>
# Nature models

The code pertaining to the demos in this section is available under the 
[miscellaneous tab](https://www.glowscript.org/#/user/zeger.hendrikse/folder/MyPrograms/)
on [glowscript.org](https://glowscript.org/#/user/zeger.hendrikse/).

### Flocking birds &amp; falling raindrops
<hr/>

<figure style="float: left; width: 50%; text-align: center">
  <a href="glowscript/Flockingbirds.html">
    <img alt="Flocking birds" src="./images/flocking_birds.png" title="Click to animate"/>
  </a>
  <figcaption>Simulation of a flock of birds: "Eagles commonly fly alone. They are crows, daws, 
  and starlings that flock together" &mdash; John Webster </figcaption>
</figure>
<figure style="float: right; width: 50%; text-align: center">
  <a href="glowscript/Raindrops.html">
    <img alt="Raindrops" src="./images/raindrops.png" title="Click to animate"/>
  </a>
  <figcaption>"There are holes in the sky. Where the rain gets in. But they're ever so small. 
  That's why the rain is thin" &mdash; Spike Milligan.</figcaption>
</figure>

<p><br clear="all"/></p>


<a name="quantum"></a>
# Particle and quantum physics
<p></p>

<blockquote>
If you think you understand quantum mechanics, you don't understand quantum mechanics.
&mdash; Richard P. Feynman 
</blockquote>

<p></p>

The code pertaining to the demos in this section is available under the 
[quantum tab](https://glowscript.org/#/user/zeger.hendrikse/folder/Quantum/)
on [glowscript.org](https://glowscript.org).

### Visualizing plane waves $\psi(x, t) = A \cdot e^{i(k x - \omega t)}$ &amp; spherical harmonics
<hr/>

<figure style="float: left; width: 50%; text-align: center">
  <a href="glowscript/Planewave.html">
    <img alt="Complex wave" src="./images/plane_wave.png" title="Click to animate"/>
  </a>
  <figcaption>Complex plane waves play a pivotal role in quantum mechanics!</figcaption>
</figure>
<figure style="float: right; width: 50%; text-align: center">
  <a href="glowscript/AtomicOrbitals.html">
    <img alt="Spherical harmonics" src="./images/atomic_orbitals.png" title="Click to animate"/>
  </a>
  <figcaption>Spherical harmonics are solutions of the Schr&#246;dinger equation for the hydrogen atom.</figcaption>
</figure>

<p><br clear="all"/></p>

<details>
  <summary><a>&dArr; For a plane wave, we can easily derive the Schr&#246;dinger equation &uArr;</a></summary>

According to <a href="https://en.wikipedia.org/wiki/Matter_wave">De Broglie</a> we have:

$$p = \dfrac{h}{\lambda} = \dfrac{h}{2\pi} \dfrac{2\pi}{\lambda} = \hbar k \Rightarrow \hbar k = \hbar \dfrac{\partial}{\partial x} \psi(x,t) = p \psi(x, t) \Rightarrow p = \hbar \dfrac{\partial}{\partial x}$$

The Kinetic energy can be expressed as:

$$K = \dfrac{p^2}{2m} = -\dfrac{\hbar^2}{2m}\dfrac{\partial^2}{\partial x^2} \psi(x,t)$$

The total energy is given by the <a href="https://en.wikipedia.org/wiki/Planck_relation">Planck-Einstein relation</a>:

$$E = hf = \dfrac{h}{2\pi}\dfrac{2\pi}{T} = \hbar \omega \Rightarrow -i\hbar\dfrac{\partial}{\partial t} \psi(x,t) = E \psi(x,t) \Rightarrow E = -i\hbar\dfrac{\partial}{\partial t}$$

From this we arrive at the <a href="https://en.wikipedia.org/wiki/Schr%C3%B6dinger_equation">Schr&#246;dinger equation</a>:

$$(KE + PE)\Psi(x,,t) = E\Psi(x,t) = -i\hbar \dfrac{\partial}{\partial t}\Psi(x, t) = -\dfrac{\hbar^2}{2m}\dfrac{\partial^2}{\partial x^2} \Psi(x,t) + V(x)\Psi(x,t)$$

In three-dimensional space this is then generalized to:

$$i\bar\dfrac{\partial}{\partial t}\Psi(\vec{r}, t) = \left(\dfrac{\har^2}{2m}\nabla^2 + V(\vec{r, t}\right)\Psi(\vec{r}, t)$$
</details>

<p><br/></p>

<details>
  <summary><a>&dArr; Python code snippet for plotting spherical harmonics &uArr;</a></summary>

The spherical harmonic function is given by

$$\begin{cases} \rho &amp; = 4 \cos^2(2\theta)\sin^2(\phi) \\  \theta &amp; = [0, 2\pi] \\ \phi &amp; = [0, \pi]  \end{cases}$$

This can then easily be translated to the graphing software, that can also be 
seen in the mathematics section on this page:


<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">def</span> <span class="nf">sphere_harmonics</span><span class="p">():</span>
    <span class="n">theta</span> <span class="o">=</span> <span class="n">np</span><span class="p">.</span><span class="n">linspace</span><span class="p">(</span><span class="o">-</span><span class="mf">1.1</span> <span class="o">*</span> <span class="n">pi</span><span class="p">,</span> <span class="n">pi</span><span class="p">,</span> <span class="mi">100</span><span class="p">)</span>
    <span class="n">phi</span> <span class="o">=</span> <span class="n">np</span><span class="p">.</span><span class="n">linspace</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="n">pi</span><span class="p">,</span> <span class="mi">100</span><span class="p">)</span>
    <span class="n">U</span><span class="p">,</span> <span class="n">V</span> <span class="o">=</span> <span class="n">np</span><span class="p">.</span><span class="n">meshgrid</span><span class="p">(</span><span class="n">theta</span><span class="p">,</span> <span class="n">phi</span><span class="p">)</span>
    
    <span class="n">R1</span> <span class="o">=</span> <span class="n">np</span><span class="p">.</span><span class="n">cos</span><span class="p">(</span><span class="n">U</span><span class="p">.</span><span class="n">multiply</span><span class="p">(</span><span class="mi">2</span><span class="p">)).</span><span class="n">multiply</span><span class="p">(</span><span class="n">np</span><span class="p">.</span><span class="n">cos</span><span class="p">(</span><span class="n">U</span><span class="p">.</span><span class="n">multiply</span><span class="p">(</span><span class="mi">2</span><span class="p">)))</span>
    <span class="n">R2</span> <span class="o">=</span> <span class="n">np</span><span class="p">.</span><span class="n">sin</span><span class="p">(</span><span class="n">V</span><span class="p">).</span><span class="n">multiply</span><span class="p">(</span><span class="n">np</span><span class="p">.</span><span class="n">sin</span><span class="p">(</span><span class="n">V</span><span class="p">))</span>
    <span class="n">R</span> <span class="o">=</span> <span class="n">R1</span><span class="p">.</span><span class="n">multiply</span><span class="p">(</span><span class="n">R2</span><span class="p">).</span><span class="n">multiply</span><span class="p">(</span><span class="mi">4</span><span class="p">)</span>
    
    <span class="n">X</span> <span class="o">=</span> <span class="n">np</span><span class="p">.</span><span class="n">sin</span><span class="p">(</span><span class="n">U</span><span class="p">).</span><span class="n">multiply</span><span class="p">(</span><span class="n">np</span><span class="p">.</span><span class="n">cos</span><span class="p">(</span><span class="n">V</span><span class="p">)).</span><span class="n">multiply</span><span class="p">(</span><span class="n">R</span><span class="p">)</span>
    <span class="n">Y</span> <span class="o">=</span> <span class="n">np</span><span class="p">.</span><span class="n">sin</span><span class="p">(</span><span class="n">U</span><span class="p">).</span><span class="n">multiply</span><span class="p">(</span><span class="n">np</span><span class="p">.</span><span class="n">sin</span><span class="p">(</span><span class="n">V</span><span class="p">)).</span><span class="n">multiply</span><span class="p">(</span><span class="n">R</span><span class="p">)</span>
    <span class="n">Z</span> <span class="o">=</span> <span class="n">np</span><span class="p">.</span><span class="n">cos</span><span class="p">(</span><span class="n">U</span><span class="p">).</span><span class="n">multiply</span><span class="p">(</span><span class="n">R</span><span class="p">)</span>
    <span class="k">return</span> <span class="n">X</span><span class="p">,</span> <span class="n">Y</span><span class="p">,</span> <span class="n">Z</span><span class="p">,</span> <span class="bp">None</span><span class="p">,</span> <span class="bp">None</span>

<span class="n">xx</span><span class="p">,</span> <span class="n">yy</span><span class="p">,</span> <span class="n">zz</span> <span class="o">=</span> <span class="n">sphere_harmonics</span><span class="p">()</span>
<span class="n">plot</span> <span class="o">=</span> <span class="n">Plot3D</span><span class="p">(</span><span class="n">xx</span><span class="p">,</span> <span class="n">yy</span><span class="p">,</span> <span class="n">zz</span><span class="p">)</span>

</code></pre></div></div>

</details>
<p><br clear="all"/></p>

### One-dimensional quantum particle bound by an infinite square well
<hr/>
<figure>
  <a href="https://www.glowscript.org/#/user/zeger.hendrikse/folder/Quantum/program/Infinitesquarewell">
    <img alt="Complex wave" width="50%" height="50%" src="./images/infinite_square_well.png" title="Click to animate"/>
  </a>
</figure>

<details>
<summary><a>&dArr; Background: particle in a box, i.e. confined by a infinite square well &uArr;</a></summary>
<p>
Although the one-dimensional particle-in-a-box problem does not correspond to any
real-world system, it illustrates quite well some (fundamental) 
quantum mechanical features nonetheless.
</p>

<p>
The box is modeled by an infinite square well, so that the particle cannot escape 
beyond the boundaries of the box.
</p>

Inside the box, the potential energy $V$ is zero (or constant). Substituting this together with the
formula for the plane wave $\psi(x,t) = Ae^{ik x}e^{-i\omega t}$ into the Schrödinger equation, we get:

$$\dfrac{\partial^2\psi}{\partial x^2} + \dfrac{8\pi^2m}{h^2}(E - 0)\psi=0 \Rightarrow \bigg(\dfrac{-h^2}{8\pi^2m}\bigg)\dfrac{\partial^2\psi}{\partial x^2}=E\psi$$

Which function does give itself (times $E$) when differentiated twice _and_ is zero at both boundaries of the box?

$$\psi = A\sin(ax) \Rightarrow \dfrac{h^2a^2}{8\pi^2m}\psi=E\psi \Rightarrow E=\dfrac{h^2a^2}{8\pi^2m}$$

To get $a$, we note that the wave function equals zero at the box boundaries:

$$\psi=A\sin(ax) = 0 \Rightarrow a=\dfrac{n\pi}{L} \Rightarrow \psi_n = A\sin\bigg(\dfrac{n\pi x}{L}\bigg) \Rightarrow E_n=\dfrac{h^2n^2}{8mL^2}$$

Normalizing the wave function results in an expression for $A$:

$$\int_0^L \psi \cdot  \psi dx = 1 \Rightarrow A^2 \int_0^L\sin^2\bigg(\dfrac{n\pi x}{L}\bigg) dx=1 \Rightarrow A^2\bigg(\dfrac{L}{2}\bigg)=1 \Rightarrow A=\sqrt{\dfrac{2}{L}}$$

So summarizing, we have

$$E=\dfrac{h^2a^2}{8\pi^2m} \text{ and } \psi_n=\sqrt{\dfrac{2}{L}}\sin(nkx), \text{where } k=\dfrac{\pi}{L}$$

These energy eigenstates (and superpositions thereof) are used in the visualization software.
</details>

<p></p>

### The quantum harmonic oscillator
<hr/>

The quantum harmonic oscillator is visualized in a semi-classical way below.

<figure>
  <a href="https://www.glowscript.org/#/user/zeger.hendrikse/folder/Quantum/program/Quantumoscillator">
    <img alt="Quantum oscillator" width="50%" height="50%" src="./images/quantum_oscillator.png" title="Click to animate"/>
  </a>
</figure>

### Charged particle moving in two electric fields
<hr />
The following demos show the movement of an electron in two different electric fields. 

<figure>
  <a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Chargedring">
    <img alt="Electron spinning around charged ring" width="45%" height="45%" src="./images/electron_and_charged_ring.png" title="Click to animate"/>
  </a>
  <a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Movingcharge">
    <img alt="Particle in electric field" width="45%" height="45%" src="./images/particle_in_electric_field.png" title="Click to animate"/>
  </a>
</figure>

### Rutherford scattering & charged particle in magnetic field
<hr/>

<figure>
  <a href="https://www.glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Rutherfordscattering">
    <img alt="Rutherford scattering" width="45%" height="45%" src="./images/rutherford_scattering.png" title="Click to animate"/>
  </a>
  <a href="https://www.glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Helicalmotion">
    <img alt="Helical motion" width="50%" height="50%" src="./images/helical_motion.png" title="Click to animate"/>
  </a>
</figure>


<a name="electromagnetism"></a>
# Electromagnetism

The code pertaining to the demos in this section is available under the 
[electromagnetism tab](https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/)
on [glowscript.org](https://glowscript.org).

### Electric fields of dipoles and point charges
<hr/>

<details>
  <summary><a>&dArr; Background: electric fields around dipoles and point charges &dArr;</a></summary>

For dipoles the field is given by

$$\vec{E} ( \vec{r} ) = \dfrac {1} {4\pi\epsilon_0} \dfrac {Q} {r^2} \hat{r}, \text{ with } \vec{F}(\vec{r}) = q \vec{E} (\vec{r}) = \dfrac {1} {4\pi\epsilon_{0}} \dfrac {qQ} {r^2}\hat{r} \text{ }$$

and for point charges by

$$\vec{E} ( \vec{r} ) = -\dfrac {1} {4\pi\epsilon_0} \nabla \bigg( \dfrac{\vec{r}  \cdot \vec{p}} {r^3} \bigg), \text{ where } \vec{p} = +q(\vec{r_{+}}) + -q(\vec{r_{-})}$$
</details>

<figure>
  <a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Pointchargefield">
    <img alt="Electric field of point charge" width="45%" height="45%" src="./images/point_charge.png" title="Click to animate"/>
  </a>
  <a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Electricdipolefield">
    <img alt="Electric field of a dipole" width="40%" height="40%" src="./images/dipole_field.png" title="Click to animate"/>
  </a>
</figure>


### Electric and magnetic fields
<hr/>

Visualization of Faraday's law by running an electric current (of electric charges) through a wire and of
an electric field inside a series of charged rings.

<figure>
  <a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Faradayslaw">
    <img alt="Faraday's law" width="45%" height="45%" src="./images/faradays_law.png" title="Click to animate"/>
  </a>
  <a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Chargedrings">
    <img alt="Charged rings" width="45%" height="45%" src="./images/charged_rings.png" title="Click to animate"/>
  </a>  
</figure>


### Charged disk and accompanying builder
<hr/>

Two rather simple demos that show the electric field around a disk. The builder allows a step-by-step
set-up of the disk by adding a charged ring at each mouse click.

<figure>
  <a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Chargeddisk">
    <img alt="Charged disk" width="30%" height="30%" src="./images/charged_disk.png" title="Click to animate"/>
  </a>
  <a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Chargeddiskbuilder">
    <img alt="Charged disk builder" width="40%" height="40%" src="./images/charged_disk_builder.png" title="Click to animate"/>
  </a>
</figure>

## Electromagnetic waves
<hr/>

Both of the two dynamic simulations below visualize the propagation of electromagnetic waves. 

<figure>
  <a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Antenna">
    <img alt="Antenna" width="45%" height="45%" src="./images/antenna.png" title="Click to animate"/>
  </a>
  <a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Electromagneticwave">
    <img alt="Electromagnetic waves" width="50%" height="50%" src="./images/electromagnetic_wave.png" title="Click to animate"/>
  </a>
</figure>

<a name="thermodynamics"></a>
# Thermodynamics

The code pertaining to the demos in this section is available under the 
[thermodynamics tab](https://glowscript.org/#/user/zeger.hendrikse/folder/Thermodynamics/)
on [glowscript.org](https://glowscript.org).

### Boltzmann gas &amp; cubic symmetry planes
<hr/>

<figure>
  <a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Thermodynamics/program/Hardspheregas">
    <img alt="Hard sphere gas" width="40%" height="40%" src="./images/hard_sphere_gas.png" title="Click to animate"/>
  </a>
  <a href="https://www.glowscript.org/#/user/zeger.hendrikse/folder/Electromagnetism/program/Crystalsymmetryplanes">
    <img alt="Symmetry planes" width="45%" height="45%" src="./images/crystal_planes.png" title="Click to animate"/>
  </a>
</figure>

### Two-dimensional Ising spin model
<hr/>

This demo models the magnetization at various temperatures using a two-dimensional Ising spin lattice.

<figure>
  <a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Thermodynamics/program/Isingspin">
    <img alt="Ising spin model" width="40%" height="40%" src="./images/ising_spin_model.png" title="Click to animate"/>
  </a>
</figure>


<a name="waves"></a>
# Waves

### Doppler effect
<hr/>

<a href="https://www.glowscript.org/#/user/zeger.hendrikse/folder/Quantum/program/Dopplereffect">
  <img alt="Doppler effect" width="50%" height="50%" src="./images/doppler_effect.png" title="Click to animate"/>
</a>

<a name="relativity"></a>
# Special relativity
<p></p>
<blockquote>
We should make things as simple as possible, but not simpler. &mdash; Albert Einstein
</blockquote>
<p></p>

The code pertaining to the demos in this section is available under the 
[relativity tab](https://glowscript.org/#/user/zeger.hendrikse/folder/Relativity/)
on [glowscript.org](https://glowscript.org).

### Lightcone animation and electric field of a fast moving proton
<hr/>

A three-dimensional lightcone is animated by simultaneously 
sending off both a photon and a spaceship from the origin.

The other code snippet visualizes an electric field of a
fast moving (relativistic) proton.

<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Relativity/program/Lightcone">
  <img alt="Light cone" width="40%" height="40%" src="./images/lightcone.png" title="Click to animate"/>
</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Relativity/program/Relativisticproton">
  <img alt="Relativistic proton" width="30%" height="30%" src="./images/relativistic_proton.png" title="Click to animate"/>
</a>

### Galilean transformation of relative motions in Euclidean plane
<hr/>

Before diving into (special) relativity, let's first get acquainted with 
the so-called Galilean transformation.

<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Relativity/program/Glalileantransformation">
  <img alt="Galilean space-time" width="50%" height="50%" src="./images/galilean_space_time.png" title="Click to animate"/>
</a>

<a name="kinematics"></a>
# Kinematics

The code pertaining to the demos in this section is available under the 
[kinematics tab](https://glowscript.org/#/user/zeger.hendrikse/folder/Kinematics/)
on [glowscript.org](https://glowscript.org).

### Fun with springs
<hr/>

The applications of a simple harmonic oscillator are almost endless. 
You may be surprised though to find out what happens when you drop such a simple harmonic oscillator!! 

<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Kinematics/program/Ballonspringdrop">
  <img alt="Ball drop" width="30%" height="30%" src="./images/ball_falling_on_spring.png" title="Click to animate"/>
</a>
<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Kinematics/program/Slinkydrop">
  <img alt="Slinky drop" width="50%" height="50%" src="./images/slinky_drop.png" title="Click to animate"/>
</a>

### The $N$-body coupled oscillator with adjustable $N$
<hr/>

<figure>
  <a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Kinematics/program/N-bodycoupledoscillator">
    <img alt="N-body coupled oscillator" width="40%" height="40%" src="./images/n_body_coupled_oscillator.png" title="Click to animate"/>
  </a>
</figure>


### Newton&apos;s pendulum and cannonball
<hr/>

<figure>
  <a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Kinematics/program/Newtonspendulum">
    <img alt="Newton's pendulum" width="45%" height="45%" src="./images/newtons_pendulum.png" title="Click to animate" align="top"/>
  </a>
  <a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Kinematics/program/Newtonscannon">
    <img alt="Newton's cannon" width="45%" height="45%" src="./images/newtons_cannon.png" title="Click to animate"/>
  </a>
</figure>

### Model of chain drop from table
<hr/>

<figure>
  <a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Kinematics/program/Chainfromtable">
    <img alt="Chain from table" width="40%" height="40%" src="./images/chain_from_table.png" title="Click to animate"/>
  </a>
</figure>


### Ball on sliding ramp &amp; ball hitting block
<hr/>

<a href="https://zegerh-6085.trinket.io/sites/ball_on_sliding_ramp">
  <img alt="Ball on sliding ramp" width="48%" height="48%" src="./images/ball_on_sliding_ramp.png" title="Click to animate"/>
</a> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Kinematics/program/Blockrotation">
  <img alt="Block rotation" width="42%" height="42%" src="./images/block_rotation.png" title="Click to animate"/>
</a>

### Water sprinkler and floating block
<hr/>

<figure>
  <a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Kinematics/program/Floatingblock">
    <img alt="Floating block" width="25%" height="25%" src="./images/floating_block.png" title="Click to animate"/>
  </a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://glowscript.org/#/user/zeger.hendrikse/folder/Kinematics/program/Watersprinkler">
    <img alt="Water sprinkler" width="45%" height="45%" src="./images/water_sprinkler.png" title="Click to animate"/>
  </a>
</figure>

<a name="fun"></a>
# Fun stuff with [VPython](https://vpython.org/) 

### [Rubik's cube](https://trinket.io/library/trinkets/00eb13fbcd14) and  [Turtle graphics robot](https://trinket.io/library/trinkets/31a188264ef1)
<hr/>

<figure>
  <a href="https://zegerh-6085.trinket.io/sites/rubiks_cube">
    <img alt="Rubiks cube" width="45%" height="50%" src="./images/rubiks_cube.png" title="Click to animate"/>
  </a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://zegerh-6085.trinket.io/sites/vturtle">
    <img alt="Robot for turtle graphics" width="45%" height="50%" src="./images/robot.png" title="Click to animate"/>
  </a>
</figure>

## Odysseus
<hr/>

<a href="https://glowscript.org/#/user/zeger.hendrikse/folder/MyPrograms/program/Odysseus">
  <img alt="Odysseus" width="85%" height="85%" src="./images/odysseus.png" title="Click to animate"/>
</a>

# Acknowledgements

- [Ruth Chabay and Bruce Sherwood](https://www.aapt.org/aboutaapt/Chabay_Sherwood_2014-Halliday-Resnick-Award.cfm)
- [Rhett Allain](https://en.wikipedia.org/wiki/Rhett_Allain)
- [Rob Salgado](https://www.linkedin.com/in/robertobsalgado)
- [Steve Spicklemire](https://github.com/sspickle)

# References

- Check this out &rarr; [QMsolve: A module for solving and visualizing the Schrödinger equation](https://github.com/quantum-visualizations/qmsolve)
- [MyScript](https://webdemo.myscript.com/): enter text, equations, or diagrams by hand, and effortlessly convert 
  it to MathML, LaTeX, etc.!
- Just for fun: [online electric circuit construction kit](https://phet.colorado.edu/sims/html/circuit-construction-kit-ac/latest/circuit-construction-kit-ac_all.html).
Make sure to check it out, it simply is brilliant.
- [Manim](https://github.com/3b1b/manim), an animation engine for explanatory math videos

## Other VPython apps

- [Glowscript apps](https://www.glowscript.org/#/user/matterandinteractions/folder/matterandinteractions/) belonging to the book [Matter and Interactions](https://matterandinteractions.org/)
- Glowscript apps written by [Bob Salgado](https://www.glowscript.org/#/user/Rob_Salgado/folder/My_Programs/)
- Glowscript apps written by [Steve Spicklemire](https://www.glowscript.org/#/user/spicklemire/)
- Glowscript apps written by [Dr Harrell Pane](https://www.glowscript.org/#/user/dr.harrell.pane/)
- Glowscript apps written by [X9Z3](https://glowscript.org/#/user/X9Z3/folder/X9Z3Publications/)
- Glowscript apps written by [priisdk](https://glowscript.org/#/user/priisdk/)
- Some [Glowscript games](https://glowscript.org/#/user/Guhan/folder/MyPrograms/) 
- [VPython user contributed programs](https://vpython.org/contents/contributed.html)
- [Physics simulations GitHub repository](https://github.com/Humboldt-Penguin/Physics_Simulations) of [Humboldt-Penguin](https://github.com/Humboldt-Penguin/)
- [Physics through Glowscript - An introductory course](https://bphilhour.trinket.io/physics-through-glowscript-an-introductory-course), an excellent tutorial!
- [VPython lecture demos](https://lectdemo.github.io/virtual/index.html) (based on deprecated (V)Python versions)

## Other resources

- [3D Modeling with VPython](https://rsehosting.reading.ac.uk/courses/py3d-basic/)
- [Hydrogen wavefunctions](https://github.com/ssebastianmag/hydrogen-wavefunctions)
- [VPython Applications for Teaching Physics](https://www.visualrelativity.com/vpython/) by Rob Salgado
- [VPython Docs](https://www.beautifulmathuncensored.de/static/GlowScript/VPythonDocs/)
- [Glowscript documentation](https://www.glowscript.org/docs/VPythonDocs/index.html)
