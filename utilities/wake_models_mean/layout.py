def read_layout(layout_file):

    layout = open(layout_file, 'r')
    layout_x = []
    layout_y = []

    for line in layout:
        columns = line.split()
        layout_x.append(float(columns[0]))
        layout_y.append(float(columns[1]))

    return layout_x, layout_y