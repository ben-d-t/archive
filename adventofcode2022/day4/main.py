# https://adventofcode.com/2022/day/4
# Part 1
import math
text = open("input.txt", "r")
pairs = text.read().splitlines()
pairs_split = []
for p in pairs:
    pairs_split.append(p.split(","))
#print(pairs_split)

assignments = []
for p in pairs_split:
    pair = []
    temp = []
    for a in p:
        temp.append(a.split("-"))
    for t in temp:
        for i in t:
            pair.append(int(i))
    assignments.append(pair)
#print(assignments)

count = 0
for a in assignments:
    if int(a[0]) <= int(a[2]) and int(a[1]) >= int(a[3]):
        count += 1
    elif int(a[2]) <= int(a[0]) and int(a[3]) >= int(a[1]):
        count += 1
print(count)

count2 = 0
for a in assignments:
    if a[0] < a[2] and a[1] < a[2]:
        count2 += 1
    elif a[2] < a[0] and a[3] < a[0]:
        count2 += 1
print(len(assignments) - count2)
