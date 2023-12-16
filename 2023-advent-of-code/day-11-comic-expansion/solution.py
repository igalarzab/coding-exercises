#!/usr/bin/env python

import argparse
import itertools
import logging
import os
import sys
import timeit


logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO').upper())


def solve_helper(problem_input: list[str], speed_of_expansion: int) -> int:
    galaxies = [(x, y) for x, row in enumerate(problem_input) for y, char in enumerate(row) if char == '#']
    empty_rows = [x for x, row in enumerate(problem_input) if set(row.strip()) == {'.'}]
    empty_cols = [x for x, col in enumerate(zip(*problem_input)) if set(col) == {'.'}]

    logging.debug(f'galaxies={galaxies}, empty_rows={empty_rows}, empty_columns={empty_cols}')
    result = 0

    # Coordinates of each galaxy in (x, y)
    for (g1x, g1y), (g2x, g2y) in itertools.combinations(galaxies, 2):
        distance = abs(g1x - g2x) + abs(g1y - g2y)

        # Let's get the coordinates in order to check if there is empty space between
        min_row, max_row = (g1x, g2x) if g1x < g2x else (g2x, g1x)
        min_col, max_col = (g1y, g2y) if g1y < g2y else (g2y, g1y)

        # How many empty rows are between both numbers
        for empty_row in empty_rows:
            if min_row < empty_row < max_row:
                distance += speed_of_expansion

        # How many empty cols are between both numbers
        for empty_col in empty_cols:
            if min_col < empty_col < max_col:
                distance += speed_of_expansion

        result += distance

    return result


def solve_part1(problem_input: list[str]) -> int:
    return solve_helper(problem_input, 1)


def solve_part2(problem_input: list[str]) -> int:
    return solve_helper(problem_input, 999_999)


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
