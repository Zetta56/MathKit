import unittest
from src.base import Base

class TestBase(unittest.TestCase):
  def test_base_to_decimal(self):
    self.assertAlmostEqual(Base.base_to_decimal(63, 7), 45, places=2)

  def test_decimal_to_base(self):
    self.assertAlmostEqual(Base.decimal_to_base(164, 4), 2210, places=2)

  def test_convert(self):
    self.assertAlmostEqual(Base.convert(53, 8, 5), 133, places=2)
  
  def test_convert_invalid(self):
    self.assertAlmostEqual(Base.convert(96, 8, 5), None, places=2)

if __name__ == '__main__':
  unittest.main()