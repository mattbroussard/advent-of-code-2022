# 12/15/2022
# https://adventofcode.com/2022/day/15

import sys
import re

def manhattanDistance(a, b):
  ax, ay = a
  bx, by = b
  return abs(ax-bx) + abs(ay-by)


def rangeLength(r):
  if r is None:
    return 0
  a, b = r
  return b - a

# https://leetcode.com/problems/merge-intervals/
# heavily inspired by Neetcode solution: https://www.youtube.com/watch?v=44H3cEC2fFM
def combineRanges(ranges):
  ranges = sorted(ranges, key=lambda range: range[0])
  output = [ranges[0]]

  for i in range(1,len(ranges)):
    start, end = ranges[i]
    lastEnd = output[-1][1]

    if start <= lastEnd:
      output[-1] = (output[-1][0], max(end, lastEnd))
    else:
      output.append((start, end))

  return output

def part1(sensors, targetRow=10):
  hRanges = []

  for sensor, beacon in sensors:
    sx, sy = sensor
    beaconDist = manhattanDistance(sensor, beacon)
    targetRowDist = abs(targetRow - sy)
    if targetRowDist > beaconDist:
      continue

    remainingHorizDist = beaconDist - targetRowDist
    hRanges.append([sx - remainingHorizDist, sx + remainingHorizDist + 1])

  combinedRanges = combineRanges(hRanges)
  rangeSum = sum(rangeLength(r) for r in combinedRanges)

  beaconInRowSet = set(beacon for _, beacon in sensors if beacon[1] == targetRow)

  print("hRanges: %s\ncombinedRanges: %s\nbeaconsInRow: %s" % (hRanges, combinedRanges, beaconInRowSet))

  return rangeSum - len(beaconInRowSet)

def main(fname):
  sensors = []

  lineRe = re.compile("Sensor at x=([-\\d]+), y=([-\\d]+): closest beacon is at x=([-\\d]+), y=([-\\d]+)")

  with open(fname, 'r') as f:
    for line in f:
      matches = lineRe.match(line)
      if matches is None:
        continue

      sx = int(matches.group(1))
      sy = int(matches.group(2))
      bx = int(matches.group(3))
      by = int(matches.group(4))

      sensors.append(((sx, sy), (bx, by)))

  print("Part 1: %s" % (part1(sensors),))
  # print("Part 2: %s" % (part2(grid),))

if __name__ == '__main__':
  main(sys.argv[1])
