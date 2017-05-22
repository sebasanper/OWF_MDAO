from numpy import exp


class Flat:
    def __init__(self):
        pass

    def depth(self, x, y):
        return 13.5


class Plane:
    def __init__(self):
        point1 = [4000.0, 0.0, 15]
        point2 = [0.0, 0.0, 12.0]
        point3 = [0.0, 1.0, 12.0]
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

        return ((y - y1) * ((x2 - x1) * (z3 - z1) - (x3 - x1) * (z2 - z1)) - (x - x1) * ((y2 - y1) * (z3 - z1) - (z2 - z1) * (y3 - y1))) / ((x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)) + z1


class Gaussian:
    def __init__(self):
        self.centre = [2000.0, 450.0]
        self.sigma_x = 3000.0  # Sigma is (max - desired value) times the distance from centre of rectangle to the sides, divided by two. Example: Rectangle is 4000x900. Centre at 2000x450. So 450 to one side, 450 * 3 = 1350 / 2 = 675.0. 3 is 15.0 m - 12.0 m (max - min water depth).
        self.sigma_y = 675.0
        self.height = 15.0

    def depth(self, x, y):
        return self.height * exp(- ((x - self.centre[0]) ** 2.0 / 2.0 / self.sigma_x ** 2.0 + (y - self.centre[1]) ** 2.0 / 2.0 / self.sigma_y ** 2.0))


class Rough:

    def __init__(self):
        from random import random
        self.coordinates_x = [float(number) for number in range(0, 4000, 500)]
        self.coordinates_y = [float(number) for number in range(0, 900, 100)]
        self.depths = [12.0 + random() * 3.0 for _ in range(len(self.coordinates_x) * len(self.coordinates_y))]
        # k = 0
        # for i in self.coordinates_x:
        #     for j in self.coordinates_y:
        #         print i, j, self.depths[k]
        #         k += 1

    def depth(self, x, y):
        from scipy.interpolate import interp2d
        degree = 'linear'  # 'cubic' 'quintic'
        function = interp2d(self.coordinates_x, self.coordinates_y, self.depths, kind=degree)
        return function(x, y)[0]


def depth(layout, model_type):
    terrain = model_type()
    return [terrain.depth(layout[i][1], layout[i][2]) for i in range(len(layout))]


if __name__ == '__main__':
    # seabed1 = Flat()
    # # print seabed1.depth
    # # print
    # seabed2 = Plane()
    # # print seabed2.depth(0, 1)
    # # print
    # seabed3 = Gaussian()
    # print seabed3.depth(2000.0, 0.8)
    # # print
    # seabed4 = Rough()
    # print seabed4.depth(2.5, 3.1)
    # print Gaussian
    # print depth([[0, 500.0, 0.0], [1, 1000.0, 0.0]], Flat)
    # [[0, 500.0, 0.0], [1, 1000.0, 0.0], [2, 1500.0, 0.0], [3, 2000.0, 0.0], [4, 2500.0, 0.0], [5, 3000.0, 0.0]] site_conditions.terrain.terrain_models.Flat
    place1 = [[0, 2000.000000,	450.000000]]
    place2 = [[0, 0.000000,	450.000000]]
    place3 = [[0, 2000.000000,	0.000000]]
    print depth(place1, Flat)
    print depth(place1, Gaussian)
    print depth(place2, Gaussian)
    print depth(place3, Gaussian)
    print depth(place1, Plane)
    print depth(place1, Rough)
