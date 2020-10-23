#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 12:18:50 2020

@author: rodrigo
"""
import os

homedir = os.getenv('HOME')

cpplib = 'cpp/GLSperiodogram.so'

from main import GLSc

__all__ = ['GLSc',]