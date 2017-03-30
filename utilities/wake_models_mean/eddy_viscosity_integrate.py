from math import exp
import time
from integrate_simpson2D import simpson_integrate2D
from thomas_algorithm import thomas
from eddy_viscosity import b, E

__author__ = 'Sebastian Sanchez Perez Moreno' \
             's.sanchezperezmoreno@tudelft.nl'


def ainslie(ct, u0, distance_parallel, distance_perpendicular, I0):

    # centreline = open('centreline.dat', 'w')
    # velocity = open('velocity.dat', 'w')

    h = 0.01
    L = distance_parallel
    n = int(L / h) + 1
    Uc1 = [0.0 for _ in range(n)]
    d1 = [0.0 for _ in range(n)]
    Ct = ct  # Thrust coefficient
    U0 = u0
    # dr = 0.1
    Y = distance_perpendicular
    # m = int(Y / dr)

    Dmi = Ct - 0.05 - (16.0 * Ct - 0.5) * I0 / 10.0

    # print Dmi, "Dmi"
    Uc1[0] = U0 * (1.0 - Dmi)  # Boundary condition at x = 2.0
    # print U0, U0 * (1.0 - Dmi)
    # print Uc1[0], "Uci[0]"
    d1[0] = Dmi
    # print d1[0], "d1[0]"
    for i in range(1, n):  # For all positions in the wake centreline direction. Recursive. Whole grid
        Uc1[i] = Uc1[i - 1] + (h * 16.0 * E(i * h, Uc1[i - 1], d1[i - 1], U0, I0, Ct) * (
        Uc1[i - 1] ** 3.0 - U0 * Uc1[i - 1] ** 2.0 - Uc1[i - 1] * U0 ** 2.0 + U0 ** 3.0) / (
                               Uc1[i - 1] * Ct * U0 ** 2.0))
        d1[i] = 1.0 - Uc1[i] / U0
    # Code to calculate wake deficit at a specific point instead of the whole grid. Namely, the rotor's centrepoint.
    # print "final"
    return d1[-1] * exp(- 3.56 * (Y / b(d1[-1], ct)) ** 2.0) * (1.0 + 7.12 * (0.07 * distance_parallel / b(d1[-1], ct))) ** (- 0.5)

    # Code to calculate average wake deficit in all area of the rotor ###############

    # Define function to integrate.

    # p. 77 Adapting and calibration of existing wake models to meet the conditions inside offshore wind farms. For integrand squared momentum deficit.
    # def G(r, theta):
    #     z = sqrt(Y ** 2.0 + r ** 2.0 + 2.0 * Y * r * cos(theta))
    #     gauss = U0 * (1.0 - d1[n - 1] * exp(- 3.56 * (z / b(d1[n - 1])) ** 2.0))
    #     return r * (U0 - gauss) ** 2.0
    #
    # A = pi * 0.5 ** 2.0  ## Unitary diameter in this program.
    # U = U0 - sqrt((1.0 / A) * simpson_integrate2D(G, 0.0, 0.5, 5, 0.0, 2.0 * pi, 10))

    # return 1.0 - U / U0


