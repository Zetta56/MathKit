import unittest
from src.base import Base

class TestBase(unittest.TestCase):
  def test_convert_lower_base(self):
    self.assertAlmostEqual(Base.convert(53, 8, 5), 133, places=2)

  def test_convert_higher_base(self):
    self.assertAlmostEqual(Base.convert(106, 7, 12), 47, places=2)
  
  def test_convert_invalid(self):
    self.assertAlmostEqual(Base.convert(96, 8, 5), None, places=2)

  def test_to_base_10(self):
    self.assertAlmostEqual(Base.to_base_10(63, 7), 45, places=2)

  def test_from_base_10(self):
    self.assertAlmostEqual(Base.from_base_10(164, 4), 2210, places=2)

if __name__ == '__main__':
  unittest.main()