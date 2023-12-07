#!/bin/bash

echo "--------- Running input-01 (part 1) ---------"
cat input-01.txt | ./solution.py --part1 | diff output-01-part1.txt - && echo "OK"

echo "--------- Running input-02 (part 1) ---------"
cat input-02.txt | ./solution.py --part1 | diff output-02-part1.txt - && echo "OK"

echo "--------- Running input-01 (part 2) ---------"
cat input-01.txt | ./solution.py --part2 | diff output-01-part2.txt - && echo "OK"

echo "--------- Running input-02 (part 2) ---------"
cat input-02.txt | ./solution.py --part2 | diff output-02-part2.txt - && echo "OK"

echo "----------------- Benchmark -----------------"
cat input-02.txt | ./solution.py --benchmark
