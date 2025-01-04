from vpython import sphere, vec, arrow, color, sin, cos, ring, curve, cross, label, scene, norm, slider, radians, rate

from ..toolbox.axis import Base, x_hat, y_hat, z_hat

theta = 45
phi = 45
radius = 4

def to_cartesian(r_, phi_, theta_):
    return vec(r_ * sin(radians(theta_)) * cos(radians(phi_)), r_ * sin(radians(theta_)) * sin(radians(phi_)), r_ * cos(radians(theta_)))

axis = Base(length=10)
axis.hide_tick_labels()
axis.show_xz_mesh()

dome = sphere(radius=radius, opacity=0.5, color=color.orange)
intersection = ring(radius=radius, color=color.gray(0.5), axis=y_hat, thickness=1/(radius * 5))

point_on_sphere = to_cartesian(radius, phi, theta)
radial_arrow = arrow(pos=point_on_sphere, axis=norm(point_on_sphere), color=color.green)
radial_axis = curve(pos=[vec(0, 0, 0), point_on_sphere], color=color.green)
theta_arrow = arrow(pos=point_on_sphere, axis=norm(point_on_sphere - y_hat * radius), color=color.red)
phi_arrow = arrow(pos=point_on_sphere, axis=cross(theta_arrow.axis, radial_arrow.axis), color=color.cyan)
#radial_label = label(pos=to_cartesian(radius * .5, phi, theta), box=False,  text="r", height=5 * radius)

scene.forward=vec(0.37, -0.55, -0.75)
scene.range=8.

def set_tangent_vectors():
    theta_arrow.axis = norm(to_cartesian(radius, phi, theta) - y_hat * radius)
    theta_arrow.pos = to_cartesian(radius, phi, theta)
    radial_arrow.axis = norm(to_cartesian(radius, phi, theta))
    radial_arrow.pos = to_cartesian(radius, phi, theta)
    radial_axis.modify(1, pos=to_cartesian(radius, phi, theta))
    phi_arrow.pos = to_cartesian(radius, phi, theta)
    phi_arrow.axis = cross(theta_arrow.axis, radial_arrow.axis)

def set_phi():
    global phi
    phi = phi_slider.value
    set_tangent_vectors()

def set_theta():
    global theta
    theta = theta_slider.value
    set_tangent_vectors()

scene.append_to_caption("\nAdjust theta using the slider\n")
theta_slider = slider(bind = set_theta, value = theta, min = 0, max = 360)
scene.append_to_caption("\nAdjust phi using the slider\n")
phi_slider = slider(bind = set_phi, value = phi, min = 0, max = 360)

while True:
    rate(60)