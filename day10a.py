class Stack:
    def __init__(self):
        self.stack = []
        self.braces = { ')': '(', ']': '[', '}': '{', '>': '<' }
        self.cost = { ')': 3, ']': 57, '}': 1197, '>': 25137 }
        self.failed = None

    def push(self, char):
        expect = self.braces.get(char, None)
        if expect is None:
            self.stack.append(char)
        elif self.stack[-1] == expect:
            self.stack.pop()
        else:
            self.failed = self.cost[char]


def error_score(line):
    stack = Stack()
    for char in line:
        if not stack.failed:
            stack.push(char)

    return stack.failed if stack.failed else 0


with open("day10.txt") as file:
    print sum(error_score(line.strip()) for line in file.readlines())
