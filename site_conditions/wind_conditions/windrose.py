from numpy import exp


class MeanWind:

    def __init__(self):
        self.windrose_file = "/home/sebasanper/PycharmProjects/owf_MDAO/site_conditions/wind_conditions/windrose2.dat"
        self.direction = []
        self.speed = []
        self.dir_probability = []

        with open(self.windrose_file, 'r') as windrose:

            for line in windrose:

                columns = line.split()
                self.direction.append(float(columns[0]))
                self.speed.append([float(columns[1])])
                self.dir_probability.append(float(columns[2]))


class WeibullWind(object):
    def __init__(self):
        self.windrose_file = "/home/sebasanper/PycharmProjects/owf_MDAO/site_conditions/wind_conditions/weibull_windrose.dat"
        self.direction = []
        self.weibull_scale = []
        self.weibull_shape = []
        self.dir_probability = []

        with open(self.windrose_file, 'r') as windrose:

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
                speed_probabilities[- 1].append(100.0 * self.weibull_shape[place] / self.weibull_scale[place] * (wind_speeds[i] / self.weibull_scale[place]) ** (self.weibull_shape[place] - 1.0) * exp(- (wind_speeds[i] / self.weibull_scale[place]) ** self.weibull_shape[place]))

        return speed_probabilities


class WeibullWindBins(WeibullWind):

    def __init__(self):
        super(WeibullWindBins, self).__init__()
        self.cutin = 3
        self.cutout = 25

    def cumulative_weibull(self, wind_speed, weibull_scale_dir, weibull_shape_dir):

        return 1.0 - exp(-(wind_speed / weibull_scale_dir) ** weibull_shape_dir)

    def get_wind_speeds(self, cutin2, cutout2):
        nbins2 = self.nbins
        delta = (cutout2 - cutin2) / nbins2
        windspeeds = []
        for i in range(nbins2 + 1):

            windspeeds.append(cutin2 + i * delta)

        return windspeeds

    def speed_probabilities2(self, cutin, cutout):
        speed_probabilities = []
        self.windspeeds = self.get_wind_speeds(cutin, cutout)

        for angle in self.direction:
            place = self.direction.index(angle)
            prob_cutout = (1.0 - self.cumulative_weibull(self.cutout, self.weibull_scale[place], self.weibull_shape[place]))
            length = len(self.windspeeds)
            windspeedprobabilities = [0.0 for _ in range(length)]

            for i in range(length):

                if i == 0:

                    windspeedprobabilities[i] = (self.cumulative_weibull(self.windspeeds[i], self.weibull_scale[place], self.weibull_shape[place]))

                elif i < length - 1:

                    windspeedprobabilities[i] = (self.cumulative_weibull(self.windspeeds[i], self.weibull_scale[place], self.weibull_shape[place]) - sum(windspeedprobabilities[:i]))

                elif i == length - 1:

                    windspeedprobabilities[i] = (self.cumulative_weibull(self.windspeeds[i], self.weibull_scale[place], self.weibull_shape[place]) - sum(windspeedprobabilities[:i]) + prob_cutout)

            speed_probabilities.append([item * 100.0 for item in windspeedprobabilities])

        return [self.windspeeds for _ in range(len(self.direction))], speed_probabilities


if __name__ == '__main__':
    seb = WeibullWind()
    # print(seb.speed_probabilities(range(3, 26)))
    bas = WeibullWindBins()
    print bas.get_wind_speeds(3.0, 25.0)
    print bas.speed_probabilities2(3.0, 25.0)
