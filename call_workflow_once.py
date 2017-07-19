from workflow import Workflow
from joblib import Parallel, delayed

from site_conditions.wind_conditions.windrose import MeanWind, WeibullWindBins
from costs.investment_costs.BOS_cost.cable_cost.cable_cost_models import cable_optimiser, radial_cable, random_cable
from costs.investment_costs.BOS_cost.cable_cost.cable_efficiency import infield_efficiency
from costs.OM_costs.om_models import oandm
from costs.investment_costs.BOS_cost.support_cost.farm_support_cost import farm_support_cost
from finance.finance_models import LPC
from farm_energy.AEP.aep import aep_average
from costs.other_costs import other_costs
from costs.total_costs import total_costs
# from farm_energy.wake_model_mean_new.aero_power_ct_models.thrust_coefficient import ct_v80
from farm_energy.wake_model_mean_new.wake_turbulence_models import frandsen2, danish_recommendation, frandsen, \
    larsen_turbulence, Quarton
from site_conditions.terrain.terrain_models import Flat, Plane, Rough, Gaussian
from farm_energy.wake_model_mean_new.downstream_effects import JensenEffects as Jensen, LarsenEffects as Larsen, Ainslie1DEffects as Ainslie1D, Ainslie2DEffects as Ainslie2D, constantwake
from farm_energy.wake_model_mean_new.wake_overlap import root_sum_square, maximum, multiplied, summed
from farm_energy.wake_model_mean_new.aero_power_ct_models.aero_models import power, thrust_coefficient, power2, thrust_coefficient2

from time import time
from random import randint, choice
import numpy as np
from statistics import mode


# a - 1
wakemodels = [constantwake, Jensen, Larsen, Ainslie1D, Ainslie2D]
# b - 2
windrosemodels = [
    "/home/sebasanper/PycharmProjects/owf_MDAO/site_conditions/wind_conditions/weibull_windrose_12unique.dat",
    "/home/sebasanper/PycharmProjects/owf_MDAO/site_conditions/wind_conditions/weibull_windrose_12sameWeibull.dat",
    "/home/sebasanper/PycharmProjects/owf_MDAO/site_conditions/wind_conditions/weibull_windrose_12identical.dat"]
# c - 3
turbmodels = ["ConstantTurbulence", frandsen2, danish_recommendation, frandsen, larsen_turbulence, Quarton]
# d - 4
cablemodels = ["ConstantCable", cable_optimiser, radial_cable, random_cable]
# e - 5
mergingmodels = [root_sum_square, maximum, multiplied, summed]
# f - 6
thrustmodels = ["/home/sebasanper/PycharmProjects/owf_MDAO/farm_energy/wake_model_mean_new/aero_power_ct_models/ConstantThrust.dat", "/home/sebasanper/PycharmProjects/owf_MDAO/farm_energy/wake_model_mean_new/aero_power_ct_models/windsim_ct.dat", "/home/sebasanper/PycharmProjects/owf_MDAO/farm_energy/wake_model_mean_new/aero_power_ct_models/NREL_5MW_C_T_new.txt", "/home/sebasanper/PycharmProjects/owf_MDAO/farm_energy/wake_model_mean_new/aero_power_ct_models/FASTstatistics_ct.dat"]
# g - 7
powermodels = ["/home/sebasanper/PycharmProjects/owf_MDAO/farm_energy/wake_model_mean_new/aero_power_ct_models/ConstantPower.dat", "/home/sebasanper/PycharmProjects/owf_MDAO/farm_energy/wake_model_mean_new/aero_power_ct_models/FASTstatistics_power.dat", "/home/sebasanper/PycharmProjects/owf_MDAO/farm_energy/wake_model_mean_new/aero_power_ct_models/windsim_power.dat", "/home/sebasanper/PycharmProjects/owf_MDAO/farm_energy/wake_model_mean_new/aero_power_ct_models/powercurve.dat", "/home/sebasanper/PycharmProjects/owf_MDAO/farm_energy/wake_model_mean_new/aero_power_ct_models/nrel_cp.dat"]
# h - 8
depthmodels = [Flat, Gaussian, Plane, Rough]
# i - 9
weibullmodels = [MeanWind, WeibullWindBins]
# j - 10
farm_support_cost_models = ["ConstantSupport", farm_support_cost]


def call_workflow_once(nbins, real_angle, artif_angle, a, b, c, d, e, f, g, h, i, j):
    workflow1 = Workflow(weibullmodels[i], windrosemodels[b], turbmodels[c], None, depthmodels[h], farm_support_cost_models[j], None, oandm, cablemodels[d], infield_efficiency, thrust_coefficient, thrustmodels[f], wakemodels[a], mergingmodels[e], power, powermodels[g], aep_average, other_costs, total_costs, LPC)
    layout_input_file = "coords3x3.dat"
    # nbins = randint(2, 25)
    # real_angle = choice([30.0, 60.0, 90.0, 120.0, 180.0])
    # artif_angle = 400.0

    workflow1.windrose.nbins = nbins
    workflow1.windrose.artificial_angle = artif_angle
    workflow1.windrose.real_angle = real_angle
    # workflow1.print_output = True
    workflow1.run(layout_input_file)
    power2.reset()
    thrust_coefficient2.reset()
    return workflow1.aep, workflow1.finance, workflow1.runtime, workflow1.power_calls, workflow1.thrust_calls


def reject_outliers(data, m=5.189):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else 0.
    return data[s<m]


def score_median_workflow(combination):
    nbins = combination[0]
    real_angle = combination[1]
    artif_angle = combination[2]
    a = combination[3]
    b = combination[4]
    c = combination[5]
    d = combination[6]
    e = combination[7]
    f = combination[8]
    g = combination[9]
    h = combination[10]
    i = combination[11]
    j = combination[12]

    aeps = []
    finances = []
    runtimes = []
    n_power_calls = []
    n_thrust_calls = []

    for _ in range(5):
        results = call_workflow_once(nbins, real_angle, artif_angle, a, b, c, d, e, f, g, h, i, j)
        aeps.append(results[0])
        finances.append(results[1])
        runtimes.append(results[2])
        n_power_calls.append(results[3])
        n_thrust_calls.append(results[4])
    runtimes = reject_outliers(np.array(runtimes))

    # return np.mean(aeps), np.mean(finances), np.mean(runtimes), mode(n_power_calls), mode(n_thrust_calls)
    return np.mean(finances), np.mean(runtimes), mode(n_power_calls), mode(n_thrust_calls)

if __name__ == '__main__':
    a = 2
    b = 0
    c = 3
    d = 3
    e = 2
    f = 0
    g = 2
    h = 2
    i = 0
    j = 0
    print(score_median_workflow([3, 30.0, 90.0, a, b, c, d, e, f, g, h, i, j]))
