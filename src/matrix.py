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

  def graph2D(self, vector=None, scale=1):
    self.init_cartesian2(plt, scale)
    plt.title("Graphical Representation")
    # Basis vectors
    plt.arrow(0, 0, self.data[0][0], self.data[1][0], head_width=(scale/50), color="g", label="Basis i")
    plt.arrow(0, 0, self.data[0][1], self.data[1][1], head_width=(scale/50), color="b", label="Basis j")
    # Vector transformation (if provided)
    if vector is not None:
      transformed = self * Matrix([[vector[0]], [vector[1]]])
      plt.arrow(0, 0, vector[0], vector[1], head_width=(scale/50), color="y", label="Pre-transform")
      plt.arrow(0, 0, transformed.data[0][0], transformed.data[1][0], head_width=(scale/50), color="tab:orange", label="Post-transform")
      plt.figtext(0.05, 0.8, "Yellow: Pre-transformation")
      plt.figtext(0.05, 0.75, "Orange: Post-transformation")
    plt.gca().legend()
    plt.show()

  # def graphBasis(self, column=0, scale=1):
  #   """
  #   Graphs the basis vectors of a 1x2 matrix on a 2D plane.
  #   For larger matrices, you can specify the matrix column to graph.
  #   """
  #   if len(self.data) == 2:
  #     self.init_cartesian2(plt, scale)
  #     plt.title("Basis Vectors")
  #     plt.arrow(0, 0, self.data[0][column], 0, lw=3, head_width=(scale/50), color="g")
  #     plt.arrow(0, 0, 0, self.data[1][column], lw=3, head_width=(scale/50), color="b")
  #     plt.arrow(0, 0, self.data[0][column], self.data[1][column], lw=3, head_width=(scale/50), color="y")
  #     plt.show()

  def graphBasis(self, column=0, scale=1):
    """
    Graphs the basis vectors of a 1x2 matrix on a 2D plane.
    For larger matrices, you can specify the matrix column to graph.
    """
    if len(self.data) == 2:
      self.init_cartesian3(plt, scale)
      plt.title("Basis Vectors")
      plt.show()

  def init_cartesian2(self, plt, scale):
    """Creates a formatted 2D cartesian plane."""
    # Setup
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.grid(True)
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

  def init_cartesian3(self, plt, scale):
    """Creates a formatted 3D cartesian plane."""
    # Setup
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    # Create custom axes centered at origin using lines
    length = scale * 1.5
    ax.plot([length, -length], [0, 0], [0, 0], 'k-', linewidth=1)
    ax.plot([0, 0], [length, -length], [0, 0], 'k-', linewidth=1)
    ax.plot([0, 0], [0, 0], [length, -length], 'k-', linewidth=1)
    ax.text(length, 0, 0, 'x', color='r', fontsize=16)
    ax.text(0, length, 0, 'y', color='g', fontsize=16)
    ax.text(0, 0, length, 'z', color='b', fontsize=16)
    # # Set axes limits to scale
    ax.set_xlim(-scale, scale)
    ax.set_ylim(-scale, scale)
    ax.set_zlim(-scale, scale)
    # print(ax.get_xticklabels()[0])
    # Hide ticks, axes, and background
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax._axis3don = False
    # ax.xaxis
    # ax.quiver(0,0,0,1,1,1)