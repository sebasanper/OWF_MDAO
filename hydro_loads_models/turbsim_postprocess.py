from numpy import std, average

# Only for plotting. Extracts matrices from output file.
# with open("/home/sebasanper/Downloads/turbsim/turbsim/TurbSimA.u", 'r') as inp:
#     i = 0
#     for line in inp:
#         if i % 15 == 0:
#             string = 'post' + str(i/15) + '.dat'
#         with open(string, "a") as out:
#             if i % 15 != 0:
#                 out.write(line)
#         i += 1

time = []
centre = []
wind_file = \
    '/home/sebasanper/PycharmProjects/owf_MDAO/aero_loads_models/turbsim_test_run/TurbSim.u'
length = sum(1 for line in open(wind_file)) / 15
mat = [[[0 for _ in range(13)] for __ in range(13)] for ___ in range(length)]

with open(wind_file, 'r') as inp:
    ii = 0
    j = 0
    for line in inp:
        if ii > 11:
            i = ii - 12
            if i % 15 == 0:
                col1 = line.split()
                time.append(float(col1[0]))
                centre.append(float(col1[1]))
                j = 0
            elif i % 15 == 14:
                pass
            else:
                col2 = line.split()
                step = i / 15
                for e in range(len(col2)):
                    mat[step][j][e] = float(col2[e])
                j += 1
        ii += 1

# print mat[-1][10][12]
# print len(mat)

TI = []
for y in range(len(mat[0][0])):
    for z in range(len(mat[0])):
        newvector = []
        for x in range(len(mat)):
            newvector.append(mat[x][y][z])
        TI.append(std(newvector) / average(newvector))
        # print TI[-1]
print average(TI)
print average(mat)
