'''Sebastian Sanchez Perez Moreno' \
             's.sanchezperezmoreno@tudelft.nl'''
# Jensen wake model with partial shadowing factor applied to horns rev.
from math import sqrt, pi, radians

import wake
import wake_geometry as wake_larsen
from ct_models import ct_v90
from eddy_viscosity_integrate import ainslie, ainslie_full
from wake import distance_to_front, determine_front


def Ct(U0):
    # return ct_bladed(U0)
    # return 0.79
    return ct_v90(U0)


def jensen_1angle(layout_x, layout_y, wind_speed, angle, rotor_radius, TI):
    U0 = wind_speed  # Free stream wind speed
    k = 0.04  # * TI
    nt = len(layout_y)  # Number of turbines ## Length of layout list

    r0 = rotor_radius  # Turbine rotor radius
    # angle2 = - 270.0 - angle  # To read windroses where N is 0 and E is 90.
    angle3 = angle + 180.0
    deficit_matrix = [[0.0 for _ in range(nt)] for _ in range(nt)]
    proportion = [[0.0 for _ in range(nt)] for _ in range(nt)]
    distance = [[0.0 for _ in range(2)] for _ in range(nt)]
    U = [U0 for _ in range(nt)]
    total_deficit = [0.0 for _ in range(nt)]

    for tur in range(nt):
        distance[tur] = [distance_to_front(layout_x[tur], layout_y[tur], angle), tur]
    distance.sort()

    for turbine in range(nt):

        for num in range(turbine):
            total_deficit[distance[turbine][1]] += deficit_matrix[distance[turbine][1]][distance[num][1]] ** 2.0
        total_deficit[distance[turbine][1]] = sqrt(total_deficit[distance[turbine][1]])
        U[distance[turbine][1]] = U0 * (1.0 - total_deficit[distance[turbine][1]])

        for i in range(turbine + 1, nt):

            determ = wake.determine_if_in_wake(layout_x[distance[turbine][1]],
                                               layout_y[distance[turbine][1]],
                                               layout_x[distance[i][1]], layout_y[distance[i][1]], k,
                                               r0, angle3)
            proportion[distance[turbine][1]][distance[i][1]] = determ[0]

            if proportion[distance[turbine][1]][distance[i][1]] != 0.0:
                deficit_matrix[distance[i][1]][distance[turbine][1]] = proportion[distance[turbine][1]][
                                                                           distance[i][1]] * wake.wake_deficit(
                    Ct(U[distance[turbine][1]]), k, determ[1], r0)
            else:
                deficit_matrix[distance[i][1]][distance[turbine][1]] = 0.0

    return U


def ainslie_1angle(layout_x, layout_y, wind_speed, angle, rotor_radius, TI):
    layout_xD = []
    layout_yD = []

    D = 2.0 * rotor_radius  # Diameter

    for x in range(len(layout_x)):
        layout_xD.append(layout_x[x] / D)

    for x in range(len(layout_y)):
        layout_yD.append(layout_y[x] / D)

    nt = len(layout_y)
    U0 = wind_speed  # Free stream wind speed
    angle3 = angle + 180.0
    wake_deficit_matrix = [[0.0 for _ in range(nt)] for _ in range(nt)]
    distance = [[0.0 for _ in range(2)] for _ in range(nt)]
    total_deficit = [0.0 for _ in range(nt)]
    U = [U0 for _ in range(nt)]

    for tur in range(nt):
        distance[tur] = [distance_to_front(layout_xD[tur], layout_yD[tur], angle), tur]
    distance.sort()

    for turbine in range(nt):
        for num in range(turbine):
            total_deficit[distance[turbine][1]] += wake_deficit_matrix[distance[turbine][1]][
                                                       distance[num][1]] ** 2.0
        total_deficit[distance[turbine][1]] = sqrt(total_deficit[distance[turbine][1]])
        U[distance[turbine][1]] = U0 * (1.0 - total_deficit[distance[turbine][1]])
        parallel_distance = [0.0 for _ in range(nt)]
        perpendicular_distance = [0.0 for _ in range(nt)]

        for i in range(turbine + 1, nt):
            parallel_distance[distance[i][1]] = determine_front(angle3, layout_xD[distance[turbine][1]],
                                                                layout_yD[distance[turbine][1]],
                                                                layout_xD[distance[i][1]],
                                                                layout_yD[distance[i][1]])
            perpendicular_distance[distance[i][1]] = wake.crosswind_distance(radians(angle3),
                                                                             layout_xD[distance[turbine][1]],
                                                                             layout_yD[distance[turbine][1]],
                                                                             layout_xD[distance[i][1]],
                                                                             layout_yD[distance[i][1]])

            if perpendicular_distance[distance[i][1]] <= 5.7 and parallel_distance[
                distance[i][1]] > 0.0:  # 1.7 gives same results as a bigger distance, many times faster.

                wake_deficit_matrix[distance[i][1]][distance[turbine][1]] = ainslie(
                    Ct(U[distance[turbine][1]]), U[distance[turbine][1]],
                    parallel_distance[distance[i][1]], perpendicular_distance[distance[i][1]], TI)
            else:
                wake_deficit_matrix[distance[i][1]][distance[turbine][1]] = 0.0

    return U


