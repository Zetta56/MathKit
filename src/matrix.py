from copy import deepcopy
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter, FuncFormatter

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

  def graph2D(self, scale=None):
    plt.title("Visual Representation")
    plt.plot([1, 2, 3], [1, 2, 3])
    self.init_cartesian(plt, scale)
    plt.show()

  def graphBasis(self, column=0, scale=1):
    """
    Graphs the basis vectors of a 1x2 matrix on a 2D plane.
    For larger matrices, you can specify the matrix column to graph.
    """
    if len(self.data) == 2:
      plt.title("Basis Vectors")
      plt.arrow(0, 0, self.data[0][column], 0, lw=3, head_width=(scale/50), color="g")
      plt.arrow(0, 0, 0, self.data[1][column], lw=3, head_width=(scale/50), color="b")
      plt.arrow(0, 0, self.data[0][column], self.data[1][column], lw=3, head_width=(scale/50), color="y")
      self.init_cartesian(plt, scale)
      plt.show()

  def init_cartesian(self, plt, scale):
    """Creates a formatted cartesian plane."""
    # Setup
    plt.grid(True)
    ax = plt.gca()
    # Center axes at origin and remove unnecessary ones
    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    ax.spines.left.set_position('center')
    ax.spines.bottom.set_position('center')
    # Set axes limits to scale
    ax.set_aspect('equal')
    ax.set_xlim(-scale, scale)
    ax.set_ylim(-scale, scale)
    # Add black(k) axes arrows that can go outside plot's borders
    # Positioning: xy-coords on stated axis and absolute on perpendicular axis
    ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 0, "<k", transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)
    ax.plot(0, 0, "vk", transform=ax.get_xaxis_transform(), clip_on=False)
    # Format tick labels to hide the origin and round to 2 decimal places
    hide_origin = lambda x, pos: "" if x == 0 else x
    ax.xaxis.set_major_formatter(FuncFormatter(hide_origin))
    ax.yaxis.set_major_formatter(FuncFormatter(hide_origin))
    if type(scale) == float:
      ax.xaxis.set_major_formatter(StrMethodFormatter('{x:.2f}'))
      ax.yaxis.set_major_formatter(StrMethodFormatter('{x:.2f}'))
    # Add x and y labels to axes
    # Labelpad moves labels relative to their normal positions
    ax.set_xlabel('x', labelpad=-30, x=1)
    ax.set_ylabel('y', labelpad=-33, y=0.98, rotation=0)