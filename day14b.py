from collections import defaultdict


def compute(level, a, b, cache, patterns):
    pattern_key = a + b
    key = pattern_key + str(level)

    if level == 0:
        counts = { a: 1 }
        cache[key] = counts
        return counts

    if key in cache:
        return cache[key]

    sub = patterns[pattern_key]
    counts = defaultdict(lambda: 0)
    for k, v in compute(level - 1, a, sub, cache, patterns).items():
        counts[k] += v

    for k, v in compute(level - 1, sub, b, cache, patterns).items():
        counts[k] += v

    cache[key] = counts
    return counts


with open("day14.txt") as file:
    seed = list(file.readline().strip())
    file.readline()
    patterns = dict(line.strip().split(' -> ') for line in file.readlines())

    cache = {}
    counts = defaultdict(lambda: 0)
    for pos in range(0, len(seed) - 1):
        for k, v in compute(40, seed[pos], seed[pos+1], cache, patterns).items():
            counts[k] += v

    counts[seed[-1]] += 1
    print max(counts.values()) - min(counts.values())
