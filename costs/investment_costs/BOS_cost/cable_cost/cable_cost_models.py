from numpy import sqrt
from Hybrid import set_cable_topology
L = 2000.0


def layout_prepare(layout_file):
    turbines_list = []
    with open(layout_file, "r") as infile:
        i = 0
        for line in infile:
            i += 1
            col = line.split()
            turbines_list.append([i, col[0], col[1]])
    turbines_list = []
    return turbines_list


def cable_cost2D(coordinates_turbine, coordinates_platform, turbines_per_cable):
    cable_length = 0.0
    for i in range(len(coordinates_turbine)):
        cable_length += sqrt((coordinates_platform[0] - coordinates_turbine[i][0]) ** 2.0 + (coordinates_platform[1] - coordinates_turbine[i][1]) ** 2.0)
    cable_length / turbines_per_cable
    cost_per_m = 200.0
    return cost_per_m * cable_length


def cable_optimisation(WT_List):
    central_platform_locations = [[0, 1000]]
    Cable_List = [[2, 200.0]]
    Crossing_penalty = 0
    Area = []
    Transmission = []

    cost_infield_cables = set_cable_topology(WT_List, central_platform_locations, Cable_List, Area, Transmission, Crossing_penalty)
    return cost_infield_cables


if __name__ == '__main__':
    l = cable_cost2D([[0.0, 2000.0], [0.0, 0.0]], [0, 1000], 2)
    m = cable_optimisation([[0, 0.0, 2000.0], [1, 0.0, 0.0]])
    print l
    print m