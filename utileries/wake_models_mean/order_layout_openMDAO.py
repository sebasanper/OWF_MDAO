import numpy as np
from numpy import array

from openmdao.api import Component, IndepVarComp, Group, Problem

from utileries.wake_models_mean import nt
from wake import distance_to_front


class OrderLayout(Component):
    def __init__(self):
        super(OrderLayout, self).__init__()
        self.add_param('layout_x', val=np.zeros(nt))
        self.add_param('layout_y', val=np.zeros(nt))
        self.add_param('angle', val=0.0)
        self.add_output('ordered_layout_x', val=np.zeros(nt))
        self.add_output('ordered_layout_y', val=np.zeros(nt))
        self.add_output('turbine_index', val=np.zeros(nt))

    def solve_nonlinear(self, params, unknowns, resids):
        layout_x = params['layout_x']
        layout_y = params['layout_y']
        angle = params['angle']
        distance = [[] for _ in range(nt)]

        for tur in range(nt):
            distance[tur] = [distance_to_front(layout_x[tur], layout_y[tur], angle), tur, layout_x[tur], layout_y[tur]]
        distance.sort()

        unknowns['turbine_index'] = array([x[1] for x in distance])
        unknowns['ordered_layout_x'] = array([x[2] for x in distance])
        unknowns['ordered_layout_y'] = array([x[3] for x in distance])

if __name__ == '__main__':
    # nt = 9
    root = Group()
    root.add('farm_x', IndepVarComp('x', array([0., 560., 1120., 1680., 2240., 2800., 3360., 3920., 4480.])))
    root.add('farm_y', IndepVarComp('y', array([0., 0., 0., 0., 0., 0., 0., 0., 0.])))
    root.add('theta', IndepVarComp('angle', 0.0))
    root.add('order', OrderLayout())

    root.connect('farm_x.x', 'order.layout_x')
    root.connect('farm_y.y', 'order.layout_y')
    root.connect('theta.angle', 'order.angle')

    prob = Problem(root)
    prob.setup()
    prob.run()

    result1 = prob['order.ordered_layout_x']
    result3 = prob['order.turbine_index']

    print result1
    print result3
