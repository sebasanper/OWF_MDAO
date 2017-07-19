__author__ = 'Sebastian Sanchez Perez-Moreno. Email: s.sanchezperezmoreno@tudelft.nl'

import sys
from math import ceil, floor, log
from random import randint, random, choice
#from ainslieOKoptimise import ainslie as fitness
# from larsenOKoptimise import larsen as fitness
import call_workflow_once as wf
fitness = wf.score_median_workflow
import time
from joblib import Parallel, delayed
from copy import deepcopy

result = open('lcoe2_gen_best_combi.dat', 'w', 1)
result2 = open('lcoe2_gen_fitness.dat', 'w', 1)
average = open('lcoe2_gen_average_fitness.dat', 'w', 1)
start_time = time.time()
# [21, 90.0, 30.0, 2, 2, 0, 0, 3, 3, 2, 1, 0, 0]


def make_vector(state, a):
    if a == 0:
        state[a] = randint(2, 25)
    elif a == 1:
        state[1] = 0.0
        while state[a] < state[2]:
            state[a] = choice([30.0, 60.0, 90.0, 120.0, 180.0])
    elif a == 2:
        state[2] = 190.0
        while state[a] > state[1]:
            state[a] = choice([1.0, 2.0, 5.0, 10.0, 15.0, 30.0, 60.0, 90.0, 120.0, 180.0])
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


def gen_individual():
    state = [None for _ in range(13)]
    state[2] = choice([1.0, 2.0, 5.0, 10.0, 15.0, 30.0, 60.0, 90.0, 120.0, 180.0])
    for a in range(13):
        make_vector(state, a)
    return state


def gen_population(n_indiv):
    return [gen_individual() for _ in range(n_indiv)]


def grade_gen(b, n):
    average = 0.0
    for item in b:
        average += item / n
    return average


def optimise():
    n_iter = 40
    n_ind = 50
    mutation_rate = 0.01
    selection_percentage = 0.2
    random_selection = 0.05

    pops = gen_population(n_ind)
    n_ind = len(pops)

    for iteration in range(n_iter):  # Iteration through generations loop
        start_time2 = time.time()
        pop = deepcopy(pops)
        pops = []
        fit = Parallel(n_jobs=-2)(delayed(fitness)(pop[i]) for i in range(n_ind))  # Parallel evaluation of fitness of all individuals

        aver = grade_gen(fit, float(n_ind))

        average.write('{}\n'.format(aver))

        for i in range(n_ind):
            fit[i] = [fit[i], i]
        for x in range(13):
            result.write('{}\t'.format(pop[min(fit)[1]][x]))  # This min implies minimisation.
        result.write('{}\n'.format(fit[int(min(fit)[1])][0]))

        for y in range(n_ind):
            result2.write('{}\n'.format(fit[y][0]))
        result2.write('\n')

        graded = [x[1] for x in sorted(fit, reverse=False)]

        retain_length = int(len(graded) * selection_percentage)
        parents_index = graded[:retain_length]

        # Add randomly other individuals for variety
        for item in graded[retain_length:]:
            if random_selection > random():
                parents_index.append(item)

        # Mutation of individuals
        for item in parents_index:
            if mutation_rate > random():
                a = randint(0, 12)
                state = pop[item]
                make_vector(state, a)
                pop[item] = state

        for item in parents_index:
            pops.append(pop[item])

        # Crossover function. Create children from parents
        parents_length = len(parents_index)
        desired_length = n_ind - parents_length
        children = []
        while len(children) < desired_length:
            parent1 = randint(0, parents_length - 1)
            parent2 = randint(0, parents_length - 1)
            if parent1 != parent2:
                parent1 = pop[parents_index[parent1]]
                parent2 = pop[parents_index[parent2]]
                cross_place = randint(0, 12)
                child = parent1[:cross_place] + parent2[cross_place:]
                while child[2] > child[1]:
                    child[2] = choice([1.0, 2.0, 5.0, 10.0, 15.0, 30.0, 60.0, 90.0, 120.0, 180.0])
                children.append(child)
        pops.extend(children)

        print("%d iteration,--- %s seconds, --- fitness: %f" % (iteration, time.time() - start_time2, fit[int(min(fit)[1])][0]))
    print("--- %s seconds ---" % (time.time() - start_time))
    result.close()
    result2.close()
    average.close()

if __name__ == '__main__':
    # print(gen_individual())
    optimise()
