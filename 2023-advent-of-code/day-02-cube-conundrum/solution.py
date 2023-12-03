#!/usr/bin/env python

import logging
import math
import sys
import os
import re


logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO').upper())

MY_GAME = {
    'red': 12,
    'green': 13,
    'blue': 14,
}
    
CUBES_GROUPS_REGEX = re.compile(r'([\d]+) ([\w]+)[;,]?')


def solve_1(problem_input: list[str]) -> int:
    "Solves the first part of the problem"
    result = 0

    for line in problem_input:
        logging.debug(line.strip())
        game_id, rest = line.split(':')

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


def solve_2(problem_input: list[str]) -> int:
    "Solves the second part of the problem"
    result = 0

    for line in problem_input:
        logging.debug(line.strip())

        cubes_groups = CUBES_GROUPS_REGEX.findall(line.split(':')[1])
        min_cubes = {}

        for cubes in cubes_groups:
            min_cubes[cubes[1]] = max(min_cubes.get(cubes[1], 0), int(cubes[0]))

        result += math.prod(min_cubes.values())

    return result


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} [--part1|--part2]')
        sys.exit(1)

    match sys.argv[1]:
        case '--part1':
            print(solve_1(sys.stdin.readlines()))
        case '--part2':
            print(solve_2(sys.stdin.readlines()))
        case invalid_value:
            print(f'Invalid part: {invalid_value}')
            sys.exit(2)
