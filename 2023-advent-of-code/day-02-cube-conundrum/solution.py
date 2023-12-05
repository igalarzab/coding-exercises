#!/usr/bin/env python

import argparse
import logging
import math
import os
import re
import sys
import timeit


logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO').upper())


MY_GAME = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

CUBES_GROUPS_REGEX = re.compile(r'([\d]+) ([\w]+)[;,]?')


def solve_part1(problem_input: list[str]) -> int:
    result = 0

    for line in problem_input:
        logging.debug(line.strip())

        # It seems game_id is incremental, but lets extract it just in case
        game_id, rest = line.split(': ')
        game_id = int(game_id[len('Game '):])

        cubes_groups = CUBES_GROUPS_REGEX.findall(rest)
        possible = True

        for cubes in cubes_groups:
            if MY_GAME.get(cubes[1], 0) < int(cubes[0]):
                logging.debug(f'Invalid Game: ID[{game_id}], Problem[{cubes}]')
                possible = False
                break

        if possible:
            logging.debug(f'Valid Game: ID[{game_id}]')
            result += game_id

    return result


def solve_part2(problem_input: list[str]) -> int:
    result = 0

    for line in problem_input:
        logging.debug(line.strip())

        cubes_groups = CUBES_GROUPS_REGEX.findall(line.split(': ')[1])
        min_cubes = {} # { color: min_num_of_cubes }

        for cubes in cubes_groups:
            min_cubes[cubes[1]] = max(min_cubes.get(cubes[1], 0), int(cubes[0]))

        result += math.prod(min_cubes.values())

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
