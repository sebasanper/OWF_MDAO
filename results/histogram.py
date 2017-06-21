import numpy as np

power = []
lcoe = []
time = []
modelpower = []
modelthrust = []

with open("/home/sebasanper/PycharmProjects/owf_MDAO/coords3x3_full_good_final.dat") as data:
    next(data)
    for line in data:
        col = line.split()
        power.append(float(col[10]))
        lcoe.append(float(col[11]))
        time.append(float(col[12]))
        modelpower.append(float(col[13]))
        modelthrust.append(float(col[14]))

a, b = np.histogram(lcoe, bins="auto", density=False)

with open("histogram_full.dat", "w") as output:
    for i in range(len(a)):
        output.write("{} {}\n".format(b[i], a[i]))
