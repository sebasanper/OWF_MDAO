def COE(total_costs, aep):
    return total_costs / aep


def LPC(investment, oandm, decommissioning, aep, electrical_efficiency):
    rate = 0.075
    annuity = 1.0 / rate * (1.0 - 1.0 / (1.0 + rate) ** 20.0)
    lpc_previous = (investment * 100.0) / (annuity * (aep / 1000.0)) + oandm * 100.0 / (aep / 1000.0) + decommissioning * 100.0 * (1.0 + 0.075) ** (- 20.0) / (annuity * (aep / 1000.0))
    return lpc_previous / electrical_efficiency


if __name__ == '__main__':
    print LPC(337000000, 10752000, 44000000, 672000000000, 0.95, 0.98)
