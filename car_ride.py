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
        deriv = partial(self.derivative,
                        time_array=timearray,
                        acc_array=self.generate_accelerations(timearray))
        xv_vals = odeint(deriv, np.array([init_x, init_v], timearray))
        return xv_vals[:,0], xv_vals[:,1]
