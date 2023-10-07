# https://adventofcode.com/2022/day/5
# Part 1
import numpy as np

text = open("input.txt", "r")
chunks = text.read().split("\n")
#print(lines)
moveslist = chunks[chunks.index("")+1:]

piles = [[],
    ["L", "N", "W", "T", "D"],
    ["C", "P", "H"],
    ["W", "P", "H", "N", "D", "G", "M", "J"],
    ["C", "W", "S", "N", "T", "Q", "L"],
    ["P", "H", "C", "N"],
    ["T", "H", "N", "D", "M", "W", "Q", "B"],
    ["M", "B", "R", "J", "G", "S", "L"],
    ["Z", "N", "W", "G", "V", "B", "R", "T"],
    ["W", "G", "D", "N", "P", "L"]
]

piles2 = [[],
    ["L", "N", "W", "T", "D"],
    ["C", "P", "H"],
    ["W", "P", "H", "N", "D", "G", "M", "J"],
    ["C", "W", "S", "N", "T", "Q", "L"],
    ["P", "H", "C", "N"],
    ["T", "H", "N", "D", "M", "W", "Q", "B"],
    ["M", "B", "R", "J", "G", "S", "L"],
    ["Z", "N", "W", "G", "V", "B", "R", "T"],
    ["W", "G", "D", "N", "P", "L"]
]

moves = []
for m in moveslist:
    to_add = []
    move = m.split(" ")
    for i in move:
        if i.isdigit():
            to_add.append(int(i))
    moves.append(to_add)
del moves[-1]
print(moves)

for m in moves:
    for x in range(0, m[0], 1):
        crate = piles[m[1]].pop(-1)
        piles[m[2]].append(crate)
        #print("Moving " + crate + " crate from pile " + str(m[1]) + " to pile " + str(m[2]))
#print(piles)

tops = ""
for x in range(1, len(piles)):
    tops = tops + piles[x][-1]
print(tops)

#Part 2
for m in moves:
    pick = m[0]
    from_pile = m[1]
    to_pile = m[2]
    #print("Picking up " + str(pick) + " crates from-to piles " + str(from_pile) + " & " + str(to_pile))
    spot = len(piles2[from_pile]) - pick

    crates = piles2[from_pile][spot:]
    #print(piles2[from_pile])
    #print(crates)
    for c in crates:
        piles2[to_pile].append(c)
    #print(piles2[to_pile])
    for x in range(0, pick, 1):
        piles2[from_pile].pop(-1)
    #print(piles2[from_pile])

#print(piles2)
tops2 = ""
for x in range(1, len(piles2)):
    tops2 = tops2 + piles2[x][-1]
print(tops2)