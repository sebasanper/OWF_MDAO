import pyOpt
from pyOpt.pyNSGA2.pyNSGA2 import NSGA2
import call_workflow_once as wf
fitness = wf.score_median_workflow


def objfun(x):
    f = fitness(x)
    g = x[2] - x[1]
    fail = 0
    return f, g, fail

opt_prob = pyOpt.Optimization('My problem', objfun)

opt_prob.addObj('f')

opt_prob.addVar('nbins', type='i', lower=2, upper=25)
opt_prob.addVar('angle_real', type='d', value=0, choices=[30.0, 60.0, 90.0, 120.0, 180.0])
opt_prob.addVar('angle_artif', type='d', value=0, choices=[1.0, 2.0, 5.0, 10.0, 15.0, 30.0, 60.0, 90.0, 120.0, 180.0])

opt_prob.addVar('a', type='d', value=0, choices=range(3))
opt_prob.addVar('b', type='d', value=0, choices=range(3))
opt_prob.addVar('c', type='d', value=0, choices=range(6))
opt_prob.addVar('d', type='d', value=0, choices=range(4))
opt_prob.addVar('e', type='d', value=0, choices=range(4))
opt_prob.addVar('f', type='d', value=0, choices=range(4))
opt_prob.addVar('g', type='d', value=0, choices=range(5))
opt_prob.addVar('h', type='d', value=0, choices=range(4))
opt_prob.addVar('i', type='d', value=0, choices=range(2))
opt_prob.addVar('j', type='d', value=0, choices=range(2))

opt_prob.addCon('angles', type='i')

# print(opt_prob)

nsga2 = NSGA2(store_hst=True)

nsga2.__solve__(opt_prob)
