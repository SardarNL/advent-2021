# brute forced
with open("day7.txt") as file:
    stand = [int(crab) for crab in file.readline().strip().split(',')]
    print min(sum(sum(range(1, abs(crab - mid) + 1)) for crab in stand) for mid in range(min(stand), max(stand)+1))
