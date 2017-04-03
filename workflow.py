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

        from site_conditions.terrain.terrain_models import depth
        from farm_energy.wake_model_mean_new.wake_1angle import energy_one_angle

        self.windrose = self.inflow_model()
        self.wind_speeds = self.windrose.speed
        self.probabilities = self.windrose.dir_probability
        self.wind_directions = self.windrose.direction
        self.water_depths = depth(turbine_coordinates, self.depth_model)

        self.cable_topology_costs, self.cable_topology = self.cable_topology_model(turbine_coordinates)

        self.energies_per_angle = []
        self.turbulences_per_angle = []
        self.cable_efficiencies_per_angle = []

        for i in range(6, 7):
        # for i in range(len(self.wind_directions)):

            self.aero_energy_one_angle, self.powers_one_angle = energy_one_angle(turbine_coordinates, [self.wind_speeds[i]], [100.0], self.wind_directions[i], [0.08], self.wake_mean_model, self.power_model, self.thrust_coefficient_model, self.wake_merging_model)

            self.turbulences = turbulence_one_angle(turbine_coordinates, self.windrose.speed[i], self.windrose.direction[i], 0.08, Jensen, self.thrust_coefficient_model, self.wake_turbulence_model)
            self.cable_topology_efficiency = self.cable_efficiency_model(self.cable_topology, turbine_coordinates, self.powers_one_angle)

            self.energies_per_angle.append(self.aero_energy_one_angle)
            self.turbulences_per_angle.append(self.turbulences)
            self.cable_efficiencies_per_angle.append(self.cable_topology_efficiency)

        self.farm_annual_energy = sum(self.energies_per_angle)
        self.cable_efficiency = sum(self.cable_efficiencies_per_angle) / len(self.cable_efficiencies_per_angle)
        self.turbulence = max(self.turbulences_per_angle)
        self.support_costs = self.support_design_model(self.water_depths, self.turbulence)
        self.aeroloads = 0.0
        self.hydroloads = 0.0
        self.om_costs, self.availability = self.OandM_model(self.aeroloads, self.hydroloads, turbine_coordinates)
        self.aep = self.aep_model(self.farm_annual_energy, self.availability, self.cable_topology_efficiency)
        print self.cable_topology_costs, self.support_costs, self.om_costs
        self.total_costs = self.costs_model(self.cable_topology_costs, self.support_costs, self.om_costs)

        self.finance = self.finance_model(self.total_costs, self.aep)

    def run(self, layout_file):
        self.coordinates = read_layout(layout_file)
        self.connect(self.coordinates)


if __name__ == '__main__':
    from farm_energy.layout.layout import read_layout
    from site_conditions.wind_conditions.windrose import MeanWind, WeibullWind
    from costs.investment_costs.BOS_cost.cable_cost.Cables_cost_topology import cable_design
    from costs.investment_costs.BOS_cost.cable_cost.cable_efficiency import infield_efficiency
    from costs.OM_costs.om_models import oandm
    from farm_energy.wake_model_mean_new.wake_1angle_turbulence import turbulence_one_angle
    from costs.investment_costs.BOS_cost.support_cost.farm_support_cost import farm_support_cost
    from finance.finance_models import COE
    from farm_energy.AEP.aep import aep_average
    from costs.total_cost import total_costs
    from farm_energy.wake_model_mean_new.aero_power_ct_models.thrust_coefficient import ct_v80
    from farm_energy.wake_model_mean_new.wake_turbulence_models import frandsen2
    from site_conditions.terrain.terrain_models import Gaussian, Flat, Plane, Rough
    from farm_energy.wake_model_mean_new.downstream_effects import JensenEffects as Jensen
    from farm_energy.wake_model_mean_new.wake_overlap import root_sum_square
    from farm_energy.wake_model_mean_new.aero_power_ct_models.aero_models import powerlaw, ctlaw

    workflow1 = Workflow(MeanWind, frandsen2, None, Flat, farm_support_cost, None, oandm, cable_design, infield_efficiency, ctlaw, Jensen, root_sum_square, powerlaw, aep_average, total_costs, COE)
    workflow1.run("coordinates.dat")
    print workflow1.aep
    print workflow1.total_costs
    print workflow1.finance
