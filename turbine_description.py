from math import sqrt

number_turbines_per_cable = [5, 9]
voltage = 33000.0
rated_power = 5000000.0
rated_current = rated_power / (sqrt(3) * voltage)  # A = Power / sqrt(3) / Voltage. 3 phase.


def read_cablelist():
    cables_info = []
    with open("/home/sebasanper/PycharmProjects/owf_MDAO/costs/investment_costs/BOS_cost/cable_cost/cable_list.dat",
              "r") as cables:
        next(cables)
        for line in cables:
            cols = line.split()
            cables_info.append([float(cols[0]), float(cols[1]), float(cols[2])])
    return cables_info
