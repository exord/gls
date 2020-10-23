#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 12:22:22 2020

@author: rodrigo
"""
import numpy as np
from matplotlib import pylab as plt
        
def plotGLS(powers, prange, pp0, faplevels=None, fapcolors=None, 
            save=False, savepath=None, **kwargs):
    
    fig1 = plt.figure()
    ax = fig1.add_subplot(111)
    ax.hist(powers, 25, histtype = 'step')
    ax.axvline(powers[0], ls = ':', color = 'k')

    fig2 = plt.figure(figsize=(8, 4))
    ax2 = fig2.add_subplot(111)
    ax2.semilogx(prange, pp0, lw=1)

    if faplevels is not None:
        
        if fapcolors is None:
            fapcolors = np.linspace(0.8, 0.0, len(faplevels)).astype(str)
        
        for i, ff in enumerate(faplevels):
            ax2.axhline(ff, color=str(fapcolors[i]), lw=0.5)
            
    if save and savepath is not None:
        fig1.savefig(savepath, **kwargs)
        
    return fig1, fig2
