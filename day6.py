# 12/6/2022
# https://adventofcode.com/2022/day/6

import sys
from collections import deque

def readUntilCondition(text, condition, lookback=4):
  buf = deque()

  for i, c in enumerate(text):
    buf.append(c)
    while len(buf) > lookback:
      buf.popleft()

    if len(buf) == lookback and condition(buf):
      return i + 1
  
  return -1

def allCharactersUnique(buf):
  s = set(buf)
  return len(s) == len(buf)

def part1(text):
  return readUntilCondition(text, allCharactersUnique, lookback=4)

def part2(text):
  return readUntilCondition(text, allCharactersUnique, lookback=14)

def main():
  fname = sys.argv[1]

  with open(fname, 'r') as f:
    text = f.read().strip()

  print("Part 1: %s" % (part1(text),))
  print("Part 2: %s" % (part2(text),))

if __name__ == '__main__':
  main()
