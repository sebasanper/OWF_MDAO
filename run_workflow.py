from workflow import Workflow
# from joblib import Parallel, delayed

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


def study(a, b, c, d, e, f, g, h, i, j, layout_input_file, output3):
    if f == g == h == i == j == 0:
        print a, b, c, d, e
    workflow1 = Workflow(weibullmodels[i], windrosemodels[b], turbmodels[c], None, depthmodels[h], farm_support_cost_models[j], None, oandm, cablemodels[d], infield_efficiency, thrust_coefficient, thrustmodels[f], wakemodels[a], mergingmodels[e], power, powermodels[g], aep_average, other_costs, total_costs, LPC)

    # nbins = randint(2, 25)
    # real_angle = choice([30.0, 60.0, 90.0, 120.0, 180.0])
    # artif_angle = 400.0
    # while artif_angle > real_angle:
    #     artif_angle = choice([1.0, 2.0, 5.0, 10.0, 15.0, 30.0, 60.0, 90.0, 120.0, 180.0])
    nbins = 17
    real_angle = 30.0
    artif_angle = 1.0

    workflow1.windrose.nbins = nbins
    workflow1.windrose.artificial_angle = artif_angle
    workflow1.windrose.real_angle = real_angle
    workflow1.print_output = True
    workflow1.run(layout_input_file)
    power2.reset()
    thrust_coefficient2.reset()
    with open(output3, "a", 1) as output2:
        output2.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(a, b, c, d, e, f, g, h, i, j, workflow1.aep, workflow1.finance, workflow1.runtime, workflow1.power_calls, workflow1.thrust_calls, nbins, real_angle, artif_angle))
    # return workflow1.aep, workflow1.finance, runtime


def run_study(layout_input_file, output_file):
    start1 = time()
    Parallel(n_jobs=-2)(delayed(study)(a, b, c, d, e, f, g, h, i, j, layout_input_file, output_file) for a in range(4, 5) for b in range(3) for c in range(6) for d in range(4) for e in range(4) for f in range(4) for g in range(5) for h in range(4) for i in range(2) for j in range(2))
    print time() - start1


def prueba_study(layout_input_file, output_file):
    start1 = time()
    study(3,	1,	1	,1	,1	,1,	1	,1	,1,	1, layout_input_file, output_file)

    print time() - start1

    # return workflow1.aep, workflow1.finance, runtime


if __name__ == '__main__':
    # run_study(15, "coords2.dat", "coords2_15bins")
    # run_study(25, "coords2.dat", "coords2_25bins")
    # run_study(15, "layout_creator/reg3x5.dat", "coords2_15bins")
    # run_study(25, "layout_creator/reg3x5.dat", "coords2_25bins")
    # run_study(15, "layout_creator/random_layout3.dat", "random3_15bins")
    # run_study(25, "layout_creator/random_layout3.dat", "random3_25bins")
    # run_study(15, "layout_creator/random_layout4.dat", "random4_15bins")
    # run_study(25, "layout_creator/random_layout4.dat", "random4_25bins")
    # run_study("coords3x3.dat", "coords3x3_full_cython_ainslie2D_random.dat")
    prueba_study("coords3x3.dat", "coords3x3_test.dat")
