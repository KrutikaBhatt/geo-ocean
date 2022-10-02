#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 16:14:27 2022

@author: KrutikaBhatt
"""
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

def CalculateAnamolies(destinationFile, folderpath, groupby, dimension,product):
    # Combine the files with coordinates
    ds_combined =  xr.open_mfdataset(f'{folderpath}/*nc', combine='by_coords')
    ds_combined.to_netcdf(f'{folderpath}/{destinationFile}_combined.nc')
    
    product_data = ds_combined[product]
    climatology_file = product_data.groupby(groupby).mean(dim=dimension)
    climatology_file.to_netcdf(f'{folderpath}/{destinationFile}.nc')
    climatology_file[0].plot()
    plt.title('1st CLimatology file Plot')
    plt.show()
        
    