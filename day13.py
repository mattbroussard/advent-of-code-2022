# 12/13/2022
# https://adventofcode.com/2022/day/13

import sys
import json
from functools import cmp_to_key, reduce

debug = False
def iprint(s, i=0):
  if not debug:
    return

  indent = " " * i
  print(indent + s)

def p1Compare(a, b, indent=0):
  iprint("- Compare %s vs %s" % (a, b), indent)
  if type(a) == int and type(b) == int:
    if a < b:
      iprint("- Left side is smaller, return TRUE", indent + 1)
      return True
    elif b < a:
      iprint("- Right side is smaller, return FALSE", indent + 1)
      return False
    else:
      return None

  if type(a) == int:
    a = [a]
  if type(b) == int:
    b = [b]

  for i in range(max(len(a), len(b))): # previously: for av, bv in zip(a, b)
    av = a[i] if i < len(a) else None
    bv = b[i] if i < len(b) else None

    if av is None:
      iprint("- Left side ran out of items, return TRUE", indent + 1)
      return True
    if bv is None:
      iprint("- Right side ran out of items, return FALSE", indent + 1)
      return False

    cmpResult = p1Compare(av, bv, indent + 1)
    if cmpResult is not None:
      return cmpResult

  return None

def part1(pairs):
  correctIndices = []

  for i, pair in enumerate(pairs):
    iprint("\n== Pair %d ==" % (i+1))

    cmpResult = p1Compare(*pair)
    iprint("Pair %d final result: %s" % (i+1, cmpResult))

    if cmpResult == True:
      correctIndices.append(i + 1)

  iprint("\nCorrect indices: %s\n" % (correctIndices,))
  return sum(correctIndices)

def flatten(arr):
  return reduce(lambda a, b: a + list(b), arr, [])

def part2(pairs):
  div1 = [[2]]
  div2 = [[6]]
  entries = [div1, div2] + flatten(pairs)

  def cmp(a, b):
    result = p1Compare(a, b)
    if result == True:
      return -1
    elif result == False:
      return 1
    else:
      return 0

  entries.sort(key=cmp_to_key(cmp))

  for e in entries:
    iprint(json.dumps(e))

  return (entries.index(div1) + 1) * (entries.index(div2) + 1)

def main(fname):
  entries = []

  with open(fname, 'r') as f:
    for line in f:
      if len(line.strip()) == 0:
        continue
      entries.append(json.loads(line))

  pairs = [(entries[i], entries[i+1]) for i in range(0,len(entries),2)]

  print("Part 1: %s" % (part1(pairs),))
  print("Part 2: %s" % (part2(pairs),))

if __name__ == '__main__':
  main(sys.argv[1])
