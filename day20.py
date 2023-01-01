# 12/20/2022 (solving on 12/31)
# https://adventofcode.com/2022/day/20

import sys

class Node(object):
  value = None
  left = None
  right = None
  parent = None
  leavesContained = 0
  def __init__(self, value = None):
    if value is not None:
      self.value = value
      self.leavesContained = 1

  def remove(self):
    if self.value is None:
      raise Exception("cannot remove non-leaf")

    p = self.parent
    isRight = p.right == self

    if isRight:
      p.right = None
    else:
      p.left = None

    while p is not None:
      if p.left is not None and p.left.leavesContained == 0:
        p.left = None
      if p.right is not None and p.right.leavesContained == 0:
        p.right = None

      p.leavesContained -= 1
      p = p.parent

    self.parent = None
    return self

  def index(self):
    if self.value is None:
      raise Exception("cannot index non-leaf")

    countLeft = 0

    cur = self
    while cur.parent is not None:
      isRight = cur.parent.right == cur
      if isRight:
        left = cur.parent.left
        if left is not None:
          countLeft += left.leavesContained
      cur = cur.parent

    return countLeft

  def insertAtIdx(self, node, idx):
    # print("before insert %d at %d:" % (node.value, idx))
    # self.debugPrint()

    needSwap = False
    if idx == 0:
      needSwap = True
      idx = 1
    nodeBefore = self.nodeAtIndex(idx - 1)
    # print("inserting %d at idx=%d; nodeBefore: %d (idx %d)" % (node.value, idx, nodeBefore.value, nodeBefore.index()))

    oldParent = nodeBefore.parent
    isRight = oldParent.right == nodeBefore

    newNode = Node()
    newNode.leavesContained = 2
    newNode.left = nodeBefore
    nodeBefore.parent = newNode
    newNode.right = node
    node.parent = newNode

    if needSwap:
      tmp = newNode.left
      newNode.left = newNode.right
      newNode.right = tmp

    if isRight:
      oldParent.right = newNode
    else:
      oldParent.left = newNode
    newNode.parent = oldParent

    while oldParent is not None:
      oldParent.leavesContained += 1
      oldParent = oldParent.parent

  def nodeAtIndex(self, idx):
    # print("(at %s): nodeAtIndex:%d" % (self.nodeType(), idx))
    if self.value is not None and idx == 0:
      return self

    leftLeaves = self.left.leavesContained if self.left is not None else 0
    rightLeaves = self.leavesContained - leftLeaves
    # print("totalLeaves:%d leftLeaves:%d rightLeaves:%d" % (self.leavesContained, leftLeaves, rightLeaves))

    if idx >= leftLeaves:
      # print("...recursive call into right")
      return self.right.nodeAtIndex(idx - leftLeaves)
    else:
      # print("...recursive call into left")
      return self.left.nodeAtIndex(idx)

  def leafNodes(self):
    if self.value is not None:
      yield self
      return

    if self.left is not None:
      for node in self.left.leafNodes():
        yield node
    if self.right is not None:
      for node in self.right.leafNodes():
        yield node

  def nodeType(self):
    return "root" if self.parent is None else "leaf" if self.value is not None else "node"

  def debugPrint(self, indent = 0):
    ws = "  " * indent
    print("%s- %s (value=%s, leavesContained=%s)" % (ws, self.nodeType(), self.value, self.leavesContained))

    if self.left is None:
      if self.value is None:
        print("%s  - left is None" % ws)
    else:
      self.left.debugPrint(indent + 1)

    if self.right is None:
      if self.value is None:
        print("%s  - right is None" % ws)
    else:
      self.right.debugPrint(indent + 1)

def buildTree(numbers):
  if len(numbers) == 0:
    return None
  elif len(numbers) == 1:
    return Node(numbers[0])
  else:
    midpoint = int(len(numbers) / 2)
    node = Node()
    node.leavesContained = len(numbers)
    node.left = buildTree(numbers[:midpoint])
    node.left.parent = node
    node.right = buildTree(numbers[midpoint:])
    node.right.parent = node
    return node

def treeTest():
  numbers = list(range(10))
  root = buildTree(numbers)
  # root.debugPrint()

  origOrderedNodes = list(root.leafNodes())
  iterTest = [n.value for n in origOrderedNodes]
  assert len(origOrderedNodes) == len(numbers)
  assert iterTest == numbers

  for i in range(len(numbers)):
    node = root.nodeAtIndex(i)
    assert node.index() == i
    assert node == origOrderedNodes[i]
    assert node.value == i

  numCopy = list(numbers)
  for i in range(0, len(numbers)*2 + 2, 2):
    node = Node(100 + i)
    numCopy.insert(i, node.value)
    root.insertAtIdx(node, i)

    values = [n.value for n in root.leafNodes()]
    assert values == numCopy

    insertedIndex = node.index()
    assert insertedIndex == i, "expected insertedIndex=%d, actually %d" % (i, insertedIndex)

  for i in range(len(numbers)*2, -2, -2):
    node = root.nodeAtIndex(i)
    node.remove()
  values = [n.value for n in root.leafNodes()]
  assert values == numbers
  root.debugPrint()

def mix(root, origOrderedNodes):
  # print(", ".join(str(n.value) for n in root.leafNodes()))

  for node in origOrderedNodes:
    index = node.index()
    newIndex = (index + node.value) % (len(origOrderedNodes) - 1)

    if index == newIndex:
      # print("%d (at %d) does not move" % (node.value, index))
      continue

    node.remove()
    root.insertAtIdx(node, newIndex)

    prev = root.nodeAtIndex((newIndex - 1 + len(origOrderedNodes)) % len(origOrderedNodes)).value
    next = root.nodeAtIndex((newIndex + 1) % len(origOrderedNodes)).value
    # print("%d moves from %d to %d (btw %d and %d)" % (node.value, index, newIndex, prev, next))
    # print(", ".join(str(n.value) for n in root.leafNodes()))

def getResult(numbers, root, origOrderedNodes):
  zeroNode = origOrderedNodes[numbers.index(0)]
  zeroIndex = zeroNode.index()
  coordIndexes = [(zeroIndex + delta) % len(numbers) for delta in [1000, 2000, 3000]]
  coordValues = [root.nodeAtIndex(idx).value for idx in coordIndexes]
  return sum(coordValues)


def part1(numbers):
  root = buildTree(numbers)
  origOrderedNodes = list(root.leafNodes())

  mix(root, origOrderedNodes)

  return getResult(numbers, root, origOrderedNodes)

def part2(numbers):
  numbers = [n * 811589153 for n in numbers]
  root = buildTree(numbers)
  origOrderedNodes = list(root.leafNodes())

  for roundIdx in range(10):
    mix(root, origOrderedNodes)

  return getResult(numbers, root, origOrderedNodes)

def main(fname):
  numbers = []
  with open(fname, 'r') as f:
    for line in f:
      numbers.append(int(line))

  # treeTest()
  print("Part 1: %s" % (part1(numbers),))
  print("Part 2: %s" % (part2(numbers),))

if __name__ == '__main__':
  main(sys.argv[1])
