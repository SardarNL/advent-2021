
def bits(i, telemetry):
    votes = sum((num >> i) & 0x1 for num in telemetry) - len(telemetry) / 2
    return 1 if votes > 0 else 0

with open("day3.txt") as file:
    lines = [line.strip() for line in file.readlines() if line.strip()]
    length = max(len(line) for line in lines)
    telemetry = [int(line, 2) for line in lines]

    gamma = sum(bits(i, telemetry) << i for i in range(0, length))
    epsilon = ~gamma & (0x1 << length) - 1
    print gamma * epsilon

