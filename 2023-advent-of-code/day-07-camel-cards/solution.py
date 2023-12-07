#!/usr/bin/env python

import argparse
import logging
import os
import sys
import timeit

from collections import Counter, OrderedDict
from typing import Optional


logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO').upper())


def solve_helper(problem_input: list[str], alphabet: str, joker: Optional[str]) -> int:
    ranked_hands = OrderedDict([
        ('five_of_a_kind', []),
        ('four_of_a_kind', []),
        ('full_house', []),
        ('three_of_a_kind', []),
        ('two_pair', []),
        ('one_pair', []),
        ('high_card', []),
        ('nothing', []),
    ])

    for line in problem_input:
        hand, bet = line[0:5], int(line[6:].strip())
        hand_without_jokers = hand if not joker else hand.replace(joker, '')

        counter = Counter(hand_without_jokers)
        values = list(counter.values())
        values.sort()

        hand_size = len(hand_without_jokers)

        if values == [hand_size]:
            ranked_hands['five_of_a_kind'].append((hand, bet))
        elif values == [1, hand_size - 1]:
                ranked_hands['four_of_a_kind'].append((hand, bet))
        elif values == [2, hand_size - 2]:
                ranked_hands['full_house'].append((hand, bet))
        elif values == [1, 1, hand_size - 2]:
                ranked_hands['three_of_a_kind'].append((hand, bet))
        elif values == [1, hand_size - 3, hand_size - 3]:
                ranked_hands['two_pair'].append((hand, bet))
        elif values == [1, 1, 1, hand_size - 3]:
                ranked_hands['one_pair'].append((hand, bet))
        elif values == [1, 1, 1, 1, 1]:
                ranked_hands['high_card'].append((hand, bet))
        elif values == []: # All jokers "JJJJJ"
            ranked_hands['five_of_a_kind'].append((hand, bet))

    multiplier = len(problem_input)
    result = 0

    for _, hands in ranked_hands.items():
        sorted_hands = sorted(
            hands,
            key=lambda h: [alphabet.index(h[0][i]) for i in range(len(h[0]))],
        )

        for hand in sorted_hands:
            logging.debug(f'result = {result} + ({hand[1]} * {multiplier}) [{hand[0]}]')
            result += hand[1] * multiplier
            multiplier = max(1, multiplier - 1)

    return result


def solve_part1(problem_input: list[str]) -> int:
    return solve_helper(problem_input, 'AKQJT98765432', None)


def solve_part2(problem_input: list[str]) -> int:
    return solve_helper(problem_input, 'AKQT98765432J', 'J')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Programming Exercise Runner')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--part1', action='store_const', dest='fn', const=solve_part1)
    group.add_argument('--part2', action='store_const', dest='fn', const=solve_part2)
    group.add_argument('--benchmark', nargs='?', type=int, const=1)

    args = parser.parse_args()

    if args.fn:
        print(args.fn(sys.stdin.readlines()))
    elif args.benchmark:
        stdin = sys.stdin.readlines()
        print('Part 1: %fs' % timeit.timeit(lambda: solve_part1(stdin), number=args.benchmark))
        print('Part 2: %fs' % timeit.timeit(lambda: solve_part2(stdin), number=args.benchmark))
