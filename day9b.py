import re
from collections import defaultdict
from functools import reduce


def trace(basins, alias, frm):
    to = alias[frm]
    basins[to] += basins[frm]
    basins[frm] = 0
    if to in alias:
        trace(basins, alias, to)


with open("day9.txt") as file:
    lines = [line.strip() for line in file.readlines()]
    terrain = [int(char) for char in ''.join(lines)]
    width = len(lines[0])

    basins = defaultdict(lambda: 0)
    alias = {}
    basin_terrain = [0] * len(terrain)
    next_label = 1
    for pos, value in enumerate(terrain):
        if value == 9:
            continue

        y = pos / width
        x = pos % width
        label_y = basin_terrain[(y - 1) * width + x] if y > 0 else 0
        label_x = basin_terrain[y * width + x - 1] if x > 0 else 0
        if label_y == 0 or label_x == 0:
            label = max(label_y, label_x)
        else:
            label = min(label_y, label_x)
            if label_y != label_x:
                alias[max(label_y, label_x)] = label

        if label == 0:
            label = next_label
            next_label += 1

        basin_terrain[pos] = label
        basins[label] += 1

    for frm in alias:
        trace(basins, alias, frm)
    
    print reduce(lambda a, b: a * b, sorted(basins.values(), reverse=True)[0:3])
