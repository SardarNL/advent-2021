import re
from math import sqrt


def solve(result, n):
    return (sqrt(1 + 4 * (2 * result + n * (n + 1))) - 1) / 2


def candidates(frm, to):
    solved = []
    for candidate in range(frm, to + 1):
        for n in range(0, candidate):
            value = solve(candidate, n)
            if value.is_integer():
                solved.append((int(value), n))

    return solved


with open("day17.txt") as file:
    x1, x2, y1, y2 = (int(g) for g in re.match(r"target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)", file.read()).groups())
    xs = [(v, v - n) for v, n in candidates(x1, x2)]

    ys = [(-(n + 1), v - n) for v, n in candidates(abs(y2), abs(y1))]
    ys.extend([(-(yv + 1), steps + abs(yv) * 2 - 1) for yv, steps in ys])

    result = []
    for x_velocity, x_time in xs:
        for y_velocity, y_time in ys:
            if (x_time == y_time) or (x_velocity == x_time and y_time >= x_time):
                result.append((x_velocity, y_velocity))
    
    max_y = max(y for _, y in result)
    print "Part 1: {}".format((max_y * (max_y + 1)) / 2)
    print "Part 2: {}".format(len(set(result)))
