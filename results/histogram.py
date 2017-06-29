import numpy as np
from numpy import mean, std

power = []
lcoe = []
time = []
modelpower = []
modelthrust = []

with open("/home/sebasanper/PycharmProjects/owf_MDAO/coords3x3_full_cython_random.dat") as data:
    next(data)
    for line in data:
        col = line.split()
        if float(col[8]) == 1 and float(col[9]) == 1:
            power.append(float(col[10]))
            lcoe.append(float(col[11]))
            time.append(float(col[12]))
            modelpower.append(float(col[13]))
            modelthrust.append(float(col[14]))

average = mean(lcoe)
stddev = std(lcoe)
residuals = [(lcoe[i] - average)/stddev for i in range(len(lcoe))]

# a, b = np.histogram(lcoe, bins=200, density=True)
c, d = np.histogram(time, bins=200, density=True)
a, b = np.histogram(lcoe, bins=200, density=True)


with open("todos.dat", "w") as output:
    for i in range(len(a)):
        output.write("{} {} {} {}\n".format(b[i], a[i], c[i], d[i]))
