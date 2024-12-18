import pytest
from hamcrest import assert_that, equal_to, is_, is_not
from src.toolbox.spring import Spring, zero_force
from vpython import vector

class TestCapacitor:
  @pytest.fixture()
  def spring(self):
     return Spring(draw=False)
  
  def test_spring_force_is_zero_in_equilibrium(self, spring):
    assert_that(spring.force, equal_to(zero_force))
  
  def test_spring_when_stretched(self, spring):
    spring.update(vector(0.5, 0, 0))
    assert_that(spring.is_stretched_or_compressed())
  
  def test_spring_force_when_stretched(self, spring):
    spring.update(vector(0.5, 0, 0))
    assert_that(spring.is_stretched_or_compressed())
    assert_that(spring.force, equal_to(vector(0.5, 0, 0)))
