import unittest
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

if __name__ == '__main__':
  unittest.main()