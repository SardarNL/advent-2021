import re

WIDTH = 10
HEIGHT = 10


def neighbours(pos):
    x = pos % WIDTH
    y = pos / WIDTH
    candidates = ((x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1),
            (x, y + 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1))

    return (y * WIDTH + x for x, y in candidates if 0 <= x < WIDTH and 0 <= y < HEIGHT)


def flash(pos, octo):
    for idx in neighbours(pos):
        increment(idx, octo)


def increment(pos, octo):
    octo[pos] += 1
    if octo[pos] == 10:
        flash(pos, octo)


def simulate(octo):
    for pos in range(0, len(octo)):
        increment(pos, octo)

    result = sum(1 for energy in octo if energy > 9)
    for pos, energy in enumerate(octo):
        if energy > 9:
            octo[pos] = 0

    return result


with open("day11.txt") as file:
    octo = [int(e) for e in re.sub(r'[^0-9]', '', file.read())]
    print sum(simulate(octo) for step in range(0, 100))
