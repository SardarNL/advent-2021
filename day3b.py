
class Holder:
    def __init__(self, telemetry, invert):
        self.telemetry = telemetry
        self.invert = invert
        self.mask = 0

    def push(self, bit):
        if (len(self.telemetry) > 1):
            self.mask = (self.mask << 1) + self.post(bits(bit, self.telemetry))
            self.telemetry = [n for n in self.telemetry if not (n >> bit) ^ self.mask]

    def post(self, bit):
        return (~bit & 0x1) if self.invert else bit


def bits(i, telemetry):
    votes = sum((num >> i) & 0x1 for num in telemetry) * 2 - len(telemetry)
    return 1 if votes >= 0 else 0


with open("day3.txt") as file:
    lines = [line.strip() for line in file.readlines() if line.strip()]
    length = max(len(line) for line in lines)
    telemetry = [int(line, 2) for line in lines]

    gamma_holder = Holder(telemetry, False)
    epsilon_holder = Holder(telemetry, True)
    for i in range(length - 1, -1, -1):
        gamma_holder.push(i)
        epsilon_holder.push(i)

    print gamma_holder.telemetry[0] * epsilon_holder.telemetry[0]

