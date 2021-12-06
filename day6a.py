with open('day6.txt') as file:
    fish = [int(n) for n in file.readline().split(',')]
    for day in range(0, 80):
        fish = [6 if f == 0 else f - 1 for f in fish + ([9] * fish.count(0))]

    print len(fish)
