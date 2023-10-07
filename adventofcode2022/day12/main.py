# https://adventofcode.com/2022/day/12
# Part 1

#import random
import heapq
from typing import List, Tuple
text = open("input.txt", "r")

lines = text.read().rstrip("\n").split("\n")
grid = [list(line) for line in lines] # F me... my biggest mistake was that I added the .rstrip("\n") above but didn't remove that here... I was literally deleting the whole bottom row


# define the start & finish
starting = []
finishing = []
for row_index, rowz in enumerate(grid):
    for col_index, item in enumerate(rowz):
        if item == "S":
            starting.append(row_index)
            starting.append(col_index)
        if item == "E":
            finishing.append(row_index)
            finishing.append(col_index)
print(starting)
print(finishing)

# replace start with a and finish with z
grid[starting[0]][starting[1]] = "a"
grid[finishing[0]][finishing[1]] = "z"
#print(grid)

grid_elevations = []
for r in range(0, len(grid)):
    rw = []
    for c in range(0, len(grid[r])):
        cell = (r, c, grid[r][c])
        rw.append(cell)
    grid_elevations.append(rw)
print(grid_elevations)


# Function for dijkstra's algorithm. Thanks ChatGPT
def dijkstra(grid: List[List[Tuple[int, int, str]]], start: Tuple[int, int, str], end: Tuple[int, int, str]) -> List[Tuple[int, int, str]]:
    # Initialize the distances of all nodes to infinity
    distances = {node: float('inf') for row in grid for node in row}
    # The starting node has a distance of 0
    distances[start] = 0
    # Create a priority queue of nodes, ordered by their distances
    queue = [(0, start)]
    # Store the predecessor of each node in the path
    predecessors = {start: None}

    while queue:
        # Find the node with the minimum distance
        distance, current_node = heapq.heappop(queue)
        # Stop when we reach the end node
        if current_node == end:
            break
        #else:
            #print(current_node)
        # Consider the neighbors of the current node
        neighbors = get_neighbors(grid, current_node)
        #print(neighbors)
        # Check if there are any valid neighbors
        if any(get_cost(current_node, neighbor) < float('inf') for neighbor in neighbors):
            for neighbor in neighbors:
                # Calculate the distance to the neighbor
                cost = get_cost(current_node, neighbor)
                # If the calculated distance is lower and the move is allowed, update it
                new_distance = distance + cost
                if new_distance < distances[neighbor] and cost < float('inf'):
                    #print(distance)
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = current_node
                    # Add the neighbor to the queue
                    heapq.heappush(queue, (new_distance, neighbor))
        #print(predecessors)

    # Check if the end node was reached
    if end not in predecessors:
        return []
    else:
        # Construct the shortest path
        path = [end]
        while path[-1] != start:
            path.append(predecessors[path[-1]])
        # Reverse the path and return it
        return path[::-1]


def get_neighbors(grid: List[List[Tuple[int, int, str]]], node: Tuple[int, int, str]) -> List[Tuple[int, int, str]]:
    # Get the row and column indices of the node
    row, col, _ = node
    # Consider all adjacent cells in the grid
    neighbors = []
    for r, c in [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]:
        # Make sure the indices are valid and the cell is not blocked
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
            neighbors.append((r, c, grid[r][c][2]))
    #print("Checking neighbors at" + str(node) + " gives" + str(neighbors))
    return neighbors


def get_cost(node1: Tuple[int, int, str], node2: Tuple[int, int, str]) -> float:
    # Return the cost of moving from node1 to node2
    # Retrieve the elevations of the two cells
    elevation1 = ord(node1[2])
    elevation2 = ord(node2[2])
    # Calculate the difference in elevation
    elevation_diff = elevation2 - elevation1
    #print(elevation_diff)
    # Return the appropriate cost based on the elevation difference
    if elevation_diff > 1:
        return float('inf')
    elif elevation_diff == 1:
        return 1
    elif elevation_diff == 0:
        return 1
    else:
        return 1


grid_start = grid_elevations[20][0]
grid_finish = grid_elevations[20][36]
print(grid_start)
print(grid_finish)

route = dijkstra(grid_elevations, grid_start, grid_finish)
#print(route)
#for s in route:
   # print(s)
print(len(route)-1)

"""
route = (dijkstra(grid_elevations, grid_elevations[39][42], grid_elevations[20][36]))
print(route)
for s in route:
    print(s)
print(len(route)-1 + 20 + 43)"""
# There are 40 rows. The S is at index 20, which is the 21st row. We need 20 steps to get from there to the 40th row
# What I am so confused by that math for some reason... it takes 1 step to go from 1 to 2... 2 steps to go from 3 to 4...
# How come every time I count the screen I get 20 steps from index 20 to index 39 WTF. OK wait it's 41 rows,
# Wait what... I must have missed a row in building the grid? That would explain wtf went wrong

"""print(len(grid))
print(len(grid_elevations))
print(len(grid[0]))
print(len(grid_elevations[0]))
"""
"""
print(get_neighbors(grid_elevations, (39, 36, grid_elevations[39][36][2])))
print(get_cost((39, 36, "c"), (39, 37, "c")))

print(get_cost((0, 0, 'b'), (0, 4, 'd')))
print(get_cost((0, 0, 'b'), (0, 4, 'c')))
print(get_cost((0, 0, 'b'), (0, 4, 'b')))
print(get_cost((0, 0, 'b'), (0, 4, 'a')))

print(get_neighbors(grid_elevations, (0, 0, 'a')))
print(get_neighbors(grid_elevations, grid_elevations[0][0]))
print(get_neighbors(grid_elevations, grid_start))
print(get_neighbors(grid_elevations, grid_finish))

print(dijkstra(grid_elevations, (0, 0, "a"), (2, 3, "c")))
print(dijkstra(grid_elevations, (20, 0, "a"), (20, 36, "z")))"""
# 237 -- oh wait, that includes the start and finish. So should guess 236
# 236 still wrong :(
# Oh it's still making some illegal moves like from "w" to "y"
# So weird... it's like the algorithm refuses to go down the edge... what if I just add an extra row of "a"?
# Well, it works if I just hack it over to the farther back "c" and add it up... guess I'll try 410
# UGH no dice on 410
# Wait I counted wrong... didn't need the up one
# 409 is wrong too?? ACK

# OOH wait I made a change to make it prioritize stepping up and it landed at 329? Guess I'll try that
# 329 is wrong ACK
# But that's gotttt to be close
# Maybe 330

# Part 2
a_start = []
for r in grid_elevations:
    for n in r:
        if n[2] == "a":
            a_start.append(n)
print(a_start)

a_distances = []
for a in a_start:
    d = dijkstra(grid_elevations, a, grid_finish)
    if len(d) > 0:
        a_distances.append(len(d)-1)
print(a_distances)
print(min(a_distances))
# ACK there's no reason this had to take so long frick me up...
# Also hah when I counted by hand I was only 2 away
