from farm_energy.layout.layout import read_layout
from site_conditions.wind_conditions.windrose import MeanWind, WeibullWind
from site_conditions.terrain.terrain_models import Plane, Flat, Gaussian, Rough
from costs.investment_costs.BOS_cost.cable_cost.Cables_cost_efficiency import cable_design


class Workflow:

    def __init__(self, inflow, wake_turbulence=7, aeroloads=7, depth=Plane, support_design=7, hydroloads=7, OandM=7, cable_costs=7, cable_efficiency=7, thrust_coefficient=7, wake_mean=7, wake_merging=7, power=7, aep=7, finance=7):

        self.inflow = inflow
        self.wake_turbulence = wake_turbulence
        self.aeroloads = aeroloads
        self.depth = depth
        self.support_design = support_design
        self.hydroloads = hydroloads
        self.OandM = OandM
        self.cable_topology = 0
        self.cable_efficiency = cable_efficiency
        self.thrust_coefficient = thrust_coefficient
        self.wake_mean = wake_mean
        self.wake_merging = wake_merging
        self.power = power
        self.aep = aep
        self.finance = finance

    def connect(self, turbine_coordinates):
        self.windrose = self.inflow()
        self.wind_speeds = self.windrose.speed
        self.probabilities = self.windrose.dir_probability
        self.wind_directions = self.windrose.direction
        self.water_depth_model = self.depth()
        self.water_depths = []
        for turbine in turbine_coordinates:
            self.water_depths.append([turbine[0], self.water_depth_model.depth(turbine[1], turbine[2])])
        self.cable_topology_costs = self.cable_costs(turbine_coordinates)
        self.wake_model = self.WakeAnalysis()

    def run(self, layout_file):
        self.coordinates = read_layout(layout_file)
        self.connect(self.coordinates)
        print self.water_depths


if __name__ == '__main__':
    wkf1 = Workflow(MeanWind)
    print wkf1.run("coords2.dat")
