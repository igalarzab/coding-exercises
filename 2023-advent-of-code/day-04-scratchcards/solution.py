#!/usr/bin/env python

import argparse
import dataclasses
import logging
import os
import sys
import timeit


logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO').upper())


@dataclasses.dataclass
class Scratchcard:
    winners: list[int]
    my_numbers: list[int]


def parse_input(problem_input: list[str]) -> list[Scratchcard]:
    result = []

    for row in problem_input:
        splitted = row.split(': ')[1].split(' | ')

        winners = [int(n) for n in splitted[0].strip().split(' ') if n != '']
        my_numbers = [int(n) for n in splitted[1].strip().split(' ') if n != '']

        scratchcard = Scratchcard(winners, my_numbers)
        result.append(scratchcard)
        logging.debug(scratchcard)

    return result


def num_matches(sc: Scratchcard) -> int:
    'Calculates how many of my cards are also in the winning deck'
    return len(set(sc.winners).intersection(set(sc.my_numbers)))


def solve_part1(problem_input: list[str]) -> int:
    result = 0

    for scratchcard in parse_input(problem_input):
        result += int(2 ** (num_matches(scratchcard) - 1))

    return result


def solve_part2(problem_input: list[str]) -> int:
    scratchcards = parse_input(problem_input)
    num_scratchcards = [1] * len(scratchcards)

    for card_no, scratchcard in enumerate(scratchcards):
        num = num_matches(scratchcard)

        for i in range(card_no + 1, min(card_no + num, len(scratchcards)) + 1):
            num_scratchcards[i] += num_scratchcards[card_no]

        logging.debug(f'Scratchcard[{card_no + 1}] = {num_scratchcards}')

    return sum(num_scratchcards)


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
