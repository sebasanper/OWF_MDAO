# -----------------------------------------Input Parameters------------------------------------------------------------------
from math import hypot
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from copy import deepcopy
from heapq import heappush, heappop, heapify
import matplotlib.ticker as ticker
from time import time

'Remove and return the lowest priority task. Raise KeyError if empty.'
REMOVED = '<removed-task>'  # placeholder for a removed task

fontsize = 20
fontsize2 = 15
Euro = "eur"
MEuro = "M%s" % Euro


# ---------------------------------------Main--------------------------------------------------------------------------------
def set_cable_topology(WT_List, central_platform_locations, Cable_List, Area, Transmission, Crossing_penalty):
    NT = len(WT_List)
    start = time()
    Wind_turbines = []
    for WT in WT_List:
        Wind_turbines.append([WT[0] + 1, WT[1], WT[2]])
    # initialize the parameters
    Wind_turbinesi, Costi, Cost0i, Costij, Savingsi, Savingsi_finder, Savingsi2, Savingsi2_finder, distancefromsubstationi, substationi, Routingi, Routing_redi, Routing_greeni, Routesi, Capacityi, Cable_Costi, Crossings_finder = dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict()
    i = 1
    for substation in central_platform_locations:
        Wind_turbinesi[i], Costi[i], distancefromsubstationi[i] = initial_values(NT, Wind_turbines, substation)
        substationi[i] = substation
        i += 1
    # splits the Wind_turbines list in the closest substation
    for j in xrange(NT):
        empty = []
        for key, value in distancefromsubstationi.iteritems():
            empty.append(value[j])
        index = empty.index(min(empty, key=lambda x: x[2])) + 1
        Wind_turbinesi[index].append([value[j][1], Wind_turbines[j][1], Wind_turbines[j][2]])
    #        Wind_turbinesi[1]=[x for x in Wind_turbines if x[0]<=118]
    #        Wind_turbinesi[2]=[x for x in Wind_turbines if x[0]>118]
    for j in xrange(len(Cable_List)):
        Capacityi[j + 1] = Cable_List[j][0]
        Cable_Costi[j + 1] = Cable_List[j][1]
    # initialize routes and Saving matrix
    for key, value in Wind_turbinesi.iteritems():
        Routesi[key], Routingi[key], Routing_redi[key], Routing_greeni[key] = initial_routes(value)
        Cost0i[key], Costij[key] = costi(value, substationi[key])
        Savingsi[key], Savingsi_finder[key], Crossings_finder[key] = savingsi(Cost0i[key], Costij[key], value,
                                                                              Cable_Costi[1], substationi[key], Area,
                                                                              Crossing_penalty)
    fig = plt.figure()
    # for area in Area:
    #     plt.plot([area[0][0], area[1][0]], [area[0][1], area[1][1]], color='k', ls='--', linewidth='2')
    # for trans in Transmission:
    #     plt.plot([trans[0][0], trans[1][0]], [trans[0][1], trans[1][1]], color='yellow', linewidth='4')
    cable_length = 0
    total_cost = 0
    crossings = 0
    for key, value in Wind_turbinesi.iteritems():
        Routesi[key], Routingi[key], Routing_redi[key], Routing_greeni[key] = Hybrid(Savingsi[key],
                                                                                     Savingsi_finder[key],
                                                                                     Wind_turbinesi[key], Routesi[key],
                                                                                     Routingi[key], substationi[key],
                                                                                     Capacityi, Routing_redi[key],
                                                                                     Routing_greeni[key], Costi[key],
                                                                                     Cable_Costi, Transmission)
        Savingsi2[key], Savingsi2_finder[key], Crossings_finder[key] = savingsi(Cost0i[key], Costij[key], value,
                                                                                Cable_Costi[1], substationi[key], Area,
                                                                                Crossing_penalty)
        Routesi[key], Routingi[key], Routing_redi[key], Routing_greeni[key] = Esau_Williams_Cable_Choice(Savingsi2[key],
                                                                                                         Savingsi2_finder[
                                                                                                             key],
                                                                                                         Crossings_finder[
                                                                                                             key],
                                                                                                         Wind_turbinesi[
                                                                                                             key],
                                                                                                         Routesi[key],
                                                                                                         Routingi[key],
                                                                                                         substationi[
                                                                                                             key],
                                                                                                         Capacityi,
                                                                                                         Routing_redi[
                                                                                                             key],
                                                                                                         Routing_greeni[
                                                                                                             key],
                                                                                                         Costi[key],
                                                                                                         Cable_Costi, Transmission, Crossing_penalty)
        Routesi[key], Routingi[key] = RouteOpt_Hybrid(Routingi[key], Routing_redi[key], Routing_greeni[key],
                                                      substationi[key], Costi[key], Capacityi, Routesi[key],
                                                      Wind_turbinesi[key], Transmission)
        length, cost, ax = plotting(fig, substationi[key], Wind_turbinesi[key], Routingi[key], Routing_redi[key],
                                    Routing_greeni[key], Capacityi, Cable_Costi)
        cable_length = cable_length + length
        total_cost = total_cost + cost
        for route in Routingi[key]:
            if edge_crossings_area([route[0], route[1]], Wind_turbinesi[key], substationi[key], Area)[0] == True:
                crossings = crossings + \
                            edge_crossings_area([route[0], route[1]], Wind_turbinesi[key], substationi[key], Area)[1]
    return total_cost
    # print 'Cable length = {0} km'.format(round(cable_length / 1000, 3))
    # print 'Cable cost = {0:,} {1}'.format(round(total_cost / 1000000, 3), MEuro)
    # if Area != []:
    #     print 'Crossings = {0}'.format(crossings)
    # print 'Elapsed time = {0:.3f} s'.format(time() - start)
    #     ######Legend######
    # if len(Cable_Costi) == 1:
    #     label1 = mpatches.Patch(color='blue', label='Capacity: {0}'.format(Capacityi[1], round(cable_length / 1000, 3),
    #                                                                        int(total_cost), name))
    #     legend = plt.legend([label1], ["Capacity: {0}".format(Capacityi[1])], loc='upper right', numpoints=1,
    #                         fontsize=fontsize2, fancybox=True, shadow=True, ncol=2,
    #                         title='Cable Cost: {0:,} {1}'.format(round(total_cost / 1000000, 3), MEuro))
    # elif len(Cable_Costi) == 2:
    #     label1 = mpatches.Patch(color='blue', label='Capacity: {0}'.format(Capacityi[1], round(cable_length / 1000, 3),
    #                                                                        int(total_cost), name))
    #     label2 = mpatches.Patch(color='red', label='Capacity: {1}'.format(Capacityi[2], round(cable_length / 1000, 3),
    #                                                                       int(total_cost), name))
    #     legend = plt.legend([label1, (label2)],
    #                         ["Capacity: {0}".format(Capacityi[1]), "Capacity: {0}".format(Capacityi[2])],
    #                         loc='upper right', numpoints=1, fontsize=fontsize2, fancybox=True, shadow=True, ncol=2,
    #                         title='Cable Cost: {0:,} {1}'.format(round(total_cost / 1000000, 3), MEuro))
    # elif len(Cable_Costi) == 3:
    #     label1 = mpatches.Patch(color='blue', label='Capacity: {0}'.format(Capacityi[1], round(cable_length / 1000, 3),
    #                                                                        int(total_cost), name))
    #     label2 = mpatches.Patch(color='red', label='Capacity: {1}'.format(Capacityi[2], round(cable_length / 1000, 3),
    #                                                                       int(total_cost), name))
    #     label3 = mpatches.Patch(color='green', label='Capacity: {2}'.format(Capacityi[3], round(cable_length / 1000, 3),
    #                                                                         int(total_cost), name))
    #     legend = plt.legend([label1, (label2), (label3)],
    #                         ["Capacity: {0}".format(Capacityi[1]), "Capacity: {0}".format(Capacityi[2]),
    #                          "Capacity: {0}".format(Capacityi[3])], loc='upper right', numpoints=1, fontsize=fontsize2,
    #                         fancybox=True, shadow=True, ncol=3,
    #                         title='Cable Cost: {0:,} {1}'.format(round(total_cost / 1000000, 3), MEuro))
    # plt.setp(legend.get_title(), fontsize=fontsize2)
    # plt.tight_layout()
    # plt.subplots_adjust(left=0.06, right=0.94, bottom=0.08)
    # plt.gca().set_aspect('equal', adjustable='box')
    # plt.title(' {0} OWF - Hybrid '.format(name), fontsize=fontsize)
    # plt.grid()
    # scale = 1000
    # ticks1 = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x / scale))
    # ax.xaxis.set_major_formatter(ticks1)
    # ticks2 = ticker.FuncFormatter(lambda y, pos: '{0:g}'.format(y / scale))
    # ax.yaxis.set_major_formatter(ticks2)
    # plt.xticks(fontsize=fontsize2)
    # plt.yticks(fontsize=fontsize2)
    # plt.show()


