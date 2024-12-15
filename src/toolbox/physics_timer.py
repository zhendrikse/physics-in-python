from vpython import color, vector, label

class PhysTimer:
    """
    This class assists students in creating an onscreen timer display.
    """
    
    def __init__(self, x, y, useScientific=False, timerColor=color.white):
        
        # PhysTimer
        # x,y - world coordinates for the timer location
        # useScientific - bool to turn off/on scientific notation for time
        # timerColor - attribute controlling the color of the text
        
        try:
            self.useScientific = useScientific
            self.timerColor = timerColor
            if useScientific is False:
                self.timerLabel = label(pos=vector(x,y,0), text='00:00:00.00', box=False)
            else:
                self.timerLabel = label(pos=vector(x,y,0), text='00E01', box=False)
        except TypeError as err:
            print("**********TYPE ERROR**********")
            print("Please check that you are not passing in a variable of the wrong type (e.g. a scalar as a vector, or vice-versa)!")
            print("******************************")
            print(err)
            raise err

    def update(self, t):
        try:
            # Basically just use sprintf formatting according to either stopwatch or scientific notation
            if self.useScientific:
                self.timerLabel.text = "%.4E" % t
            else:
                hours = int(t / 3600)
                mins = int((t / 60) % 60)
                secs = int(t % 60)
                frac = int(round(100 * (t % 1)))
                if frac == 100:
                    frac = 0
                    secs = secs + 1;
                self.timerLabel.text = "%02d:%02d:%02d.%02d" % (hours, mins, secs, frac)
        except TypeError as err:
            print("**********TYPE ERROR**********")
            print("Please check that you are not passing in a variable of the wrong type (e.g. a scalar as a vector, or vice-versa)!")
            print("******************************")
            print(err)
            raise err
