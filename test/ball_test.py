import pytest
from hamcrest import assert_that, equal_to, is_
from vpython import vector, color
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

  def test_distance_to_itself(self):
      ball = BallTestDouble()
      assert_that(ball.distance_to(ball), equal_to(vector(0, 0, 0)))

  def test_distance_to_other(self):
      ball = BallTestDouble()
      assert_that(ball.distance_to(BallTestDouble(position=vector(1, 2, 3))), equal_to(vector(1, 2, 3)))

  def test_no_collision(self):
     ball_1 = BallTestDouble(position=vector(0, 0, 0))
     ball_2 = BallTestDouble(position=vector(2 * ball_1._ball.radius, 0.0, 0.0))
     assert_that(ball_1.has_collided_with(ball_2), is_(False))

  def test_collision(self):
     ball_1 = BallTestDouble(position=vector(0, 0, 0))
     ball_2 = BallTestDouble(position=vector(ball_1._ball.radius, 0, 0))
     assert_that(ball_1.has_collided_with(ball_2), is_(True))
