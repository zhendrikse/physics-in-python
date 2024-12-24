from vpython import color, vector, label


class Timer:

    def __init__(self, x, y, use_scientific=False, timer_color=color.white):
        # x,y - world coordinates for the timer location
        # use_scientific - bool to turn off/on scientific notation for time
        # timer_color - attribute controlling the color of the text

        self.use_scientific = use_scientific
        self.timerColor = timer_color
        if use_scientific is False:
            self.timerLabel = label(pos=vector(x, y, 0), text='00:00:00.00', box=False)
        else:
            self.timerLabel = label(pos=vector(x, y, 0), text='00E01', box=False)

    def update(self, t):
        # Basically just use sprintf formatting according to either stopwatch or scientific notation
        if self.use_scientific:
            self.timerLabel.text = "%.4E" % t
        else:
            hours = int(t / 3600)
            mins = int((t / 60) % 60)
            secs = int(t % 60)
            frac = int(round(100 * (t % 1)))
            if frac == 100:
                frac = 0
                secs = secs + 1

            self.timerLabel.text = "{:02d}:".format(hours) + "{:02d}:".format(mins) + "{:02d}.".format(secs) + "{:02d}".format(frac)
