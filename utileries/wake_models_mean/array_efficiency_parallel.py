from joblib import Parallel, delayed

from farm_energy.layout import read_layout
from power_models import power_v90 as power
from site_conditions.wind_conditions.windrose import read_windrose
from wake_models import jensen_1angle, ainslie_1angle, larsen_1angle, ainsliefull_1angle


def jensen_windrose(layout_file, windrose_file):

    layout_x, layout_y = read_layout(layout_file)
    wind_direction, wind_speed, wind_frequency = read_windrose(windrose_file)
    nt = len(layout_y)

    U = Parallel(n_jobs=-1)(delayed(jensen_1angle)(layout_x, layout_y, wind_speed[i], wind_direction[i], rotor_radius=40.0, k=0.04) for i in range(len(wind_direction)))
    # print U
    P = [[power(u) for u in U[i]] for i in range(len(wind_direction))]

    profit = [sum(powers) for powers in P]
    efficiency = [profit[ii] * 100.0 / (float(nt) * max(P[ii])) for ii in range(len(wind_direction))]  # same as using U0
    efficiency_proportion = [efficiency[i] * wind_frequency[i] / 100.0 for i in range(len(wind_direction))]
    summation = sum(efficiency_proportion)

    # print profit
    # print efficiency
    # print efficiency_proportion
    # print U
    # print P

    return profit


def ainslie_windrose(layout_file, windrose_file):

    layout_x, layout_y = read_layout(layout_file)
    wind_direction, wind_speed, wind_frequency = read_windrose(windrose_file)
    nt = len(layout_y)

    U = Parallel(n_jobs=-1)(delayed(ainslie_1angle)(layout_x, layout_y, wind_speed[i], wind_direction[i], rotor_radius=40.0, TI=0.08) for i in range(len(wind_direction)))
    # print U
    P = [[power(u) for u in U[i]] for i in range(len(wind_direction))]

    profit = [sum(powers) for powers in P]
    efficiency = [profit[ii] * 100.0 / (float(nt) * max(P[ii])) for ii in range(len(wind_direction))]  # same as using U0
    efficiency_proportion = [efficiency[i] * wind_frequency[i] / 100.0 for i in range(len(wind_direction))]
    summation = sum(efficiency_proportion)

    # print profit
    # print efficiency
    # print efficiency_proportion
    # print U
    # print P

    return profit


def ainsliefull_windrose(layout_file, windrose_file):

    layout_x, layout_y = read_layout(layout_file)
    wind_direction, wind_speed, wind_frequency = read_windrose(windrose_file)
    nt = len(layout_y)

    U = Parallel(n_jobs=-1)(delayed(ainsliefull_1angle)(layout_x, layout_y, wind_speed[i], wind_direction[i], rotor_radius=40.0, TI=0.08) for i in range(len(wind_direction)))
    P = [[power(u) for u in U[i]] for i in range(len(wind_direction))]

    profit = [sum(powers) for powers in P]
    efficiency = [profit[ii] * 100.0 / (float(nt) * max(P[ii])) for ii in range(len(wind_direction))]  # same as using U0
    efficiency_proportion = [efficiency[i] * wind_frequency[i] / 100.0 for i in range(len(wind_direction))]
    summation = sum(efficiency_proportion)

    # print profit
    # print efficiency
    # print efficiency_proportion
    # print U
    # print P

    return profit


def larsen_windrose(layout_file, windrose_file):

    layout_x, layout_y = read_layout(layout_file)
    wind_direction, wind_speed, wind_frequency = read_windrose(windrose_file)
    nt = len(layout_y)

    U = Parallel(n_jobs=-1)(delayed(larsen_1angle)(layout_x, layout_y, wind_speed[i], wind_direction[i], rotor_radius=40.0, hub_height=100.0, TI=0.08) for i in range(len(wind_direction)))
    # print U
    P = [[power(u) for u in U[i]] for i in range(len(wind_direction))]

    profit = [sum(powers) for powers in P]
    efficiency = [profit[ii] * 100.0 / (float(nt) * max(P[ii])) for ii in range(len(wind_direction))]  # same as using U0
    efficiency_proportion = [efficiency[i] * wind_frequency[i] / 100.0 for i in range(len(wind_direction))]
    summation = sum(efficiency_proportion)

    # print profit
    # print efficiency
    # print efficiency_proportion
    # print U
    # print P

    return profit


if __name__ == '__main__':

    from time import time

    # start = time()
    # res = jensen_windrose('coordinates.dat', 'windrose2.dat')
    # print time() - start
    # with open('profit30_jensen_parallel.dat', 'w', 1) as angles:
    #     for i in range(len(res)):
    #         angles.write('{0}\n'.format(res[i]))
    start = time()
    res = ainslie_windrose('coordinates.dat', 'windrose.dat')
    print time() - start
    with open('profit_ainslie_parallel_meander.dat', 'w', 1) as angles:
        for i in range(len(res)):
            angles.write('{0}\n'.format(res[i]))
    # start = time()
    # res = larsen_windrose('coordinates.dat', 'windrose2.dat')
    # print time() - start
    # with open('profit30_larsen_parallel.dat', 'w', 1) as angles:
    #     for i in range(len(res)):
    #         angles.write('{0}\n'.format(res[i]))
    # start = time()
    # res = ainsliefull_windrose('coordinates.dat', 'windrose2.dat')
    # print time() - start
    # with open('profit30_ainsfull_parallel.dat', 'a', 1) as angles:
    #     for i in range(len(res)):
    #         angles.write('{0}\n'.format(res[i]))
