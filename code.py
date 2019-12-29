from operator import itemgetter


# Node class
class Node:
    def __init__(self, job_number, length):
        self.job_number = job_number
        self.length = length
        self.next = None

    def print_node(self):
        print(self.job_number, self.length)


# an always sorted LinkedList class
class LinkedList:
    def __init__(self, ascending):
        self.head = None
        self.ascending = ascending
        self.sign = 1 if ascending else -1

    # adds a node, keeping the linked list sorted
    def add(self, node):
        if self.head is None:
            self.head = node
        else:
            temp = self.head
            prev_temp = None
            while temp is not None and self.sign * temp.length < self.sign * node.length:
                prev_temp = temp
                temp = temp.next

            if prev_temp is None:
                self.head = node
            else:
                prev_temp.next = node
            node.next = temp

    def delete_node(self, node):
        temp = self.head
        if temp is not None:
            if temp == node:
                self.head = self.head.next
            else:
                while temp is not None:
                    if temp.next == node:
                        temp.next = temp.next.next
                        break
                    temp = temp.next

    def is_empty(self):
        return self.head is None

    def print_list(self):
        temp = self.head
        while temp is not None:
            temp.print_node()
            temp = temp.next


# ----------------------------------------------------------------------------------------------------------------------
# searches the database and adds the new available tasks to the linked list
def insert_available(start_time, start_index, w_index, linked_list):
    i = start_index
    while i < n:
        arrival = database[i][1]
        if arrival > start_time:
            break
        node = Node(database[i][0], database[i][w_index])
        linked_list.add(node)
        i += 1
    return i


# ----------------------------------------------------------------------------------------------------------------------
# this function checks if the other task of the given job is running on the given workstation
def is_conflicting(workstation, job_number, start_time, length):
    for i in range(start_time, start_time + length):
        if i >= len(workstation):
            break
        if workstation[i] == job_number:
            return True
    return False


# ----------------------------------------------------------------------------------------------------------------------
# the main algorithm is here
def fill_workstations(high, medium, low, ah, am, al):

    # to fit the database indexes
    high += 2
    medium += 2
    low += 2

    # available tasks LinkedLists (the tasks available on the current time, will be in these lists)
    availables = [LinkedList(ah), LinkedList(am), LinkedList(al)]

    # we also need 3 arrays for workstations (the tasks that we assign, we'll go into these arrays)
    # notice that the 0 index will contain the high priority, 1 will contain medium and 2, will contain low
    workstations = [[], [], []]

    # THE ALGORITHM:

    # filling the high priority workstation:
    count = 0
    start_index = 0
    start_time = 0
    while True:
        if start_index < n:  # if all jobs aren't already added to available list
            start_index = insert_available(start_time, start_index, high, availables[0])  # add the new ones
        linked_list = availables[0]
        if linked_list.is_empty():  # if there's no available task
            start_time += 1  # move 1 second ahead
            workstations[0].append(-1)
        else:  # if there is any task available
            # remove the task from the linked list
            head = linked_list.head
            linked_list.delete_node(head)
            # add it to workstations[0]
            for j in range(0, head.length):
                workstations[0].append(head.job_number)
            count += 1
            start_time += head.length
        if count == n:
            break

    # filling the medium priority workstation
    count = 0
    start_index = 0
    start_time = 0
    while True:
        if start_index < n:  # if all jobs aren't already added to available list
            start_index = insert_available(start_time, start_index, medium, availables[1])
        linked_list = availables[1]
        if linked_list.is_empty():  # if there's no available task
            start_time += 1  # move 1 second ahead
            workstations[1].append(-1)
        else:  # if there is any task available

            current_node = linked_list.head
            # finding the first task that has no conflicts
            while current_node is not None:
                if is_conflicting(workstations[0], current_node.job_number, start_time, current_node.length):
                    current_node = current_node.next
                else:
                    break

            # if we found one with no conflicts
            if current_node is not None:
                linked_list.delete_node(current_node)
                for j in range(0, current_node.length):
                    workstations[1].append(current_node.job_number)
                count += 1
                start_time += current_node.length

            else:  # if we didn't one with no conflicts
                start_time += 1  # move 1 second ahead
                workstations[1].append(-1)

        if count == n:
            break

    # filling the low priority workstation
    count = 0
    start_index = 0
    start_time = 0
    while True:
        if start_index < n:  # if all jobs aren't already added to available list
            start_index = insert_available(start_time, start_index, low, availables[2])
        linked_list = availables[2]
        if linked_list.is_empty():  # if there's no available task
            start_time += 1  # move 1 second ahead
            workstations[2].append(-1)
        else:  # if there is any task available

            current_node = linked_list.head
            # finding the first task that has no conflicts
            while current_node is not None:
                if is_conflicting(workstations[0], current_node.job_number, start_time, current_node.length)\
                        or is_conflicting(workstations[1], current_node.job_number, start_time, current_node.length):
                    current_node = current_node.next
                else:
                    break

            # if we found one with no conflicts
            if current_node is not None:
                linked_list.delete_node(current_node)
                for j in range(0, current_node.length):
                    workstations[2].append(current_node.job_number)
                count += 1
                start_time += current_node.length

            else:  # if we didn't one with no conflicts
                start_time += 1  # move 1 second ahead
                workstations[2].append(-1)

        if count == n:
            break

    return max([len(workstations[0]), len(workstations[1]), len(workstations[2])]), workstations


