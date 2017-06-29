from random import random, normalvariate
from numpy import sqrt
import numpy as np


def pareto_find(a):
    a.sort(reverse=False)
    # print a

    pareto = []
    pareto.append(a[0])
    for i in range(1, len(a)):
        if a[i][1] <= pareto[- 1][1]:
            pareto.append(a[i])

    # for item in pareto:
    #     print item[0], item[1], sqrt(item[0] ** 2.0 + item[1] ** 2.0)

    #  GNUPLOT script
    #  plot "data.dat" u ($1):($3==0?$2:1/0), "data.dat" u ($1):($3==1?$2:1/0) pt 7

    with open("data.dat", "a") as out2:
        for item in pareto:
            out2.write("{0} {1} 1\n".format(item[0], item[1]))


def simple_cull(inputPoints):
    with open("data.dat", "w") as out:
        for item in inputPoints:
            out.write("{0} {1} {2} 0\n".format(item[0], item[1], item[2]))

    paretoPoints = set()
    candidateRowNr = 0
    dominatedPoints = set()
    while True:
        candidateRow = inputPoints[candidateRowNr]
        inputPoints.remove(candidateRow)
        rowNr = 0
        nonDominated = True
        while len(inputPoints) != 0 and rowNr < len(inputPoints):
            row = inputPoints[rowNr]
            if dominates(candidateRow, row):
                # If it is worse on all features remove the row from the array
                inputPoints.remove(row)
                dominatedPoints.add(tuple(row))
            elif dominates(row, candidateRow):
                nonDominated = False
                dominatedPoints.add(tuple(candidateRow))
                rowNr += 1
            else:
                rowNr += 1

        if nonDominated:
            # add the non-dominated point to the Pareto frontier
            paretoPoints.add(tuple(candidateRow))

        if len(inputPoints) == 0:
            break

    with open("data.dat", "a") as out2:
        for item in paretoPoints:
            out2.write("{0} {1} {2} 1\n".format(item[0], item[1], item[2]))


def dominates(row, candidateRow):
    return sum([row[x] <= candidateRow[x] for x in range(len(row))]) == len(row)


if __name__ == '__main__':
    from math import cos, sin, pi
    # from time import time
    # a = []
    # b = [[normalvariate(1.0, 1.0), normalvariate(1.0, 1.0), normalvariate(1.0, 1.0)] for _ in range(20000)]
    b = []
    for n in range(100000):
        u = random() * 2.0 - 1.0
        theta = random() * 2.0 * pi
        c = random()
        b.append([c * sqrt(1.0 - u ** 2.0) * cos(theta), c * sqrt(1.0 - u ** 2.0) * sin(theta), c * u])
    # start = time()
    # pareto_find(b)
    # pareto_front2(a)
    # print time() - start
    # pareto_frontier_multi(np.array(b))

    simple_cull(b)
