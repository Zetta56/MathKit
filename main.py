from src.triangle import Triangle
from src.matrix import Matrix

# Sample Usage:
# triangle = Triangle(a=4, b=6, B=80)
# triangle.solve()
# triangle.graph()

matrix = Matrix([[1, -2], [5, 3]])
# matrix.graph2D(16)
matrix.graphBasis(column=0, scale=6)