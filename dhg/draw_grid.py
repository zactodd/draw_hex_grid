import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import dhg.cube_coords as cc


def _draw_hexes(hexes, ax, colour="white"):
    for h in hexes:
        x, y = cc.planer_position(h)
        patch = RegularPolygon((x, y), numVertices=6, facecolor=colour, radius=2 / 3 - 0.1,
                               orientation=0, edgecolor="k")
        ax.add_patch(patch)


def plot_hexes(hexes):
    """
    Plots hexes and the sea around them.
    :param hexes:
    """
    fig, ax = plt.subplots(1)
    ax.set_aspect("equal")

    _draw_hexes(hexes, ax, "lightgreen")
    sea_hexes = {n for h in hexes for n in cc.neighbours(h) if n not in hexes}

    _draw_hexes(sea_hexes, ax, "skyblue")

    plt.scatter(0, 0, alpha=0)
    plt.show()


def save_grid(size, directory="."):
    """
    Saves a grid.
    :param size: The side length of the grid.
    :param directory: The directory in which to save the grids.
    """
    assert size > 1, "size needs to be greater than 1."
    fig, ax = plt.subplots(1)
    ax.set_aspect("equal")
    hexes = cc.neighbours_from_centre(size - 1)

    _draw_hexes(hexes, ax)
    plt.scatter(0, 0, alpha=0)
    ax.axis("off")
    plt.savefig(f"{directory}/hex_grid_size_{size}.png", bbox_inches='tight')
