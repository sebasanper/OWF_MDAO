from utilities.pareto.non_dominance import pareto_find

accuracy = []
time = []
with open("coords3x3_15bins.dat", "r") as reading:
    with open("acc_time_3x3.dat", "w") as output:
        for line in reading:
            cols = line.split()
            accuracy.append(abs(float(cols[10]) - 7.89829164727))
            time.append(float(cols[11]))
            a = int(cols[0])
            b = int(cols[1])
            c = int(cols[2])
            d = int(cols[3])
            e = int(cols[4])
            f = int(cols[5])
            g = int(cols[6])
            h = int(cols[7])
            i = int(cols[8])

            # output.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t")
a = [[accuracy[ii], time[ii]] for ii in range(len(accuracy))]
pareto_find(a)