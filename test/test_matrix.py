import unittest
from unittest.mock import patch
from src.matrix import Matrix

class TestMatrix(unittest.TestCase):
  def test_determinant2(self):
    matrix = Matrix([[1, -2], [5, 3]])
    self.assertEqual(matrix.determinant(), 13)

  def test_determinant3(self):
    matrix = Matrix([[6, -6, -8], [1, -7, -7], [-1, 4, 4]])
    self.assertEqual(matrix.determinant(), 6)

  def test_inverse2(self):
    matrix =  Matrix([[4, -7], [2, -5]])
    inverse = matrix.inverse()
    correct =  Matrix([[5/6, -7/6], [1/3, -2/3]])
    for row in range(len(matrix.data)):
      for col in range(len(matrix.data[0])):
        self.assertAlmostEqual(inverse.data[row][col], correct.data[row][col], places=2)

  def test_inverse3(self):
    matrix = Matrix([[3, 0, 2], [2, 0, -2], [0, 1, 1]])
    inverse = matrix.inverse()
    correct = Matrix([[0.2, 0.2, 0], [-0.2, 0.3, 1], [0.2, -0.3, 0]])
    for row in range(len(matrix.data)):
      for col in range(len(matrix.data[0])):
        self.assertAlmostEqual(inverse.data[row][col], correct.data[row][col], places=2)

  def test_row_echelon2x2(self):
    matrix = Matrix([[6, 4], [3, 13]])
    ref = matrix.to_row_echelon()
    correct = Matrix([[1, 2/3], [0, 1]])
    for row in range(len(matrix.data)):
      for col in range(len(matrix.data[0])):
        self.assertAlmostEqual(ref.data[row][col], correct.data[row][col], places=2)
    
  def test_row_echelon3x4(self):
    matrix = Matrix([[5, 3, 3, 2], [6, -9, 2, 5], [-1, 5, -7, 2]])
    ref = matrix.to_row_echelon()
    correct = Matrix([[1, 3/5, 3/5, 2/5], [0, 1, 8/63, -13/63], [0, 0, 1, -1/2]])
    for row in range(len(matrix.data)):
      for col in range(len(matrix.data[0])):
        self.assertAlmostEqual(ref.data[row][col], correct.data[row][col], places=2)

  def test_row_echelon_interchange(self):
    matrix = Matrix([[0, 0, 3, 1], [-2, 0, 6, 7], [0, 5, -12, 2]])
    ref = matrix.to_row_echelon()
    correct = Matrix([[1, 0, -3, -7/2], [0, 1, -12/5, 2/5], [0, 0, 1, 1/3]])
    for row in range(len(matrix.data)):
      for col in range(len(matrix.data[0])):
        self.assertAlmostEqual(ref.data[row][col], correct.data[row][col], places=2)

  def test_row_echelon_zero_column(self):
    matrix = Matrix([[0, 0, 3, 1], [0, 0, 0, 0], [0, 5, -12, 2]])
    ref = matrix.to_row_echelon()
    correct = Matrix([[0, 1, -12/5, 2/5], [0, 0, 1, 1/3], [0, 0, 0, 0]])
    for row in range(len(matrix.data)):
      for col in range(len(matrix.data[0])):
        self.assertAlmostEqual(ref.data[row][col], correct.data[row][col], places=2)

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
  def test_graph(self, mock_show):
    try:
      matrix = Matrix([[1, -2], [5, 3]])
      matrix2 = Matrix([[-1, 2, 2], [4, -1, 5], [3, -4, 5]])
      matrix3 = Matrix([[1], [2], [3]])
      matrix.graph()
      matrix2.graph()
      self.assertRaises(ValueError, matrix3.graph)
    except:
      self.fail("An error has occurred while general graphing")

  @patch("src.matrix.plt.show")
  def test_graph2x1(self, mock_show):
    try:
      matrix = Matrix([[1, -2], [5, 3]])
      matrix.graph2x1()
      matrix.graph2x1(column=1, scale=6)
    except:
      self.fail("An error has occurred while graphing 2x1")

  @patch("src.matrix.plt.show")
  def test_graph2x2(self, mock_show):
    try:
      matrix = Matrix([[1, -2], [5, 3]])
      matrix.graph2x2()
      matrix.graph2x2(vector=(-1, 2), scale=5)
    except:
      self.fail("An error has occurred while graphing 2x2")

  @patch("src.matrix.plt.show")
  def test_graph3x3(self, mock_show):
    try:
      matrix = Matrix([[-1, 2, 2], [4, -1, 5], [3, -4, 5]])
      matrix.graph3x3()
      matrix.graph3x3(vector=(4, -2, 1), scale=10)
    except:
      self.fail("An error has occurred while graphing 3x3")

if __name__ == '__main__':
  unittest.main()