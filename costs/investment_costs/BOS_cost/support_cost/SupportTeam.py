from costs.investment_costs.BOS_cost.support_cost.lib.designers_support.dimension_team_support import DimensionTeamSupport
from costs.investment_costs.BOS_cost.support_cost.lib.system.properties import RNA
from costs.investment_costs.BOS_cost.support_cost.lib.environment.physical_environment import Site


def design_support(water_depth, TI):
    dimension_team_support = DimensionTeamSupport()
    dimension_team_support.fsf = TI + 1.0
    rna = RNA()
    site_data = Site()
    site_data.water_depth = water_depth

    # print site_data.water_depth
    dimension_team_support.run(rna, site_data)
    return dimension_team_support.total_support_structure_cost

if __name__ == '__main__':
    design_support(water_depth=20, TI=0.19)
