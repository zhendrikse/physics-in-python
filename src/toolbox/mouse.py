from vpython import vec, color, arange, rate, label

def zoom_in_on(scene):
    selected_object = scene.mouse.pick
    if selected_object is None:
        return

    ### ANIMATE TO SELECTED POSITION
    temp_color = vec(selected_object.color.x, selected_object.color.y, selected_object.color.z)
    selected_object.color = color.yellow
    target = selected_object.pos
    # TODO extend function with parameter to show label below
    #pick_r = target.x * 4.
    #pick_label_text = "r=" + str(round(pick_r, 5))
    #label(pos=target, text=pick_label_text, xoffset=-5, yoffset=5)
    step = (target - scene.center) / 20.0
    for _ in arange(1, 20, 1):
        rate(20)
        scene.center += step
        scene.range /= 1.037  # (1.037**19=1.99)

    selected_object.color = temp_color