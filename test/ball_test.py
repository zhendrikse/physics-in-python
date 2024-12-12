import pytest
from hamcrest import assert_that, equal_to, is_, is_not
from vpython import vector, color
from src.toolbox.ball import Ball

# class sphere(sphere):
#   def __init__(self, pos=vector(0, 0, 0), radius=0.1, color=color.yellow, velocity=vector(0, 0, 0), mass=1.5, make_trail=False):
#     self.pos = pos
#     self.radius = radius
#     self.color = color
#     self.velocity = velocity
#     self.mass = mass

class SphereTestDouble:
  def __init__(self, mass=1.5, position=vector(0, 0, 0), velocity=vector(0, 0, 0), radius=0.1, color=color.yellow):
    self.mass = mass
    self.pos = position
    self.velocity = velocity
    self.radius = radius
    self.color = color

class BallTestDouble(Ball):
  def __init__(self, mass=1.5, position=vector(0, 0, 0), velocity=vector(0, 0, 0), radius=0.1, color=color.yellow):
     self._ball = SphereTestDouble(mass, position, velocity, radius, color)

class TestBall:
  @pytest.fixture()
  def ball_at_origin(self):
    return BallTestDouble()

  def test_distance_to_itself(self, ball_at_origin):
      assert_that(ball_at_origin.distance_to(ball_at_origin), equal_to(vector(0, 0, 0)))

  def test_distance_to_other_ball(self, ball_at_origin):
      ball_2 = BallTestDouble(position=vector(1, 2, 3))
      assert_that(ball_at_origin.distance_to(ball_2), equal_to(vector(1, 2, 3)))

  def test_no_collision_detection_for_non_colliding_balls(self, ball_at_origin):
     ball_2 = BallTestDouble(position=vector(2 * ball_at_origin._ball.radius, 0.0, 0.0))
     assert_that(ball_at_origin.has_collided_with(ball_2), is_(False))

  def test_collision_detection_for_colliding_balls(self, ball_at_origin):
     ball_2 = BallTestDouble(position=vector(2 * ball_at_origin._ball.radius - 0.001, 0, 0))
     assert_that(ball_at_origin.has_collided_with(ball_2), is_(True))

  def test_force_is_zero_between_non_colliding_balls(self, ball_at_origin):
     ball_2 = BallTestDouble(position=vector(2 * ball_at_origin._ball.radius, 0.0, 0.0))
     assert_that(ball_at_origin.force_between(ball_2), equal_to(vector(0, 0, 0)))

  def test_force_is_not_zero_between_colliding_balls(self, ball_at_origin):
     ball_2 = BallTestDouble(position=vector(2 * ball_at_origin._ball.radius -.001, 0.0, 0.0))
     assert_that(ball_at_origin.force_between(ball_2), is_not(vector(0, 0, 0)))

  def test_momentum_for_zero_velocity(self, ball_at_origin):
     assert_that(ball_at_origin.momentum, equal_to(vector(0, 0, 0)))

  def test_momentum_for_non_zero_velocity(self):
     ball = BallTestDouble(velocity=vector(10, 0, 0))
     assert_that(ball.momentum.x, equal_to(ball._ball.mass * ball._ball.velocity.x))

  def test_move_ball_by_increment_dt(self, ball_at_origin):
     force = vector(1.5, 0, 0)
     dt = 0.1
     ball_at_origin.move(force, dt)
     assert_that(ball_at_origin.momentum, equal_to(dt * force))
     assert_that(ball_at_origin.position, equal_to(dt * dt * force / ball_at_origin.mass))
