number_turbines_per_cable = [5]
current_turbine = 151.5151


def read_cablelist():
    cables_info = []
    with open("/home/sebasanper/PycharmProjects/owf_MDAO/costs/investment_costs/BOS_cost/cable_cost/cable_list.dat",
              "r") as cables:
        next(cables)
        for line in cables:
            cols = line.split()
            cables_info.append([float(cols[0]), float(cols[1]), float(cols[2])])
    return cables_info
