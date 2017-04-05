from multiprocessing_on_dill import Pool


def f(x):
    def g(a):
        return a[0]
    return g(x) ** 2.0

if __name__ == '__main__':
    p = Pool(5)
    print(p.map(f, [[1,0], [2,0], [3,0]]))