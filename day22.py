# 12/22/2022 (solving on 1/2/2023)
# https://adventofcode.com/2022/day/22

import sys
import re

directionStrs = [">", "v", "<", "^"]
directionDeltas = [(1, 0), (0, 1), (-1, 0), (0, -1)]

sampleSquareSize = 4
sampleLayout = {
  # x,y position of face origin, divided by square size
  "B": (2, 1),
  "T": (0, 1),
  "N": (2, 0),
  "S": (2, 2),
  "E": (3, 2),
  "W": (1, 1),
}
sampleAdjacencies = {
  # outer tuple: key is direction facing when traversing edge
  # inner tuple: next face, direction facing on it
  "B": (("E", 1),     None,     None,     None),
  "W": (    None, ("S", 0),     None, ("N", 0)),
  "N": (("E", 2),     None, ("W", 1),  ("T", 1)),
  "E": (("N", 2), ("T", 0),     None,  ("B", 2)),
  "T": (    None, ("S", 3), ("E", 3),  ("N", 1)),
  "S": (    None, ("T", 3), ("W", 3),     None),
}
sampleFlippedEdges = [
  # edges where the sign direction of the edges are opposite (i.e. increasing vs decreasing)
  # must be named alphabetically (i.e. NT, not TN)
  "NT",
  "SW",
  "BE",
  "ST",
  "ET",
  "EN",

  # NOT the following remaining edges:
  # "NW",
]

inputSquareSize = 50
inputLayout = {
  "W": (1, 0),
  "T": (2, 0),
  "N": (1, 1),
  "B": (0, 2),
  "E": (2, 1),
  "S": (3, 0),
}
inputAdjacencies = {
  "B": (    None,     None,     None,     None),
  "T": (    None,     None,     None,     None),
  "N": (    None,     None,     None,     None),
  "S": (    None,     None,     None,     None),
  "E": (    None,     None,     None,     None),
  "W": (    None,     None,     None,     None),
}
inputFlippedEdges = []

def expandLayout(layout, squareSize):
  return {face: (x * squareSize, y * squareSize, (x+1)*squareSize, (y+1)*squareSize) for face, (x, y) in layout.items()}

def checkIfSampleOrInput(grid):
  if len(grid) < inputSquareSize:
    return sampleSquareSize, expandLayout(sampleLayout, sampleSquareSize), sampleAdjacencies, sampleFlippedEdges
  else:
    return inputSquareSize, expandLayout(inputLayout, inputSquareSize), inputAdjacencies, inputFlippedEdges

def whichFace(layout, pos):
  x, y = pos
  for face, bounds in layout.items():
    x1, y1, x2, y2 = bounds
    if x >= x1 and x < x2 and y >= y1 and y < y2:
      return face
  return None

def computePositionAlongEdge(layout, face, direction, pos):
  bounds = layout[face]
  isX = direction in [1, 3] # direction is up/down -> edge runs along x axis

  oneDimBounds = (bounds[0], bounds[2]) if isX else (bounds[1], bounds[3])
  oneDimCoord = pos[0] if isX else pos[1]

  return oneDimCoord - oneDimBounds[0]

def resolveEdgePosition(layout, face, direction, oneDimPos):
  bounds = layout[face]
  isX = direction in [1, 3] # if coming in facing down or up, will position along x axis
  isHigh = direction in [2, 3] # if facing left or up, we're on right or bottom edges and use the high end of bound for fixed axis

  edgeDimBounds = (bounds[0], bounds[2]) if isX else (bounds[1], bounds[3])
  fixedDimBounds = (bounds[1], bounds[3]) if isX else (bounds[0], bounds[2])

  coord = edgeDimBounds[0] + oneDimPos
  fixedCoord = fixedDimBounds[1] - 1 if isHigh else fixedDimBounds[0]

  ret = (coord, fixedCoord) if isX else (fixedCoord, coord)
  return ret

def p2_nextPosition(grid, src, direction):
  squareSize, layout, adjacencies, flippedEdges = checkIfSampleOrInput(grid)

  width = len(grid[0])
  height = len(grid)
  dx, dy = directionDeltas[direction]
  x, y = src
  srcFace = whichFace(layout, src)

  nx = x + dx
  ny = y + dy

  # simple case: faces are directly adjacent in the map, no need to recompute position
  if whichFace(layout, (nx, ny)) is not None:
    return (nx, ny), direction

  if adjacencies[srcFace][direction] is None:
    raise Exception("expected adjacency for direction %d(%s) from face %s" % (direction, directionStrs[direction], srcFace))

  posAlongEdge = computePositionAlongEdge(layout, srcFace, direction, src)
  # print("p2_nextPosition srcFace:%s srcPos:%s direction:%d(%s) posAlongEdge:%d" % (srcFace, src, direction, directionStrs[direction], posAlongEdge))

  # handle flipped edges
  destFace, destDir = adjacencies[srcFace][direction]
  edgeName = "".join(sorted([srcFace, destFace]))
  if edgeName in flippedEdges:
    posAlongEdge = squareSize - posAlongEdge - 1

  posAlongEdgeInDest = resolveEdgePosition(layout, destFace, destDir, posAlongEdge)

  return posAlongEdgeInDest, destDir

