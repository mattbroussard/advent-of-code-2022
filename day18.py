# 12/18/2022 (solving on 12/31)
# https://adventofcode.com/2022/day/18

import sys

def neighbors(pos):
  for dim in range(3):
    for delta in [-1, 1]:
      yield pos[:dim] + (pos[dim] + delta,) + pos[dim+1:]

def part1(cubes):
  cubeSet = set(cubes)

  total = 0
  for cube in cubeSet:
    total += 6
    for n in neighbors(cube):
      if n in cubeSet:
        total -= 1

  return total

def getBounds(cubes):
  first = cubes[0]
  fx, fy, fz = first
  bounds = [[fx, fx], [fy, fy], [fz, fz]]

  for cube in cubes:
    for dim in range(3):
      bounds[dim][0] = min(bounds[dim][0], cube[dim])
      bounds[dim][1] = max(bounds[dim][1], cube[dim])

  return bounds

def buildFullSpaceSet(bounds):
  ret = set()

  for x in range(bounds[0][0], bounds[0][1] + 1):
    for y in range(bounds[1][0], bounds[1][1] + 1):
      for z in range(bounds[2][0], bounds[2][1] + 1):
        ret.add((x, y, z))

  return ret

class UnionFindNode(object):
  value = None
  parent = None
  children = None # list[node]
  def __init__(self, value):
    self.value = value
    self.children = []

class UnionFind(object):
  valueToNode = None # map: value -> node
  roots = None # list[node]

  def __init__(self):
    self.valueToNode = {}
    self.roots = []

  def add(self, val):
    if val not in self.valueToNode:
      node = UnionFindNode(val)
      self.valueToNode[val] = node
      self.roots.append(node)

  def findRoot(self, node):
    while node.parent is not None:
      node = node.parent
    return node

  def merge(self, a, b):
    ar = self.findRoot(self.valueToNode[a])
    br = self.findRoot(self.valueToNode[b])
    if ar == br:
      return

    self.roots.remove(br)
    br.parent = ar
    ar.children.append(br)

  def getAllValuesInGroup(self, root):
    ret = [root.value]
    for child in root.children:
      ret += self.getAllValuesInGroup(child)
    return ret

  def getGroups(self):
    return [self.getAllValuesInGroup(root) for root in self.roots]

def groupConnectedSets(cubes):
  cubeSet = set(cubes)

  uf = UnionFind()
  for cube in cubeSet:
    uf.add(cube)

  for cube in cubeSet:
    for n in neighbors(cube):
      if n in cubeSet:
        uf.merge(cube, n)

  return uf.getGroups()

def isOutside(group, bounds):
  for cube in group:
    for v, (vMin, vMax) in zip(cube, bounds):
      if v == vMin or v == vMax:
        return True
  return False

def part2(cubes):
  cubeSet = set(cubes)

  bounds = getBounds(cubes)
  fullSpaceSet = buildFullSpaceSet(bounds)

  emptyCubes = fullSpaceSet.difference(cubeSet)
  groupedEmpties = groupConnectedSets(emptyCubes)

  total = part1(cubes)
  for group in groupedEmpties:
    if not isOutside(group, bounds):
      total -= part1(group)

  return total

def main(fname):
  cubes = []
  with open(fname, 'r') as f:
    for line in f:
      cube = tuple([int(s) for s in line.split(",")])
      cubes.append(cube)

  print("Part 1: %s" % (part1(cubes),))
  print("Part 2: %s" % (part2(cubes),))

if __name__ == '__main__':
  main(sys.argv[1])
