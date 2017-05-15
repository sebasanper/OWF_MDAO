'''Sebastian Sanchez Perez Moreno' \
             's.sanchezperezmoreno@tudelft.nl'''
# Jensen wake model with partial shadowing factor applied to horns rev.
from math import sqrt, pi, radians
from numpy import array, zeros

from openmdao.api import Component, Group, Problem

import wake
import wake_geometry as wake_larsen
from ct_models import ct_v90
from eddy_viscosity_integrate import ainslie
from myMDAO import num_turb
from wake import distance_to_front, determine_front


def Ct(U0):
    # return ct_bladed(U0)
    return ct_v90(U0)


class JensenWake1Angle(Component):
    def __init__(self):
        super(JensenWake1Angle, self).__init__()

        self.add_param('layout_x', val=zeros(num_turb))
        self.add_param('layout_y', val=zeros(num_turb))
        self.add_param('rotor_radius', val=0.0)
        self.add_param('mean_ambient_wind_speed', val=0.0)
        self.add_param('wind_direction', val=0.0)
        self.add_param('k', val=0.0)

        self.add_output('U', val=zeros(num_turb))

    def solve_nonlinear(self, params, unknowns, resids):

        U0 = params['mean_ambient_wind_speed']  # Free stream wind speed
        layout_x = params['layout_x']
        layout_y = params['layout_y']
        k = params['k'] = 0.04  # Decay constant
        r0 = params['rotor_radius']  # Turbine rotor radius
        angle = params['wind_direction']
        nt = num_turb
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

        # return [list(_) for _ in zip(
        #     zip([x for (y, x) in sorted(zip([item[0] for item in distance], layout_x))], [x for (y, x) in sorted(
        #         zip([item[0] for item in distance], layout_y))]), U)]

        unknowns['U'] = array(U)


class AinslieWake1Angle(Component):
    def __init__(self):
        super(AinslieWake1Angle, self).__init__()

        self.add_param('layout_x', val=zeros(num_turb))
        self.add_param('layout_y', val=zeros(num_turb))
        self.add_param('rotor_radius', val=0.0)
        self.add_param('mean_ambient_wind_speed', val=0.0)
        self.add_param('wind_direction', val=0.0)
        self.add_param('TI', val=0.0)

        self.add_output('U', val=zeros(num_turb))

    def solve_nonlinear(self, params, unknowns, resids):

        D = 2.0 * params['rotor_radius']  # Diameter

        layout_x = params['layout_x']
        layout_y = params['layout_y']
        layout_xD = array(layout_x) / D
        layout_yD = array(layout_y) / D

        U0 = params['mean_ambient_wind_speed']  # Free stream wind speed
        angle = params['wind_direction']
        nt = num_turb
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

                if perpendicular_distance[distance[i][1]] <= 1.7 and parallel_distance[
                    distance[i][1]] > 0.0:  ## 1.7 gives same results as a bigger distance, many times faster.

                    wake_deficit_matrix[distance[i][1]][distance[turbine][1]] = ainslie(
                        Ct(U[distance[turbine][1]]), U[distance[turbine][1]],
                        parallel_distance[distance[i][1]], perpendicular_distance[distance[i][1]], params['TI'])
                else:
                    wake_deficit_matrix[distance[i][1]][distance[turbine][1]] = 0.0

        unknowns['U'] = array(U)


