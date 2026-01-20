#Web VPython 3.2
from vpython import vector, atan2, sin, cos, pi, text, sphere, color, canvas, rate, simple_sphere, arrow, arange, checkbox

title="""&#x2022; <a href="https://www.glowscript.org/#/user/wlane/folder/Physicsin3D/program/water-flow-curl">Original code</a> by <a href="https://www.youtube.com/@LetsCodePhysics">Let&apos;s code physics</a>
&#x2022; Refactored by <a href="https://www.hendrikse.name/">Zeger Hendrikse</a> to <a href="https://github.com/zhendrikse/science/blob/main/mathematics/code/div_curl_demo.py">div_curl_demo.py</a>

"""

caption="""
$$\\text{Divergence: }\\vec{\\nabla} =\\begin{pmatrix} \\partial/\\partial x \\\\ \\partial/\\partial y \\\\  \\partial/\\partial y \\end{pmatrix} \\Rightarrow \\vec{\\nabla} \\cdot \\vec{V} = \\dfrac{\\partial V_x}{\\partial x} + \\dfrac{\\partial V_y}{\\partial y} + \\dfrac{\\partial V_z}{\\partial z}$$
$$\\text{Curl: } \\vec{\\nabla} \\times \\vec{V} = \\begin{vmatrix} \\hat{x} & \\hat{y} & \\hat{z} \\\\ \\dfrac{\\partial}{\\partial x} & \\dfrac{\\partial}{\\partial y} & \\dfrac{\\partial}{\\partial z} \\\\ V_x & V_y & v_z \\end{vmatrix} = \\begin{pmatrix} \\partial V_z/\\partial y - \\partial F_y/\\partial z \\\\ \\partial V_x/\\partial z - \\partial F_z/\\partial x \\\\ \\partial V_y/\\partial x - \\partial F_x/\\partial y\\end{pmatrix} $$ 
"""

x_max = 2
x_min = -x_max
y_max = 0.75 * x_max
y_min = -y_max

display = canvas(background=color.gray(0.075), width=600, height=400, range=2, forward=vector(0, .4, -.9), title=title)

def vector_field(position, radius=.75, a=vector(1, .5, 0), b=vector(-1, -.5, 0), c=vector(-1, .5, 0)):
    if a.x - radius <= position.x <= a.x + radius and a.y - radius <= position.y <= a.y + radius:
        theta = atan2((position.y - a.y), (position.x - a.x))
        return vector(-sin(theta), cos(theta), 0)
    elif b.x - radius <= position.x <= b.x + radius and b.y - radius <= position.y <= b.y + radius:
        theta = atan2((position.y - b.y), (position.x - b.x))
        return vector(-cos(theta), -sin(theta), 0)
    elif c.x - radius <= position.x <= c.x + radius and c.y - radius <= position.y <= c.y + radius:
        theta = atan2((position.y - c.y), (position.x - c.x))
        return vector(cos(theta), sin(theta), 0)
    elif (x_max - position.x <= 0.2 or position.x - x_min <= 0.2) and (y_max - position.y <= 0.2 or position.y - y_min <= 0.2):
        vx = -1 if x_max - position.x <= 0.2 else 1
        vy = -1 if y_max - position.y <= 0.2 else 1
        return vector(vx, vy, 0)
    elif x_max - position.x <= 0.2:
        return vector(0, 1, 0)
    elif position.x - x_min <= 0.2:
        return vector(0, -1, 0)
    elif y_max - position.y <= 0.2:
        return vector(-1, 0, 0)
    elif position.y - y_min <= 0.2:
        return vector(1, 0, 0)
    else:
        return vector(0.5, 1.5, 0)


arrows = []
for x in arange(x_min, x_max, 0.25):
    for y in arange(y_min, y_max, 0.25):
        axis = vector_field(vector(x, y, 0)) / 5
        shift = -axis * 0.1
        arrows.append(arrow(pos=vector(x, y, 0) + shift, axis=axis, opacity=0, color=color.yellow))
particles = []
for x in arange(x_min, x_max, 0.25):
    for y in arange(y_min, y_max, 0.25):
        particles.append(simple_sphere(radius=0.05, color=color.orange, pos=vector(x, y, 0)))

source = sphere(color=color.red, pos=vector(-1, 0.5, 0), radius=0.25, opacity=0.3)
sink = sphere(color=color.green, pos=vector(-1, -0.5, 0), radius=0.25, opacity=0.3)
curl = sphere(color=color.cyan,pos=vector(1, 0.5, 0), radius=0.25, opacity=0.3, visible=False)

source_div_text = text(text="source", pos=source.pos + vector(-1.25, 0.25, 0.05), color=source.color, depth=0.02, billboard=True, height=.2)
sink_div_text = text(text="sink", pos=sink.pos + vector(-1.25, 0.25, 0.05), color=sink.color, depth=0.02, billboard=True, height=.2)
zero_div_text = text(text="zero divergence", pos=vector(0, -1, 0.05), color=color.white, depth=0.02, billboard=False, height=.2)
zero_div_text.rotate(angle=pi / 8, axis=vector(0, 0, 1))

source_curl_text = text(text="no curl",pos=source.pos+vector(-1.25, -.25, 0.05), color=source.color, depth=0.02, visible=False, billboard=True, height=.2)
sink_curl_text = text(text="no curl",pos=sink.pos+vector(-1.25, -.25, 0.05), color=sink.color, depth=0.02, visible=False, billboard=True, height=.2)
zero_curl_text = text(text="counter-clockwise curl",pos=vector(0, -0.6, 0.05), color=color.white, depth=0.02, visible=False, billboard=False, height=.2)
zero_curl_text.rotate(angle=pi / 8, axis=vector(0, 0, 1))


def toggle_div(event):
    curl.visible = source_curl_text.visible = sink_curl_text.visible = zero_curl_text.visible = not event.checked
    source_div_text.visible = sink_div_text.visible = zero_div_text.visible = source.visible = sink.visible = event.checked
    curl_radio.checked = False

def toggle_curl(event):
    curl.visible = source_curl_text.visible = sink_curl_text.visible = zero_curl_text.visible = event.checked
    source_div_text.visible = sink_div_text.visible = zero_div_text.visible = source.visible = sink.visible = not event.checked
    div_radio.checked = False

display.append_to_caption("\nShow divergence ")
div_radio = checkbox(bind=toggle_div, checked=True)
display.append_to_caption("or curl ")
curl_radio = checkbox(bind=toggle_curl, checked=False)

display.append_to_caption("\n\n" + caption)
#MathJax.Hub.Queue(["Typeset", MathJax.Hub])
popup = text(text="Click mouse to start", pos=vector(-2, 2, 0.05), depth=0.02, color=color.orange, billboard=True, height=.3)
display.waitfor("click")
popup.visible = False

dt = d_o = 0.0001
time = opacity = 0
while time < 10:
    rate(.25/dt)
    for particle in particles:
        particle.pos += vector_field(particle.pos) * dt
    time += dt
    # Fading effect
    if opacity < 1 and time > 0.1:
        opacity += d_o
        for a in arrows:
            a.opacity = opacity
