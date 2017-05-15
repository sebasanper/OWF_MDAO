karman = 0.41


def b1(deficit, Ct):  # Wake width measure
        return (3.56 * Ct / (8.0 * deficit * (1.0 - 0.5 * deficit))) ** 0.5


def F(x):  # Factor for near and far wake
    if x >= 5.5:
        return 1.0
    if x < 5.5:
        if x >= 4.5:
            return 0.65 + ((x - 4.5) / 23.32) ** (1.0 / 3.0)
        else:
            return 0.65 - ((- x + 4.5) / 23.32) ** (1.0 / 3.0)


def E1(x1, Uf, Ud, Dm, ct, I0):  # Eddy viscosity term
    epsilon = F(x1) * (0.015 * b1(Dm, ct) * (Uf - Ud) + (karman ** 2.0) * I0)
    # print epsilon
    return epsilon