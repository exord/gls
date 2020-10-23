#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 13:51:29 2020

@author: rodrigo
"""
import GLS
import numpy as np

t = np.linspace(0, 10, 100) + np.random.randn(100)*0.5
per = np.random.rand()*10

rv = np.sin(2*np.pi*t/per)
rv += np.random.randn(100)*0.25

erv = rv*0.0 + 0.25

GLS.GLSc(t, rv, erv, fap=[0.05, 0.1, 0.5], 
         prange=1/np.arange(1/20.0, 100.0, 0.01))

print('Period was {:.3f}'.format(per))