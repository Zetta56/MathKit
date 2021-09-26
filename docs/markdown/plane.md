# Plane
## Conversions
### Polar to Rectangular
`Plane.to_rectangular(r, theta)` converts polar co-ordinates r and theta to rectangular co-ordinates a and b. In other words, you can obtain the horizontal and vertical components of your co-ordinate's rectangular form using the length and angular components of its polar form.

- This uses degrees by default. Pass in `isDegrees=False` to set this to radians
```
import math

print(Plane.to_rectangular(5, 30))
>>> (4.33, 2.50)
print(Plane.to_rectangular(7, math.pi / 3, isDegrees=False))
>>> (3.50, 6.06)
```

### Rectangular to Polar
`Plane.to_polar(a, b)` converts the rectangular co-ordinates a and b to polar co-ordinates r and theta. In other words, you can obtain the length and angular components of your co-ordinate's polar form using the horizontal and vertical components of its rectangular form.

- This uses degrees by default. Pass in `isDegrees=False` to set this to radians
```
print(Plane.to_polar(-2, 6))
>>> (6.32, 108.43)
print(Plane.to_polar(3, -4, isDegrees=False))
>>> (5.00, 5.36)
```

### Reference Angle to Actual Angle
`Plane.to_quadrant(ref_angle, quadrant)` returns the angle formed by the specified reference angle (angle between 0 and 90 degrees) in the specified quadrant of a cartesian plane.
```
print(Plane.to_quadrant(34, 4))
>>> 326
Plane.to_quadrant(math.pi / 6, 2, isDegrees=False)
>>> 2.62
```

## Graphs
### Rectangular Graph
`Plane.graph_rectangular(a, b)` graphs the coordinates a and b on a rectangular plane with real and imaginary axes.
- You can change the axis scale by passing in a `scale` argument.
- a and b can be separate integer/float arguments or a single list/tuple
```
# Using a tuple
Plane.graph_rectangular((3, 4), scale=5)

# Using numbers
Plane.graph_rectangular(3, 4, scale=5)
```
![Rectangular Graph](/docs/images/plane_rectangular.JPG)

### Polar Graph
`Plane.graph_polar(r, theta)` graphs the coordinates r and theta on a polar plane.
- a and b can be separate integer/float arguments or a single list/tuple
```
# Using a tuple
Plane.graph_polar((3, 10))

# Using numbers
Plane.graph_polar(3, 10)
```
![Rectangular Graph](/docs/images/plane_polar.JPG)

### Function Graph
`Plane.graph_function(function)` graphs a function on an cartesian plane.
- function must be a lambda that accepts the parameter `x` (see below). Besides that, you can create any function you want using valid mathematical operators.
- You can change the axis scale by passing in a `scale` argument.
```
Plane.graph_function(lambda x: x**2 + 1, scale=10)
```
![Function Graph](/docs/images/plane_function.JPG)

## Custom Graphs
If you want to make your own graphs, you can use the following functions to draw blank planes.

### 2D Cartesion
- plt is Matplotlib's interface obtained using the import statement: `import matplotlib.pyplot as plt` 
- scale is an integer or float that determines the size of the axes
- x_axis_label labels the x-axis
- y_axis_label labels the y-axis
```
Plane.init_cartesian2(plt, scale, x_axis_label='x', y_axis_label='y')
```

### 3D Cartesion
- plt is Matplotlib's interface obtained using the import statement: `import matplotlib.pyplot as plt` 
- scale is an integer or float that determines the size of the axes
```
Plane.init_cartesian3(plt, scale)
```

### Polar
- plt is Matplotlib's interface obtained using the import statement: `import matplotlib.pyplot as plt` 
- scale is an integer or float that determines the size of the axes
- isDegrees determines whether to label each tick on a polar plane in degrees or in radians
```
Plane.init_polar(plt, isDegrees=True)
```