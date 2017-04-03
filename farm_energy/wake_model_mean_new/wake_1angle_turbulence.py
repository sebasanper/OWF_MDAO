from order_layout import order
from utilities.min_distance.distance_algorithm import dist_point


def turbulence_one_angle(original_layout, freestream_wind_speed, wind_angle, ambient_turbulence, WakeModel, ThrustModel, TurbulenceModel):
    ordered_layout = order(original_layout, wind_angle)
    ct = []
    wind_speeds_array = freestream_wind_speed
    deficit_matrix = [[] for _ in range(len(ordered_layout))]
    front = []
    for i in range(len(ordered_layout)):
        ct.append(ThrustModel(wind_speeds_array))
        deficit_matrix[i] = [0.0 for _ in range(i + 1)]
        deficit_matrix[i] += WakeModel(ordered_layout[i], ct[i], ordered_layout[i + 1:], wind_angle, freestream_wind_speed, ambient_turbulence)
    transposed = [list(x) for x in zip(*deficit_matrix)]
    for i in range(len(transposed)):
        lista = transposed[i]
        if len(set(lista)) <= 1:
            front.append(float("inf"))
            continue
        maximo = max(lista)
        indice = lista.index(maximo)
        indice_maximo = ordered_layout[indice][0]
        front.append(indice_maximo)
    # print front
    a = zip([item[0] for item in ordered_layout], front)
    # print a
    turbine_affects = sorted(a, key=lambda pair: pair[0])

    wake_added_turbulence = []
    for item in turbine_affects:
        if float("inf") in item:
            wake_added_turbulence.append(ambient_turbulence)
        else:
            wake_added_turbulence.append(TurbulenceModel(ambient_turbulence, ThrustModel(freestream_wind_speed), dist_point(original_layout[item[0]][1], original_layout[item[0]][2], original_layout[item[1]][1], original_layout[item[1]][2]) / 100.0))

    return max(wake_added_turbulence)

if __name__ == '__main__':

    from aero_power_ct_models.thrust_coefficient import v80
    from downstream_effects import JensenEffects as Jensen
    from wake_turbulence_models import frandsen2

    def average(list):
        return sum([item / len(list) for item in list])

    layout = [[0, 423974.0, 6151447.0], [1, 424033.0, 6150889.0], [2, 424092.0, 6150332.0], [3, 424151.0, 6149774.0], [4, 424210.0, 6149216.0], [5, 424268.0, 6148658.0], [6, 424327.0, 6148101.0], [7, 424386.0, 6147543.0], [8, 424534.0, 6151447.0], [9, 424593.0, 6150889.0], [10, 424652.0, 6150332.0], [11, 424711.0, 6149774.0], [12, 424770.0, 6149216.0], [13, 424829.0, 6148658.0], [14, 424888.0, 6148101.0], [15, 424947.0, 6147543.0], [16, 425094.0, 6151447.0], [17, 425153.0, 6150889.0], [18, 425212.0, 6150332.0], [19, 425271.0, 6149774.0], [20, 425330.0, 6149216.0], [21, 425389.0, 6148658.0], [22, 425448.0, 6148101.0], [23, 425507.0, 6147543.0], [24, 425654.0, 6151447.0], [25, 425713.0, 6150889.0], [26, 425772.0, 6150332.0], [27, 425831.0, 6149774.0], [28, 425890.0, 6149216.0], [29, 425950.0, 6148659.0], [30, 426009.0, 6148101.0], [31, 426068.0, 6147543.0], [32, 426214.0, 6151447.0], [33, 426273.0, 6150889.0], [34, 426332.0, 6150332.0], [35, 426392.0, 6149774.0], [36, 426451.0, 6149216.0], [37, 426510.0, 6148659.0], [38, 426569.0, 6148101.0], [39, 426628.0, 6147543.0], [40, 426774.0, 6151447.0], [41, 426833.0, 6150889.0], [42, 426892.0, 6150332.0], [43, 426952.0, 6149774.0], [44, 427011.0, 6149216.0], [45, 427070.0, 6148659.0], [46, 427129.0, 6148101.0], [47, 427189.0, 6147543.0], [48, 427334.0, 6151447.0], [49, 427393.0, 6150889.0], [50, 427453.0, 6150332.0], [51, 427512.0, 6149774.0], [52, 427571.0, 6149216.0], [53, 427631.0, 6148659.0], [54, 427690.0, 6148101.0], [55, 427749.0, 6147543.0], [56, 427894.0, 6151447.0], [57, 427953.0, 6150889.0], [58, 428013.0, 6150332.0], [59, 428072.0, 6149774.0], [60, 428132.0, 6149216.0], [61, 428191.0, 6148659.0], [62, 428250.0, 6148101.0], [63, 428310.0, 6147543.0], [64, 428454.0, 6151447.0], [65, 428513.0, 6150889.0], [66, 428573.0, 6150332.0], [67, 428632.0, 6149774.0], [68, 428692.0, 6149216.0], [69, 428751.0, 6148659.0], [70, 428811.0, 6148101.0], [71, 428870.0, 6147543.0], [72, 429014.0, 6151447.0], [73, 429074.0, 6150889.0], [74, 429133.0, 6150332.0], [75, 429193.0, 6149774.0], [76, 429252.0, 6149216.0], [77, 429312.0, 6148659.0], [78, 429371.0, 6148101.0], [79, 429431.0, 6147543.0]]
    U_inf = 8.5
    I0 = 0.08
    print turbulence_one_angle(layout, U_inf, 68.0, I0, Jensen, v80, frandsen2)
