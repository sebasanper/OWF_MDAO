from utilities.pareto.non_dominance import pareto_find

accuracy = []
time = []
with open("obj_functions.dat", "r") as reading:
    for line in reading:
        cols = line.split()
        a = int(cols[0])
        b = int(cols[1])
        c = int(cols[2])
        d = int(cols[3])
        e = int(cols[4])
        f = int(cols[5])
        g = int(cols[6])
        h = int(cols[7])
        i = int(cols[8])
        j = int(cols[9])
        time.append(float(cols[12]))
        if g == 1:  # Time for FAST
            time[-1] += float(cols[13]) * 120.0
        elif g == 2:  # Time for WindSim
            time[-1] += float(cols[13]) * 0.032
        elif g == 4:  # Time for WT_Perf
            time[-1] += float(cols[13]) * 1.712
        else:  # Time for powercurve or constant.
            pass
        if f == 1:  # Time for WindSim
            time[-1] += float(cols[14]) * 0.032
        elif f == 2:  # Time for WT_Perf
            time[-1] += float(cols[14]) * 1.712
        elif f == 3:  # Time for FAST
            time[-1] += float(cols[14]) * 120.0
        else:  # Time for powercurve or constant.
            pass
        accuracy.append(abs(float(cols[11]) - 7.89829164727))
with open("coords3x3_10000_5_30_18_42_46.dat", "r") as reading:
    for line in reading:
        cols = line.split()
        a = int(cols[0])
        b = int(cols[1])
        c = int(cols[2])
        d = int(cols[3])
        e = int(cols[4])
        f = int(cols[5])
        g = int(cols[6])
        h = int(cols[7])
        i = int(cols[8])
        j = int(cols[9])
        time.append(float(cols[12]))
        if g == 1:  # Time for FAST
            time[-1] += float(cols[13]) * 120.0
        elif g == 2:  # Time for WindSim
            time[-1] += float(cols[13]) * 0.032
        elif g == 4:  # Time for WT_Perf
            time[-1] += float(cols[13]) * 1.712
        else:  # Time for powercurve or constant.
            pass
        if f == 1:  # Time for WindSim
            time[-1] += float(cols[14]) * 0.032
        elif f == 2:  # Time for WT_Perf
            time[-1] += float(cols[14]) * 1.712
        elif f == 3:  # Time for FAST
            time[-1] += float(cols[14]) * 120.0
        else:  # Time for powercurve or constant.
            pass
        accuracy.append(abs(float(cols[11]) - 7.89829164727))


a = [[accuracy[ii], time[ii]] for ii in range(len(accuracy))]
pareto_find(a)
