# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 17:21:08 2013

@author: hok1
"""

import numpy as np
from scipy.integrate import odeint
import car_engine

totalT = 100.0

class Car_OnRoad:
    def __init__(self):
        self.engine = car_engine.CarEngine()
        self.maxv = 60.0
        self.maxa = 40.0
        
    def accelerate(self, x, v, t):
        if v <= self.maxv:
            a = self.maxa
        else:
            a = 0.
        pedalF = self.engine.optimal_pedal_force(v, a)
        return a, pedalF
        
    def derivative(self, xvF, t):
        a, pedalF = self.accelerate(xvF[0], xvF[1], t)
        return np.array([max(0, xvF[1]), a, pedalF])

    def runOnRoad(self, xvFinit, times):
        return odeint(self.derivative, xvFinit, times)

    def mpg(self, xvFvals):
        num_steps = len(xvFvals)
        xarray = np.array(map(lambda item: item[0], xvFvals))
        Farray = np.array(map(lambda item: item[2], xvFvals))

        if num_steps <= 1:
            return np.array([float('NaN')]), np.array([float('NaN')])
        if num_steps > 1:
            dxarray = []
            dxarray.append((xarray[1]-xarray[0])*0.5)
            for tstep in range(1, num_steps-1):
                dxarray.append((xarray[tstep+1]-xarray[tstep-1])*0.5)
            dxarray.append((xarray[-1]-xarray[-2])*0.5)
            dxarray = np.array(dxarray)
            
            instwork = Farray*dxarray
            
            instMPG = instwork / dxarray
            cumlMPG = []
            for tstep in range(num_steps):
                cumlMPG.append(sum(instwork[:(tstep+1)])/sum(dxarray[:(tstep+1)]))
            cumlMPG = np.array(cumlMPG)
            
            return instMPG, cumlMPG

def main():
    car = Car_OnRoad()
    times = np.linspace(0.0, totalT, 11)
    xvFinit = np.array([0.0, 0.0, 0.0])
    xvFvals = car.runOnRoad(xvFinit, times)
    instMPG, cumlMPG = car.mpg(xvFvals)
    for t, xv, instmpg, cumlmpg in zip(times, xvFvals, instMPG, cumlMPG):
        print t, xv[1], xv[0], xv[2], instmpg, cumlmpg

if __name__ == '__main__':
    main()
