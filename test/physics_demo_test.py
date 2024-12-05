import pytest
from hamcrest import *
from physics_demo import physics_demo


class Testphysics_demo:

  def test_a_new_physics_demo(self):
      assert True is False
      # Hamcrest style
      # assert_that(True, equal_to(False))
