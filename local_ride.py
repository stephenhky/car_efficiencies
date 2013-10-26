# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 15:04:43 2013

@author: hok1
"""

from car_ride import CarRide, testride
import numpy as np
import scipy as sp

sigma_amin = 0.01

def markov_acceleration_dist(a_new, a_old, dt):
    return sp.stat.norm.pdf(a_new, 
                            loc=-a_old, 
                            scale=max(abs(a_old)/np.sqrt(2), sigma_amin*dt))
    
def sample_acceleration(a_old, dt):
    return np.random.normal(loc=-a_old, 
                            scale=max(abs(a_old)/np.sqrt(2), sigma_amin*dt))

class LocalRide(CarRide):
    def generate_accelerations(self, timearray):
        init_a = 0.0
        a_array = np.zeros(len(timearray))
        a_array[0] = init_a
        for tidx in range(1, len(timearray)):
            a_array[tidx] = sample_acceleration(a_array[tidx-1],
                                                timearray[tidx]-timearray[tidx-1])
        return a_array
        
if __name__ == '__main__':
    ride = LocalRide()
    testride(ride)
