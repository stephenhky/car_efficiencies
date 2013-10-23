# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 12:04:24 2013

@author: hok1
"""

import math

g = 1.

class CarEngine:
    def __init__(self, m=1.0, b=1.0, c=0.5, max_force=100.0):
        self.m = m
        self.b = b
        self.c = c
        self.max_force = max_force
        
    def airfriction(self, v):
        return self.b*v
    
    def accelerate(self, pedal_force, v, alpha=0):
        return min(max(0.0,
                       (pedal_force-self.airfriction(v)-self.c)/self.m)-g*math.sin(alpha),
                       self.max_force)
        
    def min_pedal_force(self, v, alpha=0):
        return (self.airfriction(v)+self.c+g*math.sin(alpha))
        
    def optimal_pedal_force(self, v, a, alpha=0):
        return (self.m*a+self.airfriction(v)+self.c+g*math.sin(alpha))
