#!/usr/bin/env python

import argparse
import dataclasses
import logging
import os
import re
import sys
import timeit


logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO').upper())


CATEGORY_REGEX = re.compile(r'^([\w]+)-to-([\w]+) map:$')
AMOUNTS_REGEX = re.compile(r'^([\d]+) ([\d]+) ([\d]+)$')


@dataclasses.dataclass
class Transformer:
    destination_start: int
    source_start: int
    length: int


@dataclasses.dataclass
class Category:
    source: str
    destination: str
    transformers: list[Transformer]


@dataclasses.dataclass
class Input:
    seeds: list[int]
    categories: list[Category]


def parse_input(problem_input: list[str]) -> Input:
    seeds = [int(s) for s in problem_input[0].strip()[len('seeds: '):].split(' ')]

    categories: list[Category] = []
    transformers: list[Transformer] = []
    category_source, category_destination = '', ''

    for line in problem_input[2:]:
        line = line.strip()

        if not line:
            continue

        if category := CATEGORY_REGEX.match(line):
            if len(transformers) > 0:
                categories.append(Category(category_source, category_destination, transformers))
                transformers = []

            category_source = category[1]
            category_destination = category[2]
        elif amounts := AMOUNTS_REGEX.match(line):
            dest, source, length = int(amounts[1]), int(amounts[2]), int(amounts[3])
            transformers.append(Transformer(dest, source, length))
        else:
            logging.error('Invalid line: ' + line)
            sys.exit(-1)

    if len(transformers) > 0:
        categories.append(Category(category_source, category_destination, transformers))

    return Input(seeds, categories)


def solve_part1(problem_input: list[str]) -> int:
    parsed = parse_input(problem_input)
    locations = []

    for seed in parsed.seeds:
        val = seed
        for category in parsed.categories:
            for transformer in category.transformers:
                if val >= transformer.source_start and val < (transformer.source_start + transformer.length):
                    old_val = val
                    val = transformer.destination_start + ( val - transformer.source_start)
                    logging.debug(f'{category.destination} {transformer} {old_val} -> {val}')
                    break

        locations.append(val)

    logging.debug(locations)
    return min(locations)


# FIXME: Too slow, takes 1h in resolve, find a better way
def solve_part2(problem_input: list[str]) -> int:
    parsed = parse_input(problem_input)
    locations = []

    for i in range(0, len(parsed.seeds), 2):
        for seed in range(parsed.seeds[i], parsed.seeds[i] + parsed.seeds[i+1]):
            val = seed
            for category in parsed.categories:
                for transformer in category.transformers:
                    if val >= transformer.source_start and val < (transformer.source_start + transformer.length):
                        val = transformer.destination_start + ( val - transformer.source_start)
                        break

            locations.append(val)

    return min(locations)


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
