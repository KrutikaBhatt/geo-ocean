import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog,Text
import os.path
import numpy as np
import pickle
import netCDF4 as nc 
import xarray as xr
import cmocean     
import matplotlib.pyplot as plt

def basePlot(filepath,variable):
    try:
        if(filepath =="" or filepath==None):
            response=tk.messagebox.showinfo("Error","Please select the dataet first")
            return
        dataset = xr.open_dataset(+filepath)
        dataset.variable.plot(x='lon', y='lat', figsize=(26,12), vmin=0, vmax=5, cmap=cmocean.cm.balance)

    except Exception as e:
        response=tk.messagebox.showinfo("Error",e.message)
