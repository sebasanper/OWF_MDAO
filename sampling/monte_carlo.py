from random import randint

with open("monte_carlo_results.dat", "w") as outwrite:
    for n in range(10000):
        a = randint(0, 4)
        b = randint(0, 2)
        c = randint(0, 5)
        d = randint(0, 3)
        e = randint(0, 3)
        f = randint(0, 3)
        g = randint(0, 4)
        h = randint(0, 3)
        i = randint(0, 1)
        j = randint(0, 1)
        outwrite.write("{} {} {} {} {} {} {} {} {} {}\n".format(a, b, c, d, e, f, g, h, i, j))