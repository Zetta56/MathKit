# Matrix
## Contructor: matrix = Matrix(data)
Creates a new matrix with elements corresponding to those in data
- data {list}
  - If data is a multi-dimensional list (ex. [[1, 2], [3, 4]]), the constructed matrix will contain an exact copy of data
  - If data is a 1-dimensional list (ex. [1, 2, 3]), the indices of each element in data will correspond to row indices in the constructed matrix and this matrix will only have 1 column (ex. [1, 2, 3] becomes [[1], [2], [3]])
```
matrix = Matrix([[1, 2], [3, 4]])
print(matrix)
>>> |   1       2    |
    |   3       4    |

matrix2 = Matrix([1, 2, 3])
print(matrix2)
>>> |   1    |
    |   2    |
    |   3    |
```

## Properties
### Determinant
`matrix.determinant()` returns the determinant of the calling matrix using cofactor expansion
```      
matrix = Matrix([[1, 2], [3, 4]])
print(matrix.determinant())
>>> -2
```
### Cofactor
`matrix.cofactor(row, col)` returns the cofactor of the element at the specified row and column in the calling matrix. The cofactor is the determinant of a smaller matrix formed by erasing the row and column of the processed element
```      
matrix = Matrix([[-1, 2, 2], [4, -1, 5], [3, -4, 5]])
print(matrix.cofactor(1, 1))
>>> -11
```

## Operations
### Dot Product
`matrix.dot(other, col=0)` returns the dot product of the calling matrix and another input matrix. Since this is mainly used on vectors (nx1 matrices), this only works on a single column, even if the overall matrix is larger. This column can be specified as `col`.
```
matrix1 = Matrix([[1, 1], [2, 3]])
matrix2 = Matrix([[3, 5], [4, 7]])
print(matrix1.dot(matrix2, col=1))
>>> 26
```

### Cross Product
`matrix.cross(other)` returns the cross product of the calling matrix and another input matrix. As this is typically used for 3D vectors (3x1 matrices), only the first column of both matrices will be used. This will also only work if both matrices have exactly 3 rows.
```
matrix1 = Matrix([1, 3, 4])
matrix2 = Matrix([5, 7, 9])
print(matrix1.cross(matrix2))
>>> |   -1   |
    |   11   |
    |   -8   |
```

### Addition
`matrix + other` returns the sum of the calling matrix and the other matrix.
```
matrix1 = Matrix([[1, 1], [2, 3]])
matrix2 = Matrix([[3, 5], [4, 7]])
print(matrix1 + matrix2)
>>> |   4       6    |
    |   6       10   |
```

### Subtraction
`matrix - other` returns the difference of the calling matrix and the other matrix.
```
matrix1 = Matrix([[1, 1], [2, 3]])
matrix2 = Matrix([[3, 5], [4, 7]])
print(matrix1 - matrix2)
>>> |   -2      -4   |
    |   -2      -4   |
```

### Multiplication
`matrix * other` returns the product of the calling matrix and other.
- If other is a scalar, this will multiply every element in the matrix by the scalar value
- If other is a matrix, this will perform matrix multiplication.
```
matrix1 = Matrix([[1, 1], [2, 3]])
matrix2 = Matrix([[3, 5], [4, 7]])
print(matrix1 * matrix2)
>>> |   7       12   |
    |   18      31   |

print(matrix1 * 5)
>>> |   5       5    |
    |   10      15   |
```

### Division
Since matrix division doesn't exist, you must instead multiply by the inverse of the other matrix.
```
matrix1 = Matrix([[1, 1], [2, 3]])
matrix2 = Matrix([[3, 5], [4, 7]])
print(matrix1 * matrix2.inverse())
>>> |   3       -2   |
    |   2       -1   |
```

## Derived Matrices
### Inverse Matrix
`matrix.inverse()` returns the inverse matrix of the calling matrix by multiplying its adjugate matrix (cofactor matrix flipped over the primary diagonal) by (1 / determinant). This can multiply with the original matrix to get the identity matrix.
```      
matrix = Matrix([[1, 2], [3, 4]])
print(matrix.inverse())
>>> |   -2      1    |
    |  1.5     -0.5  |
```

### Row Echelon Form
`matrix.to_row_echelon()` returns the calling matrix in row echelon form. This makes all leading entries 1 and all elements under them 0s. By definition, the leading entry for each row is the first non-zero value from the left and must be to the right of any leading entry in the rows above. This is useful for solving systems of equations, but may require some back-substitution (ex. x=4 => x+y=6 => 4+y=6 => y=2).
```      
matrix = Matrix([[-1, 2, 2], [4, -1, 5], [3, -4, 5]])
print(matrix.to_row_echelon())
>>> |   1       -2      -2   |
    |   0       1     1.857  |
    |   0       0       1    |
```

### Reduced Row Echelon Form
`matrix.to_reduced_row_echelon()` returns the calling matrix in reduced row echelon form. This makes all leading entries 1s and all elements under AND above them 0s. Although this is slower than computing the row echelon form, it makes solving systems of equations simpler by avoiding the need for back-substitution.
```      
matrix = Matrix([[5, 2, 5, -3], [6, 1, 0, 7], [-4, 3, -1, 3]])
print(matrix.to_row_echelon())
>>> |   1       0       0     0.9145 |
    |   0       1       0     1.513  |
    |   0       0       1     -2.12  |
```

## Visualizations
### 2D Vector
```
matrix = Matrix([2, 6])
matrix.graph_vector(scale=8)
```
![Vector2](/docs/images/matrix_vector2.JPG)

### 3D Vector
```
matrix = Matrix([2, 6, 8])
matrix.graph_vector(scale=8)
```
![Vector3](/docs/images/matrix_vector3.JPG)

### 2D Transformation
```
matrix = Matrix([[1, 6], [3, 4]])
matrix.graph_transform2(vector=(-1, 1), scale=8)
```
![Transformation2](/docs/images/matrix_transform2.JPG)

### 3D Transformation
```
matrix = Matrix([[1, 6, 2], [3, 4, 5], [2, 4, -3]])
matrix.graph_transform3(vector=(-1, 1, -2), scale=8)
```
![Transformation2](/docs/images/matrix_transform3.JPG)