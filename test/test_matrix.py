import unittest
from unittest.mock import patch
from src.matrix import Matrix

class TestMatrix(unittest.TestCase):
  def test_discriminant2(self):
    matrix = Matrix([[1, -2], [5, 3]])
    self.assertEqual(matrix.discriminant2(), 13)

  def test_invalid_discriminant2(self):
    matrix = Matrix([[6, -6, -8], [1, -7, -7], [-1, 4, 4]])
    self.assertRaises(ValueError, matrix.discriminant2)

  def test_discriminant3(self):
    matrix = Matrix([[6, -6, -8], [1, -7, -7], [-1, 4, 4]])
    self.assertEqual(matrix.discriminant3(), 6)
    
  def test_invalid_discriminant3(self):
    matrix = Matrix([[1, -2], [5, 3]])
    self.assertRaises(ValueError, matrix.discriminant3)

  def test_inverse2(self):
    matrix = Matrix([[4, -7], [2, -5]])
    inverse = matrix.inverse2().data
    self.assertAlmostEqual(inverse[0][0], 5/6, places=2)
    self.assertAlmostEqual(inverse[0][1], -7/6, places=2)
    self.assertAlmostEqual(inverse[1][0], 1/3, places=2)
    self.assertAlmostEqual(inverse[1][1], -2/3, places=2)

  def test_add(self):
    matrix1 = Matrix([[-2, 3, 1], [-1, 5, 5]])
    matrix2 = Matrix([[5, -5, -5], [4, -3, 4]])
    self.assertEqual((matrix1 + matrix2).data, [[3, -2, -4], [3, 2, 9]])

  def test_subtract(self):
    matrix1 = Matrix([[5, -1], [4, 5], [2, 1], [4, -5]])
    matrix2 = Matrix([[-2, 3], [3, 1], [1, 4], [-4, 5]])
    self.assertEqual((matrix2 - matrix1).data, [[-7, 4], [-1, -4], [-1, 3], [-8, 10]])

  def test_multiply_matrix(self):
    matrix1 = Matrix([[-3, 0, 0], [-2, 4, -3], [-1, 1, -3]])
    matrix2 = Matrix([[1, -3, -1], [1, -2, 0], [-3, 1, 0]])
    self.assertEqual((matrix1 * matrix2).data, [[-3, 9, 3], [11, -5, 2], [9, -2, 1]])

  def test_multiply_scalar(self):
    matrix = Matrix([[12, 4], [-4, -10], [-6, 12]])
    self.assertEqual((matrix * -0.5).data, [[-6, -2], [2, 5], [3, -6]])

  def test_multiply_right(self):
    matrix = Matrix([[12, 4], [-4, -10], [-6, 12]])
    self.assertEqual((-0.5 * matrix).data, [[-6, -2], [2, 5], [3, -6]])

  # Creates a MagicMock of plt.show(), so that graphs don't pop up during tests
  @patch("src.matrix.plt.show")
  def test_graphs(self, mock_show):
    try:
      matrix = Matrix([[1, -2], [5, 3]])
      matrix.graph2D()
    except:
      self.fail("An error has occurred while graphing")

if __name__ == '__main__':
  unittest.main()