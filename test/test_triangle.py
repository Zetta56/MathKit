import unittest
from unittest.mock import patch
from src.triangle import Triangle

class TriangleTest(unittest.TestCase):
  def test_sss(self):
    triangle = Triangle(a=4, b=6, c=8)
    self.assertAlmostEqual(triangle.angles[0], 28.955, places=2)
    self.assertAlmostEqual(triangle.angles[1], 46.567, places=2)
    self.assertAlmostEqual(triangle.angles[2], 104.478, places=2)

  def test_sas(self):
    triangle = Triangle(a=10, b=6, C=50)
    self.assertAlmostEqual(triangle.sides[2], 7.672, places=2)
    self.assertAlmostEqual(triangle.angles[0], 93.197, places=2)
    self.assertAlmostEqual(triangle.angles[1], 36.803, places=2)
  
  # Tests Law of Sines in quadrant 1
  def test_ssa1(self):
    triangle = Triangle(a=5, b=8, B=40)
    self.assertAlmostEqual(triangle.sides[2], 11.156, places=2)
    self.assertAlmostEqual(triangle.angles[0], 23.687, places=2)
    self.assertAlmostEqual(triangle.angles[2], 116.313, places=2)

  # Tests Law of Sines in quadrant 2
  def test_ssa2(self):
    triangle = Triangle(A=50, a=150, c=100)
    self.assertAlmostEqual(triangle.sides[1], 193.24, places=2)
    self.assertAlmostEqual(triangle.angles[1], 99.29, places=2)
    self.assertAlmostEqual(triangle.angles[2], 30.71, places=2)

  def test_asa(self):
    triangle = Triangle(A=30, c=8, B=70)
    self.assertAlmostEqual(triangle.sides[0], 4.062, places=2)
    self.assertAlmostEqual(triangle.sides[1], 7.634, places=2)
    self.assertAlmostEqual(triangle.angles[2], 80, places=2)

  def test_right(self):
    triangle = Triangle(a=3, b=4, c=5)
    self.assertAlmostEqual(triangle.angles[0], 36.87, places=2)
    self.assertAlmostEqual(triangle.angles[1], 53.13, places=2)
    self.assertAlmostEqual(triangle.angles[2], 90, places=2)

  # Ensures custom error triggers instead of default error
  def test_zero(self):
    triangle = Triangle(a=3, b=4, c=0)
    self.assertEqual(str(triangle), "Triangle could not be made with given information")

  def test_equilateral(self):
    triangle = Triangle(a=5, b=5, A=60)
    self.assertAlmostEqual(triangle.sides[2], 5, places=2)
    self.assertAlmostEqual(triangle.angles[1], 60, places=2)
    self.assertAlmostEqual(triangle.angles[2], 60, places=2)

  def test_obtuse_isosceles(self):
    triangle = Triangle(a=3, b=3, c=5)
    self.assertAlmostEqual(triangle.angles[0], 33.557, places=2)
    self.assertAlmostEqual(triangle.angles[1], 33.557, places=2)
    self.assertAlmostEqual(triangle.angles[2], 112.885, places=2)

  # Ensures longest side/angle check in is_valid works correctly 
  def test_acute_isosceles(self):
    triangle = Triangle(a=6, b=6, c=5)
    self.assertAlmostEqual(triangle.angles[0], 65.376, places=2)
    self.assertAlmostEqual(triangle.angles[1], 65.376, places=2)
    self.assertAlmostEqual(triangle.angles[2], 49.249, places=2)

  @patch("src.triangle.plt.show")
  def test_graph(self, mock_show):
    try:
      triangle = Triangle(a=6, b=6, c=5)
      triangle.graph()
    except:
      self.fail("An error has occurred while graphing triangle")

if __name__ == '__main__':
  unittest.main()