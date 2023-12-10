#!/usr/bin/env python

import argparse
import logging
import os
import sys
import timeit


logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO').upper())


def calculate_diffs(nums: list[int]) -> list[list[int]]:
    "It calculates the diffs array (until it reaches [0, 0, 0, ...])"
    diffs = [nums]

    while diffs[-1] != ([0] * len(diffs[-1])):
        diffs.append([diffs[-1][i+1] - diffs[-1][i] for i in range(len(diffs[-1]) - 1)])

    return diffs


def solve_part1(problem_input: list[str]) -> int:
    lines = [[int(num) for num in line.split()] for line in problem_input]
    result = 0

    for line in lines:
        diffs = calculate_diffs(line)

        for i in range(len(diffs) - 2, -1, -1):
            diffs[i].append(diffs[i][-1] + diffs[i+1][-1])

        result += diffs[0][-1]
        logging.debug(diffs)

    return result


def solve_part2(problem_input: list[str]) -> int:
    lines = [[int(num) for num in line.split()] for line in problem_input]
    result = 0

    for line in lines:
        diffs = calculate_diffs(line)

        # We will still append at the end as it doesn't require moving the array
        for i in range(len(diffs) - 2, -1, -1):
            diffs[i].append(diffs[i][0] - diffs[i+1][-1])

        result += diffs[0][-1]
        logging.debug(diffs)

    return result


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
