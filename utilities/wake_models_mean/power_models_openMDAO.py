from math import pi, ceil, floor
from util import interpolate
from openmdao.api import Component, Group, Problem


class PowerCurvev90(Component):

    def __init__(self):
        super(PowerCurvev90, self).__init__()

        self.add_param('wind_speed', val=0.0)

        self.add_output('power', val=0.0)

    def solve_nonlinear(self, params, unknowns, resids):

        u0 = params['wind_speed']

        if u0 < 4.0:
            p = 0.0
        elif u0 <= 25.0:
            p = 3.234808e-4 * u0 ** 7.0 - 0.0331940121 * u0 ** 6.0 + 1.3883148012 * u0 ** 5.0 - 30.3162345004 * u0 ** 4.0 + 367.6835557011 * u0 ** 3.0 - 2441.6860655008 * u0 ** 2.0 + 8345.6777042343 * u0 - 11352.9366182805
        else:
            p = 0.0

        unknowns['power'] = p


class PowerBladedNREL5MW(Component):

    def __init__(self):
        super(PowerBladedNREL5MW, self).__init__()

        self.add_param('wind_speed', val=0.0)

        self.add_output('power', val=0.0)

    def solve_nonlinear(self, params, unknowns, resids):

        u0 = params['wind_speed']

        if u0 < 4.0:
            p = 0.0
        else:
            p = 0.5 * 61.0 ** 2.0 * pi * 1.225 * 0.485 * u0 ** 3.0

        unknowns['power'] = p / 1000.0


class PowerLLTNREL5MW(Component):

    def __init__(self):
        super(PowerLLTNREL5MW, self).__init__()

        self.add_param('wind_speed', val=0.0)

        self.add_output('power', val=0.0)

    def solve_nonlinear(self, params, unknowns, resids):

        U0 = params['wind_speed']

        def power_table_LLT(U0):
            v = U0
            if v == 7: return 970.0
            if v == 8: return 1780.0
            if v == 9: return 2770.0
            if v == 10: return 3910.0
            if v == 11: return 5190.0

        if ceil(U0) == floor(U0):
            p = power_table_LLT(U0)
        else:
            p = interpolate(floor(U0), power_table_LLT(floor(U0)), ceil(U0), power_table_LLT(ceil(U0)), U0)

        unknowns['power'] = p

if __name__ == '__main__':
    root = Group()
    root.add('bladed', PowerBladedNREL5MW())
    prob = Problem(root)

    prob.setup()

    prob['bladed.wind_speed'] = 10.1

    prob.run()

    result1 = prob['bladed.power']

    print 'Bladed 5MW: {0} MW \n'.format(result1/1000.0)
