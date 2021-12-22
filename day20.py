
class Canvas:
    def __init__(self, enhance, width, original, iterations):
        self.enhance = enhance
        self.iterations = iterations
        self.width = iterations * 2 + width
        self.height = iterations * 2 + len(original) / width
        self.bits = [None] * (self.width * self.height)

        for row in range(len(original) / width):
            frm = (iterations + row) * self.width + iterations
            self.bits[frm:frm + width] = original[row * width:(row + 1) * width]

        self.swap_buffer = list(self.bits)
        self.alternating_infinity = enhance[0]


    def iterate(self):
        self.iterations -= 1

        for row in range(self.height - self.iterations * 2):
            for col in range(self.width - self.iterations * 2):
                pos = (self.iterations + row) * self.width + self.iterations + col
                self.swap_buffer[pos] = self.compute(self.iterations + row, self.iterations + col)

        self.bits[:] = self.swap_buffer


    def compute(self, row, col):
        value = 0
        for y in range(row - 1, row + 2):
            for x in range(col - 1, col + 2):
                value = (value << 1) | self.bit(x, y)

        return self.enhance[value]


    def bit(self, x, y):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return self.inifinity_bit()

        ret = self.bits[y * self.width + x]
        if ret is None:
            return self.inifinity_bit()

        return ret


    def inifinity_bit(self):
        if self.alternating_infinity:
            return (self.iterations + 1) & 1
        else:
            return 0


with open("day20.txt") as file:
    enhance = [1 if char == '#' else 0 for char in file.readline().strip()]
    lines = [line.strip() for line in file.readlines()]
    width = len(lines[1])
    image = [1 if char == '#' else 0 for line in lines[1:] for char in line]

    canvas = Canvas(enhance, width, image, 50)
    canvas.iterate()
    canvas.iterate()

    print "Part 1: {}".format(sum(1 for bit in canvas.bits if bit))

    for _ in range(48):
        canvas.iterate()

    print "Part 2: {}".format(sum(1 for bit in canvas.bits if bit))
