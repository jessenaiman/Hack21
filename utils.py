# utils.py
"""Utility functions for the game."""

import math
from constants import *

def calculate_fov(map_obj, x, y, radius):
    """
    Calculate field of view using shadowcasting.

    Args:
        map_obj: Map instance.
        x (int): X-coordinate of the viewer.
        y (int): Y-coordinate of the viewer.
        radius (int): Visibility radius.

    Returns:
        set: Set of (x, y) coordinates visible to the viewer.
    """
    visible_tiles = {(x, y)}
    for octant in range(8):
        cast_light(map_obj, visible_tiles, x, y, 1, 1.0, 0.0, radius,
                   octant_dx[octant], octant_dy[octant], octant_dx[(octant + 1) % 8], octant_dy[(octant + 1) % 8])
    return visible_tiles

def cast_light(map_obj, visible_tiles, x, y, row, start, end, radius, xx, xy, yx, yy):
    """Recursive light-casting function for FOV."""
    if start < end:
        return
    radius_squared = radius * radius
    for j in range(row, radius + 1):
        dx, dy = -j - 1, -j
        blocked = False
        while dx <= 0:
            dx += 1
            map_x, map_y = x + dx * xx + dy * xy, y + dx * yx + dy * yy
            if map_x < 0 or map_x >= MAP_WIDTH or map_y < 0 or map_y >= MAP_HEIGHT:
                continue
            l_slope = (dx - 0.5) / (dy + 0.5)
            r_slope = (dx + 0.5) / (dy - 0.5)
            if start < r_slope:
                continue
            elif end > l_slope:
                break
            if dx * dx + dy * dy <= radius_squared:
                visible_tiles.add((map_x, map_y))
            if blocked:
                if not map_obj.is_transparent(map_x, map_y):
                    new_start = r_slope
                    continue
                else:
                    blocked = False
                    start = new_start
            else:
                if not map_obj.is_transparent(map_x, map_y) and j < radius:
                    blocked = True
                    cast_light(map_obj, visible_tiles, x, y, j + 1, start, l_slope, radius, xx, xy, yx, yy)
                    new_start = r_slope
        if blocked:
            break

# Octant direction mappings for FOV
octant_dx = [1, 1, 0, -1, -1, -1, 0, 1]
octant_dy = [0, 1, 1, 1, 0, -1, -1, -1]