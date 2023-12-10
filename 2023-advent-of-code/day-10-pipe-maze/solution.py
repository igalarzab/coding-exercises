#!/usr/bin/env python

import argparse
import logging
import os
import sys
import timeit

from collections import deque


logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO').upper())


Coords = tuple[int, int]
Distance = int

POSSIBLE_MOVES = {
    '|': [(-1, 0), (1, 0)], # North, South
    '-': [(0, -1), (0, 1)], # West, East
    'L': [(-1, 0), (0, 1)], # North, East
    'J': [(-1, 0), (0, -1)], # North, West
    '7': [(1, 0), (0, -1)], # South, West
    'F': [(1, 0), (0, 1)], # South, East
    'S': [(-1, 0), (1, 0), (0, -1), (0, 1)], # North, South, West, East 
    '.': [], # Nowhere
}


def find_start_coords(matrix: list[list[str]]) -> Coords:
    for x, line in enumerate(matrix):
        for y, char in enumerate(line):
            if char == 'S':
                return (x, y)

    raise ValueError('Start coords do not exist')


def accessible_neighbours(matrix: list[list[str]], node_coords: Coords) -> list[Coords]:
    "Get all the valid neighbours from the `node_coords` param"
    result: list[Coords] = []

    matrix_x_size = len(matrix)
    matrix_y_size = len(matrix[0])
    node = matrix[node_coords[0]][node_coords[1]]

    for move in POSSIBLE_MOVES[node]:
        x = max(0, min(matrix_x_size, node_coords[0] + move[0]))
        y = max(0, min(matrix_y_size, node_coords[1] + move[1]))
        result.append((x, y))

    logging.debug(f'{node_coords} -> {list(result)}')
    return result


def distances_from_start(matrix: list[list[str]], start_coords: Coords) -> dict[Coords, Distance]:
    "We search through the whole matrix using BFS"
    distances: dict[Coords, Distance] = dict()
    queue: deque[tuple[Coords, Distance]] = deque([(start_coords, 0)])
    distance: Distance = 0

    while queue:
        node_coords, distance = queue.popleft()

        if node_coords in distances:
            continue

        distances[node_coords] = distance

        for neighbour_coords in accessible_neighbours(matrix, node_coords):
            # Check also if we can come back (needed for "." and "S")
            if node_coords in accessible_neighbours(matrix, neighbour_coords):
                queue.append((neighbour_coords, distance + 1))

    logging.debug(f'{distances}')
    return distances


def solve_part1(problem_input: list[str]) -> int:
    matrix = [list(line.strip()) for line in problem_input]
    start_coords = find_start_coords(matrix)
    distances = distances_from_start(matrix, start_coords)

    return max(distances.values()) 


def solve_part2(problem_input: list[str]) -> int:
    matrix = [list(line.strip()) for line in problem_input]
    start_coords = find_start_coords(matrix)

    distances = distances_from_start(matrix, start_coords)
    visited_nodes = distances.keys()

    # Every non-visited pipe should be taken in consideration (we change them to ".")
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            if (x, y) not in visited_nodes:
                matrix[x][y] = '.'

    return 0


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
