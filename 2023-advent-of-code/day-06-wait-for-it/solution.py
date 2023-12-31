#!/usr/bin/env python

import argparse
import logging
import math
import os
import sys
import timeit


logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO').upper())


def solve_part1(problem_input: list[str]) -> int:
    times = [int(t) for t in problem_input[0].split()[1:]]
    distances = [int(d) for d in problem_input[1].split()[1:]]
    result = []

    logging.debug(f'times={times}, distances={distances}')

    for time, distance in zip(times, distances):
        options_to_win = 0

        for i in range(1, time):
            if (time - i) * i > distance:
                options_to_win += 1

        result.append(options_to_win)

    logging.debug(f'result={result}')
    return math.prod(result)


# FIXME: It takes 2s, there is probably a better way of solving it
def solve_part2(problem_input: list[str]) -> int:
    time = int(problem_input[0][len('Time:'):].replace(' ', ''))
    distance = int(problem_input[1][len('Distance:'):].replace(' ', ''))

    logging.debug(f'time={time}, distance={distance}')
    options_to_win = 0

    for i in range(1, time):
        if (time - i) * i > distance:
            options_to_win += 1

    logging.debug(f'options_to_win={options_to_win}')
    return options_to_win


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
