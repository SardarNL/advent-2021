import re


with open("day13.txt") as file:
    lines = [line.strip() for line in file.readlines()]
    border = lines.index('')

    sheet = set((int(x), int(y)) for x, y in (pair.split(',') for pair in lines[0:border]))
    for axis, offset in (re.match(r'fold along (x|y)=(\d+)', line).groups() for line in lines[border + 1:]):
        offset = int(offset)
        if axis == "y":
            sheet = set((x, 2 * offset - y if y > offset else y) for x, y in sheet)
        else:
            sheet = set((2 * offset - x if x > offset else x, y) for x, y in sheet)

        break

    print len(sheet)
