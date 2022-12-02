# 12/2/2022
# https://adventofcode.com/2022/day/2

import sys

definitions = {
  "A": "rock",
  "B": "paper",
  "C": "scissors",
  "X": "rock",
  "Y": "paper",
  "Z": "scissors"
}

shapeScopes = {
  "rock": 1,
  "paper": 2,
  "scissors": 3
}

winsOver = {
  "rock": "scissors",
  "paper": "rock",
  "scissors": "paper"
}

invWinsOver = {v: k for k, v in winsOver.items()}

def scoreGame(game):
  a, b = game

  if a == b:
    outcomeScore = 3 # draw
  elif a == winsOver[b]:
    outcomeScore = 6 # win
  else:
    outcomeScore = 0 # loss

  score = shapeScopes[b] + outcomeScore
  # print("Game: you:%8s other:%8s score:%d" % (b, a, score))

  return score

def part1(entries):
  games = [(definitions[colA], definitions[colB]) for colA, colB in entries]
  return sum(scoreGame(game) for game in games)

def part2(entries):
  def whichMove(other, outcomeType):
    if outcomeType == "X": # loss
      return winsOver[other]
    elif outcomeType == "Y": # draw
      return other
    elif outcomeType == "Z": # win
      return invWinsOver[other]
    else:
      raise Exception("invalid")
  games = [(definitions[colA], whichMove(definitions[colA], colB)) for colA, colB in entries]
  return sum(scoreGame(game) for game in games)

def main():
  fname = sys.argv[1]

  entries = []
  with open(fname, 'r') as f:
    for line in f:
      entries.append(tuple(line.strip().split(" ")))

  print("Part 1: %s" % (part1(entries),))
  print("Part 2: %s" % (part2(entries),))

if __name__ == '__main__':
  main()
