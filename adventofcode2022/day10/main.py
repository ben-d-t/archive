# https://adventofcode.com/2022/day/10
# Part 1

text = open("input.txt", "r")
lines = text.read().split("\n")
lines.remove(lines[-1])
print(lines)

# Record the value of register X *during* each cycle in an array
X = 1
cycles = {}
cycle = 1

for line in lines:
    cycles[cycle] = X # record the value of X during (at the start of) each cycle

    if line == "noop":
        #print("This line is noop")
        cycle += 1

    else:
        value = int(line.split(" ")[1])
        #print(value)

        cycle += 1
        cycles[cycle] = X
        cycle += 1
        cycles[cycle] = X
        X += value
print(cycles)
print(len(cycles))

strength = 0
for i in range (20, 221, 40):
    strength += i*cycles[i]
    #print(i)
print(strength)

# Part 2
# Loop through the dictionary in key order
# Draw the . or the # depending on the value of the key value into an... array I guess
# Make one long array and hten split it on the 20s

pixels = ""

for k in range(1, 241):
    sprite = [cycles[k]-1, cycles[k], cycles[k]+1]
    #print(str(k) + ": " + str(sprite))

    if (k-1) % 40 in sprite:
        pixels += "#"
        print("Cycle " + str(k) + " at index " + str(k-1) + " is in: " + str(sprite))
    else:
        pixels += "."
print(pixels)


for i in range(40, 241, 40):
    print(pixels[i-40:i])

# WTF is going wrong??
# Well... huh, in my dictionary 40, 41 are both -1 but I have a hashtag drawn at 40... why would that be?

# For k = 40, 80, 120, 160 ... I need to check if sprite covers 40, which is NOT k mod 40
# for k = 1, 41, 81, 121, 161... I need to check if sprite covers 1, which is k mod 40
# for k = 5, 45, 85, 125, 165... I need to check if sprite covers 5, which is k mod 40
# OK... my problem is that the pixels are actually numbered 0 to 39, even though the cycles are 1 through 240
# And the register X value is based on that 0 to 39 indexing. So when it's at -1, it actually SHOULD tag, via -2/-1/0, a pixel at 1/41/81 etc...
# There it is -- FJUBULKZ oops -- oh R no tK