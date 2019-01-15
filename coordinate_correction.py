from math import sqrt


def correct(x, y):
    """Corrects the coordinates.

    Scale0 and scale1 define scaling constants. The scaling factor is a linear function of distance from center.

    Args:
        x (int): x coordinate
        y (int): y coordinate

    Returns:
        Tuple[int, int]: Corrected coordinates

    """

    # Scaling factors
    scale0 = 0.954
    scale1 = 0.00001

    # Convert screen coordinates to 0-based coordinates
    offset_x = 1738 / 2
    offset_y = 850 / 2

    # Calculate distance from center
    dist = sqrt((x - offset_x) ** 2 + (y - offset_y) ** 2)

    # Correct coordinates and return
    return (
        int(round((x - offset_x) * (scale0 + scale1 * dist) + offset_x)),
        int(round((y - offset_y) * (scale0 + scale1 * dist) + offset_y))
    )
