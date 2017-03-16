from copy import deepcopy

all_routes = [[[0, 7], [7, 6], [7, 2], [2, 1]], [[0, 8], [8, 3]], [[0, 9], [9, 10], [9, 4], [4, 5]],
              [[0, 12], [12, 11]], [[0, 13]], [[0, 14], [14, 15]], [[0, 17], [17, 22], [17, 16], [16, 21]],
              [[0, 18], [18, 23]], [[0, 19], [19, 24], [19, 20], [20, 25]]]

red_routes = [[7, 0], [17, 0], [9, 0], [19, 0]]

blue_routes = deepcopy(all_routes)

for red in red_routes:
    for i in range(len(blue_routes)):
        for item in all_routes[i]:
            if red == item:
                # print red, item
                blue_routes[i].remove(item)
                break
            elif red == list(reversed(item)):
                # print i, list(reversed(item))
                # print blue_routes[i]
                blue_routes[i].remove(item)
                break
            break


# print blue_routes


def current_turbine(tree, coord):
    line2 = deepcopy(tree)

    def find_ends(branch):
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

    a = list(reversed(remove_dup(reversed(all_elements))))
    print a
    counter = {n: [1, 0.0] for n in a}

    for n in a:
        for m in a:
            if [n, m] in line or [m, n] in line:
                if [n, m] in line:
                    line.remove([n, m])
                    counter[m][0] += counter[n][0]
                    counter[m][1] = distance(coord[n], coord[m])
                    # print n, m,
                if [m, n] in line:
                    line.remove([m, n])
                    counter[m][0] += counter[n][0]
                    counter[m][1] = distance(coord[n], coord[m])
                    # print m, n, distance(coord[m], coord[n])
                    # TODO solve distances of individual cables per number of turbines connected.

    return counter


if __name__ == '__main__':
    # line = [[0, 7], [7, 6], [7, 2], [2, 1]]
    # print current_turbine(line)

    def distance(t1, t2):
        return ((t1[1] - t2[1]) ** 2.0 + (t1[2] - t2[2]) ** 2.0) ** 0.5

    wt_list = [[0.0, 250.0, 250.0], [1, 0.0, 0.0], [2, 0.0, 100.0], [3, 0.0, 200.0], [4, 0.0, 300.0], [5, 0.0, 400.0], [6, 100.0, 0.0], [7, 100.0, 100.0], [8, 100.0, 200.0], [9, 100.0, 300.0], [10, 100.0, 400.0], [11, 200.0, 0.0], [12, 200.0, 100.0], [13, 200.0, 200.0], [14, 200.0, 300.0], [15, 200.0, 400.0], [16, 300.0, 0.0], [17, 300.0, 100.0], [18, 300.0, 200.0], [19, 300.0, 300.0], [20, 300.0, 400.0], [21, 400.0, 0.0], [22, 400.0, 100.0], [23, 400.0, 200.0], [24, 400.0, 300.0], [25, 400.0, 400.0]]

    all_lines = [[[0, 7], [7, 6], [7, 2], [2, 1]], [[0, 8], [8, 3]], [[0, 9], [9, 10], [9, 4], [4, 5]],
                 [[0, 12], [12, 11]], [[0, 13]], [[0, 14], [14, 15]], [[0, 17], [17, 22], [17, 16], [16, 21]],
                 [[0, 18], [18, 23]], [[0, 19], [19, 24], [19, 20], [20, 25]]]

    max_counter = [0.0 for _ in range(4)]

    for line in all_lines:
        amount = current_turbine(line, wt_list)
        print amount
        for i in range(4):
            for key in amount:
                if amount[key] == i + 1 and key != 0:
                    max_counter[i] += 1
    print
    print max_counter  # Provides the number of cables that carry the current
    #  of that number of turbines. Index one is for one turbine, etc.
