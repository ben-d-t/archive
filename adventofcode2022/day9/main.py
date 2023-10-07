# https://adventofcode.com/2022/day/9
# Part 1

text = open("input.txt", "r")
lines = text.read().split("\n")
lines.remove(lines[-1])
#print(lines)

moves = []
for line in lines:
    move = line.split(" ")
    moves.append(move)
#print(moves)

T_positions = []
H = [0, 0]
T = [0, 0]

for move in moves:
    direction = move[0]
    steps = int(move[1])
    for x in range(1, steps+1):

        # change H position 1 step based on the direction
        if direction == "R":
            H[0] += 1
        elif direction == "L":
            H[0] -= 1
        elif direction == "U":
            H[1] += 1
        elif direction == "D":
            H[1] -= 1

        # check whether T needs to move
        if H == T: # if T is under H, do nothing
            pass
        elif H[0] == T[0] and abs(H[1]-T[1]) == 1 or H[1] == T[1] and abs(H[0]-T[0]) == 1: # if T is next to H, do nothing
            pass
        elif abs(H[1]-T[1]) == 1 and abs(H[0]-T[0]) == 1: # if T is diagonal 1 to H, do nothing
            pass
        else: # Move T to the right position
            if H[0] == T[0]: # if same x, that means 2 away in y direction so move that way
                if abs(H[1]-T[1]) > 2:
                    print("ERROR H moving too fast!")
                if H[1] > T[1]:
                    T[1] += 1
                elif H[1] < T[1]:
                    T[1] -= 1
            elif H[1] == T[1]: # if same y, that means 2 away in x direction so move that way
                if abs(H[0]-T[0]) > 2:
                    print("ERROR H moving too fast! part 2")
                if H[0] > T[0]:
                    T[0] += 1
                elif H[0] < T[0]:
                    T[0] -= 1
            else: # in this case, diagonally apart, four cases there. Two moves for T
                if H[0] > T[0]:
                    T[0] += 1
                elif H[0] < T[0]:
                    T[0] -= 1
                if H[1] > T[1]:
                    T[1] += 1
                elif H[1] < T[1]:
                    T[1] -= 1

        # append T position to the set
        #print("H is now at" + str(H))
        #print("T is now at" + str(T))
        T_positions.append(str(T))

#print(T_positions)
T_set = set(T_positions)
print(len(T_set))


T9_positions = []
rope = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
move_count = 0

for move in moves:
    move_count += 1
    direction = move[0]
    steps = int(move[1])
    for x in range(1, steps+1):

        # change 1st position 1 step based on the direction
        if direction == "R":
            rope[0][0] += 1
        elif direction == "L":
            rope[0][0] -= 1
        elif direction == "U":
            rope[0][1] += 1
        elif direction == "D":
            rope[0][1] -= 1

        # now, have to loop through each of the 8 trailing pieces
        for i in range(1, len(rope)):
            #f move_count < 2:
                #print(H)
                #print(T)
            if rope[i-1] == rope[i]: # if T is under H, do nothing
                continue
            elif rope[i-1][0] == rope[i][0] and abs(rope[i-1][1]-rope[i][1]) == 1 or rope[i-1][1] == rope[i][1] and abs(rope[i-1][0]-rope[i][0]) == 1: # if T is next to H, do nothing
                continue
            elif abs(rope[i-1][1]-rope[i][1]) == 1 and abs(rope[i-1][0]-rope[i][0]) == 1: # if T is diagonal 1 to H, do nothing
                continue
            else: # Move T to the right position
                if rope[i-1][0] == rope[i][0]: # if same x, that means 2 away in y direction so move that way
                    if abs(rope[i-1][1]-rope[i][1]) > 2:
                        print("ERROR H moving too fast!")
                    if rope[i-1][1] > rope[i][1]:
                        rope[i][1] += 1
                    elif rope[i-1][1] < rope[i][1]:
                        rope[i][1] -= 1
                elif rope[i-1][1] == rope[i][1]: # if same y, that means 2 away in x direction so move that way
                    if abs(rope[i-1][0]-rope[i][0]) > 2:
                        print("ERROR H moving too fast! part 2")
                    if rope[i-1][0] > rope[i][0]:
                        rope[i][0] += 1
                    elif rope[i-1][0] < rope[i][0]:
                        rope[i][0] -= 1
                else: # in this case, diagonally apart, four cases there. Two moves for T
                    if rope[i-1][0] > rope[i][0]:
                        rope[i][0] += 1
                    elif rope[i-1][0] < rope[i][0]:
                        rope[i][0] -= 1
                    if rope[i-1][1] > rope[i][1]:
                        rope[i][1] += 1
                    elif rope[i-1][1] < rope[i][1]:
                        rope[i][1] -= 1
        # append T position to the set
        T9_positions.append(str(rope[len(rope)-1]))

#print(T9_positions)
# weird... the first one should be 0,0 for sure, based on L1 -- OK, now the first position is (0,0) but I still got 2,560? And it look right? but wait I have .append outside the for loop?
T9_set = set(T9_positions)
print(len(T9_set))

# 2560 too high :(
# My dumb ass did the code right but read it as 9 instead of 10 pieces...