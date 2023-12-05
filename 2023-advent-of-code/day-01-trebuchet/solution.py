#!/usr/bin/env python

import argparse
import logging
import os
import re
import sys
import timeit


logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO').upper())


def solve_part1(problem_input: list[str]) -> int:
    result = 0

    for line in problem_input:
        logging.debug(line.strip())
        digits = [c for c in line if c.isdigit()]

        if len(digits) == 0:
            continue

        result += int(digits[0] + digits[-1])
        logging.debug(f'result + {digits[0]}{digits[-1]} = {result}')

    return result


def solve_part2(problem_input: list[str]) -> int:
    values = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9',
    }

    regex = re.compile(f'(?=({"|".join(values.keys())}|\\d))')
    result = 0

    for line in problem_input:
        logging.debug(line.strip())
        digits = regex.findall(line)

        if len(digits) == 0:
            continue

        # Transform alpha numbers to real numbers if needed
        first_value = digits[0] if digits[0].isdigit() else values[digits[0]]
        last_value = digits[-1] if digits[-1].isdigit() else values[digits[-1]]

        result += int(first_value + last_value)
        logging.debug(f'result + {first_value}{last_value} = {result}')

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
