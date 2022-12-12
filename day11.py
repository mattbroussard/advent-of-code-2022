# 12/11/2022
# https://adventofcode.com/2022/day/11

import sys
from collections import deque
from copy import deepcopy
from math import floor, prod

class Monkey(object):
  idx = None # int
  throwIfFalse = None # int
  throwIfTrue = None # int
  moduloTest = None # int
  items = None # deque
  operation = None # function
  itemsInspected = 0

  def __init__(self, idx):
    self.idx = idx

def getTrailingNumber(line):
  s = line.split(" ")[-1]
  return int(s)

def getNumberList(line):
  s = line.split(": ")[-1].strip()
  if len(s) == 0:
    return []

  return [int(c) for c in s.split(", ")]

def getOperationFunction(line):
  s = line.split(": ")[-1]
  rhs = s.split("=")[-1].strip()
  def fn(old):
    # lol security
    return eval(rhs, None, {"old": old})
  return fn

def printMonkeys(monkeys, roundIndex=-1):
  print("After round %d:" % (roundIndex+1))
  for monkey in monkeys:
    itemStr = ", ".join(str(i) for i in monkey.items)
    print("  Monkey %d (%d inspected): %s" % (monkey.idx, monkey.itemsInspected, itemStr))

def part1(monkeys, nRounds=20, divideStep=True):
  monkeys = deepcopy(monkeys)

  for roundIndex in range(nRounds):
    # if roundIndex % 100 == 0:
    #   print("Round %d" % roundIndex)

    for monkeyIndex, monkey in enumerate(monkeys):
      while len(monkey.items) > 0:
        monkey.itemsInspected += 1
        item = monkey.items.popleft()

        # step 1: operation
        item = monkey.operation(item)

        # step 2: boredom/division
        if divideStep:
          item = floor(item / 3)

        # step 3: test
        test = item % monkey.moduloTest == 0
        nextMonkeyIdx = monkey.throwIfTrue if test else monkey.throwIfFalse
        nextMonkey = monkeys[nextMonkeyIdx]

        # step 4: throw
        nextMonkey.items.append(item)

    # printMonkeys(monkeys, roundIndex)

  sortedMonkeys = sorted(monkeys, key=lambda monkey: monkey.itemsInspected)
  return prod(monkey.itemsInspected for monkey in sortedMonkeys[-2:])

def part2(monkeys):
  # printMonkeys(monkeys)
  return part1(monkeys, 10000, False)

def main(fname):
  monkeys = []

  with open(fname, 'r') as f:
    for line in f:
      l = line.strip()

      if l.startswith("Monkey "):
        monkeys.append(Monkey(len(monkeys)))
        continue

      if l.startswith("Starting items:"):
        monkeys[-1].items = deque(getNumberList(l))
        continue

      if l.startswith("Operation:"):
        monkeys[-1].operation = getOperationFunction(l)
        continue

      if l.startswith("Test:"):
        monkeys[-1].moduloTest = getTrailingNumber(l)
        continue

      if l.startswith("If true:"):
        monkeys[-1].throwIfTrue = getTrailingNumber(l)
        continue

      if l.startswith("If false:"):
        monkeys[-1].throwIfFalse = getTrailingNumber(l)
        continue

  print("Part 1: %s" % (part1(monkeys),))
  print("Part 2: %s" % (part2(monkeys),))

if __name__ == '__main__':
  main(sys.argv[1])
