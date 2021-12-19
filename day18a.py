import re
from collections import Sequence
from functools import reduce


class Reference:
    def __init__(self, owner, idx):
        self.owner = owner
        self.idx = idx

    def __setitem__(self, key, value):
        self.owner[self.idx] = value

    def __getitem__(self, key):
        return self.owner[self.idx]


def parse(line):
    stack = [[]]
    for token in re.findall(r'([][]|\d+)', line):
        if token == '[':
            pair = []
            stack[-1].append(pair)
            stack.append(pair)
        elif token == ']':
            stack.pop()
        else:
            stack[-1].append(int(token))
    
    return stack.pop()[0]


def reduce_snail(num):
    while True:
        if explode(num):
            continue

        if split(num):
            continue

        break

    return num


def explode(num, left = None, right = None, depth = 1):
    a, b = num
    result = False
    if depth == 4:
        if isinstance(a, Sequence):
            if left is not None:
                right_most(left)[1] += a[0]

            if isinstance(b, Sequence):
                b[0] += a[1]
            else:
                num[1] += a[1]

            num[0] = 0
            result = True

        if isinstance(b, Sequence):
            if right is not None:
                left_most(right)[0] += b[1]

            num[0] += b[0]
            num[1] = 0
            result = True
    else:
        if isinstance(a, Sequence):
            result |= explode(a, left, node(b, num, 1), depth + 1)

        if isinstance(b, Sequence):
            result |= explode(b, node(a, num, 0), right, depth + 1)

    return result


def split(num):
    a, b = num
    if isinstance(a, Sequence) and split(a):
        return True

    if not isinstance(a, Sequence) and a > 9:
        num[0] = [a / 2, (a / 2) + (a % 2)]
        return True

    if isinstance(b, Sequence) and split(b):
        return True

    if not isinstance(b, Sequence) and b > 9:
        num[1] = [b / 2, (b / 2) + (b % 2)]
        return True


def right_most(num):
    if isinstance(num, Reference):
        return num

    a, b = num
    if not isinstance(b, Sequence):
        return num
    
    return right_most(b)


def left_most(num):
    if isinstance(num, Reference):
        return num

    a, b = num
    if not isinstance(a, Sequence):
        return num
    
    return left_most(a)


def node(side, current, idx):
    if isinstance(side, Sequence):
        return side

    return Reference(current, idx)


def magnitude(num):
    if not isinstance(num, Sequence):
        return num

    a, b = num
    return 3 * magnitude(a) + 2 * magnitude(b)


with open("day18.txt") as file:
    num = reduce(lambda a, b: reduce_snail([a, b]), (parse(line.strip()) for line in file.readlines()))
    print magnitude(num)

