from collections import defaultdict


def simulate(fish, days):
    for day in range(0, days):
        stock = dict((age - 1, count) for (age, count) in fish.items() if age > 0)
        stock[8] = fish.get(0, 0)
        stock[6] = stock.get(6, 0) + fish.get(0, 0)
        fish = stock

    return sum(fish.values())


with open('day6.txt') as file:
    fish = defaultdict(lambda: 0)
    for n in file.readline().split(','):
        fish[int(n)] += 1

    print simulate(fish, 256)
