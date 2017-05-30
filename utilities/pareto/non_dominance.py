from random import random
from numpy import sqrt

a = []
for n in range(200):
    a.append([random(), random()])


def pareto_find(a):
    a.sort(reverse=False)
    # print a
    with open("data.dat", "w") as out:
        for item in a:
            out.write("{0} {1} 0\n".format(item[0], item[1]))

    # pareto = [[] for _ in range(1)]
    pareto = []
    # for front in range(1):
    out = False
    pareto.append(a[0])
    for i in range(1, len(a)):
        # pareto[front].append(a[i])
        if a[i][1] <= pareto[- 1][1]:
            pareto.append(a[i])

    # print pareto

    with open("data.dat", "a") as out2:
        for item in pareto:
            out2.write("{0} {1} 1\n".format(item[0], item[1]))

    # for item in pareto:
        # print item[0], item[1], sqrt(item[0] ** 2.0 + item[1] ** 2.0)

    #  GNUPLOT script
    #  plot "data.dat" u ($1):($3==0?$2:1/0) pt 7, "data.dat" u ($1):($3==1?$2:1/0) pt 7 lc "green"
