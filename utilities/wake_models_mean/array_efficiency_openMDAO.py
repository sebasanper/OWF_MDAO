from numpy import array

from openmdao.api import Component, Group, Problem

from farm_energy.layout import read_layout
from power_models import power_v90 as power
from site_conditions.wind_conditions.windrose import read_windrose
from wake_models import jensen_1angle, ainslie_1angle, larsen_1angle


class JensenWindRose(Component):
    def __init__(self):
        super(JensenWindRose, self).__init__()

        self.add_param('layout_x', shape=(9,))
        self.add_param('layout_y', shape=(9,))
        self.add_param('windrose_direction', shape=(4,))
        self.add_param('windrose_speed', shape=(4,))
        self.add_param('windrose_probability', shape=(4,))

        self.add_output('array_efficiency', val=0.0)

    def solve_nonlinear(self, params, unknowns, resids):

        layout_x = params['layout_x']
        layout_y = params['layout_y']
        wind_direction = params['windrose_direction']
        wind_speed = params['windrose_speed']
        wind_frequency = params['windrose_probability']

        efficiency = []
        profit = []
        summation = 0.0
        nt = len(layout_y)
        P = []
        U = []

        efficiency_proportion = []

        for wind in range(len(wind_direction)):
            U0 = wind_speed[wind]  # Free stream wind speed
            angle = wind_direction[wind]
            # angle2 = - 270.0 - angle  # To read windroses where N is 0 and E is 90

            U.append(jensen_1angle(layout_x, layout_y, U0, angle, rotor_radius=40.0, k=0.04))
            P.append([power(u) for u in U[-1]])

            # Farm efficiency
            profit.append(sum(P[-1]))
            efficiency.append(profit[-1] * 100.0 / (float(nt) * max(P[-1])))  # same as using U0
            efficiency_proportion.append(efficiency[-1] * wind_frequency[wind] / 100.0)
            summation += efficiency_proportion[wind]

        # print profit
        # print efficiency
        # print efficiency_proportion
        # print U
        # print P

        unknowns['array_efficiency'] = summation


class AinslieWindRose(Component):
    def __init__(self):
        super(AinslieWindRose, self).__init__()

        self.add_param('layout_x', shape=(9,))
        self.add_param('layout_y', shape=(9,))
        self.add_param('windrose_direction', shape=(4,))
        self.add_param('windrose_speed', shape=(4,))
        self.add_param('windrose_probability', shape=(4,))

        self.add_output('array_efficiency', val=0.0)

    def solve_nonlinear(self, params, unknowns, resids):
        layout_x = params['layout_x']
        layout_y = params['layout_y']
        wind_direction = params['windrose_direction']
        wind_speed = params['windrose_speed']
        wind_frequency = params['windrose_probability']

        efficiency = []
        profit = []
        summation = 0.0
        nt = len(layout_y)
        P = []
        U = []

        efficiency_proportion = []

        for wind in range(len(wind_direction)):
            U0 = wind_speed[wind]  # Free stream wind speed
            angle = wind_direction[wind]
            # angle2 = - 270.0 - angle  # To read windroses where N is 0 and E is 90

            U.append(ainslie_1angle(layout_x, layout_y, U0, angle, rotor_radius=40.0, TI=0.08))
            P.append([power(u) for u in U[-1]])

            # Farm efficiency
            profit.append(sum(P[-1]))
            efficiency.append(profit[-1] * 100.0 / (float(nt) * max(P[-1])))  # same as using U0
            efficiency_proportion.append(efficiency[-1] * wind_frequency[wind] / 100.0)
            summation += efficiency_proportion[wind]

        # print profit
        # print efficiency
        # print efficiency_proportion
        # print U
        # print P

        unknowns['array_efficiency'] = summation


class LarsenWindRose(Component):
    def __init__(self):
        super(LarsenWindRose, self).__init__()

        self.add_param('layout_x', shape=(9,))
        self.add_param('layout_y', shape=(9,))
        self.add_param('windrose_direction', shape=(4,))
        self.add_param('windrose_speed', shape=(4,))
        self.add_param('windrose_probability', shape=(4,))

        self.add_output('array_efficiency', val=0.0)

    def solve_nonlinear(self, params, unknowns, resids):
        layout_x = params['layout_x']
        layout_y = params['layout_y']
        wind_direction = params['windrose_direction']
        wind_speed = params['windrose_speed']
        wind_frequency = params['windrose_probability']

        efficiency = []
        profit = []
        summation = 0.0
        nt = len(layout_y)
        P = []
        U = []

        efficiency_proportion = []

        for wind in range(len(wind_direction)):
            U0 = wind_speed[wind]  # Free stream wind speed
            angle = wind_direction[wind]
            # angle2 = - 270.0 - angle  # To read windroses where N is 0 and E is 90

            U.append(larsen_1angle(layout_x, layout_y, U0, angle, rotor_radius=40.0, hub_height=100.0, TI=0.08))
            P.append([power(u) for u in U[-1]])

            # Farm efficiency
            profit.append(sum(P[-1]))
            efficiency.append(profit[-1] * 100.0 / (float(nt) * max(P[-1])))  # same as using U0
            efficiency_proportion.append(efficiency[-1] * wind_frequency[wind] / 100.0)
            summation += efficiency_proportion[wind]

        # print profit
        # print efficiency
        # print efficiency_proportion
        # print U
        # print P

        unknowns['array_efficiency'] = summation


if __name__ == '__main__':
    layout_x, layout_y = read_layout('coordinates.dat')
    windrose_direction, windrose_speed, windrose_probability = read_windrose('windrose.dat')
    root = Group()
    root.add('jensen', JensenWindRose())
    root.add('ainslie', AinslieWindRose())
    root.add('larsen', LarsenWindRose())

    prob = Problem(root)
    prob.setup()
    prob['jensen.layout_x'] = prob['ainslie.layout_x'] = prob['larsen.layout_x'] = array(layout_x)
    prob['jensen.layout_y'] = prob['ainslie.layout_y'] = prob['larsen.layout_y'] = array(layout_y)
    prob['jensen.windrose_direction'] = prob['ainslie.windrose_direction'] = prob['larsen.windrose_direction'] = array(windrose_direction)
    prob['jensen.windrose_speed'] = prob['ainslie.windrose_speed'] = prob['larsen.windrose_speed'] = array(windrose_speed)
    prob['jensen.windrose_probability'] = prob['ainslie.windrose_probability'] = prob['larsen.windrose_probability'] = array(windrose_probability)

    prob.run()

    efficiency_jensen = prob['jensen.array_efficiency']
    efficiency_ainslie = prob['ainslie.array_efficiency']
    efficiency_larsen = prob['larsen.array_efficiency']

    print 'Jensen'
    print efficiency_jensen
    print
    print 'Ainslie'
    print efficiency_ainslie
    print
    print 'Larsen'
    print efficiency_larsen
