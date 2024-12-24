from vpython import color, vector, label


class Timer:

    def __init__(self, position=vector(0, 0, 0), use_scientific=False, timer_color=color.white):
        self.use_scientific = use_scientific
        if use_scientific:
            self.timerLabel = label(pos=position, text='00E01', box=False, color=timer_color)
        else:
            self.timerLabel = label(pos=position, text='00:00:00.00', box=False, color=timer_color)

    def update(self, t):
        # Basically just use sprintf formatting according to either stopwatch or scientific notation
        if self.use_scientific:
            self.timerLabel.text = "%.4E" % t
        else:
            hours = int(t / 3600)
            minutes = int((t / 60) % 60)
            secs = int(t % 60)
            frac = int(round(100 * (t % 1)))
            if frac == 100:
                frac = 0
                secs = secs + 1

            self.timerLabel.text = "{:02d}:".format(hours) + "{:02d}:".format(minutes) + "{:02d}.".format(secs) + "{:02d}".format(frac)
