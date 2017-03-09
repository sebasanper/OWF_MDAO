def interpolate(minx, miny, maxx, maxy, valx):
    print maxx, minx
    return miny + (maxy - miny) * ((valx - minx) / (maxx - minx))


