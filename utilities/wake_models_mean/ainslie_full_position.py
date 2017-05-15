from thomas_algorithm import thomas
from math import exp
from eddy_viscosity import b, E
from time import time


def ainslie_full(parallel, perpendicular, discretisation_parallel, discretisation_perpendicular, ct=0.79, u0=8.5, i0=8.0):
    Dmi = ct - 0.05 - (16.0 * ct - 0.5) * i0 / 1000.0

    if perpendicular == 0.0:
        perpendicular = 0.01
    h = perpendicular / discretisation_perpendicular
    k = parallel / discretisation_parallel

    nj = discretisation_parallel
    ni = discretisation_perpendicular

    u = [[0.0 for _ in range(ni)]]
    v = [[0.0 for _ in range(ni)] for _ in range(nj)]

    for g in range(ni):
        u[0][g] = u0 * (1.0 - Dmi * exp(- 3.56 * float(g * h) ** 2.0 / b(Dmi, ct) ** 2.0))

    print('\rPercentage: 0.0 %. Time remaining:  s'),

    for j in range(1, nj):

        start = time()

        A = []
        B = []
        C = []
        R = []

        for i in range(ni):
            #  Uncomment if v is not neglected. Radial velocity.
            if i == 1:
                v[j][i] = (i * h) / ((i * h) + h) * (v[j-1][i-1] - h / k * (u[j-1][i] - u[0][i]))
            elif i > 1:
                v[j][i] = (i * h) / ((i * h) + h) * (v[j-1][i-1] - h / k * (u[j-1][i] - u[j-2][i]))

            if i == 0:
                A.append(- k * E(j * k, u[j-1][i], (u0 - u[j-1][i]) / u0, u0, i0, ct))
                B.append(2.0 * (h ** 2.0 * u[j-1][i] + k * E(j * k, u[j-1][i], (u0 - u[j-1][i]) / u0, u0, i0, ct)))
                C.append(- k * E(j * k, u[j-1][i], (u0 - u[j-1][i]) / u0, u0, i0, ct))
                R.append(k * E(j * k, u[j-1][i], (u0 - u[j-1][i]) / u0, u0, i0, ct) * (2.0 * u[j-1][i+1] - 2.0 * u[j-1][i]) + 2.0 * h ** 2.0 * u[j-1][i] ** 2.0)

            else:
                A.append(k * (h * E(j * k, u[j-1][i], (u0 - u[j-1][i]) / u0, u0, i0, ct) - (i * h) * h * v[j][i] - 2.0 * (i * h) * E(j * k, u[j-1][i], (u0 - u[j-1][i]) / u0, u0, i0, ct)))
                B.append(4.0 * (i * h) * (h ** 2.0 * u[j-1][i] + k * E(j * k, u[j-1][i], (u0 - u[j-1][i]) / u0, u0, i0, ct)))
                C.append(k * ((i * h) * h * v[j][i] - 2.0 * (i * h) * E(j * k, u[j-1][i], (u0 - u[j-1][i]) / u0, u0, i0, ct) - h * E(j * k, u[j-1][i], (u0 - u[j-1][i]) / u0, u0, i0, ct)))
                if i < ni - 1:
                    R.append(h * k * E(j * k, u[j-1][i], (u0 - u[j-1][i]) / u0, u0, i0, ct) * (u[j-1][i+1] - u[j-1][i-1]) + 2.0 * k * E(j * k, u[j-1][i], (u0 - u[j-1][i]) / u0, u0, i0, ct) * (i * h) * (u[j-1][i+1] - 2.0 * u[j-1][i] + u[j-1][i-1]) - (i * h) * h * k * v[j-1][i] * (u[j-1][i+1] - u[j-1][i-1]) + 4.0 * (i * h) * h ** 2.0 * u[j-1][i] ** 2.0)
                elif i == ni - 1:
                    R.append(h * k * E(j * k, u[j-1][i], (u0 - u[j-1][i]) / u0, u0, i0, ct) * (u[j-1][i] - u[j-1][i-1]) + 2.0 * k * E(j * k, u[j-1][i], (u0 - u[j-1][i]) / u0, u0, i0, ct) * (i * h) * (u[j-1][i] - 2.0 * u[j-1][i] + u[j-1][i-1]) - (i * h) * h * k * v[j-1][i] * (u[j-1][i] - u[j-1][i-1]) + 4.0 * (i * h) * h ** 2.0 * u[j-1][i] ** 2.0)

        C[0] += A[0]
        del A[0]
        R[-1] -= C[-1] * u0
        del C[-1]

        u.append(thomas(A, B, C, R))

        periter = time()
        lleva = float(j) / float(nj)
        falta = (periter - start) * (nj - j - 1)
        # print('\rPercentage: {0:2.2f} %. Time remaining: {1:2.1f} s'.format(100.0 * lleva, falta)),

    print 'Position = ' + str(nj * k) + ', ' + str(ni * h)
    return u[-1][-1]

if __name__ == '__main__':
    paral = 0.5
    perpen = 0.5

    n_paral = 300
    n_perpen = 300
    res = ainslie_full(paral, perpen, n_paral, n_perpen)
    print '{0:2.10}'.format(res)
