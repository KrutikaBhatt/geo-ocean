#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 15:49:33 2022

@author: KrutikaBhatt
"""

import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
from tkinter import filedialog,Text
import os.path
import numpy as np
import pickle
import netCDF4 as nc 
import xarray as xr
import cmocean     
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
import threading
import datetime

def concatinate(folder,filename,concat_dim):
    files = []
    print(filename,folder,concat_dim)
    datetoday = datetime.datetime.now()
    f = open(f'log{datetoday}.txt',"w")
    f.write(f'Concatinating files from folder -{folder} along dimension {concat_dim}          Date: {datetoday}\n')
    for file in os.listdir(folder):
        f.write("Adding file {folder+file} ....\n")
        files.append(folder+file)
    
    f.write("\n\nConcat Parameters used:\n1. xarray - open_mfdataset\n2. combine param - nested\n3. dimension  - {concat_dim}")
    ds = xr.open_mfdataset(files,combine='nested',concat_dim=concat_dim)
    ds.to_netcdf(filename)
    f.write("Operation successfully completed")
    f.close()