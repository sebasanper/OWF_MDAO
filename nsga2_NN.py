# Program Name: NSGA-II.py
# Description: This is a python implementation of Prof. Kalyanmoy Deb's popular NSGA-II algorithm
# Author: Haris Ali Khan
# Supervisor: Prof. Manoj Kumar Tiwari

# Importing required modules
from __future__ import print_function
import math
import random
from random import randint, choice
import matplotlib.pyplot as plt
import pickle
import numpy as np
from joblib import Parallel, delayed
import call_workflow_once as wf
fitness = wf.score_median_workflow

nn = pickle.load(open('regressor_coords3x3_lcoe.pickle', 'rb'))

vec = pickle.load(open('pickle_vectorizer.pickle', 'rb'))
# nn2 = pickle.load(open('regressor_coords3x3_time.pickle', 'rb'))


# def fitness(x):
#     xx = {'A': str(x[3]), 'B': str(x[4]), 'C': str(x[5]), 'D': str(x[6]), 'E': str(x[7]), 'F': str(x[8]),
#           'G': str(x[9]), 'H': str(x[10]), 'I': str(x[11]), 'J': str(x[12])}
#     cat_x = vec.transform(xx)[0]
#     cat_x = cat_x.tolist()
#     x = x[:3] + cat_x
#     # print(np.reshape(x, (1, -1))[0])
#     output = nn.predict(np.reshape(x, (1, -1)))
#     # print(output)
#     lcoe = abs(output - 7.89829164727)
#     time = nn2.predict(np.reshape(x, (1, -1)))
#     return - lcoe, - time


# def functions(x):
#     lcoe, time, power_calls, thrust_calls = fitness(x)
#     if x[9] == 1:  # Time for FAST
#         time += power_calls * 120.0
#     elif x[9] == 2:  # Time for WindSim
#         time += power_calls * 0.032
#     elif x[9] == 4:  # Time for WT_Perf
#         time += power_calls * 1.712
#     else:  # Time for powercurve or constant.
#         pass
#     if x[8] == 1:  # Time for WindSim
#         time += thrust_calls * 0.032
#     elif x[8] == 2:  # Time for WT_Perf
#         time += thrust_calls * 1.712
#     elif x[8] == 3:  # Time for FAST
#         time += thrust_calls * 120.0
#     else:  # Time for powercurve or constant.
#         pass
#     lcoe = abs(lcoe - 7.89829164727)
#     return - lcoe, - time


# First function to optimize
def function1(x):
    xx = {'A': str(x[3]), 'B': str(x[4]), 'C': str(x[5]), 'D': str(x[6]), 'E': str(x[7]), 'F': str(x[8]),
          'G': str(x[9]), 'H': str(x[10]), 'I': str(x[11]), 'J': str(x[12])}
    cat_x = vec.transform(xx)[0]
    cat_x = cat_x.tolist()
    x = x[:3] + cat_x
    # print(np.reshape(x, (1, -1))[0])
    output = nn.predict(np.reshape(x, (1, -1)))
    # print(output)
    lcoe = abs(output - 7.89829164727)
    return - lcoe


# Second function to optimize
def function2(x):
    lcoe, time, power_calls, thrust_calls = fitness(x)
    if x[9] == 1:  # Time for FAST
        time += power_calls * 120.0
    elif x[9] == 2:  # Time for WindSim
        time += power_calls * 0.032
    elif x[9] == 4:  # Time for WT_Perf
        time += power_calls * 1.712
    else:  # Time for powercurve or constant.
        pass
    if x[8] == 1:  # Time for WindSim
        time += thrust_calls * 0.032
    elif x[8] == 2:  # Time for WT_Perf
        time += thrust_calls * 1.712
    elif x[8] == 3:  # Time for FAST
        time += thrust_calls * 120.0
    else:  # Time for powercurve or constant.
        pass
    # xx = {'A': str(x[3]), 'B': str(x[4]), 'C': str(x[5]), 'D': str(x[6]), 'E': str(x[7]), 'F': str(x[8]),
    #       'G': str(x[9]), 'H': str(x[10]), 'I': str(x[11]), 'J': str(x[12])}
    # cat_x = vec.transform(xx)[0]
    # cat_x = cat_x.tolist()
    # x = x[:3] + cat_x
    # time = nn2.predict(np.reshape(x, (1, -1)))
    return - time


# Function to find index of list
def index_of(a, list):
    for i in range(0, len(list)):
        if list[i] == a:
            return i
    return -1


# Function to sort by values
def sort_by_values(list1, values):
    sorted_list = []
    while len(sorted_list) != len(list1):
        if index_of(min(values), values) in list1:
            sorted_list.append(index_of(min(values), values))
        values[index_of(min(values), values)] = float('inf')
    return sorted_list


# Function to carry out NSGA-II's fast non dominated sort
def fast_non_dominated_sort(values1, values2):
    S = [[] for _ in range(0, len(values1))]
    front = [[]]
    n = [0 for _ in range(0, len(values1))]
    rank = [0 for _ in range(0, len(values1))]

    for p in range(0, len(values1)):
        S[p] = []
        n[p] = 0
        for q in range(0, len(values1)):
            if (values1[p] > values1[q] and values2[p] > values2[q]) or (
                            values1[p] >= values1[q] and values2[p] > values2[q]) or (
                            values1[p] > values1[q] and values2[p] >= values2[q]):
                if q not in S[p]:
                    S[p].append(q)
            elif (values1[q] > values1[p] and values2[q] > values2[p]) or (
                            values1[q] >= values1[p] and values2[q] > values2[p]) or (
                            values1[q] > values1[p] and values2[q] >= values2[p]):
                n[p] = n[p] + 1
        if n[p] == 0:
            rank[p] = 0
            if p not in front[0]:
                front[0].append(p)

    i = 0
    while front[i]:
        Q = []
        for p in front[i]:
            for q in S[p]:
                n[q] = n[q] - 1
                if n[q] == 0:
                    rank[q] = i + 1
                    if q not in Q:
                        Q.append(q)
        i = i + 1
        front.append(Q)

    del front[len(front) - 1]
    return front


# Function to calculate crowding distance
def crowding_distance(values1, values2, front):
    distance = [0 for _ in range(0, len(front))]
    sorted1 = sort_by_values(front, values1[:])
    sorted2 = sort_by_values(front, values2[:])
    distance[0] = 4444444444444444
    distance[len(front) - 1] = 4444444444444444
    for k in range(1, len(front) - 1):
        distance[k] = distance[k] + (values1[sorted1[k + 1]] - values2[sorted1[k - 1]]) / (max(values1) - min(values1))
    for k in range(1, len(front) - 1):
        distance[k] = distance[k] + (values1[sorted2[k + 1]] - values2[sorted2[k - 1]]) / (max(values2) - min(values2))
    return distance


def make_vector(state, a):
    if a == 0:
        state[a] = randint(2, 25)
        state[a] /= 25.0
    elif a == 1:
        state[1] = 0.0
        while state[a] < state[2]:
            state[a] = choice([30.0, 60.0, 90.0, 120.0, 180.0])
            state[a] /= 180.0
    elif a == 2:
        state[2] = 190.0
        while state[a] > state[1]:
            state[a] = choice([1.0, 2.0, 5.0, 10.0, 15.0, 30.0, 60.0, 90.0, 120.0, 180.0])
            state[a] /= 180.0
    elif a == 3:
        state[a] = randint(1, 2)
    elif a == 4:
        state[a] = randint(0, 2)
    elif a == 5:
        state[a] = randint(1, 5)
    elif a == 6:
        state[a] = randint(1, 3)
    elif a == 7:
        state[a] = randint(0, 3)
    elif a == 8:
        state[a] = randint(1, 3)
    elif a == 9:
        state[a] = randint(1, 4)
    elif a == 10:
        state[a] = randint(1, 3)
    elif a == 11:
        state[a] = randint(1, 1)
    elif a == 12:
        state[a] = randint(1, 1)


# Function to carry out the crossover
def crossover(a, b):
    r = random.random()
    cross_place = randint(0, 12)
    if r > 0.5:
        child = a[:cross_place] + b[cross_place:]
        while child[2] * 180.0 > child[1] * 180.0:
            child[2] = choice([1.0, 2.0, 5.0, 10.0, 15.0, 30.0, 60.0, 90.0, 120.0, 180.0])
            child[2] /= 180.0
    else:
        child = b[:cross_place] + a[cross_place:]
        while child[2] > child[1]:
            child[2] = choice([1.0, 2.0, 5.0, 10.0, 15.0, 30.0, 60.0, 90.0, 120.0, 180.0])
            child[2] /= 180.0
    return child


# Function to carry out the mutation operator
def mutation(solution):
    mutation_prob = random.random()
    if mutation_prob < 1:
        a = randint(0, 12)
        state = solution
        make_vector(state, a)
        solution = state
    return solution


# Main program starts here
pop_size = 100
max_gen = 50


# Initialization
def gen_individual():
    state = [0.0 for _ in range(13)]
    state[2] = choice([1.0, 2.0, 5.0, 10.0, 15.0, 30.0, 60.0, 90.0, 120.0, 180.0])
    state[2] /= 180.0
    for a in range(13):
        make_vector(state, a)
    return state


def gen_population(n_indiv):
    return [gen_individual() for _ in range(n_indiv)]


solution = gen_population(pop_size)
# solution[0] = [2, 30.0, 1.0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1]
# solution[1] = [25, 180.0, 180.0, 2, 2, 5, 3, 3, 3, 4, 3, 1, 1]
gen_no = 0

results_file = open("nsga2_output.dat", "w", 1)
all_results1 = []
all_results2 = []

while gen_no < max_gen:
    function1_values = Parallel(n_jobs=-2)(delayed(function1)(solution[i]) for i in range(pop_size))
    function2_values = Parallel(n_jobs=-2)(delayed(function2)(solution[i]) for i in range(pop_size))
    # function1_values = [function1(solution[i]) for i in range(0, pop_size)]
    # function2_values = [function2(solution[i]) for i in range(0, pop_size)]
    # all_results1 += function1_values
    # all_results2 += function2_values
    # for i in range(len(solution)):
    #     results_file.write("{} {} {} 0\n".format(solution[i], function1_values[i], function2_values[i]))
    non_dominated_sorted_solution = fast_non_dominated_sort(function1_values[:], function2_values[:])
    # for val in non_dominated_sorted_solution[0]:
    #     results_file.write("{} {} {} 1\n".format(solution[val], function1_values[val], function2_values[val]))
    print("The best front for Generation number ", gen_no, " is")
    # for valuez in non_dominated_sorted_solution[0]:
    #     print(solution[valuez], end=" ")
    # print("\n")
    crowding_distance_values = []
    for i in range(0, len(non_dominated_sorted_solution)):
        crowding_distance_values.append(
            crowding_distance(function1_values[:], function2_values[:], non_dominated_sorted_solution[i][:]))
    solution2 = solution[:]
    # Generating offsprings
    while len(solution2) != 2 * pop_size:
        a1 = random.randint(0, pop_size - 1)
        b1 = random.randint(0, pop_size - 1)
        solution2.append(crossover(solution[a1], solution[b1]))
    function1_values2 = Parallel(n_jobs=-2)(delayed(function1)(solution2[i]) for i in range(2 * pop_size))
    function2_values2 = Parallel(n_jobs=-2)(delayed(function2)(solution2[i]) for i in range(2 * pop_size))
    # function1_values2 = [function1(solution2[i]) for i in range(0, 2 * pop_size)]
    # function2_values2 = [function2(solution2[i]) for i in range(0, 2 * pop_size)]
    # all_results1 += function1_values2
    # all_results2 += function2_values2
    non_dominated_sorted_solution2 = fast_non_dominated_sort(function1_values2[:], function2_values2[:])
    crowding_distance_values2 = []
    for i in range(0, len(non_dominated_sorted_solution2)):
        crowding_distance_values2.append(
            crowding_distance(function1_values2[:], function2_values2[:], non_dominated_sorted_solution2[i][:]))
    new_solution = []
    for i in range(0, len(non_dominated_sorted_solution2)):
        non_dominated_sorted_solution2_1 = [
            index_of(non_dominated_sorted_solution2[i][j], non_dominated_sorted_solution2[i]) for j in
            range(0, len(non_dominated_sorted_solution2[i]))]
        front22 = sort_by_values(non_dominated_sorted_solution2_1[:], crowding_distance_values2[i][:])
        front = [non_dominated_sorted_solution2[i][front22[j]] for j in
                 range(0, len(non_dominated_sorted_solution2[i]))]
        front.reverse()
        for value in front:
            new_solution.append(value)
            if len(new_solution) == pop_size:
                break
        if len(new_solution) == pop_size:
            break
    solution = [solution2[i] for i in new_solution]
    gen_no = gen_no + 1

    # Lets plot the final front now
function1v = [i * -1 for i in function1_values]
function2v = [j * -1 for j in function2_values]
# function1vt = [i * -1 for i in all_results1]
# function2vt = [j * -1 for j in all_results2]
plt.xlabel('Function 1', fontsize=15)
plt.ylabel('Function 2', fontsize=15)
# plt.scatter(function1vt, function2vt)
plt.scatter(function1v, function2v)
plt.show()

# for i in range(len(function1_values)):
#     results_file.write("{} {} {}\n".format(solution[i], -function1_values[i], -function2_values[i]))

results_file.close()

