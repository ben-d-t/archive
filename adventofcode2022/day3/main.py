# https://adventofcode.com/2022/day/3
# Part 1
import math

text = open("input.txt", "r")
rucksacks = text.read().splitlines()

shared_items = []

# Using openai chat to figure things out instead of Google
for r in rucksacks:
    mid = math.ceil(len(r) / 2)
    shared_items.append("".join(set(r[:mid]).intersection(set(r[mid:]))))
# print(shared_items)

total = 0
for i in shared_items:
    v = 0
    lower_value = ord(i.lower()) - 96
    if i.isupper():
        v = lower_value + 26
    else:
        v = lower_value
    total += v
print(total)

# Part 2
total2 = 0
for i in range(0, len(rucksacks), 3):
    badge = "".join(set(rucksacks[i]).intersection(set(rucksacks[i + 1]), set(rucksacks[i + 2])))
    lower_value2 = ord(badge.lower()) - 96
    if badge.isupper():
        total2 += lower_value2 + 26
    else:
        total2 += lower_value2
# print(groups)
print(total2)