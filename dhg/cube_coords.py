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
    if k == 1:
        return {add(c, d) for d in DIRECTIONS}
    else:
        cx, cz, cy = c
        return {(cx + x, cz - x - y, cy + y) for x in range(-k, k + 1)
                for y in range(max(-k, -x - k), min(k, k - x) + 1)}


def neighbours_from_centre(k=1):
    """
    Gets all neighbours from the cube point (0, 0, 0).
    :param k: The distance max distance of neighbours.
    :return: A set of cube coords.
    """
    return neighbours((0, 0, 0), k)


def add(a, b):
    """
    Add two cube coords together.
    :param a: A cube coord x, z, y.
    :param b: A cube coord x, z, y.
    :return: THe added cube coordcoords.
    """
    ax, az, ay = a
    bx, bz, by = b
    return ax + bx, az + bz, ay + by


def scale(c, s):
    """
    Scales a cube coord.
    :param c: A cube coord x, z, y.
    :param s: The amount to scale the cube coord.
    :return: The scaled cube coord.
    """
    cx, cz, cy = c
    return s * cx, s * cz, s * cy


def ring(c, k):
    """
    The cube coord to centre the ring.
    :param c: A cube coord x, z, y.
    :param k: The distance at which the ring is from its centre.
    :return: A list of coords representing the ring.
    """
    assert k > 0, "The ring can only be a positive distance away from its centre."
    n = add(c, scale((-1, 0, 1), k))
    coords = []
    for d in [(1, -1, 0), (1, 0, -1), (0, 1, -1), (-1, 1, 0), (-1, 0, 1), (0, -1, 1)]:
        for _ in range(k):
            coords.append(n)
            n = neighbour(n, d)
    return coords


def edges_on_ring(ring):
    """
    Get all the edges from a ring.
    :param ring: THe ring in which to obtain the edges.
    :return: A set of edges..
    """
    edges = set()
    prev = ring[-1]
    for c in ring:
        edges.add(frozenset({prev, c}))
        prev = c
    return edges


def ring_from_centre(k):
    """
   The a ring from the centre of the coord.
   :param k: The distance at which the ring is from its centre.
   :return: A list of coords representing the ring.
   """
    return ring((0, 0, 0), k)


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


def is_triple(a, b, c):
    """
    Checks if three cube coords are a triple.
    :param a: A cube coord x, z, y.
    :param b: A cube coord x, z, y.
    :param c: A cube coord x, z, y.
    :return: True or False.
    """
    return is_neighbour(a, b) and is_neighbour(a, c) and is_neighbour(b, c)


def triples_from_neighbours(a, b):
    """
    Gets all the triples between to neighbours.
    :param a: A cube coord x, z, y.
    :param b: A cube coord x, z, y.
    :return: Two cube coords which form triples with a and b.
    """
    assert is_neighbour(a, b), f"Cubes {a} and {b} to be neighbours to have triples."
    dx, dz, dy = add(b, -a)
    if dx == 0:
        triples_diff = (dz, 0, dy), (dy, dz, 0)
    elif dz == 0:
        triples_diff = (dx, dy, 0), (0, dx, dy)
    else:
        triples_diff = (dx, 0, dz), (0, dz, dx)
    return (add(c, a) for c in triples_diff)


def triples(c):
    """
    Gets all triples that contain c.
    :param c: A cube coord x, z, y.
    :return: A set of cube coord triples.
    """
    return {frozenset({c, n, t}) for n in (add(c, d) for d in CW_CW_FLOW) for t in triples_from_neighbours(c, n)}


def edge_neighbours(edge):
    """
    Gets the edge neighbours of an edge.
    :param edge: Two cube coords neighbours.
    :return: The four edge neighbours.
    """
    assert is_neighbour(*edge), f"{edge} is not an edge. Both cube coords in the edge need to be neighbours."
    a, b = edge
    t1, t2 = triples_from_neighbours(a, b)
    return frozenset({a, t1}), frozenset({a, t2}), frozenset({b, t1}), frozenset({b, t2})


