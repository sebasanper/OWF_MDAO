class Workflow:

    def __init__(self, inflow_model, wake_turbulence_model, aeroloads_model, depth_model, support_design_model, hydroloads_model, OandM_model, cable_costs_model, cable_efficiency_model, thrust_coefficient_model, wake_mean_model, wake_merging_model, power_model, aep_model, costs_model, finance_model):

        self.inflow_model = inflow_model
        self.wake_turbulence_model = wake_turbulence_model
        self.aeroloads_model = aeroloads_model
        self.depth_model = depth_model
        self.support_design_model = support_design_model
        self.hydroloads_model = hydroloads_model
        self.OandM_model = OandM_model
        self.cable_topology_model = cable_costs_model
        self.cable_efficiency_model = cable_efficiency_model
        self.thrust_coefficient_model = thrust_coefficient_model
        self.wake_mean_model = wake_mean_model
        self.wake_merging_model = wake_merging_model
        self.power_model = power_model
        self.aep_model = aep_model
        self.costs_model = costs_model
        self.finance_model = finance_model

    def connect(self, turbine_coordinates):
        from multiprocessing_on_dill import Pool

        #print turbine_coordinates

        from site_conditions.terrain.terrain_models import depth
        from farm_energy.wake_model_mean_new.wake_1angle import energy_one_angle
        from farm_energy.wake_model_mean_new.wake_1angle_turbulence import max_turbulence_one_angle
        # from costs.investment_costs.BOS_cost.cable_cost.Hybrid import draw_cables
        from farm_description import cable_list, central_platform

        #print "=== PREPARING WIND CONDITIONS ==="
        self.windrose = self.inflow_model()
        self.wind_directions = self.windrose.direction
        self.direction_probabilities = self.windrose.dir_probability

        if self.inflow_model == MeanWind:
            self.wind_speeds = self.windrose.speed
            self.freestream_turbulence = [0.11]
            self.wind_speeds_probabilities = [[100.0] for _ in range(len(self.wind_directions))]
            # self.wind_speeds = [8.5 for _ in self.wind_speeds]

        elif self.inflow_model == WeibullWind:
            self.wind_speeds = [range(25) for _ in range(len(self.wind_directions))]
            self.freestream_turbulence = [0.11 for _ in range(len(self.wind_speeds[0]))]
            self.wind_speeds_probabilities = self.windrose.speed_probabilities(self.wind_speeds[0])

        #print "=== CALCULATING WATER DEPTH ==="
        self.water_depths = depth(turbine_coordinates, self.depth_model)

        #print "=== OPTIMISING INFIELD CABLE TOPOLOGY (COST)==="
        # draw_cables(turbine_coordinates, central_platform, cable_list)
        self.cable_topology_costs, self.cable_topology = self.cable_topology_model(turbine_coordinates)
        #print str(self.cable_topology_costs) + " EUR"

        self.energies_per_angle = []
        self.turbulences_per_angle = []
        self.cable_efficiencies_per_angle = []
        self.array_efficiencies = []
        # #print [sum(self.wind_speeds_probabilities[i]) for i in range(len(self.wind_speeds_probabilities))]

        #print "=== CALCULATING ENERGY, TURBULENCE PER WIND DIRECTION ==="

        def angle_loop(i):
            self.aero_energy_one_angle, self.powers_one_angle = energy_one_angle(turbine_coordinates, self.wind_speeds[i], self.wind_speeds_probabilities[i], self.wind_directions[i], self.freestream_turbulence, self.wake_mean_model, self.power_model, self.thrust_coefficient_model, self.wake_merging_model)
            # #print self.aero_energy_one_angle
            # #print self.powers_one_angle, max(self.powers_one_angle)
            # #print turbine_coordinates, self.wind_speeds[i], self.windrose.direction[i], self.freestream_turbulence[0], Jensen, self.thrust_coefficient_model, self.wake_turbulence_model
            self.turbulences = max_turbulence_one_angle(turbine_coordinates, self.wind_speeds[i], self.windrose.direction[i], self.freestream_turbulence, Jensen, self.thrust_coefficient_model, self.wake_turbulence_model)

            self.cable_topology_efficiency = self.cable_efficiency_model(self.cable_topology, turbine_coordinates, self.powers_one_angle)

            self.energy_one_angle_weighted = self.aero_energy_one_angle * self.direction_probabilities[i] / 100.0
            self.array_efficiency = (self.aero_energy_one_angle / (float(len(turbine_coordinates)) * max(self.powers_one_angle) * 8760.0))
            self.array_efficiencies_weighted = self.array_efficiency * self.direction_probabilities[i] / 100.0

            self.array_efficiencies.append(self.array_efficiencies_weighted)
            self.energies_per_angle.append(self.energy_one_angle_weighted)
            self.turbulences_per_angle.append(self.turbulences)
            self.cable_efficiencies_per_angle.append(self.cable_topology_efficiency)

        p = Pool(8)
        p.map(angle_loop, range(12))

        # #print self.array_efficiencies
        #print " --- Array efficiency---"
        self.array_efficiency = sum(self.array_efficiencies)
        #print str(self.array_efficiency * 100.0) + " %\n"

        #print " --- Farm annual energy without losses---"
        self.farm_annual_energy = sum(self.energies_per_angle)
        #print str(self.farm_annual_energy / 1000000.0) + " MWh\n"

        #print " --- Infield cable system efficiency ---"
        self.cable_efficiency = sum(self.cable_efficiencies_per_angle) / len(self.cable_efficiencies_per_angle)
        #print str(self.cable_efficiency * 100.0) + " %\n"

        #print " --- Maximum wind turbulence intensity ---"
        self.turbulence = max(self.turbulences_per_angle)
        #print str(self.turbulence * 100.0) + " %\n"

        #print " --- Support structure costs ---"
        self.support_costs = self.support_design_model(self.water_depths, self.turbulence)
        #print str(self.support_costs) + " EUR\n"

        self.aeroloads = 0.0
        self.hydroloads = 0.0

        #print " --- O&M costs ---"
        self.om_costs, self.availability = self.OandM_model(self.farm_annual_energy, self.aeroloads, self.hydroloads, turbine_coordinates)
        #print str(self.om_costs * 20.0) + " EUR\n"

        #print " --- AEP ---"
        self.aep = self.aep_model(self.farm_annual_energy, self.availability, self.cable_topology_efficiency) * 20.0
        #print str(self.aep / 1000000.0) + " MWh\n"

        #print " --- Total costs ---"
        self.total_costs = self.costs_model(self.cable_topology_costs, self.support_costs, self.om_costs * 20.0)
        #print str(self.total_costs) + " EUR\n"

        #print " --- COE ---"
        self.finance = self.finance_model(self.total_costs * 100.0, self.aep / 1000.0)
        print(str(self.finance) + " cents/kWh\n")

    def run(self, layout_file):
        from farm_energy.layout.layout import read_layout
        self.coordinates = read_layout(layout_file)
        self.connect(self.coordinates)


