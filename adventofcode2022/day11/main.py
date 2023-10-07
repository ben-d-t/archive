# https://adventofcode.com/2022/day/11
# Part 1
import math

# Make a dictionary of the monkeys just by hand
# Or do I need to learn classes
# I guess I can just condition the rules based on which monkey is up, though that doesn't scale well... Check out Bryson's code after

# Set up Monkey class


class Monkey:
    def __init__(self, id, items, monkey_true, monkey_false):
        self.id = id
        self.items = items
        self.monkey_true = monkey_true
        self.monkey_false = monkey_false
        self.inspections = 0

    def operation(self, item):
        if self.id == 0:
            return item * 11
        elif self.id == 1:
            return item + 1
        elif self.id == 2:
            return item * item
        elif self.id == 3:
            return item + 2
        elif self.id == 4:
            return item + 6
        elif self.id == 5:
            return item + 7
        elif self.id == 6:
            return item * 7
        elif self.id == 7:
            return item + 8

    def test(self, item):
        if self.id == 0:
            return True if item % 13 == 0 else False
        elif self.id == 1:
            return True if item % 7 == 0 else False
        elif self.id == 2:
            return True if item % 3 == 0 else False
        elif self.id == 3:
            return True if item % 19 == 0 else False
        elif self.id == 4:
            return True if item % 5 == 0 else False
        elif self.id == 5:
            return True if item % 2 == 0 else False
        elif self.id == 6:
            return True if item % 11 == 0 else False
        elif self.id == 7:
            return True if item % 17 == 0 else False


# Initialize monkeys -- id, items, monkey_true, monkey_false
monkey0 = Monkey(0, [71, 56, 50, 73], 1, 7)
monkey1 = Monkey(1, [70, 89, 82], 3, 6)
monkey2 = Monkey(2, [52, 95], 5, 4)
monkey3 = Monkey(3, [94, 64, 69, 87, 70], 2, 6)
monkey4 = Monkey(4, [98, 72, 98, 53, 97, 51], 0, 5)
monkey5 = Monkey(5, [79], 7, 0)
monkey6 = Monkey(6, [77, 55, 63, 93, 66, 90, 88, 71], 2, 4)
monkey7 = Monkey(7, [54, 97, 87, 70, 59, 82, 59], 1, 3)

monkeys = {}
monkey_list = [monkey0, monkey1, monkey2, monkey3, monkey4, monkey5, monkey6, monkey7]

for m in monkey_list:
    monkeys[m.id] = m
    # monkeys[monkey0.id] = monkey0 --> monkeys[0] = monkey0
#print(monkeys)

# Then loop through the rounds, editing the monkey's inspect count etc...

# 20 rounds total // Part 2 at 10,000
rounds = 0
for r in range(0, 10000):
    rounds += 1
    print("Start of round: " + str(rounds))

    for m in range(0, 8):

        # Use dictionary to set current monkey
        monkey = monkeys[m]

        # For each item ...
        # ERROR IN HERE SOMEWHERE... something about how I'm using .pop
        # If I check this first round first monkey, it only seems to go toss two items out of the four?
        for x in range(0, len(monkey.items)):
            item = monkey.items[x]

            item = monkey.operation(item) # Do that monkey's inspection
            monkey.inspections += 1 # COUNT that it inspected an item
            #item = item // 3 # Adjust worry level
            multiplier = 13*7*3*19*5*2*11*17
            item = item % multiplier

            # Throw to the appropriate monkey
            if monkey.test(item):
                throw_to = monkey.monkey_true
                monkeys[throw_to].items.append(item) # Wondering if this ain't working
                #monkey.items.pop(0)
            else:
                throw_to = monkey.monkey_false
                monkeys[throw_to].items.append(item)
                #monkey.items.pop(0)

        monkey.items.clear()

"""    # Inspections this round only
    post_insp_count = []
    for m in range(0, 8):
        monkey = monkeys[m]
        post_insp_count.append(monkey.inspections)

    deltas = []
    for m in range(0, 8):
        delta = post_insp_count[m] - pre_insp_count[m]
        deltas.append(delta)
    print(deltas)
"""


# See which two monkeys have the highest inspect count & calculate monkey business
first = 0
second = 0
insp_counts = []

for m in monkeys:
    insp_counts.append(monkeys[m].inspections)
print(insp_counts)

first = max(insp_counts)
insp_counts.pop(insp_counts.index(first))
second = max(insp_counts)

print(first * second)

# Part 2
# Why can't I just run it 10,000 rounds?
# Oh it really would take real long hmm
# After each round... check the # of inspections, question is if that ever gets in a "loop" -- then I can break out & math it
# 3 ideas:
# (1) if it eventually hits a loop, you can find it & calculate the answer
# (2) modify the individual monkey rules to keep worry lower
# (3) some other hack that doesn't effect the rules

# 32397480048 is too high
# Right, it was modulo
# Modular arithmetic is an equivalence relation
