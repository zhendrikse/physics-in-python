import pytest
from hamcrest import assert_that, equal_to, is_, is_not
from vpython import vec
from src.toolbox.charged_ring import ChargedRing

class TestChargedRing:
   @pytest.fixture()
   def ring(self):
      return ChargedRing(draw=False)

   def test_electric_field_values(self, ring):
      radius = ring.radius
      position = vec(0, 0, radius) + 1.5 * radius * vec(0.5, 0.5, 0.5)
      assert_that(ring.field_at(position).x - 30519217387.805046 < 1E-3)
      assert_that(ring.field_at(position).y - 30519217387.80504 < 1E-3)
      assert_that(ring.field_at(position).z - 101329864794.56285 < 1E-3)
