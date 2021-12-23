from collections import defaultdict

positions = [10] + range(1, 10)


def create_dice():
    dice = defaultdict(lambda: 0)
    for d in (d1 + d2 + d3 for d1 in xrange(1, 4) for d2 in xrange(1, 4) for d3 in xrange(1, 4)):
        dice[d] += 1

    return dice.items()


def play(player1, player2, dice, cache, level = 0):
    key = (player1, player2, level)
    if key in cache:
        return cache[key]

    p1_wins = 0
    p2_wins = 0
    for score1, times1 in dice:
        if is_winning(player1, score1):
            p1_wins += times1
        else:
            for score2, times2 in dice:
                if is_winning(player2, score2):
                    p2_wins += times1 * times2
                else:
                    w1, w2 = play(advance(player1, score1), advance(player2, score2), dice, cache, level + 1)
                    p1_wins += w1 * times1 * times2
                    p2_wins += w2 * times1 * times2

    result = (p1_wins, p2_wins)
    cache[key] = result
    return result


def is_winning(player, score):
    return advance(player, score)[1] >= 21


def advance(player, score):
    position, current_score = player
    position = positions[(position + score) % 10]
    return (position, current_score + position)


with open("day21.txt") as file:
    player1 = (int(file.readline().split(':')[1].strip()), 0)
    player2 = (int(file.readline().split(':')[1].strip()), 0)

    dice = create_dice()
    cache = {}

    p1_wins, p2_wins = play(player1, player2, dice, cache)
    print max(p1_wins, p2_wins)

