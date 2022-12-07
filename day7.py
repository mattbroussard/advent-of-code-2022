# 12/7/2022
# https://adventofcode.com/2022/day/7

import sys
from functools import reduce

class Node(object):
  size = 0
  isDir = False
  name = None
  parent = None
  children = None
  def __init__(self):
    self.children = {}
    pass

  def __str__(self):
    return self.toStringWithIndent(0)

  def toStringWithIndent(self, indent):
    childStrings = "".join(child.toStringWithIndent(indent + 1) for child in self.children.values())
    indentStr = indent * "  "
    kind = "dir" if self.isDir else "file"
    return "%s- %s (%s, size=%d)\n%s" % (indentStr, self.name, kind, self.size, childStrings)

# returns sum of a node's directories (including self) that are less than 100000
def part1(root):
  total = 0

  if root.size <= 100000:
    total += root.size
  for child in root.children.values():
    if child.isDir:
      total += part1(child)

  return total

# https://stackoverflow.com/a/2082107/622371
def flatten(arr):
  return reduce(list.__add__, arr, [])

def getAllDirs(root):
  return [root] + flatten(getAllDirs(child) for child in root.children.values() if child.isDir)

def part2(root):
  avail = 70000000 - root.size
  needed = 30000000 - avail

  allDirs = getAllDirs(root)
  allDirs.sort(key=lambda node: node.size)
  for d in allDirs:
    if d.size >= needed:
      return d.size

  return -1

def main(fname):
  with open(fname, 'r') as f:
    text = f.read()
  entries = [s.strip() for s in text.split("$")]

  root = Node()
  root.name = "/"
  root.isDir = True
  cur = root

  for entry in entries:
    # print("(cwd=%s) Parsing entry: %s" % (cur.name, entry))

    lines = entry.split("\n")
    cmd = lines[0]

    if cmd.startswith("cd"):
      arg = lines[0].split(" ")[-1]
      if arg == "/":
        cur = root
      elif arg == "..":
        cur = cur.parent
      else:
        cur = cur.children[arg]
        if cur is None:
          raise Exception("cd into nonexistent directory")

    if cmd.startswith("ls"):
      if len(cur.children) != 0:
        print(len(cur.children))
        import pdb; pdb.set_trace()
        raise Exception("second ls for same node %s" % cur.name)

      for lsLine in lines[1:]:
        typeOrSize, name = lsLine.split(" ")

        # create new node
        node = Node()
        node.name = name
        node.isDir = typeOrSize == "dir"
        node.parent = cur
        cur.children[name] = node

        # update node size & parent directories' size
        if not node.isDir:
          p = node
          size = int(typeOrSize)
          while p is not None:
            p.size += size
            p = p.parent

  # print(root)

  print("Part 1: %s" % (part1(root),))
  print("Part 2: %s" % (part2(root),))

if __name__ == '__main__':
  main(sys.argv[1])
