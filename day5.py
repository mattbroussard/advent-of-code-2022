# 12/5/2022
# https://adventofcode.com/2022/day/5

import sys
import re
from copy import deepcopy
from collections import deque

def parseInstruction(line):
  regex = re.compile("move (\\d+) from (\\d+) to (\\d+)")
  matches = regex.match(line)

  count = int(matches.group(1))
  src = int(matches.group(2))
  dest = int(matches.group(3))

  return (count, src, dest)

def parseStacks(lines, nStacks):
  stacks = [deque() for _ in range(nStacks)]

  for line in reversed(lines):
    for i, stack in enumerate(stacks):
      ci = 4 * i + 1
      if ci >= len(line):
        continue
      if line[ci] == ' ':
        continue
      stack.append(line[ci])

  return stacks

def part1(stacks, instructions):
  stacks = deepcopy(stacks)

  for count, src, dest in instructions:
    for _ in range(count):
      v = stacks[src - 1].pop()
      stacks[dest - 1].append(v)

  return "".join(stack[-1] for stack in stacks)

def part2(stacks, instructions):
  stacks = deepcopy(stacks)

  for count, src, dest in instructions:
    # we use an intermediate deque to reverse the order of the popped items so they
    # get added to destination stack in the same order they were on source stack. This
    # is a workaround for Python not supporting slice syntax on deques
    intermediate = deque()

    for _ in range(count):
      v = stacks[src - 1].pop()
      intermediate.append(v)

    for _ in range(count):
      v = intermediate.pop()
      stacks[dest - 1].append(v)

  return "".join(stack[-1] for stack in stacks)

def main():
  fname = sys.argv[1]

  stackLines = []
  nStacks = 0
  inStack = True
  instructions = []
  with open(fname, 'r') as f:
    for line in f:
      if line.startswith(" 1 "):
        inStack = False
        slots = list(filter(lambda s: len(s) > 0, line.strip().split(" ")))
        nStacks = int(slots[-1])
        continue

      if line.startswith("move "):
        instructions.append(parseInstruction(line))
        continue

      if inStack:
        stackLines.append(line)

  stacks = parseStacks(stackLines, nStacks)

  print("Part 1: %s" % (part1(stacks, instructions),))
  print("Part 2: %s" % (part2(stacks, instructions),))

if __name__ == '__main__':
  main()
