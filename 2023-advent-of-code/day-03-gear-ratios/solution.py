#!/usr/bin/env python

import argparse
import dataclasses
import logging
import os
import sys
import timeit

from typing import Optional


logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO').upper())


@dataclasses.dataclass
class Number:
    value: int
    length: int
    x: int
    y: int
    valid: Optional[bool]


@dataclasses.dataclass
class Symbol:
    value: str
    x: int
    y: int


def parse_input(problem_input: list[str]) -> tuple[dict[int, list[Number]], list[Symbol]]:
    """
    We parse the input by separately storing in a tuple all the symbols 
    and numbers we see. The numbers are stored in a dictionary with the row where 
    they are located as its key, as it will help us optimise later how many 
    checks we have to do. We also store along both numbers and symbols the position (x,y)
    were they were found to help us solving both parts of the exercise.
    """
    numbers: dict[int, list[Number]] = {} # { row_num: [num1, num2, num3, ...]}
    symbols: list[Symbol] = [] # [ symbol1, symbol2, ...]

    # We iterate line by line and char by char to find the digits and symbols:
    #  - If we see a symbol we just store it in `symbols` with its location (x, y)
    #  - If we see a number we'll store digit by digit all its value in `num_buffer` and we'll
    #    store in `found_x` and `found_y` the position (x,y) of its first digit
    for nline, line in enumerate(problem_input):
        num_buffer, found_x, found_y = '', 0, 0

        for nchar, char in enumerate(line):
            if char.isnumeric():
                # If `num_buffer` is empty it means it's the first digit of a new number 
                # so we store its location (x, y)
                if len(num_buffer) == 0:
                    found_x = nline
                    found_y = nchar

                num_buffer += char
            else:
                # If we see a non-digit and `num_buffer` is not empty it means we finished
                # a number, so we store it in our list of numbers and continue
                if len(num_buffer) != 0:
                    found_num = Number(int(num_buffer), len(num_buffer), found_x, found_y, None)
                    logging.debug(f'Found: {found_num}')

                    numbers.setdefault(nline, []).append(found_num)
                    num_buffer = ''

                # Now we see if this non-digit is a symbol
                if char.isprintable() and not char.isalpha() and char != '.':
                    found_symbol = Symbol(char, nline, nchar)
                    logging.debug(f'Found: {found_symbol}')

                    symbols.append(found_symbol)

    return numbers, symbols


def solve_part1(problem_input: list[str]) -> int:
    numbers, symbols = parse_input(problem_input)

    for symbol in symbols:
        # We only check numbers in the 3 closest rows as further away it cannot touch the symbol
        for row_offset in [-1, 0, 1]:
            for number in numbers.get(symbol.x + row_offset, []):
                if (number.y - 1) <= symbol.y < (number.y + number.length + 1):
                    logging.debug(f'Match: [{symbol}, {number}]')
                    number.valid = True

    result = 0

    # We check all the parts that have been matched to calculate the result
    for row in numbers.values():
        for number in row:
            if number.valid:
                result += number.value

    return result


def solve_part2(problem_input: list[str]) -> int:
    numbers, symbols = parse_input(problem_input)
    result = 0

    for symbol in symbols:
        matches: list[Number] = []

        # We only check numbers in the 3 closest rows as further away it cannot touch the symbol
        for row_offset in [-1, 0, 1]:
            for number in numbers.get(symbol.x + row_offset, []):
                if (number.y - 1) <= symbol.y < (number.y + number.length + 1):
                    logging.debug(f'Match: [{symbol}, {number}]')
                    matches.append(number)

        if len(matches) == 2:
            result += matches[0].value * matches[1].value

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
