from SupportTeam import design_support


def farm_support_cost(depths, turbulences):
    total_cost = 0
    for i in range(depths):
        total_cost += design_support(depths[i], turbulences[i])
