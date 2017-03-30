from copy import deepcopy
from random import randint
from Cables_cost_topology import number_turbines_per_cable, current_turbine, read_cablelist

cables_info = read_cablelist()
Cable_area = []
for number in number_turbines_per_cable:
    for cable in cables_info:
        if current_turbine * number <= cable[1]:
            Cable_area.append([number, cable[0] / 1000000.0])
            break
print Cable_area


def infield_efficiency(topology, wt_list, powers):

    def current_turbine(tree, coord):
        line2 = deepcopy(tree)

        def find_next(number, branch, outl):
            next_turbine = number
            for item in branch:
                if number == item[0]:
                    outl.append(item[1])
                    branch.remove(item)
                    next_turbine = item[1]
                elif number == item[1]:
                    outl.append(item[0])
                    branch.remove(item)
                    next_turbine = item[0]
            return next_turbine, branch, outl

        def find_ends(branch2):
            branch = deepcopy(branch2)
            all_elements = [item[i] for i in range(2) for item in branch]
            values = list(set(all_elements))
            values.remove(0)
            out_list = []
            for value in values:
                if all_elements.count(value) == 1:
                    out_list.append([value])
                    for i in range(10):
                        value, branch, out_list[-1] = find_next(value, branch, out_list[-1])
            return out_list

        tree_branches = find_ends(line2)

        def sort_branches(routes):
            routes.sort(key=lambda s: len(s))
            if routes[-1][-1] != 0:
                for item in routes:
                    if item[-1] == 0:
                        routes.append(routes.pop(routes.index(item)))
            return routes

        sort_branches(tree_branches)

        all_elements = [item[i] for item in tree_branches for i in range(len(item))]

        def remove_dup(seq):
            seen = set()
            seen_add = seen.add
            return [x for x in seq if not (x in seen or seen_add(x))]

        def distance(t1, t2):
            return ((t1[1] - t2[1]) ** 2.0 + (t1[2] - t2[2]) ** 2.0) ** 0.5

        a = list(reversed(remove_dup(reversed(all_elements))))
        # print a
        counter = {n: [1, 0.0] for n in a}

        for n in a:
            for m in a:
                if [n, m] in line2 or [m, n] in line2:
                    if [n, m] in line2:
                        line2.remove([n, m])
                        counter[m][0] += counter[n][0]
                        counter[n][1] = distance(coord[n - 1], coord[m - 1])
                    if [m, n] in line2:
                        line2.remove([m, n])
                        counter[m][0] += counter[n][0]
                        counter[n][1] = distance(coord[n - 1], coord[m - 1])
                        # TODO solve distances of individual cables per number of turbines connected.

        return counter

    all_lines = topology[1]

    max_counter = [[0.0, []] for _ in range(10)]

    for line in all_lines:
        amount = current_turbine(line, wt_list)
        for i in range(10):
            for key in amount:
                if amount[key][0] == i + 1 and key != 0:
                    max_counter[i][0] += amount[key][1]
                    max_counter[i][1].append(key)
    # Provides the length of cables that carry the current
    #  of that number of turbines, and their ID. Index one is for one turbine, etc.

    current_squared_cables = [0.00 for _ in range(len(max_counter))]
    for i in range(len(max_counter)):
        for turbine in max_counter[i][1]:
            current_squared_cables[i] += (i + 1) ** 2.0 * (151.51 * powers[turbine - 1] / 2000.0) ** 2.0
            #  Assumed linear current with power.

    losses = []  # Expresed in W.
    for i in range(len(max_counter)):
        if i <= number_turbines_per_cable[0] - 1:
            losses.append(max_counter[i][0] * 1.74e-8 / Cable_area[0][1] * current_squared_cables[i])
        elif i <= number_turbines_per_cable[1] - 1:
            losses.append(max_counter[i][0] * 1.74e-8 / Cable_area[1][1] * current_squared_cables[i])

    print sum(powers) * 1000.0  # Expressed in kW originally.
    print sum(losses)
    efficiency = (1.0 - sum(losses) / (sum(powers) * 1000.0)) * 100.0
    return efficiency

    # TODO: make function, input is cable topology, powers, output is losses (efficiency).

if __name__ == '__main__':
    turbines = [[0, 0.0, 0.0], [1, 0.0, 100.0], [2, 0.0, 200.0], [3, 0.0, 300.0], [4, 0.0, 400.0], [5, 100.0, 0.0], [6, 100.0, 100.0], [7, 100.0, 200.0], [8, 100.0, 300.0], [9, 100.0, 400.0], [10, 200.0, 0.0], [11, 200.0, 100.0], [12, 200.0, 200.0], [13, 200.0, 300.0], [14, 200.0, 400.0], [15, 300.0, 0.0], [16, 300.0, 100.0], [17, 300.0, 200.0], [18, 300.0, 300.0], [19, 300.0, 400.0], [20, 400.0, 0.0], [21, 400.0, 100.0], [22, 400.0, 200.0], [23, 400.0, 300.0], [24, 400.0, 400.0]]
    topology_infield = {1: [[[0, 7], [7, 6], [7, 2], [2, 1]], [[0, 8], [8, 3]], [[0, 9], [9, 10], [9, 4], [4, 5]], [[0, 12], [12, 11]], [[0, 13]], [[0, 14], [14, 15]], [[0, 17], [17, 22], [17, 16], [16, 21]], [[0, 18], [18, 23]], [[0, 19], [19, 24], [19, 20], [20, 25]]]}
    power_farm = [842.6954395776356, 842.6954395776356, 842.6954395776356, 842.6954395776356, 842.6954395776356, 842.6954395776356, 842.6954395776356, 842.6954395776356, 842.6954395776356, 842.6954395776356, 833.5933152665184, 833.5933152664893, 842.6954395776356, 842.6954395776356, 842.6954395776356, 800.6556940215178, 833.5933152664747, 842.6954395776356, 842.6954395776356, 842.6954395776356, 800.6556940215178, 833.5933152665184, 842.6954395776356, 842.6954395776356, 842.6954395776356]

    print infield_efficiency(topology_infield, turbines, power_farm), " %"
