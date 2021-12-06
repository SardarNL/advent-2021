
BOARD_SIZE = 5
BOARD_MASK = (0x1 << BOARD_SIZE) - 1

class Board:
    def __init__(self, file):
        self.board = []
        self.by_row = [0] * BOARD_SIZE
        self.by_col = [0] * BOARD_SIZE

        line = file.readline().strip()
        while line:
            self.board.extend(line.split())
            line = file.readline().strip()

    def __nonzero__(self):
        return bool(self.board)

    def consume(self, num):
        if num not in self.board:
            return False

        pos = self.board.index(num)
        row = pos / BOARD_SIZE
        col = pos % BOARD_SIZE
        self.by_row[col] |= 0x1 << row
        self.by_col[row] |= 0x1 << col

        return BOARD_MASK in self.by_row or BOARD_MASK in self.by_col

    def sum(self):
        result = 0
        for row_num, row in enumerate(self.by_col):
            for i in range(0, BOARD_SIZE):
                if row & (0x1 << i) == 0:
                    result += int(self.board[row_num * BOARD_SIZE + i])

        return result


with open("day4.txt") as file:
    draw = file.readline().strip().split(',')
    file.readline()

    boards = []
    while True:
        board = Board(file)
        if board:
            boards.append(board)
        else:
            break

    for num in draw:
        for board in boards:
            if board.consume(num):
                print board.sum() * int(num)
                exit()

