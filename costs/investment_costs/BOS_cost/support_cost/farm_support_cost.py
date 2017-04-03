from SupportTeam import design_support


def farm_support_cost(depths, turbulence):
    total_cost = 0
    for i in range(len(depths)):
        total_cost += design_support(depths[i], turbulence)
    return total_cost
