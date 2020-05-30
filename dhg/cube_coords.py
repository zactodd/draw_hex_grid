from itertools import combinations
import numpy as np

# The two 120 degree separated flows.
CW_CW_FLOW = {(1, -1, 0), (0, 1, -1), (-1, 0, 1)}
CW_CCW_FLOW = {(1, 0, -1), (-1, 1, 0), (0, -1, 1)}

# All possible directions
DIRECTIONS = {(1, -1, 0), (1, 0, -1), (0, 1, -1), (-1, 1, 0), (-1, 0, 1), (0, -1, 1)}


def neighbour(c, direction):
    """
    Get the neighbour in the direction of the cube.
    :param c: A cube coord x, z, y.
    :param direction: THe direction the of the neighbour.
    :return: The neighbouring cube coord in the specified direction.
    """
    return add(c, direction)


def is_neighbour(a, b):
    """
    Checks if to cube cords are neighbours.
    :param a: A cube coord x, z, y.
    :param b: A cube coord x, z, y.
    :return: True or False.
    """
    return distance(a, b) == 1


def neighbours(c, k=1):
    """
    Gets all neighbours of c.
    :param c: A cube cord x, y, z.
    :param k: The distance max distance of neighbours.
    :return: A set of cube coords.
    """
    cx, cz, cy = c
    if k == 1:
        return {(cx + x, cz + z, cy + y) for x, y, z in DIRECTIONS}
    else:
        return {
            (cx + x, cz - x - y, cy + y) for x in range(-k, k + 1) for y in range(max(-k, -x - k), min(k, k - x) + 1)
        }


def neighbours_from_centre(k=1):
    """
    Gets all neighbours from the cube point (0, 0, 0).
    :param k: The distance max distance of neighbours.
    :return: A set of cube coords.
    """
    return neighbours((0, 0, 0), k)


def planer_position(c, radius=None):
    """
    Calculates the planer position of the cube coord.
    :param c: A cube coord x, z, y.
    :param radius: The radius of the triple, defaults to 2/3.
    :return: horizontal, vertical positions.
    """
    x, z, y = c
    if radius is None:
        return np.sqrt(3) / 3 * (x - y), -z
    else:
        return np.sqrt(3) / 2 * radius * (x - y), -3 / 2 * radius * z


def distance(a, b):
    """
    Calculates the distance between two cube coords.
    :param a: A cube coord x, z, y.
    :param b: A cube coord x, z, y.
    :return: A float representing the distance.
    """
    ax, az, ay = a
    bx, bz, by = b
    return (abs(ax - bx) + abs(az - bz) + abs(ay - by)) / 2


def distance_from_centre(c):
    """
    Calculates the distance to the centre.
    :param c: A cube coord x, z, y.
    :return: A float representing the distance.
    """
    return distance(c, (0, 0, 0))


def cube_round(c):
    """
    Rounds cube coords.
    :param c: A cube coord x, z, y.
    :return: A rounded cube coord x, y, z.
    """
    x, z, y = c
    rx, ry, rz = round(x), round(y), round(x)
    x_diff = abs(rx - x)
    z_diff = abs(rz - z)
    y_diff = abs(ry - y)

    if x_diff > y_diff and x_diff > z_diff:
        rx = -ry - rz
    elif y_diff > z_diff:
        ry = -rx - rz
    else:
        rz = -rx - ry
    return rx, rz, ry


def cube_to_axial(c):
    """
    Converts a cube coord to an axial coord.
    :param c: A cube coord x, z, y.
    :return: An axial coord q, r.
    """
    x, z, _ = c
    return x, z


def axial_to_cube(h):
    """
    Converts a axial coord to an cube coord.
    :param h: An axial coord q, r.
    :return: A cube coord x, z, y.
    """
    q, r = h
    return q, -q - r, r


def axial_round(h):
    """
    Rounds an axial coord.
    :param h: An axial coord q, r.
    :return: a rounded axial coord q, r.
    """
    return cube_to_axial(cube_round(axial_to_cube(h)))


def pixel_to_axial(p, size):
    """
    Converts pixel position to axial coords.
    :param p: The point x, y.
    :param size: The size of each hex.
    :return: The axial coord q, r of the pixel.
    """
    x, y = p
    q = (x * np.sqrt(3) / 3 - y / 3) / size
    r = (2 * y / 3) / size
    return axial_round((q, r))


def pixel_to_cube(p, size):
    """
    Converts pixel position to cube coords.
    :param p: The point x, y.
    :param size: The size of each hex.
    :return: The cube coord x, y, z of the pixel.
    """
    return cube_round(axial_to_cube(pixel_to_axial(p, size)))
