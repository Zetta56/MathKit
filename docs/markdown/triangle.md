# Triangle
## Constructor: triangle = Triangle(a, b, c, A, B, C)
- a, b, c {int or float}
  - These parameters represent the known side lengths.
- A, B, C {int or float}
  - These parameters represent the known angle measures (in degrees).
- At least 3 of the above components must be filled in for the resulting triangle to be solvable. In addition, at least 1 of these must be a side length.
- Keep in mind that you do NOT have to fill in every parameter. The `triangle.solve()` function can fill in the rest for you when you instantiate the triangle.
- If you notice an error message during instantiation, it probably means that the components you pass in create a triangle that is impossible to solve.

```
triangle = Triangle(a=4, b=6, B=80)
triangle2 = Triangle(A=50, a=150, c=100)
triangle3 = Triangle(A=30, c=8, B=70)
triangle4 = Triangle(A=50, a=150, b=80, c=100)
```

## Graph
If the calling triangle can be solved, `triangle.graph()` graphs it with labels for its side lengths, angle measures, perimater, and area.
```
triangle = Triangle(a=4, b=6, B=80)
triangle.graph()
```

![Example](/docs/images/triangle.JPG)