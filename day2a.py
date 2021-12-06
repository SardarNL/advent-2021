import re
from functools import reduce


actions = {
    "forward": lambda step: (step, 0),
    "up": lambda step: (0, -step),
    "down": lambda step: (0, step)
}

def action(line):
    match = re.match(r'^(up|down|forward)\s+(\d+)\s*$', line)
    return actions[match.group(1)](int(match.group(2)))

with open("day2.txt") as file:
    course = [action(line) for line in file.readlines() if line.strip()]
    pos, depth = reduce(lambda (a, b), (c, d): (a + c, b + d), course)
    print pos * depth
