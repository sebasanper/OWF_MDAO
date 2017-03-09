from order_layout import order
#
# class Wake1Angle:
#     def __init__(self, thrust_coefficient, wake_model, wake_merging, aero_power):
#         # print "Model parameter must be Jensen, Larsen, Ainslie1D or Ainslie2D without quotation marks.\n"
#         self.WakeModel = wake_model
#         self.CT = thrust_coefficient
#         self.overlap = wake_merging
#         self.power = aero_power
#
#     def wake_one_angle(self, original_layout, freestream_wind_speed, wind_angle, ambient_turbulence):
#         ordered_layout = order(original_layout, wind_angle)
#         ct = []
#         wind_speeds_array = [freestream_wind_speed]
#         deficit_matrix = [[] for _ in range(len(ordered_layout))]
#         total_deficit = [0.0]
#         for i in range(len(ordered_layout)):
#             # start = time()
#             if i == 0:
#                 pass
#             else:
#                 total_deficit.append(root_sum_square([deficit_matrix[j][i] for j in range(i)]))
#                 wind_speeds_array.append(freestream_wind_speed * (1.0 - total_deficit[i]))
#             ct.append(self.CT(wind_speeds_array[i]))
#             deficit_matrix[i] = [0.0 for _ in range(i + 1)]
#             deficit_matrix[i] += self.WakeModel(ordered_layout[i], ct[i], [item for item in ordered_layout[i + 1:]], wind_angle, freestream_wind_speed, ambient_turbulence)
#             # print time() - start, wind_angle, i
#         # print deficit_matrix
#         wind_speeds_array_original = [x for (y, x) in sorted(zip([item[1] for item in ordered_layout], wind_speeds_array), key=lambda pair: pair[0])]
#         powers = [self.power(turbine_wind) for turbine_wind in wind_speeds_array_original]
#         return powers


def energy_one_angle(original_layout, freestream_wind_speeds, probabilities_speed, wind_angle, ambient_turbulences, WakeModel, PowerModel, ThrustModel, MergingModel):
    ordered_layout = order(original_layout, wind_angle)
    energy = 0.0
    for speed in range(len(freestream_wind_speeds)):
        ct = []
        wind_speeds_array = [freestream_wind_speeds[speed]]
        deficit_matrix = [[] for _ in range(len(ordered_layout))]
        total_deficit = [0.0]
        for i in range(len(ordered_layout)):
            if i == 0:
                pass
            else:
                total_deficit.append(MergingModel([deficit_matrix[j][i] for j in range(i)]))
                wind_speeds_array.append(freestream_wind_speeds[speed] * (1.0 - total_deficit[i]))
            ct.append(ThrustModel(wind_speeds_array[i]))
            deficit_matrix[i] = [0.0 for _ in range(i + 1)]
            deficit_matrix[i] += WakeModel(ordered_layout[i], ct[i], ordered_layout[i + 1:], wind_angle, freestream_wind_speeds[speed], ambient_turbulences[speed])
        wind_speeds_array_original = [x for (y, x) in sorted(zip([item[0] for item in ordered_layout], wind_speeds_array), key=lambda pair: pair[0])]
        individual_powers = [PowerModel(wind) for wind in wind_speeds_array_original]
        farm_power = sum(individual_powers)
        energy += farm_power * probabilities_speed[speed] / 100.0 * 8760.0
    return energy


if __name__ == '__main__':

    from aero_power_ct_models.thrust_coefficient import v80
    from downstream_effects import Ainslie2DEffects as Ainslie2D, JensenEffects as Jensen
    from aero_power_ct_models.aero_models import power_v80
    from wake_overlap import root_sum_square

    layout = [[0, 500.0, 0.0], [1, 1000.0, 0.0], [2, 1500.0, 0.0], [3, 2000.0, 0.0], [4, 2500.0, 0.0], [5, 3000.0, 0.0]]
    U_inf = [11.0, 10.0, 9.0, 8.0, 7.0, 6.0, 5.0]
    I0 = [0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]
    prob = [14.28, 14.28, 14.28, 14.28, 14.28, 14.28, 14.28]
    angle = 180.0

    print energy_one_angle(layout, U_inf, prob, angle, I0, Jensen, power_v80, v80, root_sum_square)
