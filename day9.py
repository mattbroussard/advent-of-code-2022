# 12/9/2022
# https://adventofcode.com/2022/day/9

import sys
from collections import defaultdict

directionToDelta = {
  "U": (0, 1),
  "D": (0, -1),
  "L": (-1, 0),
  "R": (1, 0)
}

diagonals = [(-1,1),(1,1),(1,-1),(-1,-1)]

def vecAdd(a, b):
  return tuple(sum(z) for z in zip(a, b))

def tooFar(a, b):
  x1, y1 = a
  x2, y2 = b
  return abs(x1-x2) > 1 or abs(y1-y2) > 1

def computeNextTailPosition(tail, head, prevHead):
  assert tooFar(tail, head)

  # in part 1, had assumed that this would always be to move into the position
  # where head just was previously:
  #   return prevHead
  #
  # but that assumption appears not to hold up in part 2. Moves are possible
  # where that strategy would move you horizontally/vertically but the correct
  # move is diagonal. See move 2, step 2 in the smaller example, repeated below:
  #
  # would have been produced by bad assumption:
  #   ......
  #   ......
  #   ....H. (H moved up)
  #   ....1.
  #   5432..
  #
  # correct:
  #   ......
  #   ......
  #   ....H.
  #   .4321.
  #   5.....

  tailX, tailY = tail
  headX, headY = head

  if tailX == headX: # same column
    direction = -1 if headY < tailY else 1
    nextTail = (tailX, tailY + direction)

    # print("same column follow")
    # printGrid([prevHead, head, tail, nextTail])
    assert not tooFar(nextTail, head)

    return nextTail

  elif tailY == headY: # same row
    direction = -1 if headX < tailX else 1
    nextTail = (tailX + direction, tailY)

    # print("same row follow")
    # printGrid([prevHead, head, tail, nextTail])
    assert not tooFar(nextTail, head)

    return nextTail

  else: # diagonal move
    # print("diagonal follow")
    for delta in diagonals:
      nextTail = vecAdd(tail, delta)
      if not tooFar(nextTail, head):
        return nextTail

  # printGrid([prevHead, head, tail])
  raise Exception("somehow none of the diagonals moved us close enough? tail:%s head:%s prevHead:%s" % (tail, head, prevHead))

def part1(moves):
  headPos = (0, 0)
  tailPos = (0, 0)
  tailVisited = set([tailPos])

  for direction, steps in moves:
    for _ in range(steps):
      oldHead = headPos
      headPos = vecAdd(headPos, directionToDelta[direction])
      if tooFar(headPos, tailPos):
        tailPos = computeNextTailPosition(tailPos, headPos, oldHead)
        tailVisited.add(tailPos)

  return len(tailVisited)

def posIndexToStr(i):
  if i == 0:
    return "H"
  elif i < 16:
    return "%x" % i
  else:
    return "#"

def boundsFromPoints(*pointLists):
  minX = 0
  minY = 0
  maxX = 0
  maxY = 0

  for pointList in pointLists:
    for pos in pointList:
      x, y = pos
      minX = min(minX, x)
      maxX = max(maxX, x)
      minY = min(minY, y)
      maxY = max(maxY, y)

  bounds = ((minX, minY), (maxX, maxY))
  return bounds

def printOcclusions(positions):
  posToId = defaultdict(list)
  for i, pos in enumerate(positions):
    posToId[pos].append(posIndexToStr(i))
  posToId[(0, 0)].append("s")

  for names in posToId.values():
    if len(names) > 1:
      front = names[0]
      others = names[1:]
      print("%s covers %s" % (front, ", ".join(others)))

def printGrid(positions, bounds = None):
  if bounds is None:
    bounds = boundsFromPoints(positions)

  def posToString(pos):
    for i, knotPos in enumerate(positions):
      if knotPos == pos:
        return posIndexToStr(i)
    if pos == (0, 0):
      return "s"
    return "."

  (minX, minY), (maxX, maxY) = bounds
  text = "\n".join("".join(posToString((x, y)) for x in range(minX, maxX+1)) for y in range(maxY, minY-1, -1))

  print(text)
  printOcclusions(positions)
  print("")

def printHistory(history, labels = []):
  bounds = boundsFromPoints(*history)
  for step, label in zip(history, labels):
    if label is not None:
      print("== %s ==\n" % label)
    printGrid(step, bounds)

def part2(moves, nKnots = 10):
  positions = [(0, 0)] * nKnots
  tailVisited = set([positions[-1]])

  history = [list(positions)]

  for direction, steps in moves:
    for _ in range(steps):
      prevPositions = list(positions)
      for i in range(nKnots):
        # head moves according to instructions
        if i == 0:
          positions[i] = vecAdd(positions[i], directionToDelta[direction])

        # all other move according to rules on previous move
        else:
          if tooFar(positions[i], positions[i-1]):
            positions[i] = computeNextTailPosition(positions[i], positions[i-1], prevPositions[i-1])

      tailVisited.add(positions[-1])
      history.append(list(positions))

  # labels = ["Initial State"] + [
  #   "Move %d/%d: %s (step %d/%d)" % (moveIdx+1, len(moves), direction, stepIdx+1, steps)
  #   for moveIdx, (direction, steps) in enumerate(moves)
  #   for stepIdx in range(steps)
  # ]
  # printHistory(history, labels)

  bounds = boundsFromPoints(*history)
  # print("tailVisited locations:")
  # printGrid(tailVisited, bounds)

  return len(tailVisited)

def main(fname):
  moves = []
  with open(fname, 'r') as f:
    for line in f:
      direction, num = line.strip().split(" ")
      moves.append((direction, int(num)))

  print("Part 1: %s" % (part1(moves),))
  print("Part 2: %s" % (part2(moves),))

if __name__ == '__main__':
  main(sys.argv[1])
