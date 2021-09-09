import math

class Probability:
  @staticmethod
  def permutations(n, r):
    """
    Finds total number of arrangements of r elements from n-element set,
    which is the same as the product of the possible number of outcomes for
    each position. Algebraically, this is 'n x (n - 1) x ... x (n - r)'
    (can also be found by cancelling out (n-r)! elements from n!).
    Formula: P(n, r) = n!/(n-r)!
    """
    if r > n:
      return 0
    else:
      return math.factorial(n) / math.factorial(n - r)

  @staticmethod
  def combinations(n, r):
    """
    Finds total number of combinations (where order doesn't matter) of r
    elements from n-element set. This is found by removing duplicate
    combinations from permutations that result from different sequences of
    the same elements (ex. 1,3,2 and 2,1,3). This adds up to exactly r!.
    Example: {10,20,30,40,50} is 1 combination, but has 5x4x3x2x1 permutations
    Formula: C(n, r) = n!/(r!(n-r)!)
    """
    if r > n:
      return 0
    else:
      return math.factorial(n) / (math.factorial(r) * math.factorial(n - r))