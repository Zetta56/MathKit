from copy import deepcopy
import re
from src.plane import Plane
import matplotlib.pyplot as plt

class Matrix:
  """
  A matrix that supports mathematical operations and graphing. As matrices
  represent tranformations, the rows are specific components in each basis
  vector (x, y, etc.) and the columns are the basis vectors used to transform
  other vectors. You can initialize a matrix with a 2D list (ex. [[a, b, c],
  [d, e, f], [g, h, i]]) or a 1D list (ex. [a, b, c]).

  *Matrix: |a  b|      Vectors: i(a,c)
           |c  d|               j(b,d)

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
    # If data is a 2D list, copy it exactly
    if(all([isinstance(item, list) for item in data])):
      self.data = data
    # If data is a 1D list, format it into a 2D list (used for nx1 vectors)
    if(all([isinstance(item, int) or isinstance(item, float) for item in data])):
      self.data = [[item] for item in data]


  def __str__(self):
    """
    Intended Representation:
    |a  b|
    |c  d|
    """
    output = "\n"
    for row in self.data:
      output += "|"
      for element in row:
        # Remove negative sign from -0 if it element is ever equal to -0
        element = element if element != 0 else abs(element)
        # Left aligned in 6-wide space, rounded to 4 decimal places, dropped trailing 0s
        output += f"{(element):^8.4g}"
      output += "|\n"
    return output

  def determinant(self, submatrix=None):
    """
    Finds the determinant of the calling matrix. By definition, this can be
    described as the sum of the products of the first row elements multiplied
    by their cofactors (read more in cofactor()). In essence, determinants
    are special numbers with many useful properties related to their matrices.
    They are used to find their inverse matrices, permutations, mensuration (ex.
    area, volume) of shapes formed by their basis vectors, and linear dependence
    when the determinant is 0 (whether their basis vectors' shape is missing
    dimensions, like a cube becoming a square when all its points are on
    the same plane). When the determinant negative, you can also think of
    it as flipping the graphed shape's orientation.

    Formula: det(A) = A11*det(A11) - A12*det(A12) + A13*det(A13) ... +- A1n*det(A1n)
    
    *A11 is read as 1st row and 1st column of matrix A

    Another definition for determinants is that they're the sum of all permutations
    of n-element symmetric groups, or sets of bijections. Bijections (represented
    by pi) are one-to-one functions where each output maps to exactly 1 input.
    These can be inverted (ex. pi({1, 2}) -> {2, 1}) and the number of inversions
    are tell you their sign (and explains where the signs come from in the
    cofactor definition!)

    Formula:
    det(A) = S1 + S2 + ... + Sn
    Sx = sign(pix)*A1(pix(1))*A2(pix(2))*...*An(pix(n))
    
    Ex. If A is a 2x2 matrix:
    S1 = {1,2} => {1, 2} (0 inversions, sign = 1)
    S2 = {1,2} => {2, 1} (1 inversion, sign = -1)
    det(A) = (1)*(a11)*(a22) + (-1)*(a12)*(a21)

    *Do not pass in an argument for 'submatrix'. This is used internally for recursive calls
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
    Gets the cofactor of the element at the specified row and col (counting
    from 0).By definition, this is the product of its minor multiplied by
    its sign. This is useful to find determinants and inverses.

    *Do not supply a submatrix. That is used for recursive calls from determinant()
    """
    matrix = self.data if submatrix is None else submatrix
    # Eliminate the specified row and column
    filtered = [row[:col] + row[col + 1:] for row in (matrix[:row] + matrix[row + 1:])]
    # Minor is defined as the determinant of a square matrix when you
    # eliminate the column and row of the processed element
    minor = self.determinant(filtered)
    # The sign is negative if row + col is even (odd if counting from 0)
    # Formula (Permutations): sign = (-1)^(inversions)
    # Formula (Cofactors): Aij = (-1)^(i + j)
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
    # Put matrix into row echelon form
    rref = self.to_row_echelon()
    # Loop through each row from bottom to top
    for entry_row in range(len(rref.data) - 1, -1, -1):
      # Get the leading non-zero entry and its column index in the row
      entry = next(iter([element for element in rref.data[entry_row] if element != 0]))
      entry_col = rref.data[entry_row].index(entry)
      # Replace the terms above the leading entry with 0 by multiplying its row
      # by a multiple of the leading entry's row
      for row in range(entry_row - 1, -1, -1):
        multiple = [rref.data[row][entry_col] * element for element in rref.data[entry_row]]
        for col in range(len(rref.data[row])):
          rref.data[row][col] -= multiple[col]
    return rref

  def dot(self, other, col=0):
    """
    Finds the dot product of two column vectors from this matrix and the other
    matrix by summing up their corresponding components. Graphically, this is
    the length of one vector if it were projected onto the line the other vector
    in on and scaled by the other vector. Since dot products are commutative,
    this length will be the same no matter which matrix is being projected.
    It's also noteworthy that this is computationally equivalent to multiplying
    a 1xn matrix with an nx1 matrix and that a 0 dot product means that
    the two vectors are perpendicular.

    Dot products can also show you the cosine of the angle between the two
    known vectors because cos(theta) is the ratio of the adjacent vector to
    the hypoteneuse vector, or the length of the adjacent vector when projected
    and scaled onto the hypoteneuse vector.

    Ex. |a|.|c| = ac+bd
        |b| |d|

    *col is the column in each matrix to extract a vector from
    """
    if len(self.data) == len(other.data):
      return sum([self.data[row][col] * other.data[row][col] for row in range(len(other.data))])
    else:
      return None

  def cross(self, other):
    """
    Finds the cross product between two 3x1 matrices (3D vectors). By definition,
    this is a 3D vector perpendicular to the two known vectors in a direction
    following the right-hand-rule (this direction is a convention agreed upon
    by mathemeticians for convenience) and a magnitude equivalent to the area
    of a parallelogram formed by the two known vectors. These particular
    properties are what makes cross products useful, especially in the study of
    rotations and physics. You can also find the volume of a parallelepiped
    formed by the two known vectors and another variable vector (x, y, z) by
    multiplying (x, y, z) by the cross product of the known vectors because
    V = bh, where b=cross product and h=(x, y, z).

    Formula:
    Given v=self and w=other,
    (v2w3-w2v3, v1w3-w1v3, v1w2-w1v2)

    Proof:
    det(|x  v1  w1|              |x|
        |y  v2  w2| = |p1 p2 p2|*|y|
        |z  v3  w3|)             |z|

    *Right-hand-rule: index finger points forward, middle finger points left,
    thumb points up
    """
    # Check if both matrices are 3D vectors (3 rows, 1 column)
    if len(self.data) == 3 and len(other.data) == 3:
      # Create a matrix with the first column being a variable input vector
      # (1s are placeholders), and the second and third being this vector
      # and the other vector.
      combined = Matrix([[1, self.data[row][0], other.data[row][0]] for row in range(len(self.data))])
      # Return a new vector containing the cofactors of each variable vector in the combined matrix
      return Matrix([combined.cofactor(row, 0) for row in range(len(combined.data))])

  # def eigenvalues(self):
  #   """
  #   ** Work in Progress **
  #
  #   Finds the eigenvectors of the current matrix, or the vectors that are only
  #   scaled (not rotated at all) by a certain scale factor (the eigenvalue)
  #   when performing this matrix transformation.

  #   Formula:
  #   λ = eigenvalue to find, In = identity matrix for nxn matrix, A = this matrix
  #   det(λIn - A) = 0
  #   |a-λ  b|
  #   | c  d-λ|
  #   (a-λ)(d-λ)-bc = 0
  #   ad+λ^2-adλ-bc = 0
  #   λ^2-adλ+ad-bc = 0
  #   λ^2-adλ = bc-ad
  #   λ^2-adλ+(a^2*d^2)/4 = bc-ad+(a^2*d^2)/4
  #   (λ-ad/2)^2 = bc-ad+(a^2*d^2)/4
  #   λ = sqrt(bc-ad+(a^2*d^2)/4)+ad/2

  #   Proof:
  #   Av = λv          | Transformation representing the above definition
  #   Av - λv = 0      | Subtract λv from both sides to put them on the same side of the equation
  #   Av - λ(In)v = 0  | Multiply λv by In to turn λv from scalar to vector multiplication
  #   (A - λIn)v = 0   | Factor out v (assume v is non-zero because v=0 has infinite eigenvalues)
  #   det(A - λIn) = 0 | The only time when an nxn matrix can to multiply to 0 (n-dimensions
  #                    | to 0-dimensions) is it squishes space to a lower dimension (indicated by det(A)=0)
  #   """

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
    elements from both rows/columns. Graphically, this transforms the other
    matrix's x and y components by this matrix's x and y coefficients

    ex. |a  b| * |x| => x * |a| + y * |b| => |ax + by|
        |c  d|   |y|        |c|       |d|    |cx + dy|
    """
    # Multiplies every element in this matrix by 'other' if 'other' is a number
    if isinstance(other, int) or isinstance(other, float):
      output = deepcopy(self)
      for row in range(len(output.data)):
        for col in range(len(output.data[0])):
          output.data[row][col] *= other
      return output
    # Performs matrix multiplication if orders (row and columns) are correct
    elif isinstance(other, Matrix):
      if len(self.data[0]) != len(other.data):
        return None
      output = Matrix.zeros(len(other.data), len(other.data[0]))
      # Loop through this matrix's row and other matrix's columns
      for row in range(len(self.data)):
        for col in range(len(other.data[0])):
          # Fills output with sum of products of corresponding elements in
          # row-column combinations
          sum = 0
          for i in range(len(self.data[0])):
            sum += self.data[row][i] * other.data[i][col]
          output.data[row][col] = sum
      return output

  def __rmul__(self, other):
    """Allows the scalar multiplication order: scalar * matrix"""
    if isinstance(other, int) or isinstance(other, float):
      return self * other

  def graph_vector(self, col=0, scale=1):
    """
    Graphs the basis vectors of a 2x1 or 3x1 matrix on a plane. For matrices
    with more than 1 column, you can specify the matrix column to graph.
    """
    if len(self.data) == 2:
      Plane.init_cartesian2(plt, scale)
      plt.title("Matrix Vector")
      plt.arrow(0, 0, self.data[0][col], self.data[1][col], lw=3, head_width=(scale/50), color="r")
      plt.text(self.data[0][col], self.data[1][col], f"({self.data[0][col]}, {self.data[1][col]})")
      plt.show()
    if len(self.data) == 3:
      Plane.init_cartesian3(plt, scale)
      plt.title("Matrix Vector")
      ax = plt.gca()
      ax.quiver(0, 0, 0, self.data[0][col], self.data[1][col], self.data[2][col], color="r")
      ax.text(self.data[0][col], self.data[1][col],  self.data[2][col], f"({self.data[0][col]}, {self.data[1][col]}, {self.data[2][col]})")
      plt.show()

  def graph_transform2(self, vector=(1, 1), scale=1):
    """
    Graphs the basis vectors of a 2x2 matrix, as well as its transformation
    on a given vector.
    """
    Plane.init_cartesian2(plt, scale)
    ax = plt.gca()
    plt.title("Matrix Transformation")
    # Determinant Area
    # Create parallelogram using: origin, basis vectors, and a point parallel to both basis vectors
    points = [(0, 0), (self.data[0][0], self.data[1][0]), (self.data[0][0] + self.data[0][1],
      self.data[1][0] + self.data[1][1]), (self.data[0][1], self.data[1][1]), (0, 0)]
    ax.add_patch(plt.Polygon(points))
    # Find center of parallelogram by getting average of x (and y) min and max
    sorted_x = sorted([0, self.data[0][0], self.data[0][1], self.data[0][0] + self.data[0][1]])
    sorted_y = sorted([0, self.data[1][0], self.data[1][1], self.data[1][0] + self.data[1][1]])
    ax.text((sorted_x[3] - sorted_x[0]) / 2, (sorted_y[3] - sorted_y[0]) / 2, f"{self.determinant()}")
    # Basis vectors
    plt.arrow(0, 0, self.data[0][0], self.data[1][0], head_width=(scale/50), color="g", label="Basis i")
    ax.text(self.data[0][0], self.data[1][0], f"({self.data[0][0]}, {self.data[1][0]})")
    plt.arrow(0, 0, self.data[0][1], self.data[1][1], head_width=(scale/50), color="b", label="Basis j")
    ax.text(self.data[0][1], self.data[1][1], f"({self.data[0][1]}, {self.data[1][1]})")
    # Pre-tranformation
    transformed = self * Matrix([vector[0], vector[1]])
    plt.arrow(0, 0, vector[0], vector[1], head_width=(scale/50), color="y", label="Pre-transform")
    ax.text(vector[0], vector[1], f"({vector[0]}, {vector[1]})")
    # Post-tranformation
    plt.arrow(0, 0, transformed.data[0][0], transformed.data[1][0], head_width=(scale/50),
      color="tab:orange", label="Post-transform")
    ax.text(transformed.data[0][0], transformed.data[1][0], f"({transformed.data[0][0]}, {transformed.data[1][0]})")
    
    # Display legend and graph
    ax.legend()
    plt.show()

  def graph_transform3(self, vector=(1, 1, 1), scale=1):
    """
    Graphs the basis vectors of a 3x3 matrix, as well as its transformation
    on a given vector.
    """
    Plane.init_cartesian3(plt, scale)
    ax = plt.gca()
    plt.title("Matrix Transformation")
    # Basis vectors and labels
    plt.quiver(0, 0, 0, self.data[0][0], self.data[1][0], self.data[2][0], color="r", label="Basis i")
    ax.text(self.data[0][0], self.data[1][0], self.data[2][0], f"({self.data[0][0]}, {self.data[1][0]}, {self.data[2][0]})")
    plt.quiver(0, 0, 0, self.data[0][1], self.data[1][1], self.data[2][1], color="g", label="Basis j")
    ax.text(self.data[0][1], self.data[1][1], self.data[2][1], f"({self.data[0][1]}, {self.data[1][1]}, {self.data[2][1]})")
    plt.quiver(0, 0, 0, self.data[0][2], self.data[1][2], self.data[2][2], color="b", label="Basis k")
    ax.text(self.data[0][2], self.data[1][2], self.data[2][2], f"({self.data[0][2]}, {self.data[1][2]}, {self.data[2][2]})")
    # Pre-transformation
    transformed = self * Matrix([vector[0], vector[1], vector[2]])
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