import re

class Submarine:
    position = 0
    depth = 0
    aim = 0

    def action(self, action, step):
        if "forward" == action:
            self.position += step
            self.depth += self.aim * step
        elif "up" == action:
            self.aim -= step
        else:
            self.aim += step

with open("day2.txt") as file:
    sub = Submarine()
    for line in [line for line in file.readlines() if line.strip()]:
        match = re.match(r'^(up|down|forward)\s+(\d+)\s*$', line)
        sub.action(match.group(1), int(match.group(2)))

    print sub.position * sub.depth
