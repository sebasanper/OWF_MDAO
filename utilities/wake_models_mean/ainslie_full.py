from thomas_algorithm import thomas
from math import exp
from eddy_viscosity import b, E
from ct_models import ct_v90
from time import time

u0 = 8.5


def ainslie_full(nj, ni, h, k, u0=8.5, ct=ct_v90(u0), i0=8.0):
    star = time()
    nj += 1
    ni += 1
    Dmi = ct - 0.05 - (16.0 * ct - 0.5) * i0 / 1000.0

    u = [[0.0 for _ in range(ni)]]
    v = [[0.0 for _ in range(ni)] for _ in range(nj)]

    for g in range(ni):
        u[0][g] = u0 * (1.0 - Dmi * exp(- 3.56 * float(g * h) ** 2.0 / b(Dmi, ct) ** 2.0))

    for j in range(1, nj):
        # start = time()
        A = []
        B = []
        C = []
        R = []

        i = 0

        A.append(- k * E(j * k, u[j-1][i], (u0 - u[j-1][i]) / u0, u0, i0, ct))
        B.append(2.0 * (h ** 2.0 * u[j-1][i] + k * E(j * k, u[j-1][i], (u0 - u[j-1][i]) / u0, u0, i0, ct)))
        C.append(- k * E(j * k, u[j-1][i], (u0 - u[j-1][i]) / u0, u0, i0, ct))
        R.append(k * E(j * k, u[j-1][i], (u0 - u[j-1][i]) / u0, u0, i0, ct) * (2.0 * u[j-1][i+1] - 2.0 * u[j-1][i]) + 2.0 * h ** 2.0 * u[j-1][i] ** 2.0)

        for i in range(1, ni):

            #  Uncomment if v is not neglected. Radial velocity.
            if j == 1:
                v[j][i] = (i * h) / ((i * h) + h) * (v[j-1][i-1] - h / k * (u[j-1][i] - u[0][i]))
            elif j > 1:
                v[j][i] = (i * h) / ((i * h) + h) * (v[j-1][i-1] - h / k * (u[j-1][i] - u[j-2][i]))

            A.append(k * (h * E(j * k, u[j-1][i], (u0 - u[j-1][i]) / u0, u0, i0, ct) - (i * h) * h * v[j][i] - 2.0 * (i * h) * E(j * k, u[j-1][i], (u0 - u[j-1][i]) / u0, u0, i0, ct)))
            B.append(4.0 * (i * h) * (h ** 2.0 * u[j-1][i] + k * E(j * k, u[j-1][i], (u0 - u[j-1][i]) / u0, u0, i0, ct)))
            C.append(k * ((i * h) * h * v[j][i] - 2.0 * (i * h) * E(j * k, u[j-1][i], (u0 - u[j-1][i]) / u0, u0, i0, ct) - h * E(j * k, u[j-1][i], (u0 - u[j-1][i]) / u0, u0, i0, ct)))
            if i < ni - 1:
                R.append(h * k * E(j * k, u[j-1][i], (u0 - u[j-1][i]) / u0, u0, i0, ct) * (u[j-1][i+1] - u[j-1][i-1]) + 2.0 * k * E(j * k, u[j-1][i], (u0 - u[j-1][i]) / u0, u0, i0, ct) * (i * h) * (u[j-1][i+1] - 2.0 * u[j-1][i] + u[j-1][i-1]) - (i * h) * h * k * v[j-1][i] * (u[j-1][i+1] - u[j-1][i-1]) + 4.0 * (i * h) * h ** 2.0 * u[j-1][i] ** 2.0)
            elif i == ni - 1:
                R.append(h * k * E(j * k, u[j-1][i], (u0 - u[j-1][i]) / u0, u0, i0, ct) * (u0 - u[j-1][i-1]) + 2.0 * k * E(j * k, u[j-1][i], (u0 - u[j-1][i]) / u0, u0, i0, ct) * (i * h) * (u0 - 2.0 * u[j-1][i] + u[j-1][i-1]) - (i * h) * h * k * v[j-1][i] * (u0 - u[j-1][i-1]) + 4.0 * (i * h) * h ** 2.0 * u[j-1][i] ** 2.0)

        # print time() - start

        C[0] += A[0]
        del A[0]
        R[-1] -= C[-1] * u0
        del C[-1]
        # start3 = time()
        u.append(thomas(A, B, C, R))
        # print time() - start3
    print time() - star,
    print 's'
    print u[-1][0]
    return u


if __name__ == '__main__':

    di = 1.7
    dj = 7.0
    ni = int(di * 80)
    nj = int(dj * 80)
    k = dj / float(nj)
    h = di / float(ni)
    res = ainslie_full(nj, ni, h, k)
    # with open('point.dat', 'w', 1) as line:
    #     for nj in range(100, 5000, 100):
    #         print nj
    #         k = dj / float(nj)
    #         for ni in range(100, 5000, 100):
    #             h = di / float(ni)
    #             start = time()
    #             finish = time()
    #             line.write('{1}\t{2}\t{0:1.10f}\t{3:1.10f}\t{4:1.10f}\t{5:3.10f}\n'.format(res[nj/2][0], nj, ni, res[-1][ni/6], res[nj/4][ni/4], finish - start))

    with open('output_metres.dat', 'w') as out:
        for i in range(ni):
            for j in range(nj):
                if res[j][ni-1-i] > u0 - 0.00001:
                    out.write('8.5\t')
                else:
                    out.write('{0:1.10f}\t'.format(res[j][ni-1-i]))
            out.write('\n')
        for i in range(ni):
            for j in range(nj):
                if res[j][i] > u0 - 0.00001:
                    out.write('8.5\t')
                else:
                    out.write('{0:1.10f}\t'.format(res[j][i]))
            out.write('\n')
