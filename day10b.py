from functools import reduce

class Stack:
    def __init__(self):
        self.stack = []
        self.braces = { ')': '(', ']': '[', '}': '{', '>': '<' }
        self.cost = "([{<"
        self.failed = None

    def push(self, char):
        expect = self.braces.get(char, None)
        if expect is None:
            self.stack.append(char)
        elif self.stack[-1] == expect:
            self.stack.pop()
        else:
            self.failed = True

    def complete_score(self):
        self.stack.reverse()
        score = (self.cost.index(char) + 1 for char in self.stack)
        return reduce(lambda acc, scr: acc * 5 + scr, score, 0)


def complete_score(line):
    stack = Stack()
    for char in line:
        if not stack.failed:
            stack.push(char)

    return 0 if stack.failed else stack.complete_score()


with open("day10.txt") as file:
    scores = sorted(s for s in (complete_score(line.strip()) for line in file.readlines()) if s > 0)
    print scores[len(scores)/2]
