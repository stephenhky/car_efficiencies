# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 18:56:15 2013

@author: hok1
"""

import straight_road as stroad
import numpy as np
from scipy.stats import norm

sigma_amin = 0.01

def markov_acceleration_dist(a_new, a_old):
    return norm.pdf(a_new, 
                    loc=-a_old, 
                    scale=max(abs(a_old)/np.sqrt(2), sigma_amin))
    
def sample_acceleration(a_old):
    return np.random.normal(loc=-a_old, 
                            scale=max(abs(a_old)/np.sqrt(2), sigma_amin))

class Car_OnLocal(stroad.Car_OnRoad):
    def __init__(self, maxv=40, init_a=0):
        stroad.Car_OnRoad.__init__(self)
        self.maxv = maxv
        np.random.seed()
        self.a = init_a
    
    def accelerate(self, x, v):
        if v>= self.maxv:
            self.a = 0
            return self.a
        elif v <= 0:
            a = 0.1
            self.a = a
            return a
        else:
            a = sample_acceleration(self.a)
            self.a = a
            return a
        
if __name__ == '__main__':
    car = Car_OnLocal()
    stroad.testCar(car, stroad.totalT, 101)