def ainsliefull_1angle(layout_x, layout_y, wind_speed, angle, rotor_radius, TI):
    layout_xD = []
    layout_yD = []

    D = 2.0 * rotor_radius  # Diameter

    for x in range(len(layout_x)):
        layout_xD.append(layout_x[x] / D)

    for x in range(len(layout_y)):
        layout_yD.append(layout_y[x] / D)

    nt = len(layout_y)
    U0 = wind_speed  # Free stream wind speed
    angle3 = angle + 180.0
    wake_deficit_matrix = [[0.0 for _ in range(nt)] for _ in range(nt)]
    distance = [[0.0 for _ in range(2)] for _ in range(nt)]
    total_deficit = [0.0 for _ in range(nt)]
    U = [U0 for _ in range(nt)]
    U = U

    for tur in range(nt):
        distance[tur] = [distance_to_front(layout_xD[tur], layout_yD[tur], angle), tur]
    distance.sort()

    for turbine in range(nt):

        for num in range(turbine):
            total_deficit[distance[turbine][1]] += wake_deficit_matrix[distance[turbine][1]][
                                                       distance[num][1]] ** 2.0
        total_deficit[distance[turbine][1]] = sqrt(total_deficit[distance[turbine][1]])
        U[distance[turbine][1]] = U0 * (1.0 - total_deficit[distance[turbine][1]])
        parallel_distance = [0.0 for _ in range(nt)]
        perpendicular_distance = [0.0 for _ in range(nt)]

        for i in range(turbine + 1, nt):
            parallel_distance[distance[i][1]] = determine_front(angle3, layout_xD[distance[turbine][1]],
                                                                layout_yD[distance[turbine][1]],
                                                                layout_xD[distance[i][1]],
                                                                layout_yD[distance[i][1]])
            perpendicular_distance[distance[i][1]] = wake.crosswind_distance(radians(angle3),
                                                                             layout_xD[distance[turbine][1]],
                                                                             layout_yD[distance[turbine][1]],
                                                                             layout_xD[distance[i][1]],
                                                                             layout_yD[distance[i][1]])

            if perpendicular_distance[distance[i][1]] <= 2.0 and parallel_distance[
                distance[i][1]] > 0.0:  ## 1.7 gives same results as a bigger distance, many times faster.

                wake_deficit_matrix[distance[i][1]][distance[turbine][1]] = ainslie_full(
                    Ct(U[distance[turbine][1]]), U[distance[turbine][1]],
                    parallel_distance[distance[i][1]], perpendicular_distance[distance[i][1]], TI)
            else:
                wake_deficit_matrix[distance[i][1]][distance[turbine][1]] = 0.0

    # print angle, sum([power(U[i]) for i in range(len(U))])
    return U


