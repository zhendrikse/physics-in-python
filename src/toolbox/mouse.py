from vpython import color, arange, rate, vec

def zoom_in_on(animation):
    selected_object = animation.mouse.pick
    if not selected_object:
        return

    temp_color = vec(selected_object.color.x, selected_object.color.y, selected_object.color.z)
    selected_object.color = color.yellow
    target = selected_object.pos
    step = (target - animation.center) / 20.0
    for _ in arange(1, 20, 1):
        rate(20)
        animation.center += step
        animation.range /= 1.037  # (1.037**19=1.99)

    selected_object.color = temp_color