# https://adventofcode.com/2022/day/7
# Part 1


text = open("input.txt", "r")
lines = text.read().split("\n")

paths = {"/": []}
path = "/"

for x in range(0, len(lines)-1):
    #print("Current path is: " + path)
    if lines[x] == "$ cd /":
        continue

    line = lines[x].split(" ")

    if line[1] == "cd":
        if line[2] == "..":
            parts = path.rsplit("/", 2) 
            #print(parts)
            path = parts[0] + "/"
            #print("Going up to: " + path)
        else:
            path = path + line[2] + "/"
            #print("Opening: " + path)
            paths[path] = []

    if lines[x] == "$ ls":
        # directory = lines[x - 1].split(" ")[2]
        for y in range(x+1, len(lines)-1):
            if lines[y][0] == "$":
                break
            else:
                sub_line = lines[y].split(" ")
                if sub_line[0] == "dir":
                    full_path = path + sub_line[1] + "/"
                    paths[path].append(full_path)
                    paths[full_path] = []
                else:
                    paths[path].append(int(sub_line[0]))

has_string = []
no_string = []
for p in paths:
    flag = 0
    for i in paths[p]:
        if type(i) == str:
            has_string.append(p)
            flag += 1
            break
    if flag == 0:
        no_string.append(p)

while len(has_string) > 0:
    for x in has_string:

        # find each sub-directory that is complete (in no_string)
        for i in paths[x]:
            if i in no_string:
                # add each item that is in that array, and remove the sub-directory
                for j in paths[i]:
                    #print("Adding " + str(j) + " to " + x)
                    paths[x].append(j)
                paths[x].remove(i)

        # check if x is now totally integers and switch it if so
        flag = 0
        for i in paths[x]:
            if type(i) == str:
                flag += 1
                break
        if flag == 0:
            #print(x + " is all integers")
            no_string.append(x)
            # while loop will stop once everything is integers only
            has_string.remove(x)
            #print("Directories to clear: " + str(len(has_string)))

total = 0
for p in paths:
    s = 0
    for f in paths[p]:
        s += f
    if s <= 100000:
        total += s

print(total)

# Part 2
# Total disk space = 70,000,000
# Currently used = ? --> 46,592,386
# Target available = 30,000,000
# Current free = ? --> 23,407,614
# Remaining to free up = ? --> 6,592,386

files = []
for line in lines:
    sub = line.split(" ")
    if sub[0].isdigit():
        files.append(int(sub[0]))

print(sum(files))

total_free = 70000000 - sum(files)
print(total_free)
to_free = 30000000 - total_free
print(to_free)

path_totals = {}
for p in paths:
    path_totals[p] = sum(paths[p])
print(path_totals)

big_enough = []
for p in path_totals:
    if path_totals[p] >= to_free:
        big_enough.append(path_totals[p])
print(big_enough)
print(min(big_enough))
