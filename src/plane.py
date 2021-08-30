import math
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter, FuncFormatter
import matplotlib.ticker as ticker

class Plane:
  @staticmethod
  def to_rectangular(r, theta, degrees=False):
    """Finds rectangular co-ords using: rect = r(cos(theta) + i*sin(theta))"""
    radians = math.radians(theta) if degrees else theta
    a = r * math.cos(radians)
    b = r * math.sin(radians)
    return (a, b)

  @staticmethod
  def to_polar(a, b, degrees=False):
    """Finds polar co-ords using: r = sqrt(x**2+y**2); theta = atan(y/x)"""
    r = math.sqrt(a**2 + b**2)
    theta = math.atan(b / a)
    # Correct angle for quadrants 3, 2, and 4, respectively
    if a < 0 and b < 0:
      theta = math.pi + abs(theta)
    elif a < 0:
      theta = math.pi - abs(theta)
    elif b < 0:
      theta = 2 * math.pi - abs(theta)
    theta = math.degrees(theta) if degrees else theta
    return (r, theta)

  @staticmethod
  def graph_rectangular(a, b, scale=1):
    Plane.init_cartesian2(plt, scale, x_axis_label='Re', y_axis_label='Im')
    plt.title("Rectangular Graph")
    plt.scatter(a, b)
    plt.show()

  @staticmethod
  def graph_polar(theta, r, degrees=False):
    Plane.init_polar(plt, degrees=degrees)
    radians = math.radians(degrees) if degrees else theta
    plt.scatter(radians, r)
    plt.title("Polar Graph")
    plt.show()

  @staticmethod
  def init_cartesian2(plt, scale, x_axis_label='x', y_axis_label='y'):
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
    # Add x and y labels to axes (labelpad moves labels relative to their normal positions)
    ax.set_xlabel(x_axis_label, labelpad=-30, x=1)
    ax.set_ylabel(y_axis_label, labelpad=-33, y=0.98, rotation=0)

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

  @staticmethod
  def init_polar(plt, degrees=False):
    """Creates a formatted polar plane."""
    # Creates a figure and polar plot from matplotlib's base projections
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    if not degrees:
      angles = list(ax.get_xticks())
      labels = [str(label / math.pi) + "π" for label in angles]
      ax.set_xticks(ax.get_xticks())
      # Use fixed locators to accurately place fixed-formatted labels (both are lists)
      ax.xaxis.set_major_locator(ticker.FixedLocator(angles))
      ax.set_xticklabels(labels)