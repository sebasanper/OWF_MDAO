from numpy import exp


class Flat:
    def __init__(self):
        pass
    def depth(self, x, y):
        return 30.0


class Plane:

    def __init__(self):
        point1 = [0.0, 0.0, 0.0]
        point2 = [1.0, 2.0, 3.0]
        point3 = [- 4.0, 2.0, - 1.0]
        self.point1 = [float(point1[i]) for i in range(3)]
        self.point2 = [float(point2[i]) for i in range(3)]
        self.point3 = [float(point3[i]) for i in range(3)]

    def depth(self, x, y):
        x1 = self.point1[0]
        x2 = self.point2[0]
        x3 = self.point3[0]
        y1 = self.point1[1]
        y2 = self.point2[1]
        y3 = self.point3[1]
        z1 = self.point1[2]
        z2 = self.point2[2]
        z3 = self.point3[2]
        return ((y - y1) * ((x2 - x1) * (z3 - z1) - (x3 - x1) * (z2 - z1))
                - (x - x1) * ((y2 - y1) * (z3 - z1) - (z2 - z1) * (y3 - y1))) \
               / ((x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)) + \
               z1


class Gaussian:
    def __init__(self):
        self.centre = [0, 0]
        self.var_x = 0.2
        self.var_y = 1.0
        self.height = 1.0

    def depth(self, x, y):
        return self.height * exp(
            - ((x - self.centre[0]) ** 2.0 / 2.0 / self.var_x + (y - self.centre[1]) ** 2.0 / 2.0 / self.var_y))


class Rough:
    def __init__(self):
        self.coordinates_x = [float(number) for number in [0, 2, 4, 6, 0, 2, 4, 6, 0, 2, 4, 6, 0, 2, 4, 6]]
        self.coordinates_y = [float(number) for number in [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4]]
        self.depths = [float(number) for number in [0, 1, 0, 1, 1, 2, 1, 2, 0, 1, 0, 1, 1, 2, 1, 2]]

    def depth(self, x, y):
        from scipy.interpolate import interp2d
        degree = 'linear'  # 'cubic' 'quintic'
        function = interp2d(self.coordinates_x, self.coordinates_y, self.depths, kind=degree)
        return function(x, y)[0]


def depth(layout, model_type):
    terrain = model_type()
    return [terrain.depth(layout[i][1], layout[i][2]) for i in range(len(layout))]


if __name__ == '__main__':
    seabed1 = Flat()
    #print seabed1.depth
    #print
    seabed2 = Plane()
    #print seabed2.depth(0, 1)
    #print
    seabed3 = Gaussian()
    #print seabed3.depth(0.4, 0.8)
    #print
    seabed4 = Rough()
    #print seabed4.depth(2.5, 3.1)
    #print Gaussian
    #print depth([[0, 500.0, 0.0], [1, 1000.0, 0.0]], Flat)
# [[0, 500.0, 0.0], [1, 1000.0, 0.0], [2, 1500.0, 0.0], [3, 2000.0, 0.0], [4, 2500.0, 0.0], [5, 3000.0, 0.0]] site_conditions.terrain.terrain_models.Flat