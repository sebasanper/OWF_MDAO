with open('gnuplot_max_moment.gp', 'w') as script:
    for i in range(5, 20):
        for j in range(1, 16):
            filename = 'root_moment_w' + str(i) + '_ti' + str(j) + '.dat'
            script.write('stats "' + filename + '" u 3\nset print "max_rm.dat" append\nprint ' + str(i) + ', ' + str(j) + ', STATS_stddev\nset print\n')
        script.write('set print "max_rm.dat" append\nprint ""\nset print\n')