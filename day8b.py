
class Matcher:
    def __init__(self, patterns):
        self.patterns = patterns
        self.matched = {}

    def match(self, digit, predicate):
        self.matched[digit] = next(p for p in self.patterns if predicate(self.matched, p))
        self.patterns = [p for p in self.patterns if p != self.matched[digit]]

    def map(self, digits):
        return int(''.join(next(k for (k, v) in self.matched.items() if v == d) for d in digits))


def detect(patterns):
    mth = Matcher(patterns)
    mth.match('1', lambda _, p: len(p) == 2)
    mth.match('4', lambda _, p: len(p) == 4)
    mth.match('7', lambda _, p: len(p) == 3)
    mth.match('8', lambda _, p: len(p) == 7)
    mth.match('9', lambda dg, p: dg['4'].issubset(p))
    mth.match('3', lambda dg, p: dg['7'].issubset(p) and p.issubset(dg['9']))
    mth.match('0', lambda dg, p: dg['7'].issubset(p))
    mth.match('6', lambda _, p: len(p) == 6)
    mth.match('5', lambda dg, p: p.issubset(dg['3'] | dg['4']))
    mth.match('2', lambda _, p: True)
    return mth


def parse(line):
    patterns, digits = ([set(pattern) for pattern in part.split()] for part in line.split('|'))
    return detect(patterns).map(digits)


with open("day8.txt") as file:
    print sum(parse(line) for line in file.readlines())