def mainroutine(arc, lines, Routes, Routing):
    if [arc[0], 0] in Routing:
        index1 = Routing.index([arc[0], 0])
    else:
        for line in lines:
            if arc[0] in line:
                index1 = Routing.index([line[0], 0])
    Routing.pop(index1)
    Routing.append([arc[0], arc[1]])
    # turbines to be reversed
    for line in lines:
        if arc[0] in line:
            indexline = lines.index(line)
            indexarc = line.index(arc[0])
    indeces = []
    for i in xrange(0, indexarc):
        turbine = lines[indexline][i]
        for route in Routing:
            if route[1] == turbine and route != [arc[0], arc[1]]:
                indexroute = Routing.index(route)
                indeces.append(indexroute)
    for index in indeces:
        Routing[index].reverse()
    Routes = []
    for route in Routing:
        if route[1] == 0:
            Routes.append([[route[1], route[0]]])
    helpRouting = [i for i in Routing if i[1] != 0]
    helpRouting.reverse()
    for path in Routes:
        for pair in path:
            for route in helpRouting:
                if pair[1] == route[1]:
                    index2 = path.index(pair)
                    index3 = Routes.index(path)
                    Routes[index3].insert(index2 + 1, [route[1], route[0]])
    indeces = []
    for zeygos in helpRouting:
        for path in Routes:
            if [zeygos[1], zeygos[0]] in path:
                indexzeygos = helpRouting.index(zeygos)
                indeces.append(indexzeygos)
    for index in indeces:
        helpRouting[index] = []
    temp = [x for x in helpRouting if x != []]
    temp2 = []
    for pair1 in temp:
        counter1 = 1
        counter2 = 1
        for pair2 in temp:
            if pair1[0] in pair2 and pair2 != pair1:
                counter1 = counter1 + 1
        if [pair1[0], counter1] not in temp2:
            temp2.append([pair1[0], counter1])
        for pair2 in temp:
            if pair1[1] in pair2 and pair2 != pair1:
                counter2 = counter2 + 1
        if [pair1[1], counter2] not in temp2:
            temp2.append([pair1[1], counter2])
    temp3 = []
    for pair1 in temp2:
        for pair2 in temp:
            if pair1[1] == 1 and pair1[0] == pair2[0]:
                temp3.append(pair2)
                temp.remove(pair2)

    for pair1 in temp3:
        for pair2 in temp:
            if pair1[1] == pair2[0]:
                indexpair1 = temp3.index(pair1)
                temp3.insert(indexpair1 + 1, pair2)
                temp.remove(pair2)
    temp3 = [x for x in temp if x not in temp3] + temp3
    indeces = []
    if temp3 != []:
        for pair in temp3:
            for route in Routes:
                for path in route:
                    if pair[0] == path[1]:
                        indexpath = route.index(path)
                        indexroute = Routes.index(route)
                        Routes[indexroute].insert(indexpath + 1, pair)
                        indextemp = temp3.index(pair)
                        indeces.append(indextemp)
        for index in indeces:
            temp3[index] = []
        while temp3 != []:
            indeces = []
            temp3 = [x for x in temp3 if x != []]
            temp3.reverse()
            for pair in temp3:
                for route in Routes:
                    for path in route:
                        if pair[1] == path[1]:
                            indexpath = route.index(path)
                            indexroute = Routes.index(route)
                            Routes[indexroute].insert(indexpath + 1, [pair[1], pair[0]])
                            indextemp = temp3.index(pair)
                            indeces.append(indextemp)
            for index in indeces:
                temp3[index] = []
            if temp3 != []:
                temp3 = [x for x in temp3 if x != []]
                indeces = []
                temp3.reverse()
                for pair in temp3:
                    for route in Routes:
                        for path in route:
                            if pair[0] == path[1]:
                                indexpath = route.index(path)
                                indexroute = Routes.index(route)
                                Routes[indexroute].insert(indexpath + 1, pair)
                                indextemp = temp3.index(pair)
                                indeces.append(indextemp)
                for index in indeces:
                    temp3[index] = []
                temp3 = [x for x in temp3 if x != []]
    return Routing, Routes


def Hybrid(Savingsi, Savingsi_finder, Wind_turbinesi, Routes, Routing, central_platform_location, Capacityi,
           Routing_red, Routing_green, Costi, Cable_Costi, Transmission):
    Paths = []
    for WT in Wind_turbinesi:
        Paths.append([0, WT[0]])
    while True:
        if Savingsi != []:
            Savingsi, Savingsi_finder, saving = pop_task(Savingsi, Savingsi_finder)
        else:
            break
        if saving is None or saving[0] > 0:
            break
        arc = [saving[1], saving[2]]
        if check_same_path(arc, Paths) == False and any(
                [True for e in [[arc[0], 0]] if e in Routing]) == True and one_neighbor(arc[1], Paths) == False:
            condition4 = dict()
            for key, value in Capacityi.iteritems():
                condition4[key] = check_capacity(arc, Paths, Capacityi[key])
            if condition4[1] is False and edge_crossings(arc, Wind_turbinesi, central_platform_location, Routing) is False and edge_crossings_area(arc, Wind_turbinesi, central_platform_location, Transmission)[0] is False:
                Routing = []
                for index1, path in enumerate(Paths):
                    if arc[0] == path[1]:
                        Paths[index1].remove(0)
                        break
                for index2, path in enumerate(Paths):
                    if arc[1] == path[-1]:
                        break
                Paths[index2] = Paths[index2] + Paths[index1]
                Paths[index1] = []
                Paths = [path for path in Paths if path != []]
                for i in Paths:
                    for j in xrange(len(i) - 1):
                        Routing.append([i[j + 1], i[j]])
    Routes = []
    for index, path in enumerate(Paths):
        route = []
        for j in xrange(len(path) - 1):
            route.append([path[j], path[j + 1]])
        Routes.append(route)
    return Routes, Routing, Routing_red, Routing_green


def Esau_Williams_Cable_Choice(Savingsi, Savingsi_finder, Crossingsi_finder, Wind_turbinesi, Routes, Routing,
                               central_platform_location, Capacityi, Routing_red, Routing_green, Costi, Cable_Costi, Transmission, Crossing_penalty):
    total_update_red = []
    total_update_green = []
    while True:
        if Savingsi != []:
            Savingsi, Savingsi_finder, saving = pop_task(Savingsi, Savingsi_finder)
        else:
            break
        if saving is None or saving[0] > 0:
            break
        arc = [saving[1], saving[2]]
        lines = turbinesinroute(Routes)
        if check_same_path(arc, lines) == False:
            condcap = dict()
            for key, value in Capacityi.iteritems():
                condcap[key] = check_capacityEW(arc, lines, Capacityi[key])
            if condcap[1] == False:
                if edge_crossings_area(arc, Wind_turbinesi, central_platform_location, Transmission)[
                    0] == False and edge_crossings(arc, Wind_turbinesi, central_platform_location, Routing) == False:
                    Routing, Routes = mainroutine(arc, lines, Routes, Routing)
                    lines = turbinesinroute(Routes)
                    for indexl, line in enumerate(lines):
                        if arc[0] in line:
                            break
                    for turbine in lines[indexl]:
                        for n in Wind_turbinesi:
                            value = -(Costi[lines[indexl][0]][0] - Costi[turbine][n[0]]) * Cable_Costi[1]
                            arc1 = [lines[indexl][0], 0]
                            arc2 = [turbine, n[0]]
                            if turbine != n[0]:
                                value += Crossing_penalty * (
                                Crossingsi_finder[(arc2[0], arc2[1])] - Crossingsi_finder[(arc1[0], arc1[1])])
                            Savingsi, Savingsi_finder = add_task(Savingsi, Savingsi_finder, (turbine, n[0]), value)
                    heapify(Savingsi)
            if len(condcap) > 1 and condcap[1] == True and condcap[2] == False:
                if edge_crossings_area(arc, Wind_turbinesi, central_platform_location, Transmission)[
                    0] == False and edge_crossings(arc, Wind_turbinesi, central_platform_location, Routing) == False:
                    Routes_temp = deepcopy(Routes)
                    Routing_temp = deepcopy(Routing)
                    total_update_red_temp = []
                    Routing_red_temp = []
                    Routing_temp, Routes_temp = mainroutine(arc, lines, Routes_temp, Routing_temp)
                    lines = turbinesinroute(Routes_temp)
                    for indexl, line in enumerate(lines):
                        if arc[0] in line:
                            break
                    update = []
                    for route in Routes_temp:
                        for i in xrange(0, len(route)):
                            if arc[1] in route[i]:
                                index = Routes_temp.index(route)
                    elements = len(Routes_temp[index])
                    if elements == 1:
                        index1 = len(Routes_temp[index][0]) - 1 - Capacityi[1]
                        for j in xrange(0, index1):
                            update.append([Routes_temp[index][0][j + 1], Routes_temp[index][0][j]])
                    connected_turbines = []
                    if elements > 1:
                        for i in xrange(0, elements):
                            for j in xrange(len(Routes_temp[index][elements - 1 - i]) - 1, 0, -1):
                                connected_turbines.append([Routes_temp[index][elements - 1 - i][j - 1],
                                                           Routes_temp[index][elements - 1 - i][j], 1])
                    for pair1 in connected_turbines:
                        for pair2 in connected_turbines:
                            if pair1[0] == pair2[1]:
                                index = connected_turbines.index(pair2)
                                connected_turbines[index][2] = connected_turbines[index][2] + pair1[2]
                    for pair in connected_turbines:
                        if pair[2] > Capacityi[1]:
                            update.append([pair[1], pair[0]])
                    total_update_red_temp = renew_update(total_update_red, total_update_red_temp, Routes_temp) + update
                    Routing_red_temp = []
                    for route in total_update_red_temp:
                        for z in xrange(0, len(route) - 1):
                            Routing_red_temp.append([route[z], route[z + 1]])
                    new = -(cable_cost(central_platform_location, Wind_turbinesi, Routing, Routing_red, Routing_green,
                                       Cable_Costi) - cable_cost(central_platform_location, Wind_turbinesi,
                                                                 Routing_temp, Routing_red_temp, Routing_green,
                                                                 Cable_Costi))
                    arc1 = [lines[indexl][0], 0]
                    new = new + Crossing_penalty * (
                    Crossingsi_finder[(arc[0], arc[1])] - Crossingsi_finder[(arc1[0], arc1[1])])
                    Savingsi, Savingsi_finder = add_task(Savingsi, Savingsi_finder, (arc[0], arc[1]), new)
                    Savingsi, Savingsi_finder, max_saving = pop_task(Savingsi, Savingsi_finder)
                    if max_saving[0] == new:
                        Routes = Routes_temp
                        Routing = Routing_temp
                        Routing_red = Routing_red_temp
                        total_update_red = total_update_red_temp
                        lines = turbinesinroute(Routes)
                        for line in lines:
                            if arc[0] in line:
                                indexl = lines.index(line)
                        for turbine in lines[indexl]:
                            for n in Wind_turbinesi:
                                value = -(Costi[lines[indexl][0]][0] - Costi[turbine][n[0]]) * Cable_Costi[1]
                                arc1 = [lines[indexl][0], 0]
                                arc2 = [turbine, n[0]]
                                if turbine != n[0]:
                                    value = value + Crossing_penalty * (
                                    Crossingsi_finder[(arc2[0], arc2[1])] - Crossingsi_finder[(arc1[0], arc1[1])])
                                Savingsi, Savingsi_finder = add_task(Savingsi, Savingsi_finder, (turbine, n[0]), value)
                        heapify(Savingsi)
                    else:
                        Savingsi, Savingsi_finder = add_task(Savingsi, Savingsi_finder, (max_saving[1], max_saving[2]),
                                                             max_saving[0])

            if len(condcap) > 2 and condcap[1] == True and condcap[2] == True and condcap[3] == False:
                if edge_crossings_area(arc, Wind_turbinesi, central_platform_location, Transmission)[
                    0] == False and edge_crossings(arc, Wind_turbinesi, central_platform_location, Routing) == False:
                    Routes_temp = deepcopy(Routes)
                    Routing_temp = deepcopy(Routing)
                    total_update_red_temp = deepcopy(total_update_red)
                    total_update_green_temp = deepcopy(total_update_green)
                    Routing_temp, Routes_temp = mainroutine(arc, lines, Routes_temp, Routing_temp)
                    lines = turbinesinroute(Routes_temp)
                    for indexl, line in enumerate(lines):
                        if arc[0] in line:
                            break
                    update_red = []
                    update_green = []
                    for route in Routes_temp:
                        for i in xrange(0, len(route)):
                            if arc[1] in route[i]:
                                index = Routes_temp.index(route)
                    elements = len(Routes_temp[index])
                    if elements == 1:
                        index1 = len(Routes_temp[index][0]) - 1 - Capacityi[1]
                        index2 = len(Routes_temp[index][0]) - 1 - Capacityi[2]
                        for j in xrange(index2, index1):
                            update_red.append([Routes_temp[index][0][j + 1], Routes_temp[index][0][j]])
                        for j in xrange(0, index2):
                            update_green.append([Routes_temp[index][0][j + 1], Routes_temp[index][0][j]])
                    connected_turbines = []
                    if elements > 1:
                        for i in xrange(0, elements):
                            for j in xrange(len(Routes_temp[index][elements - 1 - i]) - 1, 0, -1):
                                connected_turbines.append([Routes_temp[index][elements - 1 - i][j - 1],
                                                           Routes_temp[index][elements - 1 - i][j], 1])
                    for pair1 in connected_turbines:
                        for pair2 in connected_turbines:
                            if pair1[0] == pair2[1]:
                                index = connected_turbines.index(pair2)
                                connected_turbines[index][2] = connected_turbines[index][2] + pair1[2]
                    for pair in connected_turbines:
                        if pair[2] > Capacityi[2]:
                            update_green.append([pair[1], pair[0]])
                        elif pair[2] > Capacityi[1] and pair[2] <= Capacityi[2]:
                            update_red.append([pair[1], pair[0]])

                    for pair in update_red:
                        if pair not in total_update_red_temp:
                            total_update_red_temp.append(pair)
                    total_update_red_temp = [x for x in total_update_red_temp if x in Routing_temp]

                    for pair in update_green:
                        if pair not in total_update_green_temp:
                            total_update_green_temp.append(pair)
                    total_update_green_temp = [x for x in total_update_green_temp if x in Routing_temp]

                    total_update_red_temp = [x for x in total_update_red_temp if x not in total_update_green_temp]

                    Routing_red_temp = []
                    for route in total_update_red_temp:
                        for z in xrange(0, len(route) - 1):
                            Routing_red_temp.append([route[z], route[z + 1]])
                    Routing_green_temp = []
                    for route in total_update_green_temp:
                        for z in xrange(0, len(route) - 1):
                            Routing_green_temp.append([route[z], route[z + 1]])
                    arc1 = [lines[indexl][0], 0]
                    new = new + Crossing_penalty * (
                    Crossingsi_finder[arc[0], arc[1]] - Crossingsi_finder[arc1[0], arc1[1]])
                    Savingsi, Savingsi_finder = add_task(Savingsi, Savingsi_finder, (arc[0], arc[1]), new)
                    Savingsi, Savingsi_finder, max_saving = pop_task(Savingsi, Savingsi_finder)
                    if max_saving[0] == new:
                        Routes = Routes_temp
                        Routing = Routing_temp
                        Routing_red = Routing_red_temp
                        Routing_green = Routing_green_temp
                        total_update_red = total_update_red_temp
                        total_update_green = total_update_green_temp
                        lines = turbinesinroute(Routes)
                        for line in lines:
                            if arc[0] in line:
                                indexl = lines.index(line)
                        for turbine in lines[indexl]:
                            for n in Wind_turbinesi:
                                if turbine != n[0]:
                                    value = -(Costi[lines[indexl][0]][0] - Costi[turbine][n[0]]) * Cable_Costi[1]
                                    arc1 = [lines[indexl][0], 0]
                                    arc2 = [turbine, n[0]]
                                    value = value + Crossing_penalty * (
                                    Crossingsi_finder[arc2[0], arc2[1]] - Crossingsi_finder[arc1[0], arc1[1]])
                                    Savingsi, Savingsi_finder = add_task(Savingsi, Savingsi_finder, (turbine, n[0]),
                                                                         value)
                        heapify(Savingsi)
                    else:
                        Savingsi, Savingsi_finder = add_task(Savingsi, Savingsi_finder, (max_saving[1], max_saving[2]),
                                                             max_saving[0])
    return Routes, Routing, Routing_red, Routing_green