def edge_triples(edge):
    """
    Get the triples that the edge is between.
    :param edge: Two cube coords neighbours.
    :return: Two triples.
    """
    t1, t2 = triples_from_neighbours(*edge)
    return frozenset({t1, *edge}), frozenset({t2, *edge})


def triple_neighbours(t):
    """
    Gets all the neighbouring triples.
    :param t: Cube coord triple.
    :return: A set of triples.
    """
    assert is_triple(*t), f"{t} is not a triple."
    return {frozenset({*n, c}) for n in combinations(t, r=2) for c in triples_from_neighbours(*n)} - {t}


def clockwise_centre_angle(c):
    """
    Calculates the clockwise angle from the centre.
    :param c: A cube coord x, z, y.
    :return: The angle in radians.
    """
    p = planer_position(c)
    q = 0, 0
    r = 0, float("-inf")
    return np.arctan2(p[1] - q[1], p[0] - q[0]) - np.arctan2(r[1] - q[1], r[0] - q[0])


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


def triple_planner_position(t):
    """
    Calculates the planer position of the triple.
    :param t: Cube coord triple.
    :return: horizontal, vertical positions.
    """
    return planer_position(sum(i) / 3 for i in zip(*t))


def edge_planer_position(edge):
    """
    Calculates the planer position of the edge.
    :param edge: Two cube cords neighbours.
    :return: (horizontal, vertical) and (horizontal, vertical) positions.
    """
    t1, t2 = edge_triples(edge)
    return triple_planner_position(t1), triple_planner_position(t2)


def planer_order(coords):
    """
    Orders the coords based on their planer position.
    :param coords: A iterable of cube coords.
    :return: A sorted list of cube coords.
    """
    return sorted(coords, key=planer_position)


def spiral_order(coords):
    """
    Orders the coords based on their spiral position.
    :param coords: A iterable of cube coords.
    :return: A sorted list of cube coords.
    """
    return sorted(coords, key=lambda c: (distance_from_centre(c), clockwise_centre_angle(c)), reverse=True)


def rows_order(coords):
    """
    Orders the vertical and horizontal position.
    :param coords: A iterable of cube coords.
    :return: A sorted list of cube coords.
    """
    return sorted(coords, key=lambda c: (c[1], c[0]))


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


def axial_to_pixel(h, size):
    """
    Converts axial position to pixel position.
    :param h: An axial coord q, r.
    :param size: The size of each hex.
    :return: The point x, y.
    """
    q, r = h
    return np.sqrt(3) * (size * q + r / 2), 3 * size * r / 2


def cube_to_pixel(c, size):
    """
    Converts cube coords to pixel position.
    :param c: A cube coord x, z, y.
    :param size: The size of each hex.
    :return: The point x, y.
    """
    return axial_to_pixel(cube_to_axial(c), size)


def all_edges(coords):
    """
    Finds all the triples from the given cube coords.
    :param coords: A set of cube coords.
    :return: A set of triples.
    """
    return {frozenset({a, b}) for a in coords for b in coords - {a} if is_neighbour(a, b)}


def edges_from_centre(k, exclude_outer_ring=True):
    """
    Gets all the edges k positions from the centre
    :param k: The distance from the center.
    :param exclude_outer_ring: If to exclude the edge between the hexes on the outer ring from the centre.
    :return: A set of all the edges from the centre.
    """
    edges = all_edges(neighbours_from_centre(k))
    if exclude_outer_ring:
        edges -= edges_on_ring(ring_from_centre(k))
    return edges


def all_triples(coords):
    """
    Finds all the triples from the given cube coords.
    :param coords: A set of cube coords.
    :return: A set of triples.
    """
    return {frozenset({a, b, c}) for a in coords for b in coords - {a} for c in coords - {a, b} if is_triple(a, b, c)}


def triples_from_centre(k):
    """
    Gets all the triples k positions from the centre
    :param k: The distance from the center.
    :return: A set of all the triples from the centre.
    """
    return all_triples(neighbours_from_centre(k))
