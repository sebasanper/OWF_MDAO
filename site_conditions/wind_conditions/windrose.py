from numpy import exp


class MeanWind:

    def __init__(self):
        self.windrose_file = "windrose2.dat"
        self.direction = []
        self.speed = []
        self.dir_probability = []

        windrose = open(self.windrose_file, 'r')

        for line in windrose:
            columns = line.split()
            self.direction.append(float(columns[0]))
            self.speed.append(float(columns[1]))
            self.dir_probability.append(float(columns[2]))


class WeibullWind:
    def __init__(self):
        self.windrose_file = "weibull_windrose.dat"
        self.direction = []
        self.weibull_scale = []
        self.weibull_shape = []
        self.dir_probability = []

        windrose = open(self.windrose_file, 'r')

        for line in windrose:
            columns = line.split()
            self.direction.append(float(columns[0]))
            self.weibull_scale.append(float(columns[1]))
            self.weibull_shape.append(float(columns[2]))
            self.dir_probability.append(float(columns[3]))

    def speed_probabilities(self, wind_speeds):
        speed_probabilities = []
        for angle in self.direction:
            speed_probabilities.append([])
            place = self.direction.index(angle)
            for i in range(len(wind_speeds)):
                speed_probabilities[-1].append(self.weibull_shape[place] / self.weibull_scale[place] * (wind_speeds[i] / self.weibull_scale[place]) ** (self.weibull_shape[place] - 1.0) * exp(- (wind_speeds[i] / self.weibull_scale[place]) ** self.weibull_shape[place]))
        return speed_probabilities


if __name__ == '__main__':
    seb = WeibullWind()
    print seb.speed_probabilities([0.1, 5])
