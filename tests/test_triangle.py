import unittest
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
  
  def test_ssa(self):
    triangle = Triangle(a=5, b=8, B=40)
    self.assertAlmostEqual(triangle.sides[2], 11.156, places=2)
    self.assertAlmostEqual(triangle.angles[0], 23.687, places=2)
    self.assertAlmostEqual(triangle.angles[2], 116.313, places=2)

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

  def test_zero_angle(self):
    triangle = Triangle(a=3, b=4, c=0)
    self.assertEqual(str(triangle), "Triangle could not be made with given information")

  def test_zero_side(self):
    triangle = Triangle(a=0, b=4, c=50)
    self.assertEqual(str(triangle), "Triangle could not be made with given information")

unittest.main()