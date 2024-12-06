import pytest
from hamcrest import assert_that, equal_to, is_
from vpython import vector, color, mag
from src.toolbox.ball import Ball

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

  def test_distance_to_other(self, ball_at_origin):
      ball_2 = BallTestDouble(position=vector(1, 2, 3))
      assert_that(ball_at_origin.distance_to(ball_2), equal_to(vector(1, 2, 3)))

  def test_no_collision(self, ball_at_origin):
     ball_2 = BallTestDouble(position=vector(2 * ball_at_origin._ball.radius, 0.0, 0.0))
     assert_that(ball_at_origin.has_collided_with(ball_2), is_(False))

  def test_collision(self, ball_at_origin):
     ball_2 = BallTestDouble(position=vector(2 * ball_at_origin._ball.radius - 0.001, 0, 0))
     assert_that(ball_at_origin.has_collided_with(ball_2), is_(True))
