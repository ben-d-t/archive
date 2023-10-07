# https://adventofcode.com/2022/day/1
# Part 1

# https://www.tutorialkart.com/python/python-read-file-as-string/
text_file = open("input.txt", "r")
data = text_file.read()

# https://bobbyhadz.com/blog/python-split-string-on-newline-character
items = data.splitlines()
#print(items)

elves = []
elf = []
for i in items:
    if i != "":
        elf.append(int(i))
    else:
        elves.append(elf)
        elf = []
#print(elves)

totals = []
for elf in elves:
    count = 0
    for item in elf:
        count += item
    totals.append(count)
#print(totals)
print(max(totals))

# Part 2
first = max(totals)
totals.remove(max(totals))
second = max(totals)
totals.remove(max(totals))
third = max(totals)
print(first+second+third)
