from src.triangle import Triangle
from src.matrix import Matrix
from src.plane import Plane
from src.probability import Probability
import math

# Sample Usage:
# triangle = Triangle(a=4, b=6, B=80)
# triangle.solve()
# triangle.graph()

matrix = Matrix([[3, 1], [1, 2]])
matrix2 = Matrix([[-1, 2, 2], [4, -1, 5], [3, -4, 5]])
# matrix.graph_transform2(scale=5)
# matrix.graph_transform2(vector=(-1, 2), scale=5)
matrix.graph_vector(scale=5)
# matrix.graph_vector(column=0, scale=6)
# matrix2.graph_transform3(scale=10)
# matrix2.graph(scale=5)
# matrix3 = Matrix([[1], [2], [3]])
# matrix3.graph(scale=10)
# Plane.graph_rectangular(3, 4, scale=5)
# Plane.graph_rectangular((3, 4), scale=5)
# Plane.graph_polar((3, 10))
# Plane.graph_polar(3, 10)
# Plane.graph_polar(3, 50, isDegrees=False)
# Plane.to_rectangular(11, 29, isDegrees=True)
# print(Probability.permutations(15, 3))
# print(matrix.to_row_echelon())
# print(matrix.dot(Matrix([[1, 2], [3, 4]])))
# print(matrix)