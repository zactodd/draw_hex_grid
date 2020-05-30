import cv2
import numpy as np
import matplotlib.pyplot as plt
import dhg.cube_coords as cc
import dhg.draw_grid as dg


LAND_RANGE = np.asarray((200, 200, 200)), np.asarray((190, 190, 190))


def find_contours(grey_image):
    """
    Finds all the contours from a grey scale image.
    :param grey_image: A grey scale image.
    :return: a list of contours
    """
    _, thresh = cv2.threshold(grey_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def contour_centre(contour):
    """
    Calculates the centre of the contour.
    :param contour: The contour in which to obtain the centre.
    :return: x axis centre, y axis centre.
    """
    m = cv2.moments(contour)
    return m["m10"] / m["m00"], m["m01"] / m["m00"]


def draw_contours(image, contours):
    """
    Draws contours on the image.
    :param image: The image to draw on top of.
    :param contours: THe list of contours to draw.
    """
    plot_image = image.copy()
    xs, ys = [], []
    for i, c in enumerate(contours):
        x, y = contour_centre(c)
        xs.append(x)
        ys.append(y)
        plot_image = cv2.drawContours(plot_image, contours, i, (0, 255, 0), 3)

    plot_image = cv2.cvtColor(plot_image, cv2.COLOR_BGR2RGB)
    plt.imshow(plot_image)

    # Contour centres.
    plt.scatter(xs, ys)
    h, w, *_ = image.shape

    # Centre contour.
    plt.scatter(np.mean(xs), np.mean(ys), c="r")
    plt.show()


def distance(a, b):
    return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def hexagon_area(w):
    return 3 * w * w / (2 * np.sqrt(3))


def filter_contours_by_area(contours, upper, lower):
    """
    Filters a list of contours by area.
    :param contours: A list of contours.
    :param upper: The upper area bound.
    :param lower: The lower area bound.
    :return: The filtered list of contours.
    """
    return [c for c in contours if upper >= cv2.contourArea(c) >= lower]


def detect_grid(image, side_length):
    """
    Detects a grid from and an image.
    :param image: The image to detect the grid from.
    :param side_length: side length of the grid.
    :return: A set of cube coords {..., (x, z, y), ...}.
    """
    h, w, *_ = image.shape

    upper, lower = LAND_RANGE
    cnt = find_contours(cv2.inRange(image, lower, upper))

    haw = w / (2 * side_length)
    ha_max, ha_min = hexagon_area(haw), hexagon_area(haw * 0.60)
    cnt = filter_contours_by_area(cnt, ha_max, ha_min)

    cnt_centres = {contour_centre(c) for c in cnt}
    size = min(distance(i, j) for i in cnt_centres for j in cnt_centres - {i}) * 0.6
    hexes = set()
    for c in cnt_centres:
        cx, cy = c
        hexes.add(cc.pixel_to_cube((cx - (w / 2), cy - (h / 2)), size))
    return hexes


def plot_image_to_grid(image, side_length):
    """
    Plots the grid grid detected from the image.
    :param image: The image to detect the grid from.
    :param side_length: The side length of the grid.
    """
    dg.plot_hexes(detect_grid(image, side_length))


def image_to_grid(side_length, image_dir, outfile="coords.txt"):
    """
    Writes the hex grid to file.
    :param side_length: The side length of the grid.
    :param image_dir: THe directory of the ime.
    :param outfile: The outfile for the hexes.
    """
    with open(outfile, "w") as f:
        image = cv2.imread(image_dir)
        for h in detect_grid(image, side_length):
            f.write(f"{h}\n")
