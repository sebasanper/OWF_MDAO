from numpy import exp


class MeanWind(object):

    def __init__(self, windrose_file):
        from math import gamma
        self.windrose_file = windrose_file
        self.direction = []
        self.weibull_scale = []
        self.weibull_shape = []
        self.dir_probability = []
        self.expected_wind_speeds = []
        self.nbins = 0

        with open(self.windrose_file, 'r') as windrose:

            for line in windrose:
                columns = line.split()
                self.direction.append(float(columns[0]))
                self.weibull_scale.append(float(columns[1]))
                self.weibull_shape.append(float(columns[2]))
                self.dir_probability.append(float(columns[3]))
                self.expected_wind_speeds.append([self.weibull_scale[-1] * gamma(1.0 + 1.0 / self.weibull_shape[-1])])  # Gamma function used in the expected value of a Weibull random variable.


class WeibullWindBins(object):

    def __init__(self, windrose_file):
        self.windrose_file = windrose_file
        self.direction = []
        self.weibull_scale = []
        self.weibull_shape = []
        self.dir_probability = []
        self.cutin = 3.0
        self.cutout = 25.0

        with open(self.windrose_file, 'r') as windrose:

            for line in windrose:
                columns = line.split()
                self.direction.append(float(columns[0]))
                self.weibull_scale.append(float(columns[1]))
                self.weibull_shape.append(float(columns[2]))
                self.dir_probability.append(float(columns[3]))

    def cumulative_weibull(self, wind_speed, weibull_scale_dir, weibull_shape_dir):

        return 1.0 - exp(-(wind_speed / weibull_scale_dir) ** weibull_shape_dir)

    def get_wind_speeds(self):
        delta = (self.cutout - self.cutin) / self.nbins
        windspeeds = []
        for i in range(self.nbins + 1):

            windspeeds.append(self.cutin + i * delta)

        return windspeeds

    def speed_probabilities(self):
        speed_probabilities = []
        self.windspeeds = self.get_wind_speeds()

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
    # print(seb.speed_probabilities(range(3, 26)))
    bas = WeibullWindBins("/home/sebasanper/PycharmProjects/owf_MDAO/site_conditions/wind_conditions/weibull_windrose.dat")
    bas.nbins = 5
    # print bas.get_wind_speeds()
    print bas.speed_probabilities()

    expected = MeanWind("/home/sebasanper/PycharmProjects/owf_MDAO/site_conditions/wind_conditions/weibull_windrose.dat")
    print expected.speed()
