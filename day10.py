# 12/10/2022
# https://adventofcode.com/2022/day/10

import sys

def part1(code, duringCycleFn = lambda cc, x: None):
  cycleCounter = 0
  xRegister = 1

  recordCycles = [20, 60, 100, 140, 180, 220]
  totalStrength = 0

  def incrementCycle():
    nonlocal cycleCounter
    nonlocal totalStrength

    cycleCounter += 1

    if cycleCounter in recordCycles:
      strength = cycleCounter * xRegister
      totalStrength += strength
      # print("cycle %d: x=%d, strength=%d, totalStrength=%d" % (cycleCounter, xRegister, strength, totalStrength))

    duringCycleFn(cycleCounter, xRegister)

  for op, operand in code:
    if op == "noop":
      incrementCycle()
    elif op == "addx":
      incrementCycle()
      incrementCycle()
      xRegister += operand
      # print("x %d -> %d at cycle %d" % (xRegister-operand, xRegister, cycleCounter))

  return totalStrength

def part2(code):
  pixels = []
  nPixels = 240

  def duringCycle(cycleCounter, xRegister):
    if len(pixels) >= nPixels:
      return

    crtPosition = len(pixels) % 40
    pixel = '#' if crtPosition in list(range(xRegister-1,xRegister+2)) else '.'
    pixels.append(pixel)

  part1(code, duringCycle)

  ret = "\n"
  for i in range(0, len(pixels), 40):
    ret += "".join(pixels[i:i+40])
    ret += "\n"

  return ret

def main(fname):
  code = []
  with open(fname, 'r') as f:
    for line in f:
      parts = line.strip().split(" ")
      op = parts[0]
      operand = None
      if parts[0] == 'addx':
        operand = int(parts[1])
      code.append((op, operand))

  print("Part 1: %s" % (part1(code),))
  print("Part 2: %s" % (part2(code),))

if __name__ == '__main__':
  main(sys.argv[1])
