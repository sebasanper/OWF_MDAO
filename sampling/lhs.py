from random import randint

a = [[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]]


def lhs(a):
    final = []
    v = range(len(a))
    for i in range(len(a)):
        bb = randint(0, len(v) - 1)
        aa = randint(0, len(a[bb]) - 1)
        print aa
        final.append([v[bb], a[bb][aa] - 1])
        v.pop(bb)
        print a
        for j in range(len(a)):
            a[j].pop(aa)
        print a
    return final


print lhs(a)
