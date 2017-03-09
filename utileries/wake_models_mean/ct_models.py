from math import floor, ceil
from util import interpolate


def ct_v90(U0):
    if U0 < 4.0:
        return 0.1
    elif U0 <= 25.0:
        return 7.3139922126945e-7 * U0 ** 6.0 - 6.68905596915255e-5 * U0 ** 5.0 + 2.3937885e-3 * U0 ** 4.0 + - 0.0420283143 * U0 ** 3.0 + 0.3716111285 * U0 ** 2.0 - 1.5686969749 * U0 + 3.2991094727
    else:
        return 0.0


def ct_bladed(U0):
    if U0 < 4.0:
        return 0.1
    else:
        return 0.781


def ct_table_LLT(U0):
    v = U0
    if v == 7: return 0.977
    if v == 8: return 0.943
    if v == 9: return 0.899
    if v == 10: return 0.852
    if v == 11: return 0.804


def ct_LLT(U0):
    if ceil(U0) == floor(U0):
        return ct_table_LLT(U0)
    else:
        return interpolate(floor(U0), ct_table_LLT(floor(U0)), ceil(U0), ct_table_LLT(ceil(U0)), U0)

if __name__ == '__main__':
    print ct_v90(8.5)