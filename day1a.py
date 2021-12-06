with open("day1.txt") as file:
    lines = [int(line.strip()) for line in file.readlines() if line.strip()]
    print len([1 for (prev, nex) in zip(lines, lines[1:]) if prev < nex])
