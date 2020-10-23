#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 12:19:23 2020

@author: rodrigo
"""
import sys
import numpy as np

# For C++ parsing
from ctypes import cdll, c_double, c_int, POINTER

from plotting import plotGLS
from GLS import cpplib

def prepareGLSc():
    """
    PREPARE C FUNCTION
    """
    lib = cdll.LoadLibrary(cpplib)
    lib.GLS.argtypes = [POINTER(c_double), c_int,
                        POINTER(c_double), POINTER(c_double), POINTER(c_double),
                         c_int, POINTER(c_double)
                        ]
    return lib.GLS
    

def GLSc(t, rv, erv, prange=None, fap=None, plot=True, multfactor = 10.0, 
         **kwargs):
    
    """
    Missing docstring
    
    :param fap list: list of fap levels to plot (in probability).
    """
    # C++ GLS function
    glsfunc = kwargs.pop('glsfunc', None)
    
    # Number of resampling to get period
    # Nboot = kwargs.pop('Nboot', 1000)

    # Check
    assert len(t) == len(rv), "Input arrays do not have same lenght."
    assert len(t) == len(erv), "Input arrays do not have same lenght."
    
    if glsfunc is None:
        # Prepare C++ func
        glsfunc = prepareGLSc()
        
    # Get periods in which to compute the periodogram, if not given.
    if prange is None:
        ## Construct prange from time array as in yorbit
        tsorted = np.sort(t)
        Pmax = 2*(t.max() - t.min())
        Pmin = np.max([0.25, np.median(np.diff(tsorted))])
        dnu = 0.25*np.min(np.diff( tsorted ) )

        NU = np.arange(1/Pmax, 1/Pmin, dnu)
        prange = 1/NU
        #np.arange(Pmin, Pmax + dnu, dnu)

        print('Using default values: Pmin: {pmin}; Pmax: {pmax}; '
              'dnu : {dnu}; {N} frequencies.'.format(pmin = Pmin, pmax = Pmax, 
                                                     dnu = dnu, N = len(prange)))

    y = rv.copy()
    ey = erv.copy()
    
    if fap is None:
        Nsimul = 1

    else:
        Nsimul = int(multfactor/np.min(fap))

    powers = np.zeros(Nsimul)
    
    W = np.sum(1/ey**2)

    if Nsimul > 1 and fap:
        print('Running {} simulations.'.format(Nsimul))
        if sys.version_info.major >=3:
            # print('Progress: ', end="", flush=True)
            pass
        else:
            print('Progress: ')
    for j in range(Nsimul):

        if (j*100/Nsimul) % 1 == 0:
            
            #print('{:02.0f}%'.format(j*100/Nsimul), end="",
            #      flush=True)
            #print('\b'*3, end="", flush=True)
            pass
        
        pp = np.zeros(len(prange))
    
        w = 1/ey**2.0/W

        ## EXECUTE C++ FUNCTION
        glsfunc(prange.ctypes.data_as(POINTER(c_double)), len(prange),
                t.ctypes.data_as(POINTER(c_double)), 
                y.ctypes.data_as(POINTER(c_double)),
                w.ctypes.data_as(POINTER(c_double)),
                len(t),pp.ctypes.data_as(POINTER(c_double))
                )

        if j == 0:
            pp0 = pp

        ## TEMPORAL
        #powers[j] = np.sum(pp[cond])
        powers[j] = np.max(pp)

        ## Shuffle data
        ind = np.arange(len(y))
        np.random.shuffle(ind)
        y = y[ind]
        ey = ey[ind]

    if Nsimul > 1:
        print('COMPLETE!')

    # Compute FAP levels
    if fap:
        faplevels = [np.percentile(powers, q)
                     for q in (1 - np.sort(np.array(fap))[::-1])*100]
    else:
        faplevels = None

    if plot:
        plotGLS(powers, prange, pp0, faplevels, **kwargs)
                
    return pp0, faplevels, powers
