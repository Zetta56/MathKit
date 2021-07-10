from src.triangle import Triangle
from src.matrix import Matrix

# Sample Usage:
triangle = Triangle(a=4, b=6, B=80)
triangle.solve()
triangle.show()

# A = Matrix([[-2, -6], [0, 2]])
# B = Matrix([[1, -1], [2, 2]])
# C = Matrix([[4, 2], [4, 0]])
# print((C * A.inverse2()) + 4 * B)