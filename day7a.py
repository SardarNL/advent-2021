with open("day7.txt") as file:
    stand = [int(crab) for crab in file.readline().strip().split(',')]
    print min(sum(abs(crab - mid) for crab in stand) for mid in range(min(stand), max(stand)+1))
