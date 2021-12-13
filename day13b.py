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

    width = max(x for x, _ in sheet) + 1
    height = max(y for _, y in sheet) + 1
    screen = [[' '] * width for y in range(0, height)]
    for x, y in sheet:
        screen[y][x] = '#'

    print "\n".join(''.join(line) for line in screen)
    #RGZLBHFP
