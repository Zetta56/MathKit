from copy import deepcopy

class Matrix:
  """
  A matrix solver that supports arithmetic operations

  **Since matrix division doesn't exist, you have to multiply by the inverse
  on the left/right. Note that matrix multiplication is NOT commutative
  
  Ex. AX = B => A'AX = A'B => X = A'B
  
  Ex. XA = B => XAA' = BA' => X = BA'
  """
  @staticmethod
  def zeros(rows, cols):
    """Creates a matrix of a desired size and fills it with 0's"""
    return Matrix([[0 for col in range(cols)] for row in range(rows)])

  def __init__(self, matrix):
    self.matrix = matrix

  def __str__(self):
    output = "\n"
    for row in self.matrix:
      for element in row:
        output += f"{element:<6}"
      output += "\n"
    return output

  def discriminant2(self):
    """
    Finds discriminant by switching top-left element with bottom-right and
    negating top-right and bottom-left elements
    """
    if len(self.matrix) == 2 and len(self.matrix[0]) == 2:
      return (self.matrix[0][0] * self.matrix[1][1] - 
              self.matrix[0][1] * self.matrix[1][0])

  def discriminant3(self):
    """
    Finds disciminant by adding top-left to bottom-right diagonals and
    subtracting bottom-left to top-right diagonals (shortcut)
    """
    if len(self.matrix) == 3 and len(self.matrix[0]) == 3:
      total = 0
      for i in range(len(self.matrix[0])):
        positive, negative = 1, 1
        for j in range(len(self.matrix)):
          positive *= self.matrix[(i + j) % len(self.matrix[0])][j]
          negative *= self.matrix[(i + j) % len(self.matrix[0])][len(self.matrix) - 1 - j]
        total += positive - negative
      return total

  def inverse2(self):
    """Returns the inverse of self if it is a 2x2 matrix"""
    if len(self.matrix) == 2 and len(self.matrix[0]) == 2:
      coefficient = 1 / Matrix.discriminant2(self)
      output = Matrix([
        [self.matrix[1][1], -self.matrix[0][1]],
        [-self.matrix[1][0], self.matrix[0][0]]
      ])
      return output * coefficient

  def __add__(self, other):
    """Adds each corresponding element of self by other"""
    if (isinstance(other, Matrix) and len(self.matrix) == len(other.matrix)
        and len(self.matrix[0]) == len(other.matrix[0])):
      output = Matrix.zeros(len(other.matrix), len(other.matrix[0]))
      for row in range(len(self.matrix)):
        for col in range(len(other.matrix[0])):
          output.matrix[row][col] = self.matrix[row][col] + other.matrix[row][col]
      return output

  def __sub__(self, other):
    """Subtracts each corresponding element of self by other"""
    if (isinstance(other, Matrix) and len(self.matrix) == len(other.matrix)
        and len(self.matrix[0]) == len(other.matrix[0])):
      output = Matrix.zeros(len(other.matrix), len(other.matrix[0]))
      for row in range(len(self.matrix)):
        for col in range(len(other.matrix[0])):
          output.matrix[row][col] = self.matrix[row][col] - other.matrix[row][col]
      return output

  def __mul__(self, other):
    """
    Scalar: multiplies every element by the scalar value

    Matrix: multiplies each row in self's matrix by each column in the 
    other's matrix. It does so by adding the products of each corresponding
    elements from both matrices
    """
    if isinstance(other, int) or isinstance(other, float):
      output = deepcopy(self)
      # Multiplies each element by scalar
      for row in range(len(self.matrix)):
        for col in range(len(self.matrix[0])):
          output.matrix[row][col] *= other
      return output
    elif isinstance(other, Matrix):
      if len(self.matrix[0]) != len(other.matrix):
        print("Undefined")
        return None
      output = Matrix.zeros(len(other.matrix), len(other.matrix[0]))
      # Fill each element with sum of row-column products
      for row in range(len(self.matrix)):
        for col in range(len(other.matrix[0])):
          sum = 0
          for i in range(len(self.matrix[0])):
            sum += self.matrix[row][i] * other.matrix[i][col]
          output.matrix[row][col] = sum
      return output

  def __rmul__(self, other):
    """Allows the multiplication order: scalar * matrix"""
    if isinstance(other, int) or isinstance(other, float):
      output = deepcopy(self)
      # Multiplies each element by scalar
      for row in range(len(self.matrix)):
        for col in range(len(self.matrix[0])):
          output.matrix[row][col] *= other
      return output