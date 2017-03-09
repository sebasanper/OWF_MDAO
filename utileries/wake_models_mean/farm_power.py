from power_models_openMDAO import power_bladed, power_v90, power_LLT

power = power_v90


def farm_power(vector):
    Ui = [item[1] for item in vector]
    x = [item[0][0] for item in vector]
    y = [item[0][1] for item in vector]

    ind_power = [power(Ui[i]) for i in range(len(Ui))]

    total_farm_power = sum(ind_power)

    with open('power_jensen.dat', 'w') as out:
        for i in range(len(vector)):
            out.write('{0:f}\t{1:f}\t{2:f}\n'.format(x[i], y[i], power(Ui[i])))

    return total_farm_power


if __name__ == '__main__':
    print(farm_power([[(3920.0, 0.0), 6.095407644568307], [(2800.0, 0.0), 6.111950698893546], [(0.0, 0.0), 8.5], [(1120.0, 0.0), 6.248272408528181], [(4480.0, 0.0), 6.091291779875209], [(1680.0, 0.0), 6.165034955259655], [(3360.0, 0.0), 6.10171654138902], [(2240.0, 0.0), 6.12987925102486], [(560.0, 0.0), 6.541454095406106]]))

