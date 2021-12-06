import re
from collections import defaultdict


class HashCanvas:
    def __init__(self):
        self.canvas = defaultdict(lambda: 0)

    def draw_vertical(self, x, y1, y2):
        for y in range(y1, y2 + cmp(y2, y1), cmp(y2, y1)):
            self.canvas[(y, x)] += 1

    def draw_horizontal(self, x1, x2, y):
        for x in range(x1, x2 + cmp(x2, x1), cmp(x2, x1)):
            self.canvas[(y, x)] += 1

    def count(self, predicate):
        return sum(1 for dot in self.canvas.values() if predicate(dot))


with open('day5.txt') as file:
    canvas = HashCanvas()
    for line in file.readlines():
        x1, y1, x2, y2 = re.match(r'(\d+),(\d+)\s*->\s*(\d+),(\d+)', line.strip()).groups()
        if x1 == x2:
            canvas.draw_vertical(int(x1), int(y1), int(y2))
        elif y1 == y2:
            canvas.draw_horizontal(int(x1), int(x2), int(y1))

    print canvas.count(lambda x: x > 1)