if __name__ == '__main__':
    from site_conditions.wind_conditions.windrose import MeanWind, WeibullWind
    from costs.investment_costs.BOS_cost.cable_cost.Cables_cost_topology import cable_design
    from costs.investment_costs.BOS_cost.cable_cost.cable_efficiency import infield_efficiency
    from costs.OM_costs.om_models import oandm
    from costs.investment_costs.BOS_cost.support_cost.farm_support_cost import farm_support_cost
    from finance.finance_models import COE
    from farm_energy.AEP.aep import aep_average
    from costs.total_cost import total_costs
    from farm_energy.wake_model_mean_new.aero_power_ct_models.thrust_coefficient import ct_v80
    from farm_energy.wake_model_mean_new.wake_turbulence_models import frandsen2, danish_recommendation, frandsen, larsen_turbulence, Quarton
    from site_conditions.terrain.terrain_models import Gaussian, Flat, Plane, Rough
    from farm_energy.wake_model_mean_new.downstream_effects import JensenEffects as Jensen, LarsenEffects as Larsen, Ainslie1DEffects as Ainslie1D, Ainslie2DEffects as Ainslie2D
    from farm_energy.wake_model_mean_new.wake_overlap import root_sum_square
    from farm_energy.wake_model_mean_new.aero_power_ct_models.aero_models import power_coefficient, thrust, power_v80, power, thrust_coefficient

    from time import time

    workflow1 = Workflow(MeanWind, frandsen2, None, Flat, farm_support_cost, None, oandm, cable_design, infield_efficiency, ct_v80, Jensen, root_sum_square, power_v80, aep_average, total_costs, COE)
    start = time()
    workflow1.run("coordinates.dat")
    print("time: " + str(time() - start))
