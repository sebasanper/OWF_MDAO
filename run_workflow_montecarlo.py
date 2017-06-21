from workflow import Workflow
from joblib import Parallel, delayed
# from memoize import Memoize

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


def run_monte_carlo_study(n_samples, layout_input_file):
    vectors = []
    nbins = randint(2, 25)
    real_angle = choice([30.0, 60.0, 90.0, 120.0, 180.0])
    artif_angle = 400.0
    while artif_angle > real_angle:
        artif_angle = choice([1.0, 2.0, 5.0, 10.0, 15.0, 30.0, 60.0, 90.0, 120.0, 180.0])

    now = localtime()
    output_file = "results/coords3x3/coords3x3_MC" + str(n_samples) + "_m" + str(now[1]) + "_d" + str(now[2]) + "_h" + str(now[3]) + "_m" + str(now[4]) + "_s" + str(now[5]) + ".dat"

    with open(output_file, "a", 1) as output2:
        output2.write("# Weibullbins: {}\tNumberSamples: {}\tRealAngles: {}\tArtificialAngles: {}\n".format(nbins, n_samples, real_angle, artif_angle))

    for n in range(n_samples):
        vectors.append([randint(0, 4), randint(0, 2), randint(0, 5), randint(0, 3), randint(0, 3), randint(0, 3), randint(0, 4), randint(0, 3), randint(0, 1), randint(0, 1)])
    start1 = time()
    # for vector in vectors:
    #     monte_carlo_study(vector, nbins, layout_input_file, output_file)
    Parallel(n_jobs=8)(delayed(monte_carlo_study)(vector, nbins, real_angle, artif_angle, layout_input_file, output_file) for vector in vectors)

    print time() - start1


def monte_carlo_study(vector, layout_input_file, output3):

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

    workflow1 = Workflow(weibullmodels[i], windrosemodels[b], turbmodels[c], None, depthmodels[h], farm_support_cost_models[j], None, oandm, cablemodels[d], infield_efficiency, thrust_coefficient, thrustmodels[f], wakemodels[a], mergingmodels[e], power, powermodels[g], aep_average, other_costs, total_costs, LPC)

    nbins = randint(2, 25)
    real_angle = choice([30.0, 60.0, 90.0, 120.0, 180.0])
    artif_angle = 400.0
    while artif_angle > real_angle:
        artif_angle = choice([1.0, 2.0, 5.0, 10.0, 15.0, 30.0, 60.0, 90.0, 120.0, 180.0])

    workflow1.windrose.nbins = nbins
    workflow1.windrose.artificial_angle = artif_angle
    workflow1.windrose.real_angle = real_angle
    # workflow1.print_output = True
    workflow1.run(layout_input_file)
    p = workflow1.power_calls
    t = workflow1.thrust_calls
    power2.reset()
    thrust_coefficient2.reset()
    with open(output3, "a", 1) as output2:
        output2.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(a, b, c, d, e, f, g, h, i, j, workflow1.aep, workflow1.finance, workflow1.runtime, p, t, nbins, real_angle, artif_angle))


if __name__ == '__main__':
    from time import localtime
    from email_code import send_message

    def run_monte_carlo_study(n_samples, layout_input_file):
        vectors = []

        now = localtime()
        output_file = "results/coords3x3/coords3x3_MC" + str(n_samples) + "_m" + str(now[1]) + "_d" + str(now[2]) + "_h" + str(now[3]) + "_m" + str(now[4]) + "_s" + str(now[5]) + ".dat"

        for n in range(n_samples):
            vectors.append([randint(0, 4), randint(0, 2), randint(0, 5), randint(0, 3), randint(0, 3), randint(0, 3), randint(0, 4), randint(0, 3), randint(0, 1), randint(0, 1)])
        start1 = time()
        parallel(delayed(monte_carlo_study)(vector, layout_input_file, output_file) for vector in vectors)

        print time() - start1

    with Parallel(n_jobs=-1, verbose=3) as parallel:
        run_monte_carlo_study(100, "coords3x3.dat")
        print localtime()
        send_message("MC 100 ready")
        run_monte_carlo_study(1000, "coords3x3.dat")
        print localtime()
        send_message("MC 1000 ready")
        run_monte_carlo_study(10000, "coords3x3.dat")
        print localtime()
        send_message("MC 10000 ready")
        run_monte_carlo_study(100000, "coords3x3.dat")
        print localtime()
        send_message("MC 100000 ready")
        run_monte_carlo_study(2500, "coords3x3.dat")
        print localtime()
        send_message("MC 2500 ready")
        run_monte_carlo_study(50000, "coords3x3.dat")
        print localtime()
        send_message("MC 50000 ready")
        run_monte_carlo_study(5000, "coords3x3.dat")
        print localtime()
        send_message("MC 5000 ready")
        run_monte_carlo_study(7500, "coords3x3.dat")
        print localtime()
        send_message("MC 7500 ready")
        run_monte_carlo_study(25000, "coords3x3.dat")
        print localtime()
        send_message("MC 25000 ready")
        run_monte_carlo_study(75000, "coords3x3.dat")
        print localtime()
        send_message("MC 75000 ready")
