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

  def test_cofactor(self):
    matrix = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    self.assertAlmostEqual(matrix.cofactor(1, 1), -12)

  def test_row_echelon_2x2(self):
    matrix = Matrix([[6, 4], [3, 13]])
    ref = matrix.to_row_echelon()
    correct = Matrix([[1, 2/3], [0, 1]])
    for row in range(len(matrix.data)):
      for col in range(len(matrix.data[0])):
        self.assertAlmostEqual(ref.data[row][col], correct.data[row][col], places=2)
    
  def test_row_echelon_3x4(self):
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

  def test_reduced_row_echelon(self):
    matrix = Matrix([[5, 2, 5, -3], [6, 1, 0, 7], [-4, 3, -1, 3]])
    ref = matrix.to_reduced_row_echelon()
    correct = Matrix([[1, 0, 0, 107/117], [0, 1, 0, 59/39], [0, 0, 1, -248/117]])
    for row in range(len(matrix.data)):
      for col in range(len(matrix.data[0])):
        self.assertAlmostEqual(ref.data[row][col], correct.data[row][col], places=2)

  def test_dot_3x1(self):
    matrix1 = Matrix([[3], [2], [6]])
    matrix2 = Matrix([[1], [7], [4]])
    self.assertAlmostEqual(matrix1.dot(matrix2), 41)

  def test_dot_nonzero_column(self):
    matrix1 = Matrix([[5, 1, 7], [5, 3, 2], [1, 6, 2]])
    matrix2 = Matrix([[1, 6], [7, -2], [4, 1]])
    self.assertAlmostEqual(matrix1.dot(matrix2, col=1), 6)

  def test_cross(self):
    matrix1 = Matrix([4, 1, -6])
    matrix2 = Matrix([2, 3, 1])
    correct = Matrix([19, -16, 10])
    cross_product = matrix1.cross(matrix2)
    for row in range(len(cross_product.data)):
      for col in range(len(cross_product.data[0])):
        self.assertAlmostEqual(cross_product.data[row][col],
         correct.data[row][col], places=2)

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

  def test_multiply_scalar_right(self):
    matrix = Matrix([[12, 4], [-4, -10], [-6, 12]])
    self.assertEqual((-0.5 * matrix).data, [[-6, -2], [2, 5], [3, -6]])

  # Creates a MagicMock of plt.show(), so that graphs don't pop up during tests
  @patch("src.matrix.plt.show")
  def test_graph_vector2(self, mock_show):
    try:
      matrix = Matrix([[1, -2], [5, 3]])
      matrix.graph_vector()
      matrix.graph_vector(col=1, scale=6)
    except:
      self.fail("An error has occurred while graphing 2D vector")

  @patch("src.matrix.plt.show")
  def test_graph_vector3(self, mock_show):
    try:
      matrix = Matrix([[1, -2], [5, 3], [-3, 1]])
      matrix.graph_vector()
      matrix.graph_vector(scale=6)
    except:
      self.fail("An error has occurred while graphing 3D vector")

  @patch("src.matrix.plt.show")
  def test_graph_transform2(self, mock_show):
    try:
      matrix = Matrix([[1, -2], [5, 3]])
      matrix.graph_transform2()
      matrix.graph_transform2(vector=(-1, 2), scale=5)
    except:
      self.fail("An error has occurred while graphing 2D transformation")

  @patch("src.matrix.plt.show")
  def test_graph_transform3(self, mock_show):
    try:
      matrix = Matrix([[-1, 2, 2], [4, -1, 5], [3, -4, 5]])
      matrix.graph_transform3()
      matrix.graph_transform3(vector=(4, -2, 1), scale=10)
    except:
      self.fail("An error has occurred while graphing 3D transformation")

if __name__ == '__main__':
  unittest.main()