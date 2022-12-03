# 12/3/2022
# https://adventofcode.com/2022/day/3

import sys

def getMisplacedItemType(bag):
  midpoint = int(len(bag) / 2)
  a, b = bag[:midpoint], bag[midpoint:]
  intersection = set(list(a)).intersection(set(list(b)))
  if len(intersection) != 1:
    raise Exception("invalid")
  return intersection.pop()

def priorityOfItemType(itemType):
  c = ord(itemType)
  if c >= ord('a'):
    return c - ord('a') + 1
  else:
    return c - ord('A') + 27

def getCommonInGroup(group):
  s = set(list(group[0]))
  for item in group[1:]:
    s = s.intersection(set(list(item)))
  if len(s) != 1:
    raise Exception("invalid")
  return s.pop()

def part1(entries):
  types = [getMisplacedItemType(bag) for bag in entries]
  return sum(priorityOfItemType(t) for t in types)

def part2(entries):
  total = 0
  for i in range(0,len(entries),3):
    group = entries[i:i+3]
    common = getCommonInGroup(group)
    total += priorityOfItemType(common)
  return total

def main():
  fname = sys.argv[1]

  entries = []
  with open(fname, 'r') as f:
    for line in f:
      entries.append(line.strip())

  print("Part 1: %s" % (part1(entries),))
  print("Part 2: %s" % (part2(entries),))

if __name__ == '__main__':
  main()