def RouteOpt_Hybrid(Routing, Routing_red, Routing_green, central_platform_location, Costi, Capacityi, Routes,
                    Wind_turbinesi, Transmission):
    Paths = []
    temp = []
    for route in Routes:
        cond = False
        for i in range(len(route) - 1, -1, -1):
            for pair in route:
                if route[i][0] == pair[0] and route[i] != pair and cond == False:
                    cond = True
                    for pair5 in route:
                        if pair[0] == pair5[0]:
                            path = []
                            path.append(pair5[0])
                            path.append(pair5[1])
                            for pair6 in route:
                                if pair6[0] == path[-1]:
                                    path.append(pair6[1])
                            Paths.append(path)
                    temp.append(route)
        if cond == False and len(route) <= Capacityi[1]:
            path = []
            path.append(route[0][0])
            for pair in route:
                path.append(pair[1])
            Paths.append(path)
        elif cond == False and len(route) > Capacityi[1]:
            index = len(route) - Capacityi[1]
            path = []
            path.append(route[index][0])
            for i in range(index, len(route)):
                path.append(route[i][1])
            Paths.append(path)
    before = []
    after = []
    for path in Paths:
        list = []
        index = Paths.index(path)
        path.reverse()
        cond = True
        i = 0
        while cond == True:
            for l in range(1, len(path)):
                list.append([Costi[path[l - 1]][path[l]] - Costi[path[l]][path[0]], path[0], path[l]])
            s = max(list, key=lambda x: x[0])
            if s[0] > 0 and edge_crossings([s[1], s[2]], Wind_turbinesi, central_platform_location,
                                           Routing) == False and \
                            edge_crossings_area([s[1], s[2]], Wind_turbinesi, central_platform_location, Transmission)[
                                0] == False:
                for k in list:
                    if k == s:
                        lamd = list.index(k)
                        xmm = lamd + 1
                        path1 = path[:xmm]
                        path2 = path[xmm:]
                        path1.reverse()
                        if i == 0:
                            before.append(Paths[index])
                        i = 1
                        path = path1 + path2
                        Paths[index] = path
                        list = []
                        cond = True
            else:
                list = []
                cond = False
                if i == 1:
                    after.append(Paths[index])

    for path in before:
        for i in range(0, len(path) - 1):
            if [path[i], path[i + 1]] in Routing:
                Routing.remove([path[i], path[i + 1]])
            elif [path[i + 1], path[i]] in Routing:
                Routing.remove([path[i + 1], path[i]])
    for path in after:
        for i in range(0, len(path) - 1):
            Routing.append([path[i], path[i + 1]])
    return Routes, Routing


def renew_update(total_update, total_update_temp, Paths_temp):
    indeces = []
    for indexerase, route in enumerate(total_update):
        for turbine in route:
            if turbine != 0:
                for pair in total_update_temp:
                    if (pair[0] != 0 and pair[1] == 0) or (pair[0] == 0 and pair[1] != 0):
                        same1 = [turbine, pair[0]]
                    if pair[0] != 0 and pair[1] != 0:
                        same1 = [turbine, pair[0]]
                        same2 = [turbine, pair[1]]
                        if check_same_path(same1, Paths_temp) == True or check_same_path(same2, Paths_temp) == True:
                            if indexerase not in indeces:
                                indeces.append(indexerase)
    if indeces != []:
        for i in indeces:
            total_update[i] = []
    for pair in total_update[:]:
        if pair == []:
            total_update.remove(pair)
    return total_update


def initial_values(NT, Wind_turbines, central_platform_location):
    Costi = [[0 for i in xrange(NT + 1)] for j in xrange(NT + 1)]
    set_cost_matrix(Costi, Wind_turbines, central_platform_location)
    distancefromsubstationi = []
    for i in xrange(len(Costi[0]) - 1):
        distancefromsubstationi.append([0, i + 1, Costi[0][i + 1]])
    Wind_turbinesi = []
    return Wind_turbinesi, Costi, distancefromsubstationi


def initial_routes(Wind_turbinesi):
    Routing_greeni = []
    Routing_redi = []
    Routingi = []
    Routesi = []
    for WT in Wind_turbinesi:
        Routingi.append([WT[0], 0])
        Routesi.append([[0, WT[0]]])
    return Routesi, Routingi, Routing_redi, Routing_greeni


def check_same_path(arc, Paths):
    same_path = False
    for path in Paths:
        if arc[0] in path and arc[1] in path:
            same_path = True
            break
    return same_path


# Subroutine 5, check if turbine u has only one neighbor in Routing
def one_neighbor(turbine, Paths):
    more_than_one = False
    for path in Paths:
        if turbine in path and turbine != path[-1]:
            more_than_one = True
            break
    return more_than_one


def costi(Wind_turbinesi, central_platform_location):
    Cost0i = []
    Costij = []
    for i in Wind_turbinesi:
        Cost0i.append([0, i[0], hypot(central_platform_location[0] - i[1], central_platform_location[1] - i[2])])
        for j in Wind_turbinesi:
            if i != j:
                Costij.append([i[0], j[0], hypot(i[1] - j[1], i[2] - j[2])])
    return Cost0i, Costij


def savingsi(Cost0i, Costij, Wind_turbinesi, Cable_Cost1, central_platform_location, Area, Crossing_penalty, WT_List):
    Savingsi = []
    Savingsi_finder = {}
    Crossingsi_finder = {}
    counter = 0
    for i in zip(*Wind_turbinesi)[0]:
        k = Cost0i[counter]
        step = (len(Wind_turbinesi) - 1) * counter
        for j in xrange(step, step + len(Wind_turbinesi) - 1):
            saving = -(k[2] - Costij[j][2]) * Cable_Cost1
            arc1 = [i, 0]
            arc2 = [i, Costij[j][1]]
            crossings_arc1 = edge_crossings_area(arc1, Wind_turbinesi, central_platform_location, Area, WT_List)[1]
            crossings_arc2 = edge_crossings_area(arc2, Wind_turbinesi, central_platform_location, Area, WT_List)[1]
            Crossingsi_finder[(arc1[0], arc1[1])] = crossings_arc1
            Crossingsi_finder[(arc2[0], arc2[1])] = crossings_arc2
            saving = saving + Crossing_penalty * (crossings_arc2 - crossings_arc1)
            if saving < 0:
                add_task(Savingsi, Savingsi_finder, (i, Costij[j][1]), saving)
        counter += 1
    return Savingsi, Savingsi_finder, Crossingsi_finder


def add_task(Savings, entry_finder, task, priority):
    'Add a new task or update the priority of an existing task'
    if task in entry_finder:
        entry_finder = remove_task(entry_finder, task)
    entry = [priority, task[0], task[1]]
    entry_finder[(task[0], task[1])] = entry
    heappush(Savings, entry)
    return Savings, entry_finder


