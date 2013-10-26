# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 17:13:31 2013

@author: hok1
"""

import numpy as np
from scipy.integrate import odeint
from functools import partial
from car_engine import CarEngine

class CarRide:
    def __init__(self):
        self.maxv = 60
        self.maxa = 60
        self.engine = CarEngine()
        
    def generate_accelerations(self, timearray):
        return [0.0]*len(timearray)
        
    def derivative(self, xv_list, t, time_array, acc_array):
        #x = xv_list[0]
        v = xv_list[1]
        a = np.interp(t, time_array, acc_array)
        return np.array([v, a])
        
    def solve_motion(self, timearray, init_x, init_v):
        a_vals = self.generate_accelerations(timearray)        
        deriv = partial(self.derivative, time_array=timearray, 
                        acc_array=a_vals)
        xv_vals = odeint(deriv, np.array([init_x, init_v]), timearray)
        F_vals = map(self.engine.optimal_pedal_force, xv_vals[:,1], a_vals)
        return xv_vals[:,0], xv_vals[:,1], a_vals, F_vals
        
    def mpg(self, xarray, F_vals):
        num_steps = len(xarray)
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
        
def testride(ride, totalT=10, steps=101, initv=10.):
    time_array = np.linspace(0, totalT, steps)
    x_array, v_array, a_array, F_array = ride.solve_motion(time_array, 0., initv)
    inst_mpg_array, cuml_mpg_array = ride.mpg(x_array, F_array)
    for t, x, v, a, inst_mpg, cuml_mpg in zip(time_array, x_array, v_array, 
                                              a_array, inst_mpg_array,
                                              cuml_mpg_array):
        print t, x, v, a, inst_mpg, cuml_mpg
        
if __name__ == '__main__':
    ride = CarRide()
    testride(ride)
