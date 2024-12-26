from vpython import color, vector, label


class Timer:

    def __init__(self, position=vector(0, 0, 0), use_scientific=False, relative_to=None, timer_color=color.white):
        self._use_scientific = use_scientific
        self._relative_to = relative_to
        self._distance_to_attached_object = relative_to.position - position if relative_to else 0
        if use_scientific:
            self._timer_label = label(pos=position, text='00E01', box=False, color=timer_color)
        else:
            self._timer_label = label(pos=position, text='00:00:00.00', box=False, color=timer_color)

    def update(self, t):
        # Basically just use sprintf formatting according to either stopwatch or scientific notation
        if self._relative_to:
            self._timer_label.pos = self._distance_to_attached_object + self._relative_to.position

        if self._use_scientific:
            self._timer_label.text = "%.4E".format(t)
            return

        hours = int(t / 3600)
        minutes = int((t / 60) % 60)
        secs = int(t % 60)
        frac = int(round(100 * (t % 1)))
        if frac == 100:
            frac = 0
            secs = secs + 1

        self._timer_label.text = "{:02d}:".format(hours) + "{:02d}:".format(minutes) + "{:02d}.".format(secs) + "{:02d}".format(frac)
