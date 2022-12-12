# 12/12/2022
# https://adventofcode.com/2022/day/12

import sys
from heapq import heappush, heappop
from copy import deepcopy

def findAllPositions(grid, v):
  for y, row in enumerate(grid):
    for x, cell in enumerate(row):
      if cell == v:
        yield (x, y)

def findPos(grid, v):
  for pos in findAllPositions(grid, v):
    return pos

def neighbors(grid, pos):
  height = len(grid)
  width = len(grid[0])
  x, y = pos
  for dx, dy in [(0,1),(0,-1),(-1,0),(1,0)]:
    nx = x + dx
    ny = y + dy
    if nx >= 0 and nx < width and ny >= 0 and ny < height:
      yield (nx, ny)

def gridGet(grid, pos):
  x, y = pos
  return grid[y][x]

def heightCharToValue(c):
  if c == 'S':
    c = 'a'
  elif c == 'E':
    c = 'z'

  return ord(c) - ord('a')

def navigable(src, dest):
  src = heightCharToValue(src)
  dest = heightCharToValue(dest)
  return dest <= src + 1

def part1(grid):
  start = findPos(grid, "S")
  visited = set([start])
  queue = [(0, start)]

  while len(queue) > 0:
    dist, pos = heappop(queue)
    curHeight = gridGet(grid, pos)
    # print("visiting %s (dist=%d): %s (neighbors: %s)" % (pos, dist, curHeight, list(neighbors(grid, pos))))

    if gridGet(grid, pos) == 'E':
      return dist

    for n in neighbors(grid, pos):
      if n not in visited and navigable(curHeight, gridGet(grid, n)):
        visited.add(n)
        heappush(queue, (dist + 1, n))

  return None

def swap(grid, a, b):
  ax, ay = a
  bx, by = b
  tmp = grid[ay][ax]
  grid[ay][ax] = grid[by][bx]
  grid[by][bx] = tmp

def part2(grid):
  grid = deepcopy(grid)
  possibleStarts = [findPos(grid, 'S')] + list(findAllPositions(grid, 'a'))
  lengths = [float('inf')] * len(possibleStarts)

  for i in range(len(possibleStarts)):
    swap(grid, possibleStarts[0], possibleStarts[i])
    l = part1(grid)
    if l is not None:
      lengths[i] = l
    swap(grid, possibleStarts[0], possibleStarts[i])

  return min(lengths)

def main(fname):
  grid = []

  with open(fname, 'r') as f:
    for line in f:
      grid.append(list(line.strip()))

  print("Part 1: %s" % (part1(grid),))
  print("Part 2: %s" % (part2(grid),))

if __name__ == '__main__':
  main(sys.argv[1])
