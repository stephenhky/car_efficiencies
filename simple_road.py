# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 12:35:52 2013

@author: hok1
"""

import numpy as np
from scipy.integrate import odeint
import car_engine

engine = car_engine.CarEngine()
L = 100.0
maxv = 60.0
maxa = 100.0
totalT = 10.0

def accelerate(x, v, t):
    if x >= L:
        a = 0
        pedalF = engine.optimal_pedal_force(v, 0)
    elif t>=0 and t<maxv/maxa:
        a = maxa
        pedalF = engine.optimal_pedal_force(v, a)
    elif x<L and x>L-0.5*maxv*maxv/maxa:
        a = -maxa
        pedalF = 0
    else:
        a = 0
        pedalF = engine.optimal_pedal_force(v, 0)
    return a, pedalF

def deriv(xv, t):
    if (xv[0] >= L and xv[1] < 0.0):
        return np.array([0.0, 0.0, 0.0])
    else:
        a, pedalF = accelerate(xv[0], xv[1], t)
        return np.array([max(0, xv[1]), a, pedalF])

def main():
    times = np.linspace(0.0, totalT, 101)
    xvinit = np.array([0.0, 0.0, 0.0])
    xvvals = odeint(deriv, xvinit, times)
    for t, xv in zip(times, xvvals):
        print t, xv[1], xv[0], xv[2]
        pass

if __name__ == '__main__':
    main()