def remove_task(entry_finder, task):
    entry = entry_finder.pop(task)
    entry[0] = REMOVED
    return entry_finder


def pop_task(Savings, entry_finder):
    while Savings:
        saving = heappop(Savings)
        if saving[0] is not REMOVED:
            del entry_finder[(saving[1], saving[2])]
            return Savings, entry_finder, saving


def set_cost_matrix(Cost, Wind_turbines, central_platform_location):
    Cost[0][0] = float('inf')
    for i in Wind_turbines:
        Cost[0][i[0]] = hypot(central_platform_location[0] - i[1], central_platform_location[1] - i[2])
        Cost[i[0]][0] = hypot(central_platform_location[0] - i[1], central_platform_location[1] - i[2])
        for j in Wind_turbines:
            if i == j:
                Cost[i[0]][j[0]] = float('inf')
            else:
                Cost[i[0]][j[0]] = hypot(i[1] - j[1], i[2] - j[2])


def turbinesinroute(Routes):
    lines = [[] for i in xrange(len(Routes))]
    for route in Routes:
        index = Routes.index(route)
        for pair in route:
            lines[index].append(pair[1])
    return lines


def check_capacityEW(arc, Paths, Capacity):
    cap_exceeded = False
    turbines_in_branch = 0
    for path in Paths:
        if arc[0] in path or arc[1] in path:
            turbines_in_branch = turbines_in_branch + (len(path))
            if turbines_in_branch > Capacity:
                cap_exceeded = True
                break
    return cap_exceeded


def check_capacity(arc, Paths, Capacity):
    cap_exceeded = False
    turbines_in_branch = 0
    for path in Paths:
        if arc[0] in path or arc[1] in path:
            turbines_in_branch = turbines_in_branch + (len(path) - 1)
            if turbines_in_branch > Capacity:
                cap_exceeded = True
                break
    return cap_exceeded


def edge_crossings(arc, Wind_turbines, central_platform_location, Routing):
    x1, y1 = give_coordinates(arc[0], Wind_turbines, central_platform_location, WT_List)
    x2, y2 = give_coordinates(arc[1], Wind_turbines, central_platform_location, WT_List)
    intersection = False
    # Left - 0
    # Right - 1
    # Colinear - 2
    for route in Routing:
        if arc[0] not in route:
            x3, y3 = give_coordinates(route[0], Wind_turbines, central_platform_location, WT_List)
            x4, y4 = give_coordinates(route[1], Wind_turbines, central_platform_location, WT_List)
            counter = 0
            Area = [0, 0, 0, 0]
            Position = [0, 0, 0, 0]
            Area[0] = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)
            Area[1] = (x2 - x1) * (y4 - y1) - (x4 - x1) * (y2 - y1)
            Area[2] = (x4 - x3) * (y1 - y3) - (x1 - x3) * (y4 - y3)
            Area[3] = (x4 - x3) * (y2 - y3) - (x2 - x3) * (y4 - y3)
            for i in xrange(4):
                if Area[i] > 0:
                    Position[i] = 0
                elif Area[i] < 0:
                    Position[i] = 1
                else:
                    Position[i] = 2
                    counter += 1
            if Position[0] != Position[1] and Position[2] != Position[3] and counter <= 1:
                intersection = True
                break
    return intersection


def edge_crossings_area(arc, Wind_turbines, central_platform_location, Area_cross, WT_List):
    x1, y1 = give_coordinates(arc[0], Wind_turbines, central_platform_location, WT_List)
    x2, y2 = give_coordinates(arc[1], Wind_turbines, central_platform_location, WT_List)
    intersection = False
    crossings = 0
    for area in Area_cross:
        counter = 0
        x3, y3 = area[0][0], area[0][1]
        x4, y4 = area[1][0], area[1][1]
        Area = [0, 0, 0, 0]
        Position = [0, 0, 0, 0]
        Area[0] = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)
        Area[1] = (x2 - x1) * (y4 - y1) - (x4 - x1) * (y2 - y1)
        Area[2] = (x4 - x3) * (y1 - y3) - (x1 - x3) * (y4 - y3)
        Area[3] = (x4 - x3) * (y2 - y3) - (x2 - x3) * (y4 - y3)
        for i in xrange(4):
            if Area[i] > 0:
                Position[i] = 0
            elif Area[i] < 0:
                Position[i] = 1
            else:
                Position[i] = 2
                counter += 1
        if Position[0] != Position[1] and Position[2] != Position[3] and counter <= 1:
            intersection = True
            crossings += 1
    return intersection, crossings


# Plotting+Cable_length
def plotting(fig, central_platform_location1, Wind_turbines1, Routing, Routing_red, Routing_green, Capacityi,
             Cable_Costi):
    central_platform_location1_1 = [[0, central_platform_location1[0], central_platform_location1[1]]]
    Full_List = central_platform_location1_1 + Wind_turbines1
    Routing_blue = [i for i in Routing if i not in Routing_red]
    Routing_blue = [i for i in Routing_blue if i not in Routing_green]
    cable_length1blue = 0
    index, x, y = zip(*Full_List)
    ax = fig.add_subplot(111)
    ax.set_xlabel('x [km]', fontsize=fontsize2)
    ax.set_ylabel('y [km]', fontsize=fontsize2)
    arcs1 = []
    arcs2 = []
    for i in Routing_blue:
        for j in Full_List:
            if j[0] == i[0]:
                arcs1.append([j[1], j[2]])
            if j[0] == i[1]:
                arcs2.append([j[1], j[2]])
    for i in xrange(len(arcs1)):
        arcs1.insert(2 * i + 1, arcs2[i])
    for j in xrange(len(arcs1) - len(Routing_blue)):
        plt.plot([arcs1[2 * j][0], arcs1[2 * j + 1][0]], [arcs1[2 * j][1], arcs1[2 * j + 1][1]], color='b')
        cable_length1blue += hypot(arcs1[2 * j][0] - arcs1[2 * j + 1][0], arcs1[2 * j][1] - arcs1[2 * j + 1][1])
    cable_cost = Cable_Costi[1] * cable_length1blue
    cable_length = cable_length1blue

    if len(Cable_Costi) == 2:
        cable_length1red = 0
        arcs1 = []
        arcs2 = []
        for i in Routing_red:
            for j in Full_List:
                if j[0] == i[0]:
                    arcs1.append([j[1], j[2]])
                if j[0] == i[1]:
                    arcs2.append([j[1], j[2]])
        for i in xrange(len(arcs1)):
            arcs1.insert(2 * i + 1, arcs2[i])
        for j in xrange(len(arcs1) - len(Routing_red)):
            plt.plot([arcs1[2 * j][0], arcs1[2 * j + 1][0]], [arcs1[2 * j][1], arcs1[2 * j + 1][1]], color='r')
            cable_length1red = cable_length1red + hypot(arcs1[2 * j][0] - arcs1[2 * j + 1][0],
                                                        arcs1[2 * j][1] - arcs1[2 * j + 1][1])
        cable_cost = Cable_Costi[1] * (cable_length1blue) + Cable_Costi[2] * (cable_length1red)
        cable_length = cable_length1blue + cable_length1red

    if len(Cable_Costi) == 3:

        cable_length1red = 0
        arcs1 = []
        arcs2 = []
        for i in Routing_red:
            for j in Full_List:
                if j[0] == i[0]:
                    arcs1.append([j[1], j[2]])
                if j[0] == i[1]:
                    arcs2.append([j[1], j[2]])
        for i in xrange(len(arcs1)):
            arcs1.insert(2 * i + 1, arcs2[i])
        for j in xrange(len(arcs1) - len(Routing_red)):
            plt.plot([arcs1[2 * j][0], arcs1[2 * j + 1][0]], [arcs1[2 * j][1], arcs1[2 * j + 1][1]], color='r')
            cable_length1red = cable_length1red + hypot(arcs1[2 * j][0] - arcs1[2 * j + 1][0],
                                                        arcs1[2 * j][1] - arcs1[2 * j + 1][1])

        cable_length1green = 0
        arcs1 = []
        arcs2 = []
        for i in Routing_green:
            for j in Full_List:
                if j[0] == i[0]:
                    arcs1.append([j[1], j[2]])
                if j[0] == i[1]:
                    arcs2.append([j[1], j[2]])
        for i in xrange(len(arcs1)):
            arcs1.insert(2 * i + 1, arcs2[i])
        for j in xrange(len(arcs1) - len(Routing_green)):
            plt.plot([arcs1[2 * j][0], arcs1[2 * j + 1][0]], [arcs1[2 * j][1], arcs1[2 * j + 1][1]], color='g')
            cable_length1green = cable_length1green + hypot(arcs1[2 * j][0] - arcs1[2 * j + 1][0],
                                                            arcs1[2 * j][1] - arcs1[2 * j + 1][1])
        cable_length = cable_length1blue + cable_length1red + cable_length1green
        cable_cost = Cable_Costi[1] * (cable_length1blue) + Cable_Costi[2] * (cable_length1red) + Cable_Costi[3] * (
        cable_length1green)
    plt.plot([p[1] for p in central_platform_location1_1], [p[2] for p in central_platform_location1_1], marker='o',
             ms=10, color='0.35')
    plt.plot([p[1] for p in Wind_turbines1], [p[2] for p in Wind_turbines1], 'o', ms=6, color='0.3')
    return cable_length, cable_cost, ax


def cable_cost(central_platform_location, Wind_turbinesi, Routing, Routing_red, Routing_green, Cable_Costi):
    Routing_blue = [i for i in Routing if i not in Routing_red]
    Routing_blue = [i for i in Routing_blue if i not in Routing_green]
    cable_length1blue = 0
    for route in Routing_blue:
        x1, y1 = give_coordinates(route[0], Wind_turbinesi, central_platform_location, WT_List)
        x2, y2 = give_coordinates(route[1], Wind_turbinesi, central_platform_location, WT_List)
        cable_length1blue = cable_length1blue + hypot(x2 - x1, y2 - y1)
    cable_cost = Cable_Costi[1] * (cable_length1blue)

    if len(Cable_Costi) == 2:
        cable_length1red = 0
        for route in Routing_red:
            x1, y1 = give_coordinates(route[0], Wind_turbinesi, central_platform_location, WT_List)
            x2, y2 = give_coordinates(route[1], Wind_turbinesi, central_platform_location, WT_List)
            cable_length1red = cable_length1red + hypot(x2 - x1, y2 - y1)
        cable_cost = Cable_Costi[1] * (cable_length1blue) + Cable_Costi[2] * (cable_length1red)

    if len(Cable_Costi) == 3:
        cable_length1red = 0
        for route in Routing_red:
            x1, y1 = give_coordinates(route[0], Wind_turbinesi, central_platform_location, WT_List)
            x2, y2 = give_coordinates(route[1], Wind_turbinesi, central_platform_location, WT_List)
            cable_length1red = cable_length1red + hypot(x2 - x1, y2 - y1)
        cable_length1green = 0
        for route in Routing_green:
            x1, y1 = give_coordinates(route[0], Wind_turbinesi, central_platform_location, WT_List)
            x2, y2 = give_coordinates(route[1], Wind_turbinesi, central_platform_location, WT_List)
            cable_length1green = cable_length1green + hypot(x2 - x1, y2 - y1)
        cable_cost = Cable_Costi[1] * (cable_length1blue) + Cable_Costi[2] * (cable_length1red) + Cable_Costi[3] * (
        cable_length1green)
    return cable_cost


