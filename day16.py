# 12/16/2022 (solving on 12/24)
# https://adventofcode.com/2022/day/16

import sys
# from heapq import heappush, heappop
from collections import deque
from functools import cache
import re

# def part1_old(edges, rates, start = "AA", maxTime = 30):
#   # state format: (- pressure relieved, time elapsed, current pos, open valves)
#   queue = [(0, 0, start, [])]

#   bestRelief = 0

#   while len(queue) > 0:
#     pressure, time, pos, path = heappop(queue)
#     print("visiting %s at time %s: pressure=%d, path=%s, best=%d, len(queue)=%d" % (pos, time, pressure, path, bestRelief, len(queue)))

#     if time == maxTime:
#       bestRelief = max(bestRelief, -pressure)
#       continue
#     elif time > maxTime:
#       raise Exception("time > maxTime, should not be possible")

#     # open current valve
#     if pos not in path and rates[pos] > 0:
#       newRelief = rates[pos] * (maxTime - time - 1)
#       heappush(queue, (pressure - newRelief, time + 1, pos, path + [pos]))

#     # visit adjacent valves
#     for neighbor in edges[pos]:
#       heappush(queue, (pressure, time + 1, neighbor, path + [pos]))

#     # wait remaining time
#     heappush(queue, (pressure, maxTime, pos, path))

#   return bestRelief

def bfsPathFind(edges, src, dest):
  queue = deque([(src,)])
  visited = set([src])

  while len(queue) > 0:
    path = queue.popleft()
    cur = path[-1]
    if cur == dest:
      return path

    for neighbor in edges[cur]:
      if neighbor not in visited:
        visited.add(neighbor)
        queue.append(path + (neighbor,))

  return None

def part1(edges, rates, start = "AA", maxTime = 30):
  total = 0
  time = 0

  relevantValves = [k for k, v in rates.items() if v > 0]
  opened = set()

  cheat = deque(["DD","BB","JJ","HH","EE","CC"])

  cur = start
  while time < maxTime and len(opened) < len(relevantValves):
    # find paths from current position to all unopened valves
    paths = {dest: len(bfsPathFind(edges, cur, dest)) - 1 for dest in relevantValves if dest not in opened}
    potentials = {dest: (maxTime - (time + paths[dest] + 1)) * rates[dest] for dest in paths.keys()}

    print("potentials: %s" % (potentials,))

    bestNext = cheat.popleft() # max(potentials.keys(), key=lambda dest: potentials[dest])

    # best option would exceed time to get to it and open, so we're done
    if potentials[bestNext] <= 0:
      break

    print("time %d @ %s: %d steps (%s) to %s, opening it, adding %d (new total %d)" % (time, cur, paths[bestNext], bfsPathFind(edges, cur, bestNext), bestNext, potentials[bestNext], total + potentials[bestNext]))

    cur = bestNext
    opened.add(bestNext)
    time += paths[bestNext] + 1
    total += potentials[bestNext]

  print("after loop, time=%d, unopened=%s" % (time, set(relevantValves) - opened))

  return total

def main(fname):
  lineRe = re.compile("Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? ([A-Z, ]+)+")
  edges = {}
  rates = {}

  with open(fname, 'r') as f:
    for line in f:
      matches = lineRe.match(line)
      if not matches:
        continue

      src = matches.group(1)
      valveRate = int(matches.group(2))
      dests = matches.group(3).split(", ")

      edges[src] = dests
      rates[src] = valveRate

  print("Part 1: %s" % (part1(edges, rates),))
  # print("Part 2: %s" % (part2(grid),))

if __name__ == '__main__':
  main(sys.argv[1])
