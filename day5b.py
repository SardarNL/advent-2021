import re
from collections import defaultdict


class HashCanvas:
    def __init__(self):
        self.canvas = defaultdict(lambda: 0)

    def draw(self, x1, y1, x2, y2):
        for x, y in zip(self._line(x1, x2, y1, y2), self._line(y1, y2, x1, x2)):
            self.canvas[(x, y)] += 1

    def count(self, predicate):
        return sum(1 for dot in self.canvas.values() if predicate(dot))

    def _line(self, a, b, r1, r2):
        if cmp(a, b):
            return range(a, b + self._step(a, b), self._step(a, b))
        else:
            return [a] * (abs(r2 - r1) + 1)

    def _step(self, a, b):
        return 1 if b >= a else -1


with open('day5.txt') as file:
    canvas = HashCanvas()
    for line in file.readlines():
        x1, y1, x2, y2 = re.match(r'(\d+),(\d+)\s*->\s*(\d+),(\d+)', line.strip()).groups()
        canvas.draw(int(x1), int(y1), int(x2), int(y2))

    print canvas.count(lambda x: x > 1)
