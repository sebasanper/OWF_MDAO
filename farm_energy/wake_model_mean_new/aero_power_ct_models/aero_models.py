from util import interpolate
from numpy import pi


class AeroLookup:

    def __init__(self, file_in):

        with open(file_in, "r") as data:
            self.x = []
            self.y = []
            for line in data:
                col = line.split()
                self.x.append(float(col[0]))
                self.y.append(float(col[1]))

    def interpolation(self, value):
        ii = 0
        lower = []
        upper = []
        if value <= self.x[0]:
            # print "Found wind speed less than minimum in data"
            result = self.y[0]
        else:
            for x in self.x:
                if x <= value:
                    lower = [x, self.y[ii]]
                else:
                    upper = [x, self.y[ii]]
                    break
                ii += 1
            result = interpolate(float(lower[0]), float(lower[1]), float(upper[0]), float(upper[1]), value)
        return result


def powerlaw(wind_speed, r, ratedv=11.4, ratedp=5000000.0, cutin=3.0, cutout=25.0):
    table_cp = AeroLookup("nrel_cp.dat")
    if wind_speed < cutin:
        return 0.0
    elif wind_speed <= ratedv:
        cp = table_cp.interpolation(wind_speed)
        return 0.5 * 1.225 * pi * r ** 2.0 * wind_speed ** 3.0 * cp
    elif wind_speed <= cutout:
        return ratedp
    else:
        return 0.0


def power_v80(u0):
    if u0 < 4.0:
        return 0.0
    elif u0 <= 10.0:
        return 3.234808e-4 * u0 ** 7.0 - 0.0331940121 * u0 ** 6.0 + 1.3883148012 * u0 ** 5.0 - 30.3162345004 * u0 ** 4.0 + 367.6835557011 * u0 ** 3.0 - 2441.6860655008 * u0 ** 2.0 + 8345.6777042343 * u0 - 11352.9366182805
    elif u0 <= 25.0:
        return 2000.0
    else:
        return 0.0


def ctlaw(wind_speed, r):
    table_thrust = AeroLookup("./nrel_ct.dat")
    if wind_speed < table_thrust.x[0]:
        T = table_thrust.y[0]
    elif wind_speed > table_thrust.x[-1]:
        T = table_thrust.x[-1]
    else:
        T = table_thrust.interpolation(wind_speed)
    # return 1000.0 * T / (0.5 * 1.225 * pi * r ** 2.0 * wind_speed ** 2.0)
    return 0.79

if __name__ == '__main__':
    table1 = AeroLookup("./nrel_cp.dat")
    for v in range(1, 50):
        print v / 2.0, powerlaw(v / 2.0, 64.0), ctlaw(v / 2.0, 64.0)