# Submethods return x and y coordinates of a turbine if it's ID is known. The OHVS must also be included
def give_coordinates(turbineID, Wind_turbines, central_platform_location, WT_List):
    if turbineID == 0:
        x = central_platform_location[0]
        y = central_platform_location[1]
    else:
        # print WT_List, turbineID - 1
        turbine = WT_List[turbineID - 1]
        x = turbine[1]
        y = turbine[2]
    return x, y


# ------------------------------------Run------------------------------------------------------------------

if __name__ == '__main__':
    # ---------------------------------------Input--------------------------------------------------------------------------------
    name = 'Borssele'
    # WT_List = [[0, 485101.04983316606, 5732217.3257142855], [1, 485503.6486449828, 5731759.337142857], [2, 485866.01741583704, 5731311.565714286], [3, 486268.61622765375, 5730792.548571428], [4, 486671.24216694245, 5732675.28], [5, 487089.95469712175, 5732217.3257142855], [6, 487444.23948132276, 5731708.457142857], [7, 487846.86542061146, 5731250.502857143], [8, 487846.86542061146, 5733591.222857143], [9, 488249.4642324282, 5733061.988571429], [10, 488660.1199034262, 5732624.4], [11, 489014.43181509915, 5732166.411428572], [12, 489425.0874860972, 5731657.577142857], [13, 489827.7134253859, 5731199.622857143], [14, 489425.0874860972, 5733998.297142857], [15, 489827.7134253859, 5733530.16], [16, 490238.3690963839, 5733021.291428572], [17, 490592.65388058487, 5732563.337142857], [18, 491003.3366790549, 5732095.2], [19, 491405.9354908716, 5731596.514285714], [20, 491808.5614301603, 5733479.245714285], [21, 492170.9030735426, 5732960.228571429], [22, 492581.5587445406, 5732502.274285714], [23, 492984.1846838293, 5732034.137142858], [24, 494152.1579903969, 5735245.577142857], [25, 494553.2647912541, 5734783.68], [26, 494963.2965303963, 5734321.782857143], [27, 495319.8328947725, 5733803.554285714], [28, 495720.93969562976, 5735684.938285714], [29, 496130.971434772, 5735166.72], [30, 496541.0031739142, 5734716.102857143], [31, 496897.5395382904, 5734265.451428572], [32, 497307.57127743267, 5736090.504], [33, 497708.6780782899, 5735628.610285714], [34, 489415.4029785964, 5729387.485714286], [35, 489820.4161354203, 5728866.377142857], [36, 490184.08702493017, 5728396.285714285], [37, 490589.07305428205, 5727947.108571429], [38, 490994.086211106, 5727435.222857143], [39, 491407.34611941513, 5726975.588571428], [40, 491762.7431299677, 5726526.411428572], [41, 490994.086211106, 5729775.188571429], [42, 491407.34611941513, 5729315.554285714], [43, 491771.0170089249, 5728803.702857143], [44, 492167.72915931966, 5728354.491428572], [45, 492581.0161951008, 5727894.857142857], [46, 492977.7283454955, 5727435.222857143], [47, 492977.7283454955, 5729712.514285714], [48, 493349.6731139625, 5729263.337142857], [49, 493746.4123918292, 5728803.702857143], [50, 494556.41157800506, 5730172.148571429], [51, 492974.7985785205, 5725094.708571428], [52, 493341.1279602854, 5724641.794285715], [53, 493755.25594769826, 5724128.468571428], [54, 494153.43298158044, 5723665.474285714], [55, 494511.78688658006, 5723212.56], [56, 493747.2804709329, 5726463.565714286], [57, 494153.43298158044, 5726000.571428572], [58, 494511.78688658006, 5725487.28], [59, 494917.93939722754, 5725044.411428572], [60, 495332.06738464045, 5724571.337142857], [61, 494909.9910479342, 5727379.508571428], [62, 495324.0919078751, 5726856.102857143], [63, 495722.2689417573, 5726403.188571429], [64, 496080.6499742289, 5725950.274285714], [65, 495722.2689417573, 5728738.285714285], [66, 496128.4214524049, 5728224.96], [67, 496494.75083416974, 5727782.125714285], [68, 496892.95499552396, 5727319.131428571], [69, 496892.95499552396, 5729593.817142857], [70, 497299.0803786995, 5729140.9028571425], [71, 497705.232889347, 5728677.908571429], [72, 498071.56227111194, 5730509.76], [73, 498477.7147817595, 5730056.811428571], [74, 496082.4403873803, 5721297.565714286], [75, 496497.110924233, 5720823.737142857], [76, 496894.71828120336, 5720378.64], [77, 496889.0215120853, 5722668.754285715], [78, 497297.9952798199, 5722202.125714285], [79, 497667.2001736158, 5721749.828571429], [80, 498070.50429970433, 5721225.771428571], [81, 498473.7812983208, 5720780.6742857145], [82, 498837.31655047066, 5720314.045714286], [83, 499240.62067655916, 5719876.114285714], [84, 499643.8976751756, 5719344.857142857], [85, 500041.50503214606, 5718899.76], [86, 500410.737053414, 5718440.297142857], [87, 497655.86089032365, 5724025.577142857], [88, 498064.8075305862, 5723558.948571429], [89, 498468.1116566747, 5723106.651428571], [90, 498871.4157827632, 5722604.125714285], [91, 499240.62067655916, 5722144.662857143], [92, 499643.8976751756, 5721692.4], [93, 500041.50503214606, 5721225.771428571], [94, 500410.737053414, 5720723.245714285], [95, 500808.3444103844, 5720263.782857143], [96, 498466.9180479071, 5725386.377142857], [97, 498878.8487100887, 5724931.851428571], [98, 499238.47760627186, 5724469.062857143], [99, 499643.87054770364, 5724014.537142857], [100, 500042.72576838563, 5723502.137142858], [101, 500454.68355803925, 5723047.611428572], [102, 500820.8501749722, 5722593.085714285], [103, 501219.7053956542, 5722080.72], [104, 499226.080351572, 5726806.422857143], [105, 499635.02699183463, 5726298.514285714], [106, 500048.9922144155, 5725835.142857143], [107, 500452.8660174158, 5725380.685714286], [109, 501206.0874047148, 5724461.348571429], [108, 500819.49380137265, 5724849.84], [110, 500043.94650462526, 5728169.794285715], [111, 500452.8660174158, 5727661.885714286], [112, 500812.440658655, 5727198.514285714], [113, 501221.36017144565, 5726752.971428571], [114, 501623.25366899057, 5726236.148571429], [115, 501221.36017144565, 5729025.257142857], [116, 501630.3068117082, 5728570.8], [117, 502032.1731817812, 5728125.257142857], [118, 498462.27925019665, 5732385.12], [119, 499640.1540840409, 5733242.228571429], [120, 500044.678946369, 5732783.588571428], [121, 500449.20380869706, 5732324.948571429], [122, 501621.1377261753, 5730911.451428572], [123, 500445.7857472262, 5734610.777142857], [124, 500858.2589588476, 5734151.417142857], [125, 501217.48094295093, 5733680.777142857], [126, 501222.55378021323, 5735978.989714285], [127, 501621.1377261753, 5735520.342857143], [128, 502031.6035048694, 5735069.245714285], [129, 502783.82117570465, 5731772.468571428], [130, 502421.94069934625, 5736879.929142857], [131, 502785.88286357594, 5736427.9954285715], [132, 503194.55822911864, 5735911.505142857], [133, 503603.2064671893, 5735467.645714286], [134, 503181.78118981095, 5738251.858285714], [135, 503603.2064671893, 5737799.928], [136, 504005.47974934214, 5737339.926857143], [137, 505180.37056126737, 5735919.576], [138, 506757.5346553455, 5733974.6742857145], [139, 507115.1018636573, 5733522.72], [140, 507523.804356672, 5733062.742857143], [141, 507932.3440848547, 5732562.377142857], [142, 503961.66888207686, 5730339.6342857145], [143, 504370.69690475543, 5729889.12], [144, 504773.919648428, 5729416.457142857], [145, 504364.8644982774, 5732222.914285715], [146, 504779.752054906, 5731772.4], [147, 505177.1152646285, 5731248.034285714], [148, 505539.40265306673, 5730797.52], [149, 505948.4306757453, 5730347.005714286], [150, 506357.48582589586, 5729822.6742857145], [151, 506760.6814420964, 5729364.754285715], [152, 507117.1092965846, 5728914.274285714], [153, 507526.2458291512, 5728397.28], [154, 507923.39201909775, 5727946.765714286], [155, 505182.94767110655, 5733581.794285715], [156, 505591.9756937851, 5733131.314285714], [157, 505942.5982692673, 5732629.0971428575], [158, 506351.62629194587, 5732156.434285714], [159, 506754.8219081464, 5731705.92], [160, 507122.96883053466, 5731203.737142857], [161, 507526.2458291512, 5730745.817142857], [162, 507929.36006293574, 5730280.56], [163, 508332.4742967203, 5729763.565714286], [164, 508688.92927868053, 5729313.085714285], [165, 501973.27944008895, 5716503.462857143], [166, 502388.62816374144, 5716045.165714285], [167, 502790.79293600627, 5715595.165714285], [168, 503153.40585410845, 5715070.217142857], [169, 503562.1897295391, 5714620.2514285715], [170, 503964.354501804, 5714161.954285714], [171, 501979.8714157828, 5718844.937142857], [172, 502388.62816374144, 5718378.308571429], [173, 502790.79293600627, 5717870.022857143], [174, 503199.5768114369, 5717420.057142857], [175, 503555.59775384533, 5716953.428571428], [176, 503964.354501804, 5716445.108571429], [177, 504366.5192740688, 5715986.811428571], [178, 504729.159319643, 5715528.514285714], [179, 505137.91606760165, 5715020.228571429], [180, 502388.62816374144, 5720661.497142857], [181, 502797.3849117001, 5720203.165714285], [182, 503199.5768114369, 5719744.868571429], [183, 503555.59775384533, 5719236.582857143], [184, 503964.354501804, 5718778.285714285], [185, 504373.11124976265, 5718311.657142857], [186, 504781.8951251933, 5717811.702857143], [187, 505137.91606760165, 5717353.371428572], [188, 505540.08083986654, 5716886.742857143], [189, 505955.45669099095, 5716445.108571429], [190, 502790.7115535903, 5722545.531428572], [191, 503196.9454466538, 5722024.32], [192, 503553.97010552586, 5721573.12], [193, 503966.3619347313, 5721121.885714286], [194, 504372.6229552668, 5720600.6742857145], [195, 504772.69891218835, 5720141.657142857], [196, 505135.88150720234, 5719690.457142857], [197, 505542.11540026584, 5719239.257142857], [198, 505948.37642080133, 5718725.794285715], [199, 506351.62629194587, 5718259.028571429], [200, 506711.6349727369, 5717815.611428572], [201, 503196.9454466538, 5724358.182857143], [202, 503603.2064671893, 5723922.514285714], [203, 503960.20399858936, 5723393.52], [204, 504366.46501912485, 5722942.285714285], [205, 504772.69891218835, 5722483.302857143], [206, 505135.88150720234, 5722024.32], [207, 505542.11540026584, 5721510.857142857], [208, 505948.37642080133, 5721059.657142857], [209, 506354.61031386483, 5720600.6742857145], [210, 506717.7929088788, 5720087.2114285715], [211, 507117.8688658004, 5719628.228571429], [212, 503594.17301901634, 5726185.371428572], [213, 503964.354501804, 5725724.3657142855], [214, 504367.2245883406, 5725270.2514285715], [215, 504770.06754740526, 5724822.994285714], [216, 505134.8235357947, 5724313.851428571], [217, 505548.5717385997, 5723839.0971428575], [218, 505945.98920326616, 5723384.982857143], [219, 506354.28478420095, 5722882.697142857], [220, 506713.5881507202, 5722421.691428571], [221, 507116.43110978487, 5721967.577142857], [222, 507524.6181808317, 5721458.4], [223, 504775.5201692754, 5727100.457142857], [224, 505172.9376339419, 5726639.485714286], [225, 505537.6664948593, 5726185.371428572], [226, 505951.4146976643, 5725669.302857143], [227, 506354.28478420095, 5725215.188571429], [228, 506713.5881507202, 5724761.074285714], [229, 507116.43110978487, 5724245.04], [230, 507524.6181808317, 5723790.925714286], [231, 507927.7324146163, 5723336.811428571], [232, 507927.7324146163, 5725614.274285714], [233, 508286.9001437756, 5725167.051428571]]
    # central_platform_locations = [[497362.28738843824, 5730299.074285714], [503845.86170414777, 5727342.685714286]]
    # SiteI=[[[504493.4, 5733553.1], [503747.98, 5729571.28]], [[505886.23, 5733861.05], [504493.4, 5733553.1]], [[507026.1, 5735095.07], [505886.23, 5733861.05]], [[507655.72, 5734196.99], [507026.1, 5735095.07]],[[508924.84, 5727139.08], [507655.72, 5734196.99]], [[508924.84, 5727139.08], [503747.98, 5729571.28]],[[503052.9, 5738460.1], [498195.61, 5732179.9]], [[504373.7, 5738878.38], [503052.9, 5738460.1]], [[504463.61, 5738750.14], [504373.7, 5738878.38]],[[504134.55, 5737015.25], [504463.61, 5738750.14]], [[503861.53, 5735540.39], [504134.55, 5737015.25]], [[503747.98, 5734937.96], [503861.53, 5735540.39]],[[502550.86, 5734689.23], [503747.98, 5734937.96]], [[502297.43, 5734542.91], [502550.86, 5734689.23]], [[502109.51, 5734388.39], [502297.43, 5734542.91]], [[499933.11, 5731363.59], [502109.51, 5734388.39]],[[499933.11, 5731363.59], [498195.61, 5732179.9]], [[505263.12, 5737609.74], [504839.79, 5735150.31]], [[506123.85, 5736382.01], [505263.12, 5737609.74]], [[505057.19, 5735195.83], [506123.85, 5736382.01]], [[505057.19, 5735195.83], [504839.79, 5735150.31]],[[503224.07, 5733301.78], [501321.18, 5730711.44]], [[503434.54, 5733344.75], [503224.07, 5733301.78]], [[502818.17, 5730008.13], [503434.54, 5733344.75]],[[502818.17, 5730008.13], [501321.18, 5730711.44]]]
    # SiteII=[[[501724.83, 5715801.34], [501754.86, 5715458.97]], [[501693.71, 5716155.97], [501724.83, 5715801.34]], [[501658.62, 5717090.63], [501693.71, 5716155.97]], [[501692.76, 5718163.04], [501658.62, 5717090.63]], [[501817.78, 5719280.64], [501692.76, 5718163.04]],[[503475.25, 5728042.11], [501817.78, 5719280.64]], [[508416.71, 5725720.51], [503475.25, 5728042.11]], [[508564.67, 5725586.88], [508416.71, 5725720.51]], [[508654.27, 5725505.95], [508564.67, 5725586.88]], [[507087.05, 5716811.66], [508654.27, 5725505.95]], [[504039.56, 5713246.09], [507087.05, 5716811.66]], [[504039.56, 5713246.09], [501754.86, 5715458.97]]]
    # SiteIII=[[[500393.44, 5729507.48], [494903.44, 5722095.03]], [[502535.07, 5728483.83], [500393.44, 5729507.48]], [[500831.2, 5719450.19], [502535.07, 5728483.83]], [[500697.23, 5718257.76], [500831.2, 5719450.19]],[[500671.65, 5717925.78], [500697.23, 5718257.76]], [[500655.94, 5717378.08], [500671.65, 5717925.78]], [[500658.88, 5716785.88], [500655.94, 5717378.08]], [[500670.75, 5716509.01], [500658.88, 5716785.88]],[[498105.4, 5718993.72], [500670.75, 5716509.01]], [[498105.4, 5718993.72], [494903.44, 5722095.03]], [[497245.6, 5730968.94], [492218.64, 5724695.43]], [[499006.34, 5730141.7], [497245.6, 5730968.94]], [[493825.18, 5723139.39], [499006.34, 5730141.7]], [[493825.18, 5723139.39], [492218.64, 5724695.43]]]
    # SiteIV=[[[490059.36, 5734345.19], [484178.55, 5732482.8]],[[494528.58, 5732245.45], [490059.36, 5734345.19]], [[486500.85, 5730233.5], [494528.58, 5732245.45]], [[486500.85, 5730233.5], [484178.55, 5732482.8]], [[496081.24, 5731086.3], [487772.2, 5729002.11]], [[491497.54, 5725393.86], [496081.24, 5731086.3]], [[491497.54, 5725393.86], [487772.2, 5729002.11]], [[499676.28, 5737390.76], [492166.47, 5735012.48]], [[497567.0, 5734751.25], [499676.28, 5737390.76]], [[497365.84, 5734486.31], [497567.0, 5734751.25]], [[496248.58, 5733101.4], [497365.84, 5734486.31]], [[496248.58, 5733101.4], [492166.47, 5735012.48]]]
    # Cable_List=[[8,200],[13,425]]
    # WT_List= [[0, 10566.8958235751, 19589.3756977131], [1, 9948.631596405023, 19629.4810668796], [2, 9034.587387679716, 19512.268952051036], [3, 11304.581575440265, 19579.814024971674], [4, 9964.839307491762, 18857.239784681464], [5, 8909.253190787076, 19007.272109684618], [6, 9158.752245745432, 18352.444351834856], [7, 8326.51938626085, 19201.957317829434], [8, 11603.49823545817, 18675.595553985553], [9, 10331.860455176606, 18306.778263879976], [10, 9904.69760041116, 20536.71561115692], [11, 12343.095420371492, 18343.946308755854], [12, 11957.37507260179, 19549.058534649233], [13, 11644.50001141853, 17717.7379830942], [14, 10569.595786818198, 20104.495002408057], [15, 12536.05617170514, 20301.527076885493], [16, 7838.684757496683, 18387.02932755849], [17, 12523.949763389486, 20829.10041975918], [18, 9988.239230040203, 17642.021311719596], [19, 9069.946882572394, 20571.81257817196], [20, 8690.535968023305, 17887.57437457218], [21, 9392.620252720684, 20131.438299612913], [22, 11755.079799711288, 20652.268356829984], [23, 12580.809464938347, 21326.35752526545], [24, 8873.660371306636, 21445.852530080712], [25, 11174.444448184562, 17374.99260124299], [26, 11035.14695217786, 20684.85401703482], [27, 9390.983360690047, 17222.7275680976], [28, 12979.115982173329, 19100.378178119186], [29, 10940.637105273376, 16498.602959006275], [30, 10703.114881134923, 17578.533676312636], [31, 8698.562499982154, 22178.258869102567], [32, 9121.127032282267, 16758.94197036054], [33, 8908.962561674976, 22958.02925877072], [34, 7576.677307132973, 17904.209422676027], [35, 13021.049181921662, 21881.29010567054], [36, 9095.483840856283, 23600.423096902985], [37, 8460.109925531417, 20257.880511603184], [38, 8131.867682859495, 22052.350239958174], [39, 10853.285936171082, 18680.09783113293], [40, 13273.950912919257, 18140.025648710824], [41, 7143.753192579327, 22119.819759160353], [42, 10832.049649153298, 21219.60831025498], [43, 9950.353034827425, 16331.285548880065], [44, 7176.43668653844, 18973.714858609936], [45, 7156.78114828654, 17410.010899195055], [46, 13078.261692774468, 17547.21371125115], [47, 10056.540456634217, 16907.529123110206], [48, 9751.395707409205, 18267.80311608865], [49, 9836.057855335906, 23978.02576145126], [50, 9378.743307135468, 21660.723703062667], [51, 7034.2954345067765, 21608.056139425473], [52, 6917.255073393558, 16959.943462375206], [53, 9886.37815723769, 24875.064469251196], [54, 11819.49361804467, 21288.7446378568], [55, 8790.197348245521, 24263.259445745072], [56, 12933.559442693804, 22816.255190952255], [57, 12796.015304454972, 19773.233607319456], [58, 8290.595886986495, 23607.832499005748], [59, 7275.756069489814, 22693.39571480285], [60, 10721.954836840536, 24525.809598760905], [61, 7894.492289363269, 19991.93421187775], [62, 9300.772502751559, 24654.911756081743], [63, 7563.269218411001, 23885.618411037012], [64, 6877.883622637549, 18375.65625347044], [65, 12250.127104659025, 17025.796132973304], [66, 9946.749962188283, 22330.92210044203], [67, 11707.879536190358, 16734.56441464083], [68, 13115.810108949943, 21243.899338964995], [69, 13543.523452383593, 21880.78657295773], [70, 13462.479559529405, 19584.825374374977], [71, 9664.996621671224, 21124.701782390177], [72, 9167.599560872131, 22512.580586026797], [73, 7622.271143768444, 21144.012974806243], [74, 11988.855851285423, 20127.96012964381], [75, 11316.724592789957, 24272.738348605355], [76, 12182.831183988279, 16321.806754521118], [77, 11935.782985502046, 23664.459685295125], [78, 11167.042268667748, 18037.505401893777], [79, 7774.975399328121, 16944.63368712339], [80, 11169.699729846705, 21663.88425252424], [81, 12543.58192463954, 23969.961704550547], [82, 8657.419891354868, 18488.20756902584], [83, 9273.351858481183, 15924.153860815088], [84, 7160.732047889395, 20945.068026304754], [85, 12160.777708611742, 24742.824719113134], [86, 9740.625573381534, 15389.227788462178], [87, 6743.591558034723, 24445.82387522336], [88, 11532.94451638937, 23357.75108247955], [89, 6351.676968762759, 24828.526911865058], [90, 8881.801800407502, 25547.271271705395], [91, 9671.08739672401, 14699.97295204355], [92, 6296.552297881513, 17404.070769171143], [93, 10792.503377524998, 23706.62596425036], [94, 12427.61485799892, 17564.562051381134], [95, 11425.75915101407, 22303.980378081822], [96, 9735.824854079972, 13972.566892611332], [97, 6776.691155353759, 20513.682641072588], [98, 13526.71061667008, 20859.575295385792], [99, 5813.562539757361, 23993.665340567455]]
    # central_platform_locations= [[9678.542996070477, 12972.566892611332]]
    # name='Sheringham Shoal'
    # WT_List=[[0, 371699.5719219753, 5893241.806519924], [1, 371995.3916897116, 5892425.047601489], [2, 372291.3211300142, 5891608.309391071], [3, 372587.40957536316, 5890793.445684481], [4, 372882.4435747459, 5889976.778503153], [5, 373178.701618516, 5889160.102382287], [6, 373474.00324840855, 5888345.330233697], [7, 373769.3649981286, 5887528.724892957], [8, 372367.3944881697, 5892954.9457356], [9, 372662.2826866942, 5892140.113842672], [10, 372958.34498994105, 5891323.419147399], [11, 373253.45153464744, 5890508.6284770295], [12, 373549.7327848602, 5889691.975161428], [13, 373846.12364272366, 5888875.342581324], [14, 374141.5577436912, 5888060.613827967], [15, 374437.0522109928, 5887244.051888607], [16, 373034.2787428773, 5892671.916643782], [17, 373329.2502761629, 5891855.274317262], [18, 373625.44543083035, 5891038.623146914], [19, 373921.7502092533, 5890221.992707997], [20, 374217.09855293424, 5889407.2660823865], [21, 374512.50728671474, 5888590.706263175], [22, 374808.07365863345, 5887776.020843163], [23, 375103.70064295316, 5886959.502243293], [24, 373701.14117933105, 5892385.2741902955], [25, 373997.3598671812, 5891568.645893387], [26, 374292.62244248076, 5890753.9213963365], [27, 374587.9454316481, 5889937.36369809], [28, 374884.54086877685, 5889122.651272739], [29, 375180.0823296546, 5888306.134857392], [30, 375475.73297124443, 5887489.639057397], [31, 375771.49277738784, 5886673.163878971], [32, 374368.1294053509, 5892100.579769947], [33, 374664.4809378369, 5891283.995008986], [34, 374959.8760146963, 5890469.3139023855], [35, 375255.3317519824, 5889652.799600759], [36, 375550.89668603474, 5888836.305910463], [37, 375846.57080069993, 5888019.832837754], [38, 376142.4019959868, 5887205.234185741], [39, 376438.29429617216, 5886388.802366199], [40, 375035.19420472725, 5891815.9795934465], [41, 375331.67857033823, 5890999.4383782], [42, 375627.15797487483, 5890182.94687], [43, 375922.7946111842, 5889368.329776515], [44, 376218.49226561154, 5888551.8795010615], [45, 376514.2990843741, 5887735.449851662], [46, 376810.2150513149, 5886919.040834519], [47, 377105.17218006426, 5886104.534852779], [48, 375702.2874126797, 5891529.619862177], [49, 375997.83832749014, 5890715.004879552], [50, 376294.5649003857, 5889898.527907181], [51, 376589.17142149794, 5889082.129157247], [52, 376885.00172293803, 5888265.722235409], [53, 377180.98869090143, 5887451.189750126], [54, 377477.0371451763, 5886634.824102809], [55, 377772.07915434014, 5885818.507544663], [56, 376369.50559096, 5891245.208191273], [57, 376665.1412246148, 5890428.782812815], [58, 376960.9336758249, 5889614.231864982], [59, 377256.78752666747, 5888797.847740677], [60, 377552.75052549806, 5887981.484253119], [61, 377847.7074089357, 5887165.169837662], [62, 378143.8884662277, 5886348.847570532], [63, 378440.1786230234, 5885532.545958748], [64, 377036.80031198735, 5890960.89078442], [65, 377332.5686802814, 5890144.50882459], [66, 377628.446212595, 5889328.1474975245], [67, 377924.4328927772, 5888511.806809452], [68, 378219.4135821399, 5887695.515110976], [69, 378515.6653140885, 5886881.0694543375], [70, 378810.8635246777, 5886064.818849385], [71, 379107.2861296495, 5885248.560635188], [72, 377704.1241993909, 5890674.8138361825], [73, 378000.0254180379, 5889858.475305391], [74, 378294.9680879301, 5889044.039557952], [75, 378591.0872697145, 5888227.7422435], [76, 378887.31556697463, 5887411.465582661], [77, 379182.5375881144, 5886595.237698214], [78, 379477.86831442814, 5885779.030336655], [79, 379773.3077298053, 5884962.843504098], [80, 378370.45774357766, 5890390.713293606], [81, 378666.49148480647, 5889574.418129274], [82, 378962.63435755007, 5888758.143614624], [83, 379257.7712839471, 5887941.91785935], [84, 379554.1321822215, 5887125.684590942], [85, 379849.4867238326, 5886309.499951179], [86, 380144.94995438034, 5885493.33584266], [87, 380440.5218577546, 5884677.192271525]]
    # central_platform_locations=[[374258.98870082205, 5889940.42689391],[377955.9295068521, 5887952.645952081]]
    # name='Walney1'
    # WT_List=[[0, 470700.0519758684, 5986944.077405927], [1, 470141.4633088345, 5987444.436992147], [2, 469582.66797249735, 5987944.866788965], [3, 469024.1026254509, 5988445.36398708], [4, 468465.438616437, 5988945.74533049], [5, 467906.78507381084, 5989446.010131838], [6, 467348.0354941398, 5989946.530056367], [7, 466789.5146339284, 5990446.931958795], [8, 466230.8951768803, 5990947.218174867], [9, 465672.17988966615, 5991447.759640807], [10, 465113.58423521, 5991948.183913912], [11, 469789.9795978106, 5986643.197601605], [12, 469231.3408848343, 5987143.482083133], [13, 468672.7137743346, 5987643.835381663], [14, 468113.98917418305, 5988144.258277019], [15, 467555.3854293765, 5988644.749309866], [16, 466996.7921153519, 5989145.123813369], [17, 466438.10145080177, 5989645.568040247], [18, 465879.5303444295, 5990145.8950183885], [19, 465320.86196522653, 5990646.291804205], [20, 464762.20546945883, 5991146.757636321], [21, 468879.8944103828, 5986342.12454561], [22, 468321.31721836084, 5986842.704070766], [23, 467762.6399352937, 5987342.982318456], [24, 467203.9755952672, 5987843.51488409], [25, 466645.4294495736, 5988343.744711976], [26, 466086.6780718186, 5988844.230486631], [27, 465528.15534567146, 5989344.598202739], [28, 464969.42617675633, 5989845.036543218], [29, 464410.8179560335, 5990345.543101727], [30, 467969.90799218166, 5986041.228303273], [31, 467411.2792861988, 5986541.547312371], [32, 466852.55432011053, 5987042.121403023], [33, 466293.9488624308, 5987542.578191056], [34, 465735.3537155807, 5988042.918472514], [35, 465176.77025479503, 5988543.32770927], [36, 464617.97887204046, 5989043.62216363], [37, 464059.4189333042, 5989544.169424382], [38, 467059.90989339625, 5985740.324105964], [39, 466501.2321630026, 5986240.7534928145], [40, 465942.56467708654, 5986741.066354277], [41, 465383.9101864116, 5987241.633584609], [42, 464825.26599444373, 5987742.084347507], [43, 464266.6320831295, 5988242.4186718315], [44, 463708.00988654204, 5988742.822019298], [45, 466149.7908435478, 5985439.412703788], [46, 465591.17187489383, 5985939.766267085], [47, 465032.564468099, 5986440.188750061], [48, 464473.9695252009, 5986940.791441247], [49, 463915.27393679344, 5987441.056008246], [50, 463356.59088994766, 5987941.500867804]]
    # central_platform_locations=[[467098.75856926845, 5988612]]
    # name = "Gwynt"
    # WT_List = [[0, 459441.6993065632, 5926964.419429744], [1, 460159.4141880284, 5926965.736468953],[2, 460877.1271657141, 5926967.162420835], [3, 462486.43410463945, 5927004.189045537],[4, 463204.1360586641, 5927005.966982847], [5, 463921.83615248837, 5927007.854942454],[6, 464639.5204374885, 5927007.997281583], [7, 459086.0987814048, 5926381.527669789], [8, 459805.00877598056, 5926382.780653938], [9, 460522.81107242394, 5926384.153233846], [10, 462128.6911199685, 5926382.149509275], [11, 462846.488192115, 5926383.874683669], [12, 463564.2834566511, 5926385.707661511], [13, 464282.06285378244, 5926385.796139746], [14, 464999.85458896594, 5926387.848061185], [15, 465686.4369191773, 5926356.858553827], [16, 458011.04856699187, 5925756.779953272], [17, 465360.2844421859, 5925767.727252839], [18, 466036.19085211767, 5925777.660575316], [19, 458728.9661202731, 5925759.734183486], [20, 459446.849440374, 5925759.0894157775], [21, 460164.76277837536, 5925762.261498855], [22, 460882.6583926553, 5925763.689099623], [23, 462488.74763033836, 5925761.808498565], [24, 463206.62358592503, 5925761.734189016], [25, 463924.51244198106, 5925763.623325531], [26, 464642.3994130705, 5925765.620271799], [27, 457652.6219922533, 5925135.077222065], [28, 465002.8179645692, 5925143.6194014], [29, 465720.7965519036, 5925145.780335235], [30, 466438.7601660682, 5925146.196781144], [31, 458370.61851795064, 5925136.1241231905],[32, 459088.6132148289, 5925137.278844075], [33, 459806.6060284827, 5925138.543609773], [34, 460524.59707443416, 5925139.917306177], [35, 462130.89942870423, 5925137.916136341], [36, 462848.88530718774, 5925139.641355943], [37, 463566.8692626145, 5925141.4766179025], [38, 464284.85141138954, 5925143.4208082445], [39, 455140.8882686299, 5924507.359209624], [40, 462491.05423146154, 5924517.576865624], [41, 463209.13340153097, 5924519.357133284],  [42, 463927.21064463654, 5924521.247449497], [43, 464645.27222487936, 5924521.392176862], [44, 465363.3460545966, 5924523.500361362], [45, 466080.2983354392, 5924523.870883255], [46, 466798.3685826683, 5924526.195654977], [47, 467516.42427016975, 5924526.775944956], [48, 455859.0031731814, 5924509.8789246995], [49, 456577.09871894127, 5924510.654183696], [50, 457295.19239756936, 5924511.538383209], [51, 458013.3007752298, 5924514.384922763], [52, 458731.39061527984, 5924515.487001157], [53, 459449.4785563691, 5924516.696906064], [54, 460167.56474305777, 5924518.016860825], [55, 460884.5427182218, 5924519.454896047], [56, 454783.09740593785, 5923885.862232086], [57, 462133.13041862485, 5923895.538496991], [58, 462851.29019349004, 5923895.4114703825], [59, 463569.4629361687, 5923897.247904224], [60, 464286.5272821167, 5923899.200514524], [61, 465004.69620590063, 5923901.25466409], [62, 465722.84988053585, 5923901.563230896], [63, 466441.01536847855, 5923903.835260341], [64, 467159.16602225247, 5923904.361705294], [65, 467877.327970698, 5923906.850500941], [66, 455501.2901367648, 5923886.474761605], [67, 456219.49821750744, 5923889.049634829], [68, 456937.68701388064, 5923889.88005985], [69, 457654.7675479191, 5923890.829327579], [70, 458372.95278532594, 5923891.87636333], [71, 459091.1522383839, 5923894.887970368], [72, 459809.33348226635, 5923896.152897527], [73, 460527.5129678423, 5923897.527880732], [74, 454425.1963672582, 5923262.538998684], [75, 460887.54160303925, 5923275.212764468], [76, 462493.36866592575, 5923273.346448856], [77, 463211.63655198074, 5923275.12899561], [78, 463928.79590755305, 5923277.028920965], [79, 464647.0462021265, 5923277.174676245], [80, 465365.3086650738, 5923279.282786074], [81, 466083.5693108742, 5923281.500954986], [82, 466800.7083981768, 5923281.9813067345], [83, 467518.96552049485, 5923284.417199748], [84, 468237.20822225633, 5923285.107514451], [85, 455143.5020384612, 5923264.951126042], [86, 455861.7880850936, 5923265.61881533], [87, 456578.96566680324, 5923266.405605838], [88, 457297.26476779475, 5923269.144430551], [89, 458015.54513127415, 5923270.138811441], [90, 458733.8236691888, 5923271.241031625], [91, 459450.9937270475, 5923272.462792289], [92, 460169.26855550567, 5923273.783859739], [93, 454068.3275244537, 5922641.085565572], [94, 460529.31508929486, 5922653.296601454], [95, 462135.3544987852, 5922651.309776112], [96, 462853.71744426084, 5922653.037317613], [97, 463570.9717924201, 5922654.883439328], [98, 464289.3170917119, 5922654.975316793], [99, 465007.674774754, 5922657.030665235], [100, 465724.9237579525, 5922659.201864736], [101, 466443.26445216686, 5922659.620432173], [102, 467161.60387226864, 5922660.14795017], [103, 467878.8477209855, 5922662.646447684], [104, 454785.60391124466, 5922641.601233883], [105, 468597.1841573077, 5922663.391699628], [106, 469315.5311797266, 5922666.100426013], [107, 455504.0027485449, 5922644.068520432], [108, 456221.27528507134, 5922644.801606966], [109, 456939.6527757871, 5922645.63325486], [110, 457658.04509779956, 5922648.4272565935], [111, 458375.3119432416, 5922649.486549818], [112, 459093.6837738591, 5922650.643793212], [113, 459812.0537207237, 5922651.9111071145], [114, 454427.93425863265, 5922051.652827185], [115, 460889.4573377584, 5922032.837725661], [116, 462495.70569930086, 5922030.973986618], [117, 463213.0406294889, 5922030.911783924], [118, 463931.49525155104, 5922032.803179981], [119, 464649.94807148864, 5922034.8046488175], [120, 465367.29205750325, 5922036.923170831], [121, 466085.7278248216, 5922037.287873634], [122, 466799.8514862391, 5922054.479901108], [123, 455146.1075301369, 5922020.691968218], [124, 455863.4752935328, 5922021.371343429], [125, 456581.9651481341, 5922024.002595857], [126, 457299.3290388134, 5922024.899400542], [127, 458017.7980725899, 5922025.893911817], [128, 458736.2814545088, 5922028.853008177], [129, 459453.63961091253, 5922030.074924036], [130, 460172.1028376936, 5922031.397273953], [131, 455505.6001035967, 5921399.82160361], [132, 462856.13804467535, 5921408.81208737], [133, 463573.58076769335, 5921410.659382215], [134, 456224.1851815012, 5921402.399061246], [135, 456941.64401692647, 5921403.242162954], [136, 457660.20815455576, 5921404.184007517], [137, 458377.66336568724, 5921405.243436323], [138, 459096.2238720502, 5921406.403055035], [139, 459813.67544903804, 5921407.681033953], [140, 460532.23221866466, 5921409.0573129505], [141, 462137.6011778128, 5921408.93678312], [142, 456583.8496788125, 5920779.758659322], [143, 457302.5258814839, 5920782.500107177], [144, 458020.0760456584, 5920783.506952609], [145, 458738.73163468577, 5920784.611686777], [146, 459456.2781620802, 5920785.835983101], [147, 460173.8228604673, 5920787.168920322],  [148, 460892.4728923558, 5920788.6002486], [149, 462498.0358080813, 5920786.74822472],[150, 457662.3798086427, 5920159.941969918], [151, 458380.03966124955, 5920162.858262983],[152, 459098.78851512796, 5920164.018034596], [153, 459816.428158879, 5920165.297289694], [154, 460534.065969818, 5920166.685191828], [155, 458022.34616628813, 5919539.266698915], [156, 458741.1903897782, 5919540.373804142], [157, 459458.9252508438, 5919541.599369865], [158, 460176.6582733201, 5919542.932476778], [159, 459100.62183842354, 5918964.290601598]]
    # central_platform_locations = [[464107.4101949312, 5924210.21681328], [458557.6238058922, 5921094.002139392]]
    # name='Barrow'
    # WT_List=[[0, 482336.2266630862, 5982594.708765928], [1, 481970.3561861951, 5982926.191039691], [2, 481605.6305661812, 5983257.698080603], [3, 481240.95709241804, 5983589.234042294], [4, 480875.23572541634, 5983918.949087668], [5, 480510.6664877563, 5984250.542967437], [6, 480145.0492268668, 5984580.316095969], [7, 482003.3816064054, 5981861.66062294], [8, 481638.56927666016, 5982193.164367253], [9, 481272.71635482146, 5982524.7014423115], [10, 480908.0007617738, 5982854.408786093], [11, 480542.252218011, 5983186.003958343], [12, 480177.640562582, 5983515.769219947], [13, 479813.08883443486, 5983847.41772664], [14, 479447.4969229777, 5984179.099979807], [15, 481305.5856580518, 5981460.166393137], [16, 480940.7833687051, 5981789.8704492515], [17, 480574.9478557584, 5982121.462326081], [18, 480210.24949078244, 5982451.224306888], [19, 479845.61103064765, 5982782.869533297], [20, 479479.93213005364, 5983114.548501376], [21, 479114.3055426408, 5983446.256551689], [22, 480973.58354318124, 5980725.334077481], [23, 480608.754149417, 5981056.918095737], [24, 480243.969008446, 5981386.676708869], [25, 479878.15082728054, 5981718.32330236], [26, 479513.47779285174, 5982049.994163989], [27, 479147.76414276456, 5982381.698845545], [28, 478783.1870193452, 5982711.573287291], [29, 478417.57776979357, 5983043.336044547]]
    # central_platform_locations=[[482283.2420978712, 5982168.408105517]]

    # List of cable types: [Capacity,Cost] in increasing order (maximum 3 cable types)
    # Cable_List = [[6, 256 + 365], [10, 406 + 365]]
    # Cable_List=[[5,110],[8,180]]
    WT_List = [[0, 0.0, 0.0], [1, 0.0, 100.0], [2, 0.0, 200.0], [3, 0.0, 300.0], [4, 0.0, 400.0], [5, 100.0, 0.0], [6, 100.0, 100.0], [7, 100.0, 200.0], [8, 100.0, 300.0], [9, 100.0, 400.0], [10, 200.0, 0.0], [11, 200.0, 100.0], [12, 200.0, 200.0], [13, 200.0, 300.0], [14, 200.0, 400.0], [15, 300.0, 0.0], [16, 300.0, 100.0], [17, 300.0, 200.0], [18, 300.0, 300.0], [19, 300.0, 400.0], [20, 400.0, 0.0], [21, 400.0, 100.0], [22, 400.0, 200.0], [23, 400.0, 300.0], [24, 400.0, 400.0]]
    central_platform_locations = [[250.0, 250.0]]
    Cable_List = [[5, 406+365]]
    Crossing_penalty = 0
    # Area=[[[491858.09, 5725044.65], [502208.11, 5738192.56]], [[508800.53, 5726317.36], [491112.91, 5734678.83]], [[487136.52, 5729617.8], [496459.2, 5732167.05]], [[496459.2, 5732167.05], [500959.72, 5737797.21]], [[494364.31, 5722617.21], [502992.7, 5734016.99]], [[502992.7, 5734016.99], [505471.71, 5734528.44]], [[505471.71, 5734528.44], [506574.97, 5735738.54]], [[501212.81, 5715983.99], [501194.99, 5718210.4]], [[501194.99, 5718210.4], [504863.36, 5738179.94]]]
    Area = []
    # Transmission = [[central_platform_locations[0], [463000, 5918000]],
    #                 [central_platform_locations[1], [463000, 5918000]]]
    Transmission = []

    print set_cable_topology(WT_List, central_platform_locations, Cable_List, Area, Transmission, Crossing_penalty)
