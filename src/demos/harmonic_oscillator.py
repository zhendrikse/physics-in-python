from vpython import vector, rate, graph, gcurve, color, button, mag, canvas
from toolbox.ball import Ball
from toolbox.spring import Spring

running = False

def run(button_instance):
    global running
    running = not running
    button_instance.text = "Pause" if running else "Run"

def set_scene():
    position_plot = graph(title="", xtitle="Time", ytitle="Amplitude")
    # scene = canvas(width=500, height=300, align='left')
    b1 = button(text="run", bind=run, background=color.cyan)
    # scene.camera.pos = vector(150, 75, 120)
    # scene.camera.axis = vector(-115, -150, -190)

class HarmonicOscillator:
    def __init__(self):
        self._left_ball  = Ball(mass=1.0, position=vector(-150, 0, 0), radius=30, color=color.red)
        self._right_ball = Ball(mass=1.0, position=vector( 150, 0, 0), radius=30, color=color.blue)
        distance = self._left_ball.distance_to(self._right_ball)
        self._size = distance
        self._spring = Spring(position=-distance / 2, axis=distance, spring_constant=1.0, equilibrium_size=200.0, radius=20, thickness=3)

    def increment_by(self, dt):
      self._right_ball.move(self._spring.force, dt)
      self._left_ball.move(-self._spring.force, dt)
      distance = self._left_ball.distance_to(self._right_ball)
      self._spring.update(distance, -distance / 2)

    @property
    def ball_position_vectors(self):
       return [self._left_ball.position, self._right_ball.position]
    
    @property
    def size(self):
       return mag(self._size)

curve_left = gcurve(color=color.blue)
curve_right = gcurve(color=color.red)
set_scene()
oscillator = HarmonicOscillator()

dt = 0.1
t = 0
while True:
  if running:
    rate(2/dt)
    oscillator.increment_by(dt)
    curve_left.plot(t * dt, oscillator.ball_position_vectors[0].x + oscillator.size)
    curve_right.plot(t * dt, oscillator.ball_position_vectors[1].x)
    t += dt

