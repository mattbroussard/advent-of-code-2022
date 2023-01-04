# 12/25/2022 (solving on 1/3/2023)
# https://adventofcode.com/2022/day/25

import sys

def snafuToDec(s):
  d = 0
  for i in range(len(s)):
    digit = s[len(s) - i - 1]
    val = 0
    if digit == "-":
      val = -1
    elif digit == "=":
      val = -2
    else:
      val = int(digit)

    d += val * (5 ** i)
  return d

def decToSnafu(d):
  decDigits = []

  while d != 0:
    decDigits.append(d % 5)
    d = d // 5

  decDigits.append(0)
  for i in range(len(decDigits)-1):
    if decDigits[i] > 2:
      decDigits[i] -= 5
      decDigits[i+1] += 1

  if decDigits[-1] == 0:
    decDigits.pop()

  return "".join("-" if d == -1 else "=" if d == -2 else str(d) for d in reversed(decDigits))

def part1(snafuNums):
  decNums = [snafuToDec(s) for s in snafuNums]

  decSum = sum(decNums)
  print("Part 1 decimal sum: %d" % decSum)

  return decToSnafu(decSum)

def main(fname):
  snafuNums = []

  with open(fname, 'r') as f:
    for line in f:
      s = line.strip()
      if len(s) > 0:
        snafuNums.append(s)

  print("Part 1: %s" % (part1(snafuNums),))

if __name__ == '__main__':
  main(sys.argv[1])
