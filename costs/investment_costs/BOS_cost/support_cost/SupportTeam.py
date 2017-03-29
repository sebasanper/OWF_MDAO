from lib.designers_support.dimension_team_support import DimensionTeamSupport
from lib.system.properties import RNA
from lib.environment.physical_environment import Site


def design_support(water_depth, TI):
    print "Start"
    dimension_team_support = DimensionTeamSupport()
    dimension_team_support.fsf = TI + 1.0
    rna = RNA()
    site_data = Site()
    site_data.water_depth = water_depth

    # print site_data.water_depth
    dimension_team_support.run(rna, site_data)
    print "The total cost of the support structure is:",

    print "End"
    return dimension_team_support.total_support_structure_cost

if __name__ == '__main__':
    design_support(water_depth=20, TI=0.19)
