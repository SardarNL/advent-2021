from collections import Counter


with open("day14.txt") as file:
    seed = file.readline().strip()
    file.readline()
    patterns = dict(line.strip().split(' -> ') for line in file.readlines())

    for step in range(0, 10):
        seed = ''.join(seed[pos] + patterns.get(seed[pos:pos + 2], '') for pos in range(0, len(seed) - 1)) + seed[-1]

    counts = Counter(seed).most_common()
    print counts[0][1] - counts[-1][1]
