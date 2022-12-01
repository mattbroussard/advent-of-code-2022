# 12/1/2022
# https://adventofcode.com/2022/day/1

import sys

def part1(elves):
  sums = [sum(c) for c in elves]
  return max(sums)

def part2(elves):
  sums = [sum(c) for c in elves]
  sums.sort()
  return sum(sums[-3:])

def main():
  fname = sys.argv[1]

  elves = [[]]
  with open(fname, 'r') as f:
    for line in f:
      if len(line.strip()) == 0:
        elves.append([])
        continue

      elves[-1].append(int(line))

  print("Part 1: %s" % (part1(elves),))
  print("Part 2: %s" % (part2(elves),))

if __name__ == '__main__':
  main()
