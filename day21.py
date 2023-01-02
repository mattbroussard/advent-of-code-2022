# 12/21/2022 (solving on 1/1/2023)
# https://adventofcode.com/2022/day/21

import sys
import re

operatorFuncs = {
  "+": lambda a, b: a + b,
  "-": lambda a, b: a - b,
  "/": lambda a, b: int(a / b),
  "*": lambda a, b: a * b
}

def evaluateKey(exprs, key):
  if key not in exprs:
    raise Exception("unknown key %s" % key)

  rhs = exprs[key]
  if type(rhs) == int:
    return rhs

  op1, operator, op2 = rhs
  operatorFn = operatorFuncs[operator]
  return operatorFn(evaluateKey(exprs, op1), evaluateKey(exprs, op2))

def part1(exprs):
  return evaluateKey(exprs, "root")

FREE_VAR = "__FREE_VARIABLE_SENTINEL__"

class ExprNode(object):
  op1 = None # ExprNode
  op2 = None # ExprNode
  operator = None # str
  containsFreeVar = False
  origName = None # str

  def __init__(self, op1, operator, op2, origName):
    self.op1 = op1
    self.op2 = op2
    self.operator = operator
    self.containsFreeVar = \
      op1 == FREE_VAR or \
      op2 == FREE_VAR or \
      (type(op1) == type(self) and op1.containsFreeVar) or \
      (type(op2) == type(self) and op2.containsFreeVar)
    self.origName = origName

  def evaluate(self):
    if self.containsFreeVar:
      raise Exception("cannot evaluate with free var")

    opFn = operatorFuncs[self.operator]
    op1 = self.op1 if type(self.op1) == int else self.op1.evaluate()
    op2 = self.op2 if type(self.op2) == int else self.op2.evaluate()
    return opFn(op1, op2)

  def __str__(self):
    return "(%s %s %s)" % (self.op1, self.operator, self.op2)

def buildTree(exprs, rootName, freeName = "humn"):
  if rootName == freeName:
    return FREE_VAR

  rhs = exprs[rootName]
  if type(rhs) == int:
    return rhs

  op1, operator, op2 = rhs
  return ExprNode(buildTree(exprs, op1, freeName), operator, buildTree(exprs, op2, freeName), rootName)

def part2(exprs):
  leftName, _, rightName = exprs["root"]

  left = buildTree(exprs, leftName)
  right = buildTree(exprs, rightName)
  assert not (left.containsFreeVar and right.containsFreeVar)

  # for simplicity, force free variable to the left side
  if right.containsFreeVar:
    left, right = right, left

  iterationCount = 0
  while left != FREE_VAR:
    iterationCount += 1
    freeIsOp1 = left.op1 == FREE_VAR or (type(left.op1) == ExprNode and left.op1.containsFreeVar)
    freeOp = left.op1 if freeIsOp1 else left.op2
    staticOp = left.op2 if freeIsOp1 else left.op1
    staticOp = staticOp.evaluate() if type(staticOp) == ExprNode else staticOp
    operator = left.operator
    newNodeMemo = "inverted %s" % left.origName

    if operator == "+":
      left = freeOp
      right = ExprNode(right, "-", staticOp, newNodeMemo)
    elif operator == "-":
      if freeIsOp1:
        left = freeOp
        right = ExprNode(right, "+", staticOp, newNodeMemo)
      else:
        # note: originally this made left into "0 - freeOp" and right into "right - staticOp",
        # but that results in an infinite loop because that expression will fall into this same
        # branch in the next iteration
        left = freeOp
        right = ExprNode(staticOp, "-", right, newNodeMemo)
    elif operator == "*":
      left = freeOp
      right = ExprNode(right, "/", staticOp, newNodeMemo)
    elif operator == "/":
      if freeIsOp1:
        left = freeOp
        right = ExprNode(right, "*", staticOp, newNodeMemo)
      else:
        left = freeOp
        right = ExprNode(staticOp, "/", right, newNodeMemo)
    else:
      raise Exception("unknown operator")

    right = right.evaluate() if type(right) == ExprNode else right

  return right

def main(fname):
  pattern = re.compile("([a-z]+): (\\d+|([a-z]+) ([+*/-]) ([a-z]+))")
  exprs = {}
  
  with open(fname, 'r') as f:
    for line in f:
      matches = pattern.match(line)
      if matches:
        lhs = matches.group(1)
        isLiteral = matches.group(3) is None
        if isLiteral:
          rhs = matches.group(2)
          exprs[lhs] = int(rhs)
        else:
          op1, operator, op2 = matches.group(3, 4, 5)
          exprs[lhs] = (op1, operator, op2)

  print("Part 1: %s" % (part1(exprs),))
  print("Part 2: %s" % (part2(exprs),))

if __name__ == '__main__':
  main(sys.argv[1])
