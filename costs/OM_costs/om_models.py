def oandm(aep, aeroloads, hydroloads, layout):
    costs_om = 16 * aep / 1000000.0
    availability = 0.98
    return costs_om, availability


total_operation_maintenance_costs = 0.0238 * 628773403.489