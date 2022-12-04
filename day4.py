# 12/4/2022
# https://adventofcode.com/2022/day/4

import sys

def rangeIntersect(r1, r2):
  a, b = r1
  c, d = r2

  start = max(a, c)
  end = min(b, d)

  if end < start:
    return None
  return (start, end)

def part1(entries):
  count = 0
  for pair in entries:
    a, b = pair
    intersection = rangeIntersect(a, b)
    if intersection == a or intersection == b:
      count += 1
  return count

def part2(entries):
  count = 0
  for pair in entries:
    if rangeIntersect(*pair) is not None:
      count += 1
  return count

def main():
  fname = sys.argv[1]

  entries = []
  with open(fname, 'r') as f:
    for line in f:
      commaParts = line.strip().split(',')
      ranges = [tuple(int(c) for c in s.split("-")) for s in commaParts]
      entries.append(ranges)

  print("Part 1: %s" % (part1(entries),))
  print("Part 2: %s" % (part2(entries),))

if __name__ == '__main__':
  main()
