# 12/8/2022
# https://adventofcode.com/2022/day/8

import sys
from functools import reduce

# https://stackoverflow.com/a/2082107/622371
def flatten(arr):
  return reduce(list.__add__, arr, [])

def printGrid(grid):
  # we print in hex because we may want to use values >9 for debug info
  print("\n".join("".join("%x" % v for v in row) for row in grid))
  print("")

def col(grid, x):
  for row in grid:
    yield row[x]

def transpose(grid):
  width = len(grid[0])
  return [list(col(grid, x)) for x in range(width)]

# for a given grid, computes a true/false mask of whether each cell
# is visible from the left (or right if fromLeft=false) side
def computeHorizVisibilityMask(grid, fromLeft = True):
  width = len(grid[0])
  height = len(grid)
  def colRange():
    if fromLeft:
      return range(width)
    else:
      return range(width-1,-1,-1)

  mask = [[False]*width for _ in range(height)]
  for y in range(height):
    maxSeen = -1
    for x in colRange():
      cell = grid[y][x]
      mask[y][x] = cell > maxSeen
      maxSeen = max(maxSeen, cell)

  return mask

def isVisible(x, y, *masks):
  for mask in masks:
    if mask[y][x]:
      return True
  return False

def part1(grid):
  width = len(grid[0])
  height = len(grid)

  leftMask = computeHorizVisibilityMask(grid)
  rightMask = computeHorizVisibilityMask(grid, fromLeft=False)
  transposedGrid = transpose(grid)
  topMask = transpose(computeHorizVisibilityMask(transposedGrid))
  bottomMask = transpose(computeHorizVisibilityMask(transposedGrid, fromLeft=False))

  visibleMask = [
    [
      int(isVisible(x, y, leftMask, rightMask, topMask, bottomMask))
      for x in range(width)
    ]
    for y in range(height)
  ]

  # printGrid(grid)
  # printGrid(visibleMask)

  visibleCount = sum(flatten(visibleMask))
  return visibleCount

def vecAdd(a, b):
  return tuple(sum(z) for z in zip(a, b))

def gridGet(grid, point):
  x, y = point
  return grid[y][x]

def scenicScore(grid, x, y):
  directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
  width = len(grid[0])
  height = len(grid)
  selfHeight = gridGet(grid, (x, y))

  def inBounds(x, y):
    return x >= 0 and x < width and y >=0 and y < width

  score = 1
  for delta in directions:
    dirScore = 0
    neighbor = vecAdd((x, y), delta)
    while inBounds(*neighbor):
      dirScore += 1
      neighborHeight = gridGet(grid, neighbor)
      if neighborHeight >= selfHeight:
        break
      neighbor = vecAdd(neighbor, delta)

    score *= dirScore

  return score

def part2(grid):
  maxSeen = 0
  width = len(grid[0])
  height = len(grid)

  # skip outer edges, they all have scenic score 0 because the view
  # is immediately blocked on edge
  for y in range(1,height-1):
    for x in range(1,width-1):
      score = scenicScore(grid, x, y)
      maxSeen = max(maxSeen, score)

  return maxSeen

def main(fname):
  with open(fname, 'r') as f:
    text = f.read().strip()
  
  rows = text.split("\n")
  grid = [[int(c) for c in list(row)] for row in rows]

  print("Part 1: %s" % (part1(grid),))
  print("Part 2: %s" % (part2(grid),))

if __name__ == '__main__':
  main(sys.argv[1])
