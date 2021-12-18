from heapq import heappush, heappop
from collections import namedtuple

Point = namedtuple('Point', ('cost', 'risk', 'position', 'parent'))

class Board:
    def __init__(self, board, width):
        self.board = board
        self.width = width
        self.height = len(board) / width
        self.heap = []

        start = Point(0, 0, (0, 0), None)
        self.points = { start.position: start }
        heappush(self.heap, start)


    def lowest_cost(self):
        while True:
            current = self.head()
            if self.is_end(current):
                return self.trace_back(current)

            if not self.is_replaced(current):
                for neighbour in self.neighbours(current):
                    if self.is_cheaper(neighbour):
                        self.points[neighbour.position] = neighbour
                        heappush(self.heap, neighbour)


    def neighbours(self, point):
        x, y = point.position
        for cx, cy in ((x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)):
            if 0 <= cx < self.width and 0 <= cy < self.height:
                risk = self.board[cy * self.width + cx] + point.risk
                yield Point(cx + cy + risk, risk, (cx, cy), point.position)


    def head(self):
        current = heappop(self.heap)
        if self.points[current.position].parent == current.parent:
            return current
        
        return self.head()

    
    def is_end(self, point):
        x, y = point.position
        return x == self.width - 1 and y == self.height - 1


    def is_cheaper(self, point):
        if point.position not in self.points:
            return True

        return point.risk < self.points[point.position].risk

    
    def is_replaced(self, point):
        if point.position not in self.points:
            return False

        return point.parent != self.points[point.position].parent


    def trace_back(self, point):
        risk = 0
        while point.parent is not None:
            x, y = point.position
            risk += self.board[y * self.width + x]
            point = self.points[point.parent]

        return risk


def tiled_cost(digit, idx, width):
    cost = (int(digit) + (idx / width) / (width / 5) + (idx % width) / (width / 5)) % 9
    return 9 if cost == 0 else cost


with open("day15.txt") as file:
    lines =  [line.strip() * 5 for line in file.readlines()] * 5
    width = len(lines[0])
    cave = [tiled_cost(digit, idx, width) for idx, digit in enumerate(''.join(lines))]

    board = Board(cave, width)

    # using A* algorithm
    print board.lowest_cost()
