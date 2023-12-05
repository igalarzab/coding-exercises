#!/usr/bin/env python

import logging
import sys
import os

from typing import Generator


logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO').upper())


def parse_input(problem_input: list[str]) -> Generator[tuple[list[int], list[int]], None, None]:
    for row in problem_input:
        splitted = row.split(': ')[1].split(' | ')

        my_numbers = [int(n) for n in splitted[0].strip().split(' ') if n != '']
        winners = [int(n) for n in splitted[1].strip().split(' ') if n != '']

        # We sort the lists as it will be faster to check later
        my_numbers.sort()
        winners.sort()

        logging.debug(f'MyNumbers{my_numbers}, Winners{winners}')

        yield (my_numbers, winners)


def num_matches(my_numbers: list[int], winners: list[int]) -> int:
    "Calculates how many cards I have of the winners"
    num = 0

    for winner in winners:
        for number in my_numbers:
            if number == winner:
                logging.debug(f'Match: {number}')
                num += 1

            # As the lists are sorted we can stop checking after the number is greater
            if number >= winner:
                break

    return num


def solve_1(problem_input: list[str]) -> int:
    "Solves the first part of the problem"
    result = 0

    for my_numbers, winners in parse_input(problem_input):
        result += int(2 ** (num_matches(my_numbers, winners) - 1))

    return result


def solve_2(problem_input: list[str]) -> int:
    "Solves the second part of the problem"
    cards = list(parse_input(problem_input))
    num_scratchcards = [1] * len(cards)

    for card_no, (my_numbers, winners) in enumerate(cards):
        num = num_matches(my_numbers, winners)

        for i in range(card_no + 1, min(card_no + num, len(cards)) + 1):
            num_scratchcards[i] += num_scratchcards[card_no]

        logging.debug(f'Scratchboard after Card {card_no + 1}: {num_scratchcards}')

    return sum(num_scratchcards)


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
