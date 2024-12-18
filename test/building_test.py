import pytest
from hamcrest import assert_that, equal_to, is_, is_not
from vpython import vector
from src.toolbox.building import Building


class TestBuilding:
  @pytest.fixture()
  def building_at_origin(self):
    return Building(draw=False)
  
  def test_moment_of_inertia(self, building_at_origin):
    assert_that(building_at_origin.moment_of_inertia, equal_to(8666.666666666668))

  def test_building_at_origin(self, building_at_origin):
    assert_that(building_at_origin._angular_acceleration(), equal_to(0))