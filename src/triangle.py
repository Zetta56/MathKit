import math
import matplotlib.pyplot as plt
from src.plane import Plane

class InvalidException(Exception):
  """Exception for when triangle contains an invalid property"""
  pass

class Triangle():
  """
  A triangle solver that finds missing sides and angles. This can also
  plot them with Matplotlib.

  Input Triangle Conditions:
    - At least 1 side is known
    - At least 3 components are known in total
    - Angles are in degrees

  Useful Equations:
    Law of Sines: x/sinX = y/sinY
    Law of Cosines: x2=y2+z2-2yzcosX
    Angles Sum Theorem: X + Y + Z = 180
    Pythagorean Theorem: x^2 + y^2 = z^2
    Distance Formula: d = sqrt((x2-x1)^2 + (y2-y1)^2)
  """

  def __init__(self, a=None, b=None, c=None, A=None, B=None, C=None):
    # Initial properties
    self.sides = [a, b, c]
    self.angles = [A, B, C]
    self.default = {'sides': [a, b, c], 'angles': [A, B, C]} # Used to reset triangle
    self.perimeter = 0
    self.area = 0
    self.height = 0

    # Properties needed to solve triangle
    self.known_sides = len([side for side in self.sides if side is not None])
    self.known_angles = len([angle for angle in self.angles if angle is not None])
    self.solve()

  def __str__(self):
    """Formats triangle info into string after solving for unknowns"""
    if self.is_valid():
      return (
        "\nTriangle:" + 
        "\na: " + str(self.sides[0]) + 
        "\nb: " + str(self.sides[1]) + 
        "\nc: " + str(self.sides[2]) + 
        "\nA: " + str(self.angles[0]) + 
        "\nB: " + str(self.angles[1]) + 
        "\nC: " + str(self.angles[2]) +
        "\nPerimeter: " + str(self.perimeter) +
        "\nArea: " + str(self.area) +
        "\nHeight: " + str(self.height)
      )
    else:
      return "Triangle could not be made with given information"

  def is_valid(self):
    """Checks if the created triangle's properties are valid"""
    try:
      # Test for missing components
      if None in self.sides or None in self.angles:
        raise InvalidException()

      # Test for non-positive angles
      for angle in self.angles:
        if angle <= 0:
          raise InvalidException()

      # Test for non-positive sides
      for side in self.sides:
        if side <= 0:
          raise InvalidException()
      
      # Test if angles add to 180
      if not math.isclose(sum(self.angles), 180, abs_tol=2):
        raise InvalidException()

      # Test if longest side is opposite of largest angle
      longest_side_index = self.sides.index(max(self.sides))
      largest_angle_index = self.angles.index(max(self.angles))
      if longest_side_index != largest_angle_index:
        raise InvalidException()

      # Test if longest side isn't too big nor small
      sorted_sides = sorted(self.sides)
      if not (abs(sorted_sides[1] - sorted_sides[0]) < sorted_sides[2] < sorted_sides[1] + sorted_sides[0]):
        raise InvalidException()

      # Test if isosceles triangle has congruent sides and base angles
      for index in range(0, 3):
        nextIndex = index + 1 if index + 1 < 3 else 0 # Gets each pair of sides and angles
        congruent_sides = math.isclose(self.sides[index], self.sides[nextIndex], abs_tol=0.01)
        congruent_angles = math.isclose(self.angles[index], self.angles[nextIndex], abs_tol=0.01)
        if((congruent_sides and not congruent_angles) or (congruent_angles and not congruent_sides)):
          raise InvalidException()

      return True
    except InvalidException as err:
      return False

  def angle_sum(self):
    """
    Finds third angle given 2 known angles
    Formula: X = 180 - Y - Z
    """
    try:
      # Get index of unknown angle
      x = self.angles.index(None)
      # Get list of angles that aren't None (missing angles)
      known = [angle for angle in self.angles if angle is not None]
      self.angles[x] = (180 - known[0] - known[1])
    except:
      return

  def sss_cosine(self, x):
    """
    Finds angle opposite specified side 3 known sides
    Formula:  X = acos(y^2 + z^2 - x^2 / 2yz)
    """
    try:
      # Get sides that are not opposite the desired angle
      known = [side for index, side in enumerate(self.sides) if index != x]
      # The above formula, converted to degrees
      self.angles[x] = math.degrees(math.acos((known[0]**2 + known[1]**2 -
        self.sides[x]**2) / (2 * known[0] * known[1])))
    except:
      return

  def sas_cosine(self):
    """
    Finds side opposite known angle given 2 known sides and 1 known angle in-between
    Formula: x = sqrt(y^2 + z^2 - 2yz*cosX)
    """
    try:
      # Get index of unknown side
      x = self.sides.index(None)
      # Get list of all sides that aren't None (missing sides)
      known = [side for side in self.sides if side is not None]
      # The above formula, converted to degrees
      self.sides[x] = math.sqrt((known[0]**2 + known[1]**2) - (2 *
        known[0] * known[1] * math.cos(math.radians(self.angles[x]))))
    except:
      return

  def aas_sine(self, x):
    """
    Finds side opposite specified angle given 2 known angles and 1 known side
    Formula: x = sinX * y / sinY
    """
    try:
      # Finds a known side-angle pair
      known = next(index for index, side in enumerate(self.sides)
        if self.sides[index] is not None and self.angles[index] is not None)
      # The above formula, where angles are converted to radians
      self.sides[x] = (math.sin(math.radians(self.angles[x])) * 
        (self.sides[known] / math.sin(math.radians(self.angles[known]))))
    except:
      return

  def ssa_sine(self, x, quadrant=1):
    """
    Finds angle opposite specified side given 2 known sides and 1 known angle
    Formula: X = asin(x * sinY / y)
    """
    try:
      # Finds a known side-angle pair
      known = next(index for index, side in enumerate(self.sides)
        if self.sides[index] is not None and self.angles[index] is not None)
      # The above formula, where angles are converted to radians
      reference_angle = math.degrees(math.asin(self.sides[x] * (math.sin(
        math.radians(self.angles[known])) / self.sides[known])))
      # Converts reference angle to angle in specified quadrant
      self.angles[x] = Plane.to_quadrant(reference_angle, quadrant)
    except:
      return

  def solve(self):
    """
    Solves triangle with relevant formulas and displays result.
    
    If no triangles can be made from the given information, this
    will assign the missing components to None
    """
    # SSS Triangle
    if self.known_sides == 3:
      self.sss_cosine(0)
      self.sss_cosine(1)
      self.sss_cosine(2)

    # SSA or SAS Triangle
    elif self.known_angles >= 1 and self.known_sides == 2:
      # Get index of the only known angle (used to determine triangle type)
      known_angle = next(index for index, angle in enumerate(self.angles) if angle is not None)
      # SSA Triangle
      if(self.sides[known_angle] is not None):
        # Gets first known side that isn't opposite of the known angle
        known_side = next(index for index, side in enumerate(self.sides) 
          if side is not None and index != known_angle)
        # Tries to solve triangle using SSA formula in quadrant 1
        self.ssa_sine(known_side, quadrant=1)
        self.angle_sum()
        self.sas_cosine()
        # Tries to solve triangle using SSA formula in quadrant 2
        # This may be needed because SSA uses arcsin, which has solutions in
        # Q1 and QII, but may form invalid triangles when finding components afterwards
        if not self.is_valid():
          self.__dict__.update(self.default) # Resets angles and sides
          self.ssa_sine(known_side, quadrant=2)
          self.angle_sum()
          self.sas_cosine()

      # SAS Triangle
      else:
        self.sas_cosine()
        for index, angle in enumerate(self.angles):
          if angle is None:
            self.sss_cosine(index)

    # ASA Triangle
    elif self.known_angles >= 2 and self.known_sides == 1:
      self.angle_sum()
      for index, side in enumerate(self.sides):
        if side is None:
          self.aas_sine(index)

    # Triangle Properties
    if self.is_valid():
      self.perimeter = sum(self.sides)
      self.area = (1/2 * self.sides[0] * self.sides[1] * math.sin(math.radians(self.angles[2])))
      self.height = 2 * self.area / max(self.sides)

  def graph(self):
    """
    Draws triangle using matplotlib.

    Proof to find third point of triangle:
      Solving for (x2,y2) if (x1,y1)=point1, (x3,y3)=point3, s1=leg, s2=leg
      (x2-x1)^2 + (y2-y1)^2 = s1^2     | Pythagorean Theorem
      (x2-x3)^2 + (y2-y3)^2 = s2^2     | Pythagorean Theorem
      Let x1=0, y1=0, y3=0
      x2^2 + y2^2 = s1^2               | equation1
      y2 = sqrt(s1^2 - x^2)            | **Solution for y2
      (x2-x3)^2 + y2^2 = s2^2          | equation2
      equation2 - equation1
      s2^2 - s1^2 = (x2-x3)^2 - x2^2
      s2^2 - s1^2 = x2^2 - 2x2x3 + x3^2 - x2^2
      s2^2 - s1^2 = -2x2x3 + x3^2
      s2^2 - s1^2 - x3^2 = -2x2x3
      x2 = (s2^2 - s1^2 - x3^2) / -2x3 | **Solution for x2
    """
    if not self.is_valid():
      print("Triangle could not be made with given information")

    # Sort sides and angles from least to greatest
    sides = sorted(self.sides) 
    angles = sorted(self.angles)

    # Calculates co-ordinates of third point
    x = (sides[0]**2 - sides[1]**2 - sides[2]**2) / (-2 * sides[2])
    y = math.sqrt(sides[1]**2 - x**2)
    points = [(0, 0), (sides[2], 0), (x, y)]

    # Plot triangle
    triangle = plt.Polygon(points, color="#e55", label="Triangle")
    plt.gca().add_patch(triangle)
    plt.plot((points[2][0], points[2][0]), (0, points[2][1]), color="#55e") # height
    
    # Angle Labels
    plt.annotate(f"{round(angles[0], 3)}??", points[0])
    plt.annotate(f"{round(angles[1], 3)}??", points[1])
    plt.annotate(f"{round(angles[2], 3)}??", points[2])
    # Side Length Labels
    plt.annotate(round(sides[0], 3), ((points[1][0] + points[2][0]) / 2, points[2][1] / 2))
    plt.annotate(round(sides[1], 3), (points[2][0] / 2, points[2][1] / 2))
    plt.annotate(round(sides[2], 3), (points[1][0] / 2, 0))
    plt.annotate(round(self.height, 3), (points[2][0], points[2][1] / 2))
    # Property Labels
    plt.figtext(0.1, 0.9, f"Perimeter: {round(self.perimeter, 4)}")
    plt.figtext(0.1, 0.85, f"Area: {round(self.area, 4)}")

    # Plot Settings
    plt.axis('off')
    plt.xlim([0, max(sides[2], y)])
    plt.ylim([0, max(sides[2], y)]) 
    plt.show()