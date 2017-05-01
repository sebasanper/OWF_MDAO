def oandm(aep, aeroloads, hydroloads, layout):
    costs_om = 16.0 * aep / 1000000.0
    availability = 0.98
    return costs_om, availability
