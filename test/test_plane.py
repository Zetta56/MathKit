import matplotlib.pyplot as plt
import unittest
from unittest.mock import patch
from src.plane import Plane

class TestPlane(unittest.TestCase):
  def test_degrees_to_rectangular(self):
    rectangular = Plane.to_rectangular(11, 29, degrees=True)
    self.assertAlmostEqual(rectangular[0], 9.62, places=2)
    self.assertAlmostEqual(rectangular[1], 5.33, places=2)
  
  def test_radians_to_rectangular(self):
    rectangular = Plane.to_rectangular(5, 2)
    self.assertAlmostEqual(rectangular[0], -2.08, places=2)
    self.assertAlmostEqual(rectangular[1], 4.55, places=2)

  def test_q1_to_polar(self):
    polar = Plane.to_polar(5, 2)
    self.assertAlmostEqual(polar[0], 5.39, places=2)
    self.assertAlmostEqual(polar[1], 0.38, places=2)

  def test_q2_to_polar(self):
    polar = Plane.to_polar(-3, 8)
    self.assertAlmostEqual(polar[0], 8.54, places=2)
    self.assertAlmostEqual(polar[1], 1.93, places=2)

  def test_q3_to_polar(self):
    polar = Plane.to_polar(-4, -6)
    self.assertAlmostEqual(polar[0], 7.21, places=2)
    self.assertAlmostEqual(polar[1], 4.12, places=2)

  def test_q4_to_polar(self):
    polar = Plane.to_polar(6, -5)
    self.assertAlmostEqual(polar[0], 7.81, places=2)
    self.assertAlmostEqual(polar[1], 5.59, places=2)

  def test_to_polar_degrees(self):
    polar = Plane.to_polar(6, -5, degrees=True)
    self.assertAlmostEqual(polar[0], 7.81, places=2)
    self.assertAlmostEqual(polar[1], 320.19, places=2)

  @patch("src.matrix.plt.show")
  def test_graph_rectangular(self, mock_show):
    try:
      Plane.graph_rectangular(3, 4, scale=5)
    except:
      self.fail("An error has occurred while graphing rectangular")

  @patch("src.matrix.plt.show")
  def test_graph_polar(self, mock_show):
    try:
      Plane.graph_polar(10, 3)
      Plane.graph_polar(10, 3, degrees=True)
    except:
      self.fail("An error has occurred while graphing polar")

  @patch("src.matrix.plt.show")
  def test_init_graphs(self, mock_show):
    try:
      Plane.init_cartesian2(plt, scale=5)
      Plane.init_cartesian3(plt, scale=3)
      Plane.init_polar(plt)
      Plane.init_polar(plt, degrees=True)
    except:
      self.fail("An error has occurred while initializing graphs")

if __name__ == '__main__':
  unittest.main()