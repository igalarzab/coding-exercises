# Coding Exercises

Solutions for some of the coding exercises I've done. There are folders for each specific competition/challenge.

### Run locally

I'm using a variaty of languages so, to simplify the execution, there is a shell script in each exercise that runs the
problem using the right compiler/interpreter and checks the output with the expected one. Example:

```sh
$ cd 2023-advent-of-code/day-01-trebuchet
$ ./runner.sh
```

As a general rule I'm using only the standard library of each language so there should be no external
dependencies needed, but there is a `.tools-version` file ([asdf](https://asdf-vm.com/)) pointing to the right versions
of the compilers/interpreters I'm using.
