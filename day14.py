# 12/14/2022
# https://adventofcode.com/2022/day/14

import sys
from copy import deepcopy

sandSourcePosition = (500, 0)

class Grid(object):
  data = None # dict: (x, y) -> value
  minX = None
  minY = None
  maxX = None
  maxY = None
  floorY = None
  def __init__(self):
    self.data = {}

  def __getitem__(self, key):
    if type(key) == list:
      return [self[k] for k in key]
    elif type(key) == tuple and len(key) == 2:
      if self.isFloor(key):
        return "rock"

      if key in self.data:
        return self.data[key]

      return "air"
    else:
      raise Exception("invalid input to __getitem__")

  def __setitem__(self, key, val):
    if type(key) == list:
      for k in key:
        self[k] = val
    elif type(key) == tuple and len(key) == 2:
      self.data[key] = val
      if val == "air":
        del self.data[key]
      self.updateBounds(key)
    else:
      raise Exception("invalid input to __setitem__")

  def isAbyss(self, key):
    if self.floorY is not None:
      return False

    if self.minX is None:
      # uninited, everything is abyss
      return True

    x, y = key
    return x < self.minX or x > self.maxX or y < self.minY or y > self.maxY

  def isFloor(self, key):
    if self.floorY is None:
      return False

    x, y = key
    return y >= self.floorY

  def addFloor(self):
    self.floorY = self.maxY + 2

  def updateBounds(self, key):
    x, y = key
    self.minX = x if self.minX is None else min(self.minX, x)
    self.minY = y if self.minY is None else min(self.minY, y)
    self.maxX = x if self.maxX is None else max(self.maxX, x)
    self.maxY = y if self.maxY is None else max(self.maxY, y)

  def valueToPrintChar(self, value, pos):
    if value == "air":
      if pos == sandSourcePosition:
        return "+"
      return "."
    elif value == "rock":
      return "#"
    elif value == "sand":
      return "o"
    elif value == "sand_source":
      return "+"
    else:
      return "?"

  def __str__(self):
    def colRange():
      return range(self.minX, self.maxX+1)

    rows = []
    maxY = self.floorY if self.floorY is not None else self.maxY
    for y in range(self.minY, maxY+1):
      label = "%3d " % y
      row = "".join(self.valueToPrintChar(self[(x, y)], (x, y)) for x in colRange())
      rows.append(label + row)

    colLabels = ["%3d" % x for x in colRange()]
    colTextRows = ["    " + "".join(colLabels[x - self.minX][y] for x in colRange()) for y in range(3)]

    return "\n" + "\n".join(colTextRows + rows) + "\n"

def drawLine(a, b):
  xa, ya = a
  xb, yb = b

  if xa == xb:
    minY = min(ya, yb)
    maxY = max(ya, yb)
    for y in range(minY, maxY+1):
      yield (xa, y)
  elif ya == yb:
    minX = min(xa, xb)
    maxX = max(xa, xb)
    for x in range(minX, maxX+1):
      yield (x, ya)
  else:
    raise Exception("no diagonal lines in drawLine helper")

def down(pos):
  x, y = pos
  return (x, y+1)

def downLeft(pos):
  x, y = pos
  return (x-1, y+1)

def downRight(pos):
  x, y = pos
  return (x+1, y+1)

def buildGrid(entries):
  grid = Grid()
  for points in entries:
    for i in range(1, len(points)):
      line = list(drawLine(points[i-1], points[i]))
      grid[line] = "rock"

  return grid

def parsePoint(ptString):
  vals = [int(v) for v in ptString.split(",")]
  return (vals[0], vals[1])

def part1(grid):
  grid = deepcopy(grid)

  sands = 0
  finalized = False
  while not finalized: # loop over new sand blocks
    sands += 1
    pos = sandSourcePosition

    if grid[pos] != "air":
      break
    grid[pos] = "sand"

    moved = True
    while moved: # loop over steps of a block falling
      moved = False
      for dirFn in [down, downLeft, downRight]:
        nextPos = dirFn(pos)
        if grid[nextPos] != "air":
          continue

        if grid.isAbyss(nextPos):
          finalized = True
          grid[pos] = "air"
          break

        grid[pos] = "air"
        grid[nextPos] = "sand"
        pos = nextPos
        moved = True
        break

      # print(grid)

  # print(grid)
  return sands - 1

def part2(grid):
  grid = deepcopy(grid)
  grid.addFloor()
  return part1(grid)

def main(fname):
  entries = []

  with open(fname, 'r') as f:
    for line in f:
      points = [parsePoint(s.strip()) for s in line.split("->")]
      entries.append(points)

  grid = buildGrid(entries)
  # print(grid)

  print("Part 1: %s" % (part1(grid),))
  print("Part 2: %s" % (part2(grid),))

if __name__ == '__main__':
  main(sys.argv[1])
