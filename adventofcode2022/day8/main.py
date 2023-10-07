# https://adventofcode.com/2022/day/8
# Part 1
text = open("input.txt", "r")
lines = text.read().split("\n")

grid = []
for l in lines:
    row = []
    for x in l:
        row.append(int(x))
    grid.append(row)
grid.remove(grid[-1]) # remove empty array at the end
#print(grid)

count_visible = (len(grid))*2 + len(grid[0])*2 - 4 # start with full perimeter visible
print("There are: " + str(count_visible) + " trees around the edge")
print("Rows: " + str(len(grid)))
print("columns: " + str(len(grid[0])))
trees_checked = (len(grid))*2 + len(grid[0])*2 - 4
visible_trees = []

for row in range(1, 98): # skip the edges since we already counted those. range is exclusive of last value so len(grid) = 99, want to index 1 to 97
    for col in range(1, 98): # check each tree in every row, up to the edge. len(grid[row]) = 99, so will loop through to 97
        tree_height = grid[row][col]
        tree_coordinates = "(" + str(row) + ", "+ str(col)+ ")"
        #print("Checking tree at " + tree_coordinates + " of height " + str(tree_height))
        trees_checked += 1
        keep_looking = True

        # check row before:
        if keep_looking:
            count = 0
            for before_tree in range(0, col):
                if grid[row][before_tree] < tree_height:
                    count += 1
            if count == col: # For 5th column, index is 4, 4 trees to check before
                count_visible += 1
                #print("Tree is visible at: " + tree_coordinates)
                visible_trees.append(tree_coordinates)
                keep_looking = False
        # check row after:
        if keep_looking:
            count = 0
            for after_tree in range(col+1, len(grid[row])): # forgot to start 1 column after!
                if grid[row][after_tree] < tree_height:
                    count += 1
            if count == len(grid[row]) - col - 1: # tree at column 98 of 99 has to check 1 tree; length is 99, column index of tree is 97
                count_visible += 1
                #print("Tree is visible at: " + tree_coordinates)
                visible_trees.append(tree_coordinates)
                keep_looking = False
        # check column before:
        if keep_looking:
            count = 0
            for above_tree in range(0, row):
                if grid[above_tree][col] < tree_height:
                    count += 1
            if count == row: # for tree in row 5, there are 4 trees to check. index of row is 4
                count_visible += 1
                #print("Tree is visible at: " + tree_coordinates)
                visible_trees.append(tree_coordinates)
                keep_looking = False
        # check column after:
        if keep_looking:
            count = 0
            for below_tree in range(row+1, len(grid)): #AH I forgot to start 1 row below...
                if grid[below_tree][col] < tree_height:
                    count += 1
            if count == len(grid) - row - 1: # for tree in 98th row, index of 97, there is 1 tree to check. len(grid) = 99
                count_visible += 1
                #print("Tree is visible at: " + tree_coordinates)
                visible_trees.append(tree_coordinates)
                keep_looking = False
# Lesson learned... a stray "break" that you forgot to delete will getcha

print("Trees checked: " + str(trees_checked))
print(count_visible)
#print(len(visible_trees))
#print(len(set(visible_trees)))

# Part 2
scenic_scores = {}

for row in range(1, 98): # just going to assume the edges are a no-go
    for col in range(1, 98):
        tree_height = grid[row][col]
        tree_coordinates = "(" + str(row) + ", "+ str(col)+ ")"
        #print("Checking tree at " + tree_coordinates + " of height " + str(tree_height))
        trees_checked += 1

        # check row before:
        count_before = 0
        for before_tree in reversed(range(0, col)):
            if grid[row][before_tree] < tree_height:
                count_before += 1
            elif grid[row][before_tree] == tree_height:
                count_before += 1
                break
            else:
                break
        # check row after:
        count_after = 0
        for after_tree in range(col+1, len(grid[row])):
            if grid[row][after_tree] < tree_height:
                count_after += 1
            elif grid[row][after_tree] == tree_height:
                count_after += 1
                break
            else:
                break
        # check column before:
        count_above = 0
        for above_tree in reversed(range(0, row)):
            if grid[above_tree][col] < tree_height:
                count_above += 1
            elif grid[above_tree][col] == tree_height:
                count_above += 1
                break
            else:
                break
        # check column after:
        count_below = 0
        for below_tree in range(row+1, len(grid)): #AH I forgot to start 1 row below...
            if grid[below_tree][col] < tree_height:
                count_below += 1
            elif grid[below_tree][col] == tree_height:
                count_below += 1
                break
            else:
                break
        score = count_before * count_after * count_above * count_below
        print(str(score) + "is from" + str(count_before) + "/" + str(count_after) + "/" + str(count_above) + "/" + str(count_below))
        scenic_scores[tree_coordinates] = score
#print(scenic_scores)
print(max(scenic_scores.values()))