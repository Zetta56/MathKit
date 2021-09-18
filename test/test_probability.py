import unittest
from unittest.mock import patch
from src.probability import Probability

class TestProbability(unittest.TestCase):
  def test_permutations_greater_n(self):
    self.assertEqual(Probability.permutations(15, 3), 2730)

  def test_permutations_greater_r(self):
    self.assertEqual(Probability.permutations(3, 5), 0)

  def test_combinations_greater_n(self):
    self.assertEqual(Probability.combinations(12, 4), 495)

  def test_combinations_greater_r(self):
    self.assertEqual(Probability.combinations(2, 6), 0)

  def test_binomial_min(self):
    self.assertAlmostEqual(Probability.binomial(4, 2, 0.45, "min"), 0.609, places=3)

  def test_binomial_max(self):
    self.assertAlmostEqual(Probability.binomial(6, 1, 1/9, "max"), 0.863, places=3)

  def test_binomial_exact(self):
    self.assertAlmostEqual(Probability.binomial(10, 6, 0.5), 0.205, places=3)

  @patch("src.probability.plt.show")
  @patch("src.probability.plt.pause")
  def test_graph_binomial(self, mock_show, mock_pause):
    try:
      Probability.graph_binomial(5, 3, 4/7, r_meaning="min")
    except:
      self.fail("An error has occurred while graphing binomial probability")

if __name__ == '__main__':
  unittest.main()