# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 17:21:08 2013

@author: hok1
"""

import numpy as np
from scipy.integrate import odeint
import car_engine

engine = car_engine.CarEngine()

maxv = 60.0
maxa = 40.0
totalT = 100.0

def accelerate(x, v, t):    
    if v <= maxv:
        a = maxa
        pedalF = engine.optimal_pedal_force(v, a)
    else:
        a = 0.
        pedalF = 0.0
    return a, pedalF

def deriv(xvF, t):
    a, pedalF = accelerate(xvF[0], xvF[1], t)
    return np.array([max(0, xvF[1]), a, pedalF])

def main():
    times = np.linspace(0.0, totalT, 101)
    xvFinit = np.array([0.0, 0.0, 0.0])
    xvFvals = odeint(deriv, xvFinit, times)
    for t, xv in zip(times, xvFvals):
        print t, xv[1], xv[0], xv[2]

if __name__ == '__main__':
    main()
