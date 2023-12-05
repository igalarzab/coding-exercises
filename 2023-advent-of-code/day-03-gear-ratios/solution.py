#!/usr/bin/env python

import logging
import sys
import os

from dataclasses import dataclass


logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO').upper())


@dataclass
class Number:
    value: int
    length: int
    x: int
    y: int
    valid: bool

    def __hash__(self):
        return hash(f'{self.x}-{self.y}')


@dataclass
class Symbol:
    value: str
    x: int
    y: int


def parse_input(problem_input: list[str]) -> tuple[dict[int, list[Number]], list[Symbol]]: 
    "Finds all the numbers in the input, storing also where they start (x, y)"
    numbers: dict[int, list[Number]] = {} # { row_num: [num1, num2, num3, ...]}
    symbols: list[Symbol] = [] # [ symbol1, symbol2, ...]

    for nline, line in enumerate(problem_input):
        buffer, found_x, found_y = '', 0, 0

        for nchar, char in enumerate(line):
            if char.isnumeric():
                if len(buffer) == 0:
                    found_x = nline
                    found_y = nchar

                buffer += char
            else:
                # First we see if there is a number that we finished
                if len(buffer) != 0:
                    found_num = Number(int(buffer), len(buffer), found_x, found_y, False)
                    logging.debug(f'Found: {found_num}')

                    numbers.setdefault(nline, []).append(found_num)
                    buffer = ''

                # Now we see if there is also a symbol here
                if char.isprintable() and not char.isalpha() and char != '.':
                    found_symbol = Symbol(char, nline, nchar)
                    logging.debug(f'Found: {found_symbol}')

                    symbols.append(found_symbol)

    return numbers, symbols


def solve_1(problem_input: list[str]) -> int:
    "Solves the first part of the problem"
    numbers, symbols = parse_input(problem_input)

    # We only check numbers in 3 rows per symbol
    for symbol in symbols:
        for row_offset in [-1, 0, 1]:
            for number in numbers.get(symbol.x + row_offset, []):
                if (number.y - 1) <= symbol.y < (number.y + number.length + 1):
                    logging.debug(f'Match: [{symbol}, {number}]')
                    number.valid = True

    result = 0

    # We check all the parts that have not been matched
    for row in numbers.values():
        for number in row:
            if number.valid:
                result += number.value

    return result


def solve_2(problem_input: list[str]) -> int:
    "Solves the second part of the problem"
    numbers, symbols = parse_input(problem_input)
    result = 0

    for symbol in symbols:
        matches: list[Number] = []

        for row_offset in [-1, 0, 1]:
            for number in numbers.get(symbol.x + row_offset, []):
                if (number.y - 1) <= symbol.y < (number.y + number.length + 1):
                    logging.debug(f'Match: [{symbol}, {number}]')
                    matches.append(number)

        if len(matches) == 2:
            result += matches[0].value * matches[1].value

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
