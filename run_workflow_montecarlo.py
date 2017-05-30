from workflow import Workflow
from joblib import Parallel, delayed
from memoize import Memoize

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
from farm_energy.wake_model_mean_new.aero_power_ct_models.aero_models import power, thrust_coefficient

from time import time

# a
wakemodels = [constantwake, Jensen, Larsen, Ainslie1D, Ainslie2D]
# b
windrosemodels = [
    "/home/sebasanper/PycharmProjects/owf_MDAO/site_conditions/wind_conditions/weibull_windrose_12unique.dat",
    "/home/sebasanper/PycharmProjects/owf_MDAO/site_conditions/wind_conditions/weibull_windrose_12sameWeibull.dat",
    "/home/sebasanper/PycharmProjects/owf_MDAO/site_conditions/wind_conditions/weibull_windrose_12identical.dat"]
# c
turbmodels = ["ConstantTurbulence", frandsen2, danish_recommendation, frandsen, larsen_turbulence, Quarton]
# d
cablemodels = ["ConstantCable", cable_optimiser, radial_cable, random_cable]
# e
mergingmodels = [root_sum_square, maximum, multiplied, summed]
# f
thrustmodels = ["/home/sebasanper/PycharmProjects/owf_MDAO/farm_energy/wake_model_mean_new/aero_power_ct_models/ConstantThrust.dat", "/home/sebasanper/PycharmProjects/owf_MDAO/farm_energy/wake_model_mean_new/aero_power_ct_models/windsim_ct.dat", "/home/sebasanper/PycharmProjects/owf_MDAO/farm_energy/wake_model_mean_new/aero_power_ct_models/NREL_5MW_C_T_new.txt", "/home/sebasanper/PycharmProjects/owf_MDAO/farm_energy/wake_model_mean_new/aero_power_ct_models/FASTstatistics_ct.dat"]
# g
powermodels = ["/home/sebasanper/PycharmProjects/owf_MDAO/farm_energy/wake_model_mean_new/aero_power_ct_models/ConstantPower.dat", "/home/sebasanper/PycharmProjects/owf_MDAO/farm_energy/wake_model_mean_new/aero_power_ct_models/FASTstatistics_power.dat", "/home/sebasanper/PycharmProjects/owf_MDAO/farm_energy/wake_model_mean_new/aero_power_ct_models/windsim_power.dat", "/home/sebasanper/PycharmProjects/owf_MDAO/farm_energy/wake_model_mean_new/aero_power_ct_models/powercurve.dat", "/home/sebasanper/PycharmProjects/owf_MDAO/farm_energy/wake_model_mean_new/aero_power_ct_models/nrel_cp.dat"]
# h
depthmodels = [Flat, Gaussian, Plane, Rough]
# i
weibullmodels = [MeanWind, WeibullWindBins]
# j
farm_support_cost_models = ["ConstantSupport", farm_support_cost]


def run_monte_carlo_study(nbins, layout_input_file, output_file):
    start1 = time()
    vectors = []

    with open("sampling/monte_carlo_results.dat", "r") as readin:
        for line in readin:
            cols = line.split()
            vectors.append([int(cols[0]), int(cols[1]), int(cols[2]), int(cols[3]), int(cols[4]), int(cols[5]), int(cols[6]), int(cols[7]), int(cols[8]), int(cols[9])])

    Parallel(n_jobs=8)(delayed(monte_carlo_study)(vector, nbins, layout_input_file, output_file) for vector in vectors)

    print time() - start1


def monte_carlo_study(vector, nbins, layout_input_file, output3):
    a = vector[0]
    b = vector[1]
    c = vector[2]
    d = vector[3]
    e = vector[4]
    f = vector[5]
    g = vector[6]
    h = vector[7]
    i = vector[8]
    j = vector[9]
    if f == g == h == i == j == 0:
        print vector

    workflow1 = Workflow(weibullmodels[i], windrosemodels[b], turbmodels[c], None, depthmodels[h], farm_support_cost_models[j], None, oandm, cablemodels[d], infield_efficiency, thrust_coefficient, thrustmodels[f], wakemodels[a], mergingmodels[e], power, powermodels[g], aep_average, other_costs, total_costs, LPC)
    workflow1.windrose.nbins = nbins
    # workflow1.print_output = True
    start = time()
    workflow1.run(layout_input_file)
    runtime = time() - start
    with open(output3, "a", 1) as output2:
        output2.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(a, b, c, d, e, f, g, h, i, j, workflow1.aep, workflow1.finance, runtime))


# monte_carlo_study = Memoize(monte_carlo_study)


if __name__ == '__main__':
    run_monte_carlo_study(15, "coords3x3.dat", "coords3x3_MC10000.dat")
