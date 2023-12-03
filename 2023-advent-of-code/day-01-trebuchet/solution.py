#!/usr/bin/env python

import logging
import sys
import os
import re


logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO').upper())


def solve_1(problem_input: list[str]) -> int:
    "Solves the first part of the problem"
    result = 0

    for line in problem_input:
        logging.debug(line.strip())
        digits = [c for c in line if c.isdigit()]

        if len(digits) == 0:
            continue

        result += int(digits[0] + digits[-1])
        logging.debug(f'result + {digits[0]}{digits[-1]} = {result}')

    return result


def solve_2(problem_input: list[str]) -> int:
    "Solves the second part of the problem"
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
        logging.debug(digits)

        if len(digits) == 0:
            continue

        first_value = digits[0] if digits[0].isdigit() else values[digits[0]]
        last_value = digits[-1] if digits[-1].isdigit() else values[digits[-1]]

        result += int(first_value + last_value)
        logging.debug(f'result + {first_value}{last_value} = {result}')

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
