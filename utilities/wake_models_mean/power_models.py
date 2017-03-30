from math import pi, ceil, floor
from util import interpolate


def power_v90(u0):
    if u0 < 4.0:
        return 0.0
    elif u0 <= 15.0:
        return 3.234808e-4 * u0 ** 7.0 - 0.0331940121 * u0 ** 6.0 + 1.3883148012 * u0 ** 5.0 - 30.3162345004 * u0 ** 4.0 + 367.6835557011 * u0 ** 3.0 - 2441.6860655008 * u0 ** 2.0 + 8345.6777042343 * u0 - 11352.9366182805
    elif u0 <= 25.0:
        return 2000000.0
    else:
        return 0.0


def power_bladed(u0):
    if u0 < 4.0:
        return 0.0
    else:
        return 0.5 * 61.0 ** 2.0 * pi * 1.225 * 0.485 * u0 ** 3.0


def power_table_LLT(U0):
    v = U0
    if v == 7: return 970.0
    if v == 8: return 1780.0
    if v == 9: return 2770.0
    if v == 10: return 3910.0
    if v == 11: return 5190.0


def power_LLT(U0):
    if ceil(U0) == floor(U0):
        return power_table_LLT(U0)
    else:
        return interpolate(floor(U0), power_table_LLT(floor(U0)), ceil(U0), power_table_LLT(ceil(U0)), U0)
