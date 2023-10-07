# https://adventofcode.com/2022/day/6
# Part 1

text = open("input.txt", "r")
signal = text.read()
# print(signal)

packet = ["w", "w", "w", "w"]
count = 0
for letter in signal:
    # pop the first
    packet.pop(0)
    # add the last
    packet.append(letter)
    #print(packet)
    # check if all are different, and break if so
    if len(packet) == len(set(packet)):
        count += 1
        break
    else:
        count += 1

print(count)

#Part 2

packet2 = ["s", "s", "s", "s", "s", "s", "s", "s", "s", "s", "s", "s", "s", "s"]
count2 = 0
for letter in signal:
    # pop the first
    packet2.pop(0)
    # add the last
    packet2.append(letter)
    #print(packet)
    # check if all are different, and break if so
    if len(packet2) == len(set(packet2)):
        count2 += 1
        break
    else:
        count2 += 1
print(count2)