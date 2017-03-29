# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 21:48:57 2016

@author: alv_m_000
"""
import random


def gWTListMaster(xmin, ymin, xmax, ymax, xn, yn,
                  d):  # it creates the structured grid as rows and columns with a fixed step
    tmpList = []
    xstep = (xmax - xmin) / (xn - 1)
    if xstep < d:
        print "Invalid xstep=", xstep
        return []
    ystep = (ymax - ymin) / (yn - 1)
    if ystep < d:
        print "Invalid ystep=", ystep
        return []
    t = 0
    for i in range(xn):
        for j in range(yn):
            tmpList.append([t, xmin + i * xstep, ymax - j * ystep])
            t += 1
    return tmpList


def gRandIndiv(posMax,
               posI):  # it creates the Individual. Each individual is a list which contains posI elements out of posMax elements
    tmpListMax = []

    for i in range(posMax):
        tmpListMax.append(i)
    for i in range(posMax - posI):
        tmpListMax.pop(random.randint(0, len(tmpListMax) - 1))
    # tmpList.sort()  #if uncommented the individual has its numbers sorted
    return tmpListMax


def gIndiv2Layout(WT_List_Master, Indiv):  # converts an individual to a layout with coordinates
    tmpLayout = []
    i = 0
    for pos in Indiv:
        tmpLayout.append([i, WT_List_Master[pos][1], WT_List_Master[pos][2]])
        i = i + 1
    return tmpLayout


def gInitPop(popN, posMax,
             posI):  # creates a random population with popN individuals. Each individual contains random posI numbers out of posMax
    tmpPop = []

    for i in range(popN):
        # @@instead of random I must run the LPC for the individual
        tmpPop.append([random.random(), gRandIndiv(posMax,
                                                   posI)])  # the first element of the tmpPop list is the efficiency of each Individual
    return tmpPop


def gGiveBirth(m, f):  # it creates children from parents (father & mother)
    tmpPosI = len(m)
    tmpM = [] + m
    tmpF = [] + f
    tmpC = []

    for i in range(tmpPosI):  # 50% of Parents are fathers and the other 50% are mothers
        if ((len(tmpF) != 0) and (i % 2 == 0)) or (len(tmpM) == 0):  # take a number from father
            tmpPos = tmpF.pop(random.randint(0, len(tmpF) - 1))
            while tmpPos in tmpC:  # put the random father position only if this position does not already exist in child
                # print "F "+str(i)+" "+ str(tmpPos)
                tmpPos = tmpF.pop(random.randint(0, len(tmpF) - 1))
        else:  # take a number from mother
            tmpPos = tmpM.pop(random.randint(0, len(tmpM) - 1))
            while (
                tmpPos in tmpC):  # put the random father position only if this position does not already exist in child
                # print "M "+str(i)+" "+ str(tmpPos)
                tmpPos = tmpM.pop(random.randint(0, len(tmpM) - 1))

        tmpC.append(tmpPos)
    tmpC.sort()
    return tmpC

# unit testing
# print gWTListMaster(423900,6147540,429440,6151510,10,10,100)
# m=gRandIndiv(10,5)
# f=gRandIndiv(10,5)
# print m
# print f
# print gGiveBirth(m,f)
