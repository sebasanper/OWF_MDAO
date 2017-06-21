plot "histogram.dat" u 2:1 smooth csplines w filledcurves x1
set style fill transparent solid 0.5 noborder
FILES = system("ls -1 histogra*.dat")
plot for [data in FILES] data u 1:2 smooth csplines w filledcurves x1