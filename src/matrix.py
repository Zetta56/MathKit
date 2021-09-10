from copy import deepcopy
from src.plane import Plane
import matplotlib.pyplot as plt

class Matrix:
  """
  A matrix that supports mathematical operations and graphing. As matrices
  represent tranformations, the columns are the component transformed (x, y, etc.)
  and the rows are the variables (x, y, etc.) used to determine the transformed
  value. You can initialize a matrix with a 2D Array (ex. [[a, b, c], [d, e, f], [g, h, i]]).

  **Since matrix division doesn't exist, you have to multiply by the inverse
  on the left/right. Note that matrix multiplication is NOT commutative
  
  Example:

  AX = B => A'AX = A'B => X = A'B

  XA = B => XAA' = BA' => X = BA'
  """
  @staticmethod
  def zeros(rows, cols):
    """Creates a matrix of a desired size and fills it with 0s"""
    # Make 'cols' 0s per row and 'rows' rows per matrix
    return Matrix([[0 for col in range(cols)] for row in range(rows)])

  def __init__(self, data):
    self.data = data

  def __str__(self):
    """
    Intended Representation:
    |a  b|
    |c  d|
    """
    output = "\n"
    for row in self.data:
      for element in row:
        # Left aligned in 6-wide space, rounded to 4 decimal places, dropped trailing 0s
        output += f"{element:<8.4g}"
      output += "\n"
    return output

  def determinant2(self):
    """
    Finds determinant of 2D matrix. Graphically, this represents the area
    of the shape formed by basis vectors i and j
    Formula: |a  b|  =>  (a x d) - (b x c)
             |c  d|
    """
    if len(self.data) != 2 or len(self.data[0]) != 2:
      raise ValueError("Matrix must contain 2 rows and 2 columns")
    return (self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0])

  def determinant3(self):
    """
    Finds disciminant by adding top-left to bottom-right diagonals and
    subtracting bottom-left to top-right diagonals (shortcut)
    Graphically, this represents the volume of the shape formed by basis
    vectors i, j, and k.
    Formula: |a  b  c|      
             |d  e  f|  =>  ((a x e x i) + (b x f g) + (c x d x h)) -
             |g  h  i|      ((g x e x c) + (h x f x a) + (i x d x b))
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

  def determinant(self, submatrix=None):
    """
    Finds the determinant of the calling matrix. By definition, this can be
    described as the sum of the products of the first row elements multiplied
    by their cofactors (read more in cofactor()). In essence, determinants
    are special numbers with many useful properties related to their matrices.
    They are used to find their inverse matrices, mensuration (ex. area,
    volume) of shapes formed by their basis vectors, and linear dependence when
    the determinant is 0 (whether their basis vectors' shape is missing
    dimensions, like a cube becoming a square when all its points are on
    the same plane). When the determinant negative, you can also think of
    it as flipping the graphed shape's orientation.

    Formula: det(A) = a11*det(A11) - a12*det(A12) + a13*det(A13) ... +- a1n*det(A1n)
    
    *a11 is read as 1st row and 1st column of matrix A

    **Do not pass in an argument for 'submatrix'. This is used internally for recursive calls
    """
    matrix = self.data if submatrix is None else submatrix
    # Base cases when matrix order is either 1x1 or 0x0
    if len(matrix) == 1 and len(matrix[0]) == 1:
      return matrix[0][0]
    elif len(matrix) == 0:
      return 1

    # Get the sum of each first row element times its cofactor
    return sum([matrix[0][index] * self.cofactor(0, index, matrix) for
      index in range(len(matrix[0]))])

  def inverse(self):
    """
    Finds the inverse of a matrix, or the matrix you can multiply by to get
    the identity matrix. This is useful if you want to reverse the transformation
    done by this matrix on another vector (typically in a matrix equation, like Ax = b).
    
    Proof (2x2 matrix): |a  b | 1  0|*|    r1   | => |  a     b   | 1   0|*|r1*d-r2*b| =>
                        |c  d | 0  1| |r2*a-r1*c|    |ca-ac da-bc | -c  a| |    r2   |
    |ad-cb  bd-db | d  -b| => |ad-bc   0   | d  -b| => |1  0 | d  -b| * (1/ad-bc)
    |ca-ac  da-bc | -c  a|    |  0   ad-bc | -c  a|    |0  1 | -c  a|
    
    *r1 is the element at that column and 1st row (ex. a, b, 1, 0), while
     r2 is the same but for the 2nd row.
    **Notice how the final matrix's signs match up to the cofactor signs
    """
    # Create a new cofactors matrix
    cofactors = Matrix.zeros(len(self.data), len(self.data[0]))
    # Loop through each elemeent in the matrix
    for row in range(len(self.data)):
      for col in range(len(self.data[0])):
        # Notice that each element is reflected over the top-left to bottom-right diagonal
        cofactors.data[col][row] = self.cofactor(row, col)
    return cofactors * (1 / self.determinant())

  def cofactor(self, row, col, submatrix=None):
    """
    Gets the cofactor of an element. By definition, this is the products of 
    its minor multiplied by its sign. This is useful to find determinants
    and inverses.
    *Do not supply a submatrix. That is used for recursive calls from determinant()
    """
    matrix = self.data if submatrix is None else submatrix
    # Eliminate the specified row and column
    filtered = [row[:col] + row[col + 1:] for row in (matrix[:row] + matrix[row + 1:])]
    # Minor is defined as the determinant of a square matrix when you
    # eliminate the column and row of the processed element
    minor = self.determinant(filtered)
    # Sign is negative if sum of row and column indices is even (odd when counting from 0)
    # Formula: A[i][j] = (-1)^(i+j)
    # Visually: |+ - +|
    #           |- + -|
    #           |+ - +|
    sign = -1 if (row + col) % 2 == 1 else 1
    return minor * sign

  def to_row_echelon(self):
    """
    Returns the calling matrix in row-echelon form using Gaussian Elimination.
    This is used to efficiently solve systems of equations, especially for
    higher orders. Note that this requires you to do back-substitution
    afterwards (ex. x=4 => x+y=6 => 4+y=6 => y=2). If you've ever used
    elimination to solve a systems in basic algebra, you have basically
    converted it into row-echelon form!

    Row-Echelon Rules:
    - All nonzero rows are above any all-zero rows
    - Each leading entry of a row is in a column to the right of the leading entry above it
    - All entries of a column below a leading entries are zeros
    - (Optional, but recommended) Leading non-zero terms are 1
    """
    ref = deepcopy(self)
    previous_row = -1
    # Loop through each element in column-major order
    for entry_col in range(len(ref.data[0])):
      for entry_row in range(len(ref.data)):
        # Find the first valid entry in a column (non-zero and right of the previous entry)
        if ref.data[entry_row][entry_col] != 0 and entry_row > previous_row:
          # Interchange the found row with the next sequential row if it
          # would otherwise skip a row
          # ex. |1 0 2|    |1 0 2|
          #     |0 0 3| => |0 4 0|
          #     |0 4 0|    |0 0 3|
          if previous_row + 1 != entry_row:
            temp = ref.data[previous_row + 1][:]
            ref.data[previous_row + 1] = ref.data[entry_row]
            ref.data[entry_row] = temp
            # Correcting entry row index after swapping
            entry_row = previous_row + 1
          # Set the entry term to 1 by dividing its row by the entry itself
          ref.data[entry_row] = [element / ref.data[entry_row][entry_col]
            for element in ref.data[entry_row]]
          # Set the terms below the entry term to 0 by subtracting a multiple of the entry row
          for row in range(entry_row + 1, len(ref.data)):
            # Get a multiple of the entry row that can subtract from the current element to
            # equal 0. You must use the top-left-most row (entry row) because
            # its left-most elements are already 0 and 0 - 0x = 0, preserving
            # any 0s that were already in the current row
            multiple = [ref.data[row][entry_col] * element for element in ref.data[entry_row]]
            for col in range(len(ref.data[row])):
              ref.data[row][col] -= multiple[col]

          # Setup for the next entry column
          previous_row += 1
          break
    return ref

  def multiply_row(self, row, scalar):
    return [scalar * element for element in row]

  def to_reduced_row_echelon(self):
    """
    Returns the calling matrix in reduced row-echelon form using Gauss-Jordan
    Elimination. Much like Gaussian Elimination, this is used to solve systems
    of equations. While this does require more steps, it avoids the need for
    back-substitution.

    Reduced Row-Echelon Rules:
    - All rules from row-echelon form
    - The leading entry in each row must be the only non-zero number in its column.
    - Leading non-zero terms are 1
    """
    ref = self.to_row_echelon()
    # Loop backwards through each element in column-major order
    for entry_row in range(len(ref.data) - 1, -1, -1):
      entry = next(iter([element for element in ref.data[entry_row] if element != 0]))
      entry_col = ref.data[entry_row].index(entry)
      for row in range(entry_row - 1, -1, -1):
        # Get a multiple of the entry row that can subtract from the current element to
        # equal 0. You must use the top-left-most row (entry row) because
        # its left-most elements are already 0 and 0 - 0x = 0, preserving
        # any 0s that were already in the current row
        multiple = [ref.data[row][entry_col] * element for element in ref.data[entry_row]]
        for col in range(len(ref.data[row])):
          ref.data[row][col] -= multiple[col]
    return ref

  def __add__(self, other):
    """
    Adds each element of this matrix with a corresponding element
    of the other matrix. Graphically, this is the same as taking two vectors
    and putting the second's tail on the first's head
    """
    if (isinstance(other, Matrix) and len(self.data) == len(other.data)
        and len(self.data[0]) == len(other.data[0])):
      output = Matrix.zeros(len(other.data), len(other.data[0]))
      for row in range(len(self.data)):
        for col in range(len(other.data[0])):
          output.data[row][col] = self.data[row][col] + other.data[row][col]
      return output

  def __sub__(self, other):
    """
    Subtracts each element of this matrix with a corresponding element
    of the other matrix. Graphically, this is the same as addition, but
    in the second vector is in the reverse direction
    """
    if (isinstance(other, Matrix) and len(self.data) == len(other.data)
        and len(self.data[0]) == len(other.data[0])):
      output = Matrix.zeros(len(other.data), len(other.data[0]))
      for row in range(len(self.data)):
        for col in range(len(other.data[0])):
          output.data[row][col] = self.data[row][col] - other.data[row][col]
      return output

  def __mul__(self, other):
    """
    Multiplies each row in this matrix by each column in the other
    matrix. It does so by adding the products of each corresponding
    elements from both rows/columns. Graphically, this transforms
    the other vector's x and y components by this matrix's x and y
    components (columns), respectively.

    ex. |a  b| * |x| => x * |a| + y * |b| => |ax + by|
        |c  d|   |y|        |c|       |d|    |cx + dy|
    """
    # Uses multiply_scalar if 'other' is an int or float
    if isinstance(other, int) or isinstance(other, float):
      return self.multiply_scalar(other)
    # Performs matrix multiplication, assuming rows and columns are correct
    elif isinstance(other, Matrix):
      if len(self.data[0]) != len(other.data):
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

  def multiply_scalar(self, scalar):
    """Multiplies each value in matrix with the scalar value"""
    output = deepcopy(self)
    for row in range(len(output.data)):
      for col in range(len(output.data[0])):
        output.data[row][col] *= scalar
    return output

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
      plt.title("2x1 Matrix")
      # x and y components
      plt.arrow(0, 0, self.data[0][column], 0, lw=3, head_width=(scale/50), color="g")
      plt.arrow(0, 0, 0, self.data[1][column], lw=3, head_width=(scale/50), color="b")
      # Final vector
      plt.arrow(0, 0, self.data[0][column], self.data[1][column], lw=3, head_width=(scale/50), color="y")
      plt.show()

  def graph2x2(self, vector=(1, 1), scale=1):
    """
    Graphs the basis vectors of a 2x2 matrix, as well as its transformation
    on a given vector.
    """
    Plane.init_cartesian2(plt, scale)
    ax = plt.gca()
    plt.title("2x2 Matrix")
    # Basis vectors
    plt.arrow(0, 0, self.data[0][0], self.data[1][0], head_width=(scale/50), color="g", label="Basis i")
    ax.text(self.data[0][0], self.data[1][0], f"({self.data[0][0]}, {self.data[1][0]})")
    plt.arrow(0, 0, self.data[0][1], self.data[1][1], head_width=(scale/50), color="b", label="Basis j")
    ax.text(self.data[0][1], self.data[1][1], f"({self.data[0][1]}, {self.data[1][1]})")
    # Pre-tranformation
    transformed = self * Matrix([[vector[0]], [vector[1]]])
    plt.arrow(0, 0, vector[0], vector[1], head_width=(scale/50), color="y", label="Pre-transform")
    ax.text(vector[0], vector[1], f"({vector[0]}, {vector[1]})")
    # Post-tranformation
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
    plt.title("3x3 Matrix")
    # Basis vectors and labels
    plt.quiver(0, 0, 0, self.data[0][0], self.data[1][0], self.data[2][0], color="r", label="Basis i")
    ax.text(self.data[0][0], self.data[1][0], self.data[2][0], f"({self.data[0][0]}, {self.data[1][0]}, {self.data[2][0]})")
    plt.quiver(0, 0, 0, self.data[0][1], self.data[1][1], self.data[2][1], color="g", label="Basis j")
    ax.text(self.data[0][1], self.data[1][1], self.data[2][1], f"({self.data[0][1]}, {self.data[1][1]}, {self.data[2][1]})")
    plt.quiver(0, 0, 0, self.data[0][2], self.data[1][2], self.data[2][2], color="b", label="Basis k")
    ax.text(self.data[0][2], self.data[1][2], self.data[2][2], f"({self.data[0][2]}, {self.data[1][2]}, {self.data[2][2]})")
    # Pre-transformation
    transformed = self * Matrix([[vector[0]], [vector[1]], [vector[2]]])
    plt.quiver(0, 0, 0, vector[0], vector[1], vector[2], color="y", label="Pre-transform")
    ax.text(vector[0], vector[1], vector[2], f"({vector[0]}, {vector[1]}, {vector[2]})")
    # Post-transformation
    plt.quiver(0, 0, 0, transformed.data[0][0], transformed.data[1][0],
      transformed.data[2][0], color="tab:orange", label="Post-transform")
    ax.text(transformed.data[0][0], transformed.data[1][0], transformed.data[2][0],
      f"({transformed.data[0][0]}, {transformed.data[1][0]}, {transformed.data[2][0]})")
    # Display legend and graph
    ax.legend()
    plt.show()