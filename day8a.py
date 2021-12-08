with open("day8.txt") as file:
    print sum(sum(1 for seg in line.split('|')[1].split() if len(seg) in (2, 3, 4, 7)) for line in file.readlines())
