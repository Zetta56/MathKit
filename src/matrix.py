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

  def __init__(self, data):
    self.data = data

  def __str__(self):
    output = "\n"
    for row in self.data:
      for element in row:
        output += f"{element:<6}"
      output += "\n"
    return output

  def discriminant2(self):
    """
    Finds discriminant by multiplying top-left element with bottom-right and
    subtracting the opposite of the top-right and bottom-left elements
    """
    if len(self.data) != 2 or len(self.data[0]) != 2:
      raise ValueError("Matrix must contain 2 rows and 2 columns")
    return (self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0])

  def discriminant3(self):
    """
    Finds disciminant by adding top-left to bottom-right diagonals and
    subtracting bottom-left to top-right diagonals (shortcut)
    """
    if len(self.data) != 3 or len(self.data[0]) != 3:
      raise ValueError("Matrix must contain 3 rows and 3 columns")

    total = 0
    for i in range(len(self.data[0])):
      positive, negative = 1, 1
      for j in range(len(self.data)):
        positive *= self.data[(i + j) % len(self.data[0])][j]
        negative *= self.data[(i + j) % len(self.data[0])][len(self.data) - 1 - j]
      total += positive - negative
    return total

  def inverse2(self):
    """Returns the inverse of self if it is a 2x2 matrix"""
    if len(self.data) == 2 and len(self.data[0]) == 2:
      coefficient = 1 / Matrix.discriminant2(self)
      output = Matrix([
        [self.data[1][1], -self.data[0][1]],
        [-self.data[1][0], self.data[0][0]]
      ])
      return output * coefficient

  def __add__(self, other):
    """Adds each corresponding element of self by other"""
    if (isinstance(other, Matrix) and len(self.data) == len(other.data)
        and len(self.data[0]) == len(other.data[0])):
      output = Matrix.zeros(len(other.data), len(other.data[0]))
      for row in range(len(self.data)):
        for col in range(len(other.data[0])):
          output.data[row][col] = self.data[row][col] + other.data[row][col]
      return output

  def __sub__(self, other):
    """Subtracts each corresponding element of self by other"""
    if (isinstance(other, Matrix) and len(self.data) == len(other.data)
        and len(self.data[0]) == len(other.data[0])):
      output = Matrix.zeros(len(other.data), len(other.data[0]))
      for row in range(len(self.data)):
        for col in range(len(other.data[0])):
          output.data[row][col] = self.data[row][col] - other.data[row][col]
      return output

  def __mul__(self, other):
    """
    Scalar: multiplies every element by the scalar value

    Matrix: multiplies each row in self's matrix by each column in the 
    other's matrix. It does so by adding the products of each corresponding
    elements from both matrices
    """
    # Multiplies each element by scalar
    if isinstance(other, int) or isinstance(other, float):
      output = deepcopy(self)
      for row in range(len(self.data)):
        for col in range(len(self.data[0])):
          output.data[row][col] *= other
      return output
    # Performs matrix multiplication, assuming rows and columns are correct
    elif isinstance(other, Matrix):
      if len(self.data[0]) != len(other.data):
        print("Undefined")
        return None
      output = Matrix.zeros(len(other.data), len(other.data[0]))
      # Fill each element with sum of row-column products
      for row in range(len(self.data)):
        for col in range(len(other.data[0])):
          sum = 0
          for i in range(len(self.data[0])):
            sum += self.data[row][i] * other.data[i][col]
          output.data[row][col] = sum
      return output

  def __rmul__(self, other):
    """Allows the multiplication order: scalar * matrix"""
    if isinstance(other, int) or isinstance(other, float):
      output = deepcopy(self)
      # Multiplies each element by scalar
      for row in range(len(self.data)):
        for col in range(len(self.data[0])):
          output.data[row][col] *= other
      return output