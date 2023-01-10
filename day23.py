# 12/23/2022 (solving on 1/9/2023)
# https://adventofcode.com/2022/day/23

import sys
from collections import defaultdict

directions = {
  "N": (0, -1),
  "S": (0, 1),
  "E": (1, 0),
  "W": (-1, 0),
  "NE": (1, -1),
  "NW": (-1, -1),
  "SE": (1, 1),
  "SW": (-1, 1),
}

moveModes = [
  # first element: directions to check
  # second element: direction to propose moving
  (["N", "NE", "NW"], "N"),
  (["S", "SE", "SW"], "S"),
  (["W", "NW", "SW"], "W"),
  (["E", "NE", "SE"], "E"),
]

def findAll(str, sub):
  i = 0
  while i < len(str):
    found = str.find(sub, i)
    if found >= 0:
      yield found
    else:
      return
    i = found + 1

def rotateList(l, n):
  return l[n:] + l[:n]

def move(pos, direction):
  if type(direction) != tuple:
    direction = directions[direction]
  dx, dy = direction
  x, y = pos
  return (x+dx, y+dy)

def simulate(positions, maxRounds = None):
  posToElf = {pos: i for i, pos in enumerate(positions)}
  elfToPos = {i: pos for i, pos in enumerate(positions)}

  roundIdx = -1
  while True:
    roundIdx += 1
    if maxRounds is not None and roundIdx >= maxRounds:
      break

    # first, each elf checks neighbors and proposes a move
    proposals = {}
    for pos, i in posToElf.items():
      # check if no-move condition applies
      allNeighbors = [move(pos, d) for d in directions.keys()]
      nAllNeighbors = sum(int(p in posToElf) for p in allNeighbors)
      if nAllNeighbors == 0:
        proposals[i] = None
        continue

      # check neighbors to decide a move
      checks = rotateList(moveModes, roundIdx % len(moveModes))
      for checkDirs, moveDir in checks:
        neighbors = [move(pos, d) for d in checkDirs]
        nNeighbors = sum(int(p in posToElf) for p in neighbors)
        if nNeighbors == 0:
          proposals[i] = move(pos, moveDir)
          break

      # possible for none of the 4 moves to be allowed?
      if i not in proposals:
        proposals[i] = None
        # raise Exception("somehow didnt propose anything (round %d, elf %d at %s)" % (roundIdx, i, pos))

    # if no elves proposed to move, we're done
    nProposedMoves = sum(int(v is not None) for v in proposals.values())
    if nProposedMoves == 0:
      break

    # second, check proposals for conflicts
    nextPosToElf = defaultdict(list)
    for i, pos in proposals.items():
      nextPosToElf[pos].append(i)

    # execute any non-conflicting moves
    for nextPos, proposers in nextPosToElf.items():
      if len(proposers) > 1:
        continue

      i = proposers[0]
      oldPos = elfToPos[i]

      del posToElf[oldPos]
      posToElf[nextPos] = i
      elfToPos[i] = nextPos

  # print("Done after %d rounds" % roundIdx)

  minX, minY, maxX, maxY = (float('inf'), float('inf'), -1, -1)
  for x, y in posToElf.keys():
    minX = min(minX, x)
    maxX = max(maxX, x)
    minY = min(minY, y)
    maxY = max(maxY, y)

  gridArea = (maxX + 1 - minX) * (maxY + 1 - minY)
  return (gridArea - len(positions), roundIdx)

def part1(positions):
  ret, _ = simulate(positions, 10)
  return ret

def part2(positions):
  _, roundIdx = simulate(positions)
  return roundIdx + 1

def main(fname):
  positions = []

  with open(fname, 'r') as f:
    for y, line in enumerate(f):
      s = line.strip()
      if len(s) == 0:
        continue

      for x in findAll(s, '#'):
        positions.append((x, y))

  print("Part 1: %s" % (part1(positions),))
  print("Part 2: %s" % (part2(positions),))

if __name__ == '__main__':
  main(sys.argv[1])
