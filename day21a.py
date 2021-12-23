from itertools import count

scores = [10] + range(1, 10)


with open("day21.txt") as file:
    player1 = int(file.readline().split(':')[1].strip())
    player2 = int(file.readline().split(':')[1].strip())

    points1 = 0
    points2 = 0
    rolled = 0

    for dice in count(1, 3):
        score = (dice + 1) * 3

        if dice & 1:
            player1 = scores[(player1 + score) % 10]
            points1 += player1
        else:
            player2 = scores[(player2 + score) % 10]
            points2 += player2

        rolled += 3
        if points1 >= 1000 or points2 >= 1000:
            break

    print min(points1, points2) * rolled

