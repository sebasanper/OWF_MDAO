from copy import deepcopy

# all_routes = {1: [[[0, 7], [7, 6], [7, 2], [2, 1]], [[0, 8], [8, 3]], [[0, 9], [9, 10], [9, 4], [4, 5]], [[0, 12], [12, 11]], [[0, 13]], [[0, 14], [14, 15]], [[0, 17], [17, 22], [17, 16], [16, 21]], [[0, 18], [18, 23]], [[0, 19], [19, 24], [19, 20], [20, 25]]]}

# red_routes = {1: [[[7, 0], [6, 7]], [17, 0], [9, 0], [19, 0]]}

# blue_routes = deepcopy(all_routes)


def current_turbine(tree):
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

    counter = {n: 1 for n in a}

    for n in a:
        for m in a:
            if [n, m] in line or [m, n] in line:
                if [n, m] in line:
                    line.remove([n, m])
                    counter[m] += counter[n]
                if [m, n] in line:
                    line.remove([m, n])
                    counter[m] += counter[n]

    return counter


if __name__ == '__main__':
    # line = [[0, 7], [7, 6], [7, 2], [2, 1]]
    # print current_turbine(line)

    all_lines = [[[0, 7], [7, 6], [7, 2], [2, 1]], [[0, 8], [8, 3]], [[0, 9], [9, 10], [9, 4], [4, 5]], [[0, 12], [12, 11]], [[0, 13]], [[0, 14], [14, 15]], [[0, 17], [17, 22], [17, 16], [16, 21]], [[0, 18], [18, 23]], [[0, 19], [19, 24], [19, 20], [20, 25]]]

    max_counter = [0.0 for _ in range(4)]
    for line in all_lines:
        dictionary = current_turbine(line)
        print dictionary
        for i in range(4):
            for key in dictionary:
                if dictionary[key] == i + 1 and key != 0:
                    max_counter[i] += 1
    print
    print max_counter
