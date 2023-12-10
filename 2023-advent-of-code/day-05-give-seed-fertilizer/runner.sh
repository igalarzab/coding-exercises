#!/bin/bash

echo "--------- Running input-01 (part 1) ---------"
cat input-01.txt | ./solution.py --part1 | diff output-part1-01.txt - && echo "OK"

echo "--------- Running input-02 (part 1) ---------"
cat input-02.txt | ./solution.py --part1 | diff output-part1-02.txt - && echo "OK"

echo "--------- Running input-01 (part 2) ---------"
cat input-01.txt | ./solution.py --part2 | diff output-part2-01.txt - && echo "OK"

echo "--------- Running input-02 (part 2) ---------"
cat input-02.txt | ./solution.py --part2 | diff output-part2-02.txt - && echo "OK"

echo "----------------- Benchmark -----------------"
cat input-02.txt | ./solution.py --benchmark