def ainslie_full(ct, u0, distance_parallel, distance_perpendicular, i0):
    # centreline = open('centreline.dat', 'w')
    # velocity = open('velocity.dat', 'w')

    di = 2.0
    dj = distance_parallel
    # ni = int(di * 80)
    # nj = int(dj * 80)
    ni = nj = 100
    k = dj / float(nj)
    h = di / float(ni)

    nj += 1
    ni += 1
    Dmi = ct - 0.05 - (16.0 * ct - 0.5) * i0 / 10.0

    u = [0.0 for _ in range(ni)]
    v = [0.0 for _ in range(ni)]

    for g in range(ni):
        u[g] = u0 * (1.0 - Dmi * exp(- 3.56 * float(g * h) ** 2.0 / b(Dmi, ct) ** 2.0))

    old_u = u
    u_initial = u
    old_v = v
    old2_u = 0.0

    for j in range(1, nj):
        # start = time()
        A = []
        B = []
        C = []
        R = []

        i = 0
        A.append(- k * E(j * k, old_u[i], (u0 - old_u[i]) / u0, u0, i0, ct))
        B.append(2.0 * (h ** 2.0 * old_u[i] + k * E(j * k, old_u[i], (u0 - old_u[i]) / u0, u0, i0, ct)))
        C.append(- k * E(j * k, old_u[i], (u0 - old_u[i]) / u0, u0, i0, ct))
        R.append(k * E(j * k, old_u[i], (u0 - old_u[i]) / u0, u0, i0, ct) * (2.0 * old_u[i+1] - 2.0 * old_u[i]) + 2.0 * h ** 2.0 * old_u[i] ** 2.0)

        v[0] = 0.0

        for i in range(1, ni):

            #  Uncomment if v is not neglected. Radial velocity.
            if j == 1:
                v[i] = (i * h) / ((i * h) + h) * (old_v[i-1] - h / k * (old_u[i] - u_initial[i]))
            elif j > 1:
                v[i] = (i * h) / ((i * h) + h) * (old_v[i-1] - h / k * (old_u[i] - old2_u[i]))

            A.append(k * (h * E(j * k, old_u[i], (u0 - old_u[i]) / u0, u0, i0, ct) - (i * h) * h * v[i] - 2.0 * (i * h) * E(j * k, old_u[i], (u0 - old_u[i]) / u0, u0, i0, ct)))
            B.append(4.0 * (i * h) * (h ** 2.0 * old_u[i] + k * E(j * k, old_u[i], (u0 - old_u[i]) / u0, u0, i0, ct)))
            C.append(k * ((i * h) * h * v[i] - 2.0 * (i * h) * E(j * k, old_u[i], (u0 - old_u[i]) / u0, u0, i0, ct) - h * E(j * k, old_u[i], (u0 - old_u[i]) / u0, u0, i0, ct)))
            if i < ni - 1:
                R.append(h * k * E(j * k, old_u[i], (u0 - old_u[i]) / u0, u0, i0, ct) * (old_u[i+1] - old_u[i-1]) + 2.0 * k * E(j * k, old_u[i], (u0 - old_u[i]) / u0, u0, i0, ct) * (i * h) * (old_u[i+1] - 2.0 * old_u[i] + old_u[i-1]) - (i * h) * h * k * old_v[i] * (old_u[i+1] - old_u[i-1]) + 4.0 * (i * h) * h ** 2.0 * old_u[i] ** 2.0)
            elif i == ni - 1:
                R.append(h * k * E(j * k, old_u[i], (u0 - old_u[i]) / u0, u0, i0, ct) * (u0 - old_u[i-1]) + 2.0 * k * E(j * k, old_u[i], (u0 - old_u[i]) / u0, u0, i0, ct) * (i * h) * (u0 - 2.0 * old_u[i] + old_u[i-1]) - (i * h) * h * k * old_v[i] * (u0 - old_u[i-1]) + 4.0 * (i * h) * h ** 2.0 * old_u[i] ** 2.0)

        # print time() - start

        C[0] += A[0]
        del A[0]
        R[-1] -= C[-1] * u0
        del C[-1]
        # start3 = time()
        old2_u = old_u
        old_u = thomas(A, B, C, R)

        old_v = v
        # print time() - start3
    # print time() - star,
    # print 's'

    # Code to calculate the average wake deficit in all the area of the rotor ###############

    # Define function to integrate.

    # p. 77 Adapting and calibration of existing wake models to meet the conditions inside
    # -----offshore wind farms. For integrand squared momentum deficit.

    # def G(r, theta):
    #     z = sqrt(Y ** 2.0 + r ** 2.0 + 2.0 * Y * r * cos(theta))
    #     gauss = U0 * (1.0 - d1[n - 1] * exp(- 3.56 * (z / b(d1[n - 1])) ** 2.0))
    #     return r * (U0 - gauss) ** 2.0
    #
    # A = pi * 0.5 ** 2.0  ## Unitary diameter in this program.
    # U = U0 - sqrt((1.0 / A) * simpson_integrate2D(G, 0.0, 0.5, 5, 0.0, 2.0 * pi, 10))
    # print old_u[int(round(distance_perpendicular * 80.0, 0))]
    return 1.0 - old_u[int(distance_perpendicular * 50.0)] / u0

    # centreline.close()
    # velocity.close()

if __name__ == '__main__':
    # start_time = time.time()
    # with open('ainslies.dat', 'w') as out:
    #     for i in range(1, 81):
    #         out.write('{0}\t{1}\t{2}\n'.format(2.0 + i/10.0, ainslie(0.79, 8.5, 2.0 + i/10.0, 0.0, 8.0), ainslie(0.79, 8.5, 2.0 + i/10.0, 0.0, 8.0)))
    print ainslie_full(0.79, 8.5, 3.0, 0.0, 0.08)
    print ainslie(0.79, 8.5, 3.0, 0.0, 0.08)
    # print("--- %s seconds ---" % (time.time() - start_time))
    # print ainslie_full(0.79, 8.5, 6.0, 0.5, 8.0)
    # print E(0.01, 8.5 ,3.03552, 0.64288, 0.08, 0.79)