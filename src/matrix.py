from copy import deepcopy
from src.plane import Plane
import matplotlib.pyplot as plt

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
    """Data Format: [[a, b, c], [d, e, f], [g, h, i]]"""
    self.data = data

  def __str__(self):
    """
    Intended Representation:
    a   b
    c   d
    """
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

  def multiply_scalar(self, scalar):
    """Multiplies each value in matrix with the scalar value"""
    output = deepcopy(self)
    for row in range(len(output.data)):
      for col in range(len(output.data[0])):
        output.data[row][col] *= scalar
    return output

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
    Multiplies each row in self's matrix by each column in the other's
    matrix. It does so by adding the products of each corresponding
    elements from both matrices. This also handles scalar multiplication.
    """
    # Uses multiply_scalar if 'other' is an int or float
    if isinstance(other, int) or isinstance(other, float):
      return self.multiply_scalar(other)
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
    """Allows the scalar multiplication order: scalar * matrix"""
    if isinstance(other, int) or isinstance(other, float):
      return self.multiply_scalar(other)

  def graph(self, vector=None, column=0, scale=1):
    """
    Shortcut to access graph2x1, graph2x2, or graph3x3, depending on
    the current matrix's order (number of rows and columns)
    """
    if len(self.data) == 2 and len(self.data[0]) == 1:
      self.graph2x1(column=column, scale=scale)
    elif len(self.data) == 2 and len(self.data[0]) == 2:
      vector = (1, 1) if vector is None else vector
      self.graph2x2(vector=vector, scale=scale)
    elif len(self.data) == 3 and len(self.data[0]) == 3:
      vector = (1, 1, 1) if vector is None else vector
      self.graph3x3(vector=vector, scale=scale)
    else:
      raise ValueError("Matrix is neither a 2x1, 2x2, nor 3x3 matrix")

  def graph2x1(self, column=0, scale=1):
    """
    Graphs the basis vectors of a 2x1 matrix on a 2D plane.
    For larger matrices, you can specify the matrix column to graph.
    """
    if len(self.data) == 2:
      Plane.init_cartesian2(plt, scale)
      plt.title("Basis Vectors")
      plt.arrow(0, 0, self.data[0][column], 0, lw=3, head_width=(scale/50), color="g")
      plt.arrow(0, 0, 0, self.data[1][column], lw=3, head_width=(scale/50), color="b")
      plt.arrow(0, 0, self.data[0][column], self.data[1][column], lw=3, head_width=(scale/50), color="y")
      plt.show()

  def graph2x2(self, vector=(1, 1), scale=1):
    """
    Graphs the basis vectors of a 2x2 matrix, as well as its transformation
    on a given vector.
    """
    Plane.init_cartesian2(plt, scale)
    ax = plt.gca()
    plt.title("Vector Graph")
    # Basis vectors
    plt.arrow(0, 0, self.data[0][0], self.data[1][0], head_width=(scale/50), color="g", label="Basis i")
    ax.text(self.data[0][0], self.data[1][0], f"({self.data[0][0]}, {self.data[1][0]})")
    plt.arrow(0, 0, self.data[0][1], self.data[1][1], head_width=(scale/50), color="b", label="Basis j")
    ax.text(self.data[0][1], self.data[1][1], f"({self.data[0][1]}, {self.data[1][1]})")
    # Matrix transformation on specified vector
    transformed = self * Matrix([[vector[0]], [vector[1]]])
    plt.arrow(0, 0, vector[0], vector[1], head_width=(scale/50), color="y", label="Pre-transform")
    ax.text(vector[0], vector[1], f"({vector[0]}, {vector[1]})")
    plt.arrow(0, 0, transformed.data[0][0], transformed.data[1][0], head_width=(scale/50),
      color="tab:orange", label="Post-transform")
    ax.text(transformed.data[0][0], transformed.data[1][0], f"({transformed.data[0][0]}, {transformed.data[1][0]})")
    # Display legend and graph
    ax.legend()
    plt.show()

  def graph3x3(self, vector=(1, 1, 1), scale=1):
    """
    Graphs the basis vectors of a 3x3 matrix, as well as its transformation
    on a given vector.
    """
    Plane.init_cartesian3(plt, scale)
    ax = plt.gca()
    plt.title("Vector Graph")
    # Basis vectors
    plt.quiver(0, 0, 0, self.data[0][0], self.data[1][0], self.data[2][0], color="r", label="Basis i")
    ax.text(self.data[0][0], self.data[1][0], self.data[2][0], f"({self.data[0][0]}, {self.data[1][0]}, {self.data[2][0]})")
    plt.quiver(0, 0, 0, self.data[0][1], self.data[1][1], self.data[2][1], color="g", label="Basis j")
    ax.text(self.data[0][1], self.data[1][1], self.data[2][1], f"({self.data[0][1]}, {self.data[1][1]}, {self.data[2][1]})")
    plt.quiver(0, 0, 0, self.data[0][2], self.data[1][2], self.data[2][2], color="b", label="Basis k")
    ax.text(self.data[0][2], self.data[1][2], self.data[2][2], f"({self.data[0][2]}, {self.data[1][2]}, {self.data[2][2]})")
    # Matrix transformation on specified vector
    transformed = self * Matrix([[vector[0]], [vector[1]], [vector[2]]])
    plt.quiver(0, 0, 0, vector[0], vector[1], vector[2], color="y", label="Pre-transform")
    ax.text(vector[0], vector[1], vector[2], f"({vector[0]}, {vector[1]}, {vector[2]})")
    plt.quiver(0, 0, 0, transformed.data[0][0], transformed.data[1][0],
      transformed.data[2][0], color="tab:orange", label="Post-transform")
    ax.text(transformed.data[0][0], transformed.data[1][0], transformed.data[2][0],
      f"({transformed.data[0][0]}, {transformed.data[1][0]}, {transformed.data[2][0]})")
    # Display legend and graph
    ax.legend()
    plt.show()