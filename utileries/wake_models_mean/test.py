# ---------------Create a script to plot "point.dat"
# with open('plotscript.plt', 'w') as out:
#     out.write('plot ')
#     for i in range(28):
#         if i < 27:
#             out.write("'point.dat' u 2:5 every ::" + str(i * 49) + "::" + str((i + 1) * 49 - 1) + " w lp ps 1 title 'ni= " + str((i + 1) * 100) + "',")
#         else:
#             out.write("'point.dat' u 2:5 every ::" + str(i * 49) + "::" + str((i + 1) * 49 - 1) + " w lp ps 1 title 'ni= " + str((i + 1) * 100) + "'\n")
#     out.write('pause -1')


# ---------------Create a script to plot "discretise.dat"
# with open('discrete.plt', 'w') as out:
#     out.write('plot ')
#     for i in range(1,50):
#         if i < 49:
#             out.write("'discretise.dat' every "+str(i)+" w lp pt 7,")
#         else:
#             out.write("'discretise.dat' every "+str(i)+" w lp pt 7\n")
#     out.write('pause -1')


#  -------------------Nested parallel loop don't work---------------------------------
# from joblib import Parallel, delayed
#
# a = [[i * j for i in range(1, 9)] for j in range(1, 9)]
#
#
# def loop1(a1, j):
#     b = a1[j]
#     return Parallel(n_jobs=-1)(delayed(loop2)(b[i]) for i in range(len(b)))
#
#
# def loop2(first):
#     return first ** 2.0
#
# h = Parallel(n_jobs=-1)(delayed(loop1)(a, j) for j in range(len(a)))


#  integrate

from scipy import integrate
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2, num=100)
y = x
y_int = integrate.cumtrapz(y, x, initial=0)
plt.plot(x, y_int, 'ro', x, y[0] + 0.5 * x**2, 'b-', x, y, 'g')
plt.show()