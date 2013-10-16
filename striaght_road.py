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
        
    def accelerate(self, x, v):
        if v <= self.maxv:
            a = self.maxa
        else:
            a = 0.
        return a
        
    def derivative(self, xv, t):
        a = self.accelerate(xv[0], xv[1])
        return np.array([max(0, xv[1]), a])

    def runOnRoad(self, xvinit, times):
        xv_vals = odeint(self.derivative, xvinit, times)
        F_vals = map(lambda xv: self.engine.optimal_pedal_force(xv[1], self.accelerate(xv[0], xv[1])),
                     xv_vals)
        return xv_vals, F_vals

    def mpg(self, xv_vals, F_vals):
        num_steps = len(xv_vals)
        xarray = np.array(map(lambda item: item[0], xv_vals))
        Farray = np.array(F_vals)

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

def testCar(car, totalT, numT):
    times = np.linspace(0.0, totalT, numT)
    xvinit = np.array([0.0, 10.0])
    xv_vals, F_vals = car.runOnRoad(xvinit, times)
    instMPG, cumlMPG = car.mpg(xv_vals, F_vals)
    for t, xv, F, instmpg, cumlmpg in zip(times, xv_vals, F_vals, instMPG, cumlMPG):
        print t, xv[1], xv[0], F, instmpg, cumlmpg    

if __name__ == '__main__':
    car = Car_OnRoad()
    testCar(car, totalT, 101)
