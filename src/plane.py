import math
from matplotlib.ticker import StrMethodFormatter, FuncFormatter

class Plane:
  @staticmethod
  def to_rectangular(radius, theta, degrees=False):
    """rectangular = radius(cos(theta) + i*sin(theta))"""
    radians = math.radians(theta) if degrees else theta
    x = radius * math.cos(radians)
    y = radius * math.sin(radians)
    return (x, y)

  @staticmethod
  def to_polar(x, y, degrees=False):
    """radius = sqrt(a**2+b**2); theta = atan(b/a)"""
    radius = math.sqrt(x**2 + y**2)
    theta = math.atan(y / x)
    # Correct angle for quadrants 3, 2, and 4, respectively
    if x < 0 and y < 0:
      theta = math.pi + abs(theta)
    elif x < 0:
      theta = math.pi - abs(theta)
    elif y < 0:
      theta = 2 * math.pi - abs(theta)
    theta = math.degrees(theta) if degrees else theta
    return (radius, theta)

  @staticmethod
  def init_cartesian2(plt, scale):
    """Creates a formatted 2D cartesian plane."""
    # Setup
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.grid(True)
    # Center axes at origin and remove unnecessary ones
    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    ax.spines.left.set_position('center')
    ax.spines.bottom.set_position('center')
    # Set axes limits to scale
    ax.set_aspect('equal')
    ax.set_xlim(-scale, scale)
    ax.set_ylim(-scale, scale)
    # Add black(k) axes arrows that can go outside plot's borders
    # Positioning: xy-coords on stated axis and absolute on perpendicular axis
    ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 0, "<k", transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)
    ax.plot(0, 0, "vk", transform=ax.get_xaxis_transform(), clip_on=False)
    # Format tick labels to hide the origin and round to 2 decimal places
    hide_origin = lambda x, pos: "" if x == 0 else x
    ax.xaxis.set_major_formatter(FuncFormatter(hide_origin))
    ax.yaxis.set_major_formatter(FuncFormatter(hide_origin))
    if type(scale) == float:
      ax.xaxis.set_major_formatter(StrMethodFormatter('{x:.2f}'))
      ax.yaxis.set_major_formatter(StrMethodFormatter('{x:.2f}'))
    # Add x and y labels to axes
    # Labelpad moves labels relative to their normal positions
    ax.set_xlabel('x', labelpad=-30, x=1)
    ax.set_ylabel('y', labelpad=-33, y=0.98, rotation=0)

  @staticmethod
  def init_cartesian3(plt, scale):
    """Creates a formatted 3D cartesian plane."""
    # Setup
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    # Graph and label xyz axes
    length = scale * 0.75
    ax.quiver(0, 0, 0, length, 0, 0, color='k')
    ax.quiver(0, 0, 0, 0, length, 0, color='k')
    ax.quiver(0, 0, 0, 0, 0, length, color='k')
    ax.text(length, 0, 0, 'x', color='k', fontsize=16)
    ax.text(0, length, 0, 'y', color='k', fontsize=16)
    ax.text(0, 0, length, 'z', color='k', fontsize=16)
    # Set axes limits to scale
    ax.set_xlim(-scale, scale)
    ax.set_ylim(-scale, scale)
    ax.set_zlim(-scale, scale)