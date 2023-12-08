#!/usr/bin/env python

import argparse
import dataclasses
import logging
import os
import math
import sys
import timeit

from typing import Callable


logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO').upper())


@dataclasses.dataclass
class Input:
    instructions: str
    network: dict[str, tuple[str, str]]


def parse_input(problem_input: list[str]) -> Input:
    instructions = problem_input[0].strip()
    network = {}

    for line in problem_input[2:]:
        # Doc: network[starting_node] = (left_node, right_node)
        network[line[0:3]] = (line[7:10], line[12:15])

    return Input(instructions, network)


def solve_helper(mapp: Input, first_node: str, stop_cond: Callable[[str], bool]) -> int:
    current_node = first_node
    num_steps = 0
    instruction_idx = 0

    while stop_cond(current_node):
        left_node, right_node = mapp.network[current_node]
        num_steps += 1

        match mapp.instructions[instruction_idx]:
            case 'L':
                current_node = left_node
            case 'R':
                current_node = right_node
            case _:
                logging.error(f'Invalid instruction in {instruction_idx}')

        logging.debug(f' -> {current_node}')
        instruction_idx = (instruction_idx + 1) % len(mapp.instructions)

    return num_steps


def solve_part1(problem_input: list[str]) -> int:
    mapp = parse_input(problem_input)
    return solve_helper(mapp, 'AAA', lambda c: c != 'ZZZ')


def solve_part2(problem_input: list[str]) -> int:
    mapp = parse_input(problem_input)

    all_nodes_steps = []
    starting_nodes = [n for n in mapp.network.keys() if n.endswith("A")]

    for starting_node in starting_nodes:
        steps = solve_helper(mapp, starting_node, lambda c: not c.endswith('Z'))
        all_nodes_steps.append(steps)

    return math.lcm(*all_nodes_steps)


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
