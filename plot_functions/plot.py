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


cmapnames ={
    'thermal':cmocean.cm.thermal
}

def basePlot(filepath,variable,title,vmin=-10,vmax=10,colorbar='thermal'):
    try:
        if(filepath =="" or filepath==None):
            response=tk.messagebox.showinfo("Error","Please select the dataet first")
            return
        dataset = xr.open_dataset(filepath)
        plot_variable = dataset[variable]
        selected_colorbar = cmapnames[colorbar]
        plot_variable.plot(x='lon', y='lat', figsize=(26,12), vmin=vmin, vmax=vmax,cmap=selected_colorbar)
        plt.title(title)
       
    except Exception as e:
        response=tk.messagebox.showinfo("Error",str(e))