class LarsenWake1Angle(Component):
    def __init__(self):
        super(LarsenWake1Angle, self).__init__()

        self.add_param('layout_x', val=zeros(num_turb))
        self.add_param('layout_y', val=zeros(num_turb))
        self.add_param('rotor_radius', val=0.0)
        self.add_param('mean_ambient_wind_speed', val=0.0)
        self.add_param('wind_direction', val=0.0)
        self.add_param('TI', val=0.0)
        self.add_param('hub_height', val=0.0)

        self.add_output('U', val=zeros(num_turb))

    def solve_nonlinear(self, params, unknowns, resids):

        U0 = params['mean_ambient_wind_speed']
        layout_y = params['layout_y']
        layout_x = params['layout_x']
        angle = params['wind_direction']
        nt = num_turb
        r0 = params['rotor_radius']  # Turbine rotor radius
        D = 2.0 * r0
        A = pi * r0 ** 2.0
        ia = params['TI']  # Ambient turbulence intensity according to vanluvanee. 8% on average
        H = params['hub_height']

        def deff(U0):
            return D * sqrt((1.0 + sqrt(1.0 - Ct(U0))) / (2.0 * sqrt(1.0 - Ct(U0))))

        rnb = max(1.08 * D, 1.08 * D + 21.7 * D * (ia - 0.05))
        r95 = 0.5 * (rnb + min(H, rnb))

        def x0(U0):
            return 9.5 * D / ((2.0 * r95 / deff(U0)) ** 3.0 - 1.0)

        def c1(U0):
            return (deff(U0) / 2.0) ** (5.0 / 2.0) * (105.0 / 2.0 / pi) ** (- 1.0 / 2.0) * (Ct(U0) * A * x0(U0)) ** (
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

                if parallel_distance[
                    distance[i][1]] > 0.0:
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

        unknowns['U'] = array(U)


if __name__ == '__main__':
    root = Group()
    root.add('ainslie', AinslieWake1Angle())
    root.add('jensen', JensenWake1Angle())
    root.add('larsen', LarsenWake1Angle())

    # root.add('farm_x', IndepVarComp('x', array([0., 560.0, 1120., 1680., 2240., 2800., 3360., 3920., 4480.])))
    # root.add('farm_y', IndepVarComp('y', array([0., 0., 0., 0., 0., 0., 0., 0., 0.])))
    # root.add('radius', IndepVarComp('radius', 40.0))
    # root.add('U', IndepVarComp('mean', 8.5))
    # root.add('theta', IndepVarComp('angle', 180.0))
    # root.add('factor', IndepVarComp('k', 0.04))
    # root.add('turb', IndepVarComp('intens', 8.0))

    # root.connect('farm_x.x', 'jensen.layout_x')
    # root.connect('farm_x.x', 'ainslie.layout_x')
    # root.connect('farm_y.y', 'jensen.layout_y')
    # root.connect('farm_y.y', 'ainslie.layout_y')
    # root.connect('theta.angle', 'jensen.wind_direction')
    # root.connect('theta.angle', 'ainslie.wind_direction')
    # root.connect('radius.radius', 'jensen.rotor_radius')
    # root.connect('radius.radius', 'ainslie.rotor_radius')
    # root.connect('U.mean', 'jensen.mean_ambient_wind_speed')
    # root.connect('U.mean', 'ainslie.mean_ambient_wind_speed')
    # root.connect('factor.k', 'jensen.k')
    # root.connect('turb.intens', 'ainslie.TI')

    prob = Problem(root)

    prob.setup()

    prob['jensen.layout_x'] = prob['ainslie.layout_x'] = prob['larsen.layout_x'] = array([0., 560.0, 1120., 1680., 2240., 2800., 3360., 3920., 4480.])
    prob['jensen.layout_y'] = prob['ainslie.layout_y'] = prob['larsen.layout_y'] = array([0., 0., 0., 0., 0., 0., 0., 0., 0.])
    prob['jensen.rotor_radius'] = prob['ainslie.rotor_radius'] = prob['larsen.rotor_radius'] = 40.0
    prob['jensen.mean_ambient_wind_speed'] = prob['ainslie.mean_ambient_wind_speed'] = prob['larsen.mean_ambient_wind_speed'] = 8.5
    prob['jensen.wind_direction'] = prob['ainslie.wind_direction'] = prob['larsen.wind_direction'] = 180.0
    prob['jensen.k'] = 0.04
    prob['ainslie.TI'] = 8.0
    prob['larsen.TI'] = 0.08
    prob['larsen.hub_height'] = 100.0

    prob.run()

    result1 = prob['jensen.U']
    result2 = prob['ainslie.U']
    result3 = prob['larsen.U']

    print 'Jensen: {0}\n'.format(result1)
    print 'Ainslie: {0}\n'.format(result2)
    print 'Larsen: {0}\n'.format(result3)
