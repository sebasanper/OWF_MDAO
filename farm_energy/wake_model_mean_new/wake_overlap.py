from math import sqrt


def root_sum_square(array_deficits):
    #  This is one model, root sum square of individual wind speed deficits.
    total_deficit = sqrt(sum([deficit ** 2.0 for deficit in array_deficits]))
    return total_deficit


def multiplied(array_deficits):
    total_deficit = reduce(lambda x, y: x * y, array_deficits)
    return total_deficit


def summed(array_deficits):
    total_deficit = sum(array_deficits)
    return total_deficit

if __name__ == '__main__':
    deficits = [3, 4]
    print root_sum_square(deficits)
    print multiplied(deficits)
    print summed(deficits)