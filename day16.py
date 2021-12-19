from functools import reduce


MASK = (0, 0b1000, 0b1100, 0b1110, 0b1111)

OPS = {
    0: sum,
    1: lambda values: reduce(lambda a, b: a * b, values),
    2: min,
    3: max,
    5: lambda (a, b): 1 if a > b else 0,
    6: lambda (a, b): 1 if a < b else 0,
    7: lambda (a, b): 1 if a == b else 0
}


class Bitstream:
    def __init__(self, hexstring):
        self.source = (int(c, 16) for c in hexstring)
        self.bits = 0
        self.quad = None
        self.lengths = []


    def parse(self):
        version = stream.read(3)
        type_id = stream.read(3)

        if type_id == 4:
            return (version, type_id, self.read_literal())
        
        if stream.read(1) == 0:
            nodes = self.read_bitsize()
        else:
            nodes = self.read_fields()

        return (version, type_id, nodes)


    def read(self, size):
        for idx, length in enumerate(self.lengths):
            self.lengths[idx] = length - size

        return self._read(size)


    def _read(self, size):
        if self.bits == 0:
            self.quad = next(self.source)
            self.bits = 4

        to_read = min(self.bits, size)
        size -= to_read
        value = self.read_quad(to_read)
        if size == 0:
            return value

        return (value << size) + self._read(size)


    def read_quad(self, size):
        value = (self.quad & MASK[size]) >> (4 - size)
        self.quad <<= size
        self.bits -= size
        return value


    def read_literal(self, acc = 0):
        pack = self.read(5)
        value = (pack & 0xF) + acc
        if pack & 0x10:
            return self.read_literal(value << 4)
        else:
            return value


    def read_bitsize(self):
        self.lengths.append(stream.read(15))
        nodes = []
        while self.lengths[-1] > 0:
            nodes.append(self.parse())

        self.lengths.pop()
        return nodes


    def read_fields(self):
        return [stream.parse() for x in range(0, stream.read(11))]


def sum_version(node):
    version, node_id, payload = node
    if node_id != 4:
        version += sum(sum_version(n) for n in payload)

    return version


def eval(tree):
    _, type_id, payload = tree
    if type_id == 4:
        return payload
    else:
        values = [eval(n) for n in payload]
        return OPS[type_id](values)


with open("day16.txt") as file:
    stream = Bitstream(file.read().strip())
    tree = stream.parse()

    print "Part 1: {}".format(sum_version(tree))
    print "Part 2: {}".format(eval(tree))