def part2(grid, instructions):
  return part1(grid, instructions, p2_nextPosition)

def debugEdgeTraversal(grid):
  def labels():
    while True:
      for c in range(25):
        yield chr(ord('A') + c)

  squareSize, layout, adjacencies, flippedEdges = checkIfSampleOrInput(grid)

  # remove walls for readability
  grid = [row.replace("#", ".") for row in grid]

  for face, bounds in layout.items():
    directionToEdgePositions = [
      # right edge
      [(bounds[2] - 1, y) for y in range(bounds[1], bounds[3])],
      # bottom
      [(x, bounds[3] - 1) for x in range(bounds[0], bounds[2])],
      # left
      [(bounds[0], y) for y in range(bounds[1], bounds[3])],
      # top
      [(x, bounds[1]) for x in range(bounds[0], bounds[2])],
    ]

    for direction, edgePositions in enumerate(directionToEdgePositions):
      adj = adjacencies[face][direction]
      if adj is None:
        continue

      destFace = adj[0]
      edgeName = "".join(sorted([face, destFace]))
      print("Face %s -> %s (edge %s), facing %s (dir %d):" % (face, destFace, edgeName, directionStrs[direction], direction))

      history = {}
      for srcPos, letter in zip(edgePositions, labels()):
        history[srcPos] = letter
        nextPos, nextDir = p2_nextPosition(grid, srcPos, direction)
        history[nextPos] = letter.lower()
        nextNextPos, _ = p2_nextPosition(grid, nextPos, nextDir)
        history[nextNextPos] = nextDir

      printGrid(grid, history)
      print(history)

def printGrid(grid, history):
  def characterAtPosition(pos):
    if pos in history:
      val = history[pos]
      if type(val) == int:
        return directionStrs[history[pos]]
      else:
        return str(val)[0]
    x, y = pos
    return grid[y][x]

  height = len(grid)
  width = len(grid[0])
  for y in range(height):
    print("".join(characterAtPosition((x, y)) for x in range(width)))

def p1_nextPosition(grid, src, direction):
  width = len(grid[0])
  height = len(grid)
  dx, dy = directionDeltas[direction]
  x, y = src

  cur = " "
  while cur == " ":
    x = (x + dx + width) % width
    y = (y + dy + height) % height
    cur = grid[y][x]

  return (x, y), direction

def part1(grid, instructions, nextFn = p1_nextPosition):
  pos = (grid[0].index("."), 0)
  direction = 0

  history = {}
  history[pos] = direction

  for instType, instValue in instructions:
    if instType == "rotate":
      dirDelta = 1 if instValue == "R" else -1
      direction = (direction + 4 + dirDelta) % 4
      history[pos] = direction

    elif instType == "move":
      for _ in range(instValue):
        (nx, ny), nd = nextFn(grid, pos, direction)
        if grid[ny][nx] == "#":
          break
        pos = (nx, ny)
        direction = nd
        history[pos] = direction

  # printGrid(grid, history)

  x, y = pos
  return 1000 * (y + 1) + 4 * (x + 1) + direction

def main(fname):
  grid = []
  instructions = []
  instrPattern = re.compile("\\d+|[LR]")
  
  with open(fname, 'r') as f:
    for line in f:
      matches = re.findall(instrPattern, line)
      if len(matches) > 0:
        for match in matches:
          if match in ["L", "R"]:
            instructions.append(("rotate", match))
          else:
            instructions.append(("move", int(match)))
      elif len(line.strip()) > 0:
        grid.append(line.rstrip())

  maxLen = max(len(row) for row in grid)
  for i, row in enumerate(grid):
    grid[i] = row.ljust(maxLen, " ")

  # debugEdgeTraversal(grid)
  print("Part 1: %s" % (part1(grid, instructions),))
  print("Part 2: %s" % (part2(grid, instructions),))

if __name__ == '__main__':
  main(sys.argv[1])