# ----------------------------------------------------------------------------------------------------------------------
# the main function solving the problem
def solve():
    # first of all we'll sort all the jobs in database based on the arrival time
    database.sort(key=itemgetter(1))

    # now there are (3! * 8) ways to solve this problem
    # we will try of all them, and return the best one

    params = [
        [0, 1, 2, False, False, False],
        [0, 1, 2, False, False, True],
        [0, 1, 2, False, True, False],
        [0, 1, 2, False, True, True],
        [0, 1, 2, True, False, False],
        [0, 1, 2, True, False, True],
        [0, 1, 2, True, True, False],
        [0, 1, 2, True, True, True],

        [0, 2, 1, False, False, False],
        [0, 2, 1, False, False, True],
        [0, 2, 1, False, True, False],
        [0, 2, 1, False, True, True],
        [0, 2, 1, True, False, False],
        [0, 2, 1, True, False, True],
        [0, 2, 1, True, True, False],
        [0, 2, 1, True, True, True],

        [1, 0, 2, False, False, False],
        [1, 0, 2, False, False, True],
        [1, 0, 2, False, True, False],
        [1, 0, 2, False, True, True],
        [1, 0, 2, True, False, False],
        [1, 0, 2, True, False, True],
        [1, 0, 2, True, True, False],
        [1, 0, 2, True, True, True],

        [1, 2, 0, False, False, False],
        [1, 2, 0, False, False, True],
        [1, 2, 0, False, True, False],
        [1, 2, 0, False, True, True],
        [1, 2, 0, True, False, False],
        [1, 2, 0, True, False, True],
        [1, 2, 0, True, True, False],
        [1, 2, 0, True, True, True],

        [2, 0, 1, False, False, False],
        [2, 0, 1, False, False, True],
        [2, 0, 1, False, True, False],
        [2, 0, 1, False, True, True],
        [2, 0, 1, True, False, False],
        [2, 0, 1, True, False, True],
        [2, 0, 1, True, True, False],
        [2, 0, 1, True, True, True],

        [2, 1, 0, False, False, False],
        [2, 1, 0, False, False, True],
        [2, 1, 0, False, True, False],
        [2, 1, 0, False, True, True],
        [2, 1, 0, True, False, False],
        [2, 1, 0, True, False, True],
        [2, 1, 0, True, True, False],
        [2, 1, 0, True, True, True]
    ]

    min_time = 10**10
    min_workstations = []
    for i in range(0, len(params)):
        t, workstations = fill_workstations(params[i][0], params[i][1], params[i][2], params[i][3], params[i][4], params[i][5])

        # uncomment to print every 48 answers
        # print('t=', t)

        if t < min_time:
            h = params[i][0]
            m = params[i][1]
            l = params[i][2]
            min_time = t
            min_workstations = workstations

    # returning the needed output
    w_out = [[], [], []]
    w_out[h] = min_workstations[0]
    w_out[m] = min_workstations[1]
    w_out[l] = min_workstations[2]
    return min_time, w_out


# ----------------------------------------------------------------------------------------------------------------------
# getting the inputs
n = int(input().split()[0])
# m = 3

# database of all jobs
database = []
for i in range(0, n):
    jobData = input().split()
    database.append([i])
    database[i].append(int(jobData[0]))
    for j in range(0, 3):
        database[i].append(int(jobData[j + 1]))


# calling the main function solving the problem
total_time, workstations = solve()

# printing the output
print('------------------------------')
print(total_time)
output = [[-1 for i in range(3)] for j in range(n)]

for i in range(0, 3):
    job_number = -1
    prev_job_number = -1
    for t in range(0, len(workstations[i])):
        job_number = workstations[i][t]
        if job_number != -1 and job_number != prev_job_number:
            output[job_number][i] = t
        prev_job_number = job_number


for i in range(0, n):
    print(output[i][0], output[i][1], output[i][2])


# uncomment to print statistics

# def cost(w_number):  # this function calculates the time a workstation will finish it's tasks SUPPOSING that there's no
#     # other workstation to cause any conflicts
#
#     w_number += 2
#     count = 0
#     start_index = 0
#     start_time = 0
#     linked_list = LinkedList(False)
#     workstation = []
#     while True:
#         if start_index < n:  # if all jobs aren't already added to available list
#             start_index = insert_available(start_time, start_index, w_number, linked_list)
#         if linked_list.is_empty():  # if there's no available task
#             start_time += 1  # move 1 second ahead
#             workstation.append(-1)
#         else:  # if there is any task available
#             head = linked_list.head
#             linked_list.delete_node(head)
#             for j in range(0, head.length):
#                 workstation.append(head.job_number)
#             count += 1
#             start_time += head.length
#         if count == n:
#             break
#     return len(workstation)
#
#
# print('------------------------------')
# print('statistics:')
#
# print('costs: (the time a workstation will finish it\'s tasks SUPPOSING that there\'s no other workstation to cause'
#       ' any conflicts')
# print('cost(w0)=', cost(0))
# print('cost(w1)=', cost(1))
# print('cost(w2)=', cost(2))
#
# print()
# print('the answer:')
# print('t(w0)=', len(workstations[0]))
# print('t(w1)=', len(workstations[1]))
# print('t(w2)=', len(workstations[2]))
#
# print()
# print('gaps:')
# gap = 0
# for i in range(0, len(workstations[0])):
#     if workstations[0][i] == -1:
#         gap += 1
# print('gap(w0)=', gap)
#
# gap = 0
# for i in range(0, len(workstations[1])):
#     if workstations[1][i] == -1:
#         gap += 1
# print('gap(w1)=', gap)
#
# gap = 0
# for i in range(0, len(workstations[2])):
#     if workstations[2][i] == -1:
#         gap += 1
# print('gap(w2)=', gap)
#
# print()
# print('workstation:')
# print(workstations[0])
# print(workstations[1])
# print(workstations[2])
