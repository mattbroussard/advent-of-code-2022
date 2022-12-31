# 12/17/2022 (solving on 12/30)
# https://adventofcode.com/2022/day/17

import sys
import re

class Shape(object):
  points = None # set((x, y))
  width = 0
  height = 0
  def __init__(self, strRep):
    self.points = set()

    ws = re.compile("\\s")
    rows = [re.sub(ws, "", row) for row in strRep.strip().split("\n")]
    self.height = len(rows)
    self.width = len(rows[0])

    for y, row in enumerate(rows):
      for x, c in enumerate(row):
        if c == "#":
          pt = (x, self.height - y - 1)
          self.points.add(pt)

class Obj(object):
  shape = None
  pos = None
  finalized = False
  def __init__(self, shape, pos):
    self.shape = shape
    self.pos = pos

  def points(self):
    ox, oy = self.pos
    for x, y in self.shape.points:
      yield (ox + x, oy + y)

class Board(object):
  objs = None # Obj[]
  points = None # map: (x, y) -> Obj
  def __init__(self):
    self.objs = []
    self.points = {}

  def getDefaultInsertionPositionForShape(self, shape):
    return (2, self.maxY() + 4)

  def addObjectWithShape(self, shape, pos=None):
    if pos is None:
      pos = self.getDefaultInsertionPositionForShape(shape)

    obj = Obj(shape, pos)
    if self.wouldCollide(obj):
      raise Exception("cannot insert object, it would collide -- bad pos?")

    self.objs.append(obj)
    for pt in obj.points():
      self.points[pt] = obj

    return obj

  def lastObject(self):
    return self.objs[-1]

  # assumption: object not already in points map
  def wouldCollide(self, obj):
    for pt in obj.points():
      x, y = pt
      if x < 0 or x >= 7:
        return True

      if y < 0:
        return True

      if pt in self.points:
        return True

    return False

  # assumption: object already in points map
  # returns: true if successfully moved, false if would collide
  def moveObject(self, obj, delta, dryRun = False):
    # first, remove points from points map
    for pt in obj.points():
      del self.points[pt]

    # then, move object
    x, y = obj.pos
    dx, dy = delta
    obj.pos = (x + dx, y + dy)

    # check if would collide
    collides = self.wouldCollide(obj)

    # if collides, unmove
    if collides:
      obj.pos = (x, y)

    # re-add to points map before returning
    for pt in obj.points():
      self.points[pt] = obj

    return (not collides)

  def maxY(self):
    if len(self.points) == 0:
      return -1

    pt = max(self.points.keys(), key=lambda pt: pt[1])
    return pt[1]

  def charAtPoint(self, pos):
    if pos not in self.points:
      return "."

    obj = self.points[pos]
    if obj.finalized:
      return "#"

    return "@"

  def __str__(self):
    ret = "\n"
    for y in range(self.maxY(), -1, -1):
      line = "".join(self.charAtPoint((x, y)) for x in range(7))
      ret += "|%s|\n" % line

    ret += "+-------+\n"

    return ret


shapes = [
  Shape("""
    ####
  """),
  Shape("""
    .#.
    ###
    .#.
  """),
  Shape("""
    ..#
    ..#
    ###
  """),
  Shape("""
    #
    #
    #
    #
  """),
  Shape("""
    ##
    ##
  """)
]

def part1(jets, maxObjects=2022):
  board = Board()

  jetIdx = 0
  for objIndex in range(maxObjects):
    shape = shapes[objIndex % len(shapes)]

    # first, insert object
    obj = board.addObjectWithShape(shape)
    # print("Object %d: %s" % (objIndex+1, board))

    # then, follow jets/gravity until object settled
    stepIdx = 0
    while True:
      # horiz movement from jet
      if stepIdx % 2 == 0:
        jet = jets[jetIdx % len(jets)]
        jetIdx += 1
        delta = (-1 if jet == "<" else 1, 0)
        board.moveObject(obj, delta)

      # vert movement from gravity
      else:
        delta = (0, -1)
        moved = board.moveObject(obj, delta)
        if not moved:
          obj.finalized = True

      # print("(Object %d) After step %d (%s; jetIdx=%d; lastJet=%s): %s" % (objIndex+1, stepIdx+1, "jet" if stepIdx % 2 == 0 else "gravity", jetIdx % len(jets), jets[(jetIdx-1) % len(jets)], board))

      stepIdx += 1
      if obj.finalized:
        break

  return board.maxY() + 1

def part2(jets):
  # one trillion rocks
  return part1(jets, maxObjects=1000000000000)

def main(fname):
  with open(fname, 'r') as f:
    jets = list(f.read().strip())

  print("Part 1: %s" % (part1(jets),))
  print("Part 2: %s" % (part2(jets),))

if __name__ == '__main__':
  main(sys.argv[1])
