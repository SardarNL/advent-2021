import re

def is_low(terrain, width, idx):
    y = idx / width
    x = idx % width
    value = terrain[idx]
    height = len(terrain) / width
    
    return not ((y > 0 and terrain[(y - 1) * width + x] <= value)
        or (y + 1 < height and terrain[(y + 1) * width + x] <= value)
        or (x > 0 and terrain[y * width + x - 1] <= value)
        or (x + 1 < width and terrain[y * width + x + 1] <= value))


with open("day9.txt") as file:
    lines = [line.strip() for line in file.readlines()]
    terrain = [int(char) for char in ''.join(lines)]
    width = len(lines[0])
    print sum(terrain[idx] + 1 for idx in range(0, len(terrain)) if is_low(terrain, width, idx))