def larsen_1angle(layout_x, layout_y, wind_speed, angle, rotor_radius, hub_height, TI):
    U0 = wind_speed

    r0 = rotor_radius
    nt = len(layout_y)  # Number of turbines
    D = 2.0 * r0
    A = pi * r0 ** 2.0
    H = hub_height  # Hub height
    ia = TI  # Ambient turbulence intensity according to vanluvanee. 8% on average

    def deff(u1):
        return D * sqrt((1.0 + sqrt(1.0 - Ct(u1))) / (2.0 * sqrt(1.0 - Ct(u1))))

    rnb = max(1.08 * D, 1.08 * D + 21.7 * D * (ia - 0.05))
    r95 = 0.5 * (rnb + min(H, rnb))

    def x0(u2):
        return 9.5 * D / ((2.0 * r95 / deff(u2)) ** 3.0 - 1.0)

    def c1(u3):
        return (deff(u3) / 2.0) ** (5.0 / 2.0) * (105.0 / 2.0 / pi) ** (- 1.0 / 2.0) * (Ct(u3) * A * x0(u3)) ** (
            - 5.0 / 6.0)  # Prandtl mixing length

    angle3 = angle + 180.0
    deficit_matrix = [[0.0 for _ in range(nt)] for _ in range(nt)]
    distance = [[0.0 for _ in range(2)] for _ in range(nt)]
    U = [U0 for _ in range(nt)]
    total_deficit = [0.0 for _ in range(nt)]

    for tur in range(nt):
        distance[tur] = [distance_to_front(layout_x[tur], layout_y[tur], angle), tur]
    distance.sort()

    for turbine in range(nt):
        for num in range(turbine):
            total_deficit[distance[turbine][1]] += deficit_matrix[distance[turbine][1]][distance[num][1]] ** 2.0
        total_deficit[distance[turbine][1]] = sqrt(total_deficit[distance[turbine][1]])
        U[distance[turbine][1]] = U0 * (1.0 - total_deficit[distance[turbine][1]])
        flag = [False for _ in range(nt)]
        proportion = [0.0 for _ in range(nt)]
        perpendicular_distance = [0.0 for _ in range(nt)]
        parallel_distance = [0.0 for _ in range(nt)]
        for i in range(turbine + 1, nt):
            proportion[distance[i][1]], flag[distance[i][1]], perpendicular_distance[distance[i][1]], \
            parallel_distance[distance[i][1]] = wake_larsen.determine_if_in_wake_larsen(
                layout_x[distance[turbine][1]],
                layout_y[distance[turbine][1]],
                layout_x[distance[i][1]],
                layout_y[distance[i][1]], A,
                c1(U[distance[turbine][1]]),
                Ct(U[distance[turbine][1]]), angle3,
                r0, x0(U[distance[turbine][1]]))
            if parallel_distance[distance[i][1]] > 0.0:
                if proportion[distance[i][1]] != 0.0:
                    deficit_matrix[distance[i][1]][distance[turbine][1]] = proportion[
                                                                               distance[i][
                                                                                   1]] * wake_larsen.wake_deficit(
                        U[distance[turbine][1]], Ct(U[distance[turbine][1]]), A,
                        parallel_distance[distance[i][1]] + x0(U[distance[turbine][1]]),
                        perpendicular_distance[distance[i][1]], c1(U[distance[turbine][1]]))
                else:
                    deficit_matrix[distance[i][1]][distance[turbine][1]] = 0.0
            else:
                deficit_matrix[distance[i][1]][distance[turbine][1]] = 0.0

    return U


if __name__ == '__main__':
    # with open('discretise.dat', 'w', 1) as out:
    #     res1 = ainslie_1angle([0., 560.0, 1120., 1680., 2240., 2800., 3360., 3920., 4480.],
    #                    [0., 0., 0., 0., 0., 0., 0., 0., 0.], 8.5, 180.0, 40.0, 0.08)
    #     for j in range(9):
    #         out.write('{0}\t'.format(res1[j]))
    #     out.write('\n')
    #     for i in range(50):
    #         disc = 100 + i * 10
    #         res2 = ainsliefull_1angle([0., 560.0, 1120., 1680., 2240., 2800., 3360., 3920., 4480.],
    #                        [0., 0., 0., 0., 0., 0., 0., 0., 0.], 8.5, 0.0, 40.0, 0.08)
    #         for j in range(9):
    #             out.write('{0}\t'.format(res2[j]))
    #         out.write('\n')

    print ainsliefull_1angle([0., 560.0, 1120., 1680., 2240., 2800., 3360., 3920., 4480.],
                        [0., 0., 0., 0., 0., 0., 0., 0., 0.], 8.5, 180.0, 40.0, 0.08)

    print ainslie_1angle([0., 560.0, 1120., 1680., 2240., 2800., 3360., 3920., 4480.],
                       [0., 0., 0., 0., 0., 0., 0., 0., 0.], 8.5, 180.0, 40.0, 0.08)