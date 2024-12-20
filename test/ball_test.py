import pytest
from hamcrest import assert_that, equal_to, is_, is_not
from vpython import vector
from src.toolbox.ball import Ball
from src.toolbox.building import Building

class TestBall:
   @pytest.fixture()
   def ball_at_origin(self):
      return Ball(radius=1.0, draw=False)

   def test_distance_to_itself(self, ball_at_origin):
      assert_that(ball_at_origin.distance_to(ball_at_origin), equal_to(vector(0, 0, 0)))

   def test_distance_to_other_ball(self, ball_at_origin):
      ball_2 = Ball(position=vector(1, 2, 3), draw=False)
      assert_that(ball_at_origin.distance_to(ball_2), equal_to(vector(1, 2, 3)))

   def test_no_collision_detection_for_non_colliding_balls(self, ball_at_origin):
      ball_2 = Ball(position=vector(2 * ball_at_origin.radius, 0.0, 0.0), radius=1.0, draw=False)
      assert_that(ball_at_origin.has_collided_with(ball_2), is_(False))

   def test_collision_detection_for_colliding_balls(self, ball_at_origin):
      ball_2 = Ball(position=vector(2 * ball_at_origin.radius - 0.001, 0, 0), radius=1.0, draw=False)
      assert_that(ball_at_origin.has_collided_with(ball_2), is_(True))

   def test_force_is_zero_between_non_colliding_balls(self, ball_at_origin):
      ball_2 = Ball(position=vector(2 * ball_at_origin.radius, 0.0, 0.0), radius=1.0, draw=False)
      assert_that(ball_at_origin.force_between(ball_2), equal_to(vector(0, 0, 0)))

   def test_force_is_not_zero_between_colliding_balls(self, ball_at_origin):
      ball_2 = Ball(position=vector(2 * ball_at_origin.radius -.001, 0.0, 0.0), radius=1.0, draw=False)
      assert_that(ball_at_origin.force_between(ball_2), is_not(vector(0, 0, 0)))

   def test_momentum_for_zero_velocity(self, ball_at_origin):
      assert_that(ball_at_origin.momentum, equal_to(vector(0, 0, 0)))

   def test_momentum_for_non_zero_velocity(self):
      ball = Ball(velocity=vector(10, 0, 0), draw=False)
      assert_that(ball.momentum.x, equal_to(ball.mass * ball.velocity.x))

   def test_move_ball_by_increment_dt(self, ball_at_origin):
      force = vector(1.5, 0, 0)
      dt = 0.1
      ball_at_origin.move(force, dt)
      assert_that(ball_at_origin.momentum, equal_to(dt * force))
      assert_that(ball_at_origin.position, equal_to(dt * dt * force / ball_at_origin.mass))

   def test_ball_with_zero_velocity_does_not_hit_building(self, ball_at_origin):
      building = Building(position=vector(-10, 0, 0), draw=False)
      assert_that(not ball_at_origin.hits(building))

   def test_moving_ball_hits_building_from_left(self):
      building = Building(length=4, width=2, height=10, draw=False)
      radius = 1
      collision_point = vector(building.position.x + building.L / 2 + radius, building.position.y, building.position.z)
      ball = Ball(position=collision_point, velocity=vector(-1, 0, 0), radius=1, draw= False)
      assert_that(ball.hits(building))

   def test_moving_ball_hits_building_from_right(self):
      building = Building(length=4, width=2, height=10, draw=False)
      radius = 1
      collision_point = vector(building.position.x - building.L / 2 - radius, building.position.y, building.position.z)
      ball = Ball(position=collision_point, velocity=vector(1, 0, 0), radius=1, draw= False)
      assert_that(ball.hits(building))

   def test_moving_ball_flies_over_building_from_the_right(self):
      building = Building(length=4, width=2, height=10, draw=False)
      radius = 1
      collision_point = vector(building.position.x - building.L / 2 - radius, building.H + 3, building.position.z)
      ball = Ball(position=collision_point, velocity=vector(1, 0, 0), radius=1, draw= False)
      assert_that(not ball.hits(building))

   def test_moving_ball_flies_over_building_from_left(self):
      building = Building(length=4, width=2, height=10, draw=False)
      radius = 1
      collision_point = vector(building.position.x + building.L / 2 + radius, building.H + 3, building.position.z)
      ball = Ball(position=collision_point, velocity=vector(-1, 0, 0), radius=1, draw= False)
      assert_that(not ball.hits(building))
     
