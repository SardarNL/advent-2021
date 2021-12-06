with open("day1.txt") as file:
    lines = [int(line.strip()) for line in file.readlines() if line.strip()]
    sums = [sum(lines[i:i+3]) for i in range(0, len(lines) - 2)]
    print len([1 for (prev, nex) in zip(sums, sums[1:]) if prev < nex])
