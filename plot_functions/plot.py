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

cmapnames ={
    'thermal':cmocean.cm.thermal,
    'haline':cmocean.cm.haline,
    'solar':cmocean.cm.solar,
    'ice':cmocean.cm.ice,
    'gray':cmocean.cm.gray,
    'oxy':cmocean.cm.oxy,
    'deep':cmocean.cm.deep,
    'dense':cmocean.cm.dense,
    'algae':cmocean.cm.algae,
    'matter':cmocean.cm.matter,
    'turbid':cmocean.cm.turbid,
    'speed':cmocean.cm.speed,
    'amp':cmocean.cm.amp,
    'tempo':cmocean.cm.tempo,
    'rain':cmocean.cm.rain,
    'phase':cmocean.cm.phase,
    "topo": cmocean.cm.topo,
    "balance": cmocean.cm.balance,
    "delta":cmocean.cm.delta,
    "curl":cmocean.cm.curl,
    "diff":cmocean.cm.diff,
    "tarn":cmocean.cm.tarn
}

colormaps = ["thermal","haline","solar","ice","gray","oxy","deep","dense","algae","matter","turbid","speed","amp","tempo","rain","phase","topo","balance","delta","curl","diff","tarn"]

def subset_file(dataset1,filepath):
    filename = "SUBSET_"+filepath.split('/')[len(filepath.split('/'))-1]
    dataset1.to_netcdf(filename)
    response=tk.messagebox.showinfo("Sucess",f'The file {filename} is saved successfully')

def basePlot(filepath,variable,title,PlotFrame,vmin=0,vmax=5,colorbar='thermal',longStart="None",longEnd="None",latStart="None",latEnd="None"):
    try:
        if(filepath =="" or filepath==None):
            response=tk.messagebox.showinfo("Error","Please select the dataet first")
            return
        dataset1 = xr.open_dataset(filepath)
        if (longStart!="None" and longEnd!="None" and latStart!="None" and latEnd!="None"):
            dataset1 = dataset1.sel(lat =slice(float(latStart),float(latEnd)),lon=slice(float(longStart),float(longEnd)))
        plot_variable = dataset1[variable]
        selected_colorbar = cmapnames[colorbar]
        fig = Figure(figsize = (3,3), dpi=100)
        plot1 = fig.add_subplot(111)
        plot_variable.plot(x='lon', y='lat', vmin=int(float(vmin)), vmax=int(float(vmax)),cmap=selected_colorbar,ax=plot1)
        plot1.set_title(title)
        plot1.grid()
        tk.Button(PlotFrame,text="Subset",padx=3,pady=3,fg="black",command=lambda:subset_file(dataset1,filepath)).pack(side=tk.TOP,anchor="ne",pady=(15,0),padx=(0,10))
        PlotFrame.config(bg="white")
        canvas = FigureCanvasTkAgg(fig,master= PlotFrame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP,fill=tkinter.BOTH,expand=1)
        toolbar = NavigationToolbar2Tk(canvas,PlotFrame)
        toolbar.update()
        
        canvas.get_tk_widget().pack(side=tkinter.TOP,fill=tkinter.BOTH,expand=1)
        
       
    except IOError as e:
        print(e)
        response=tk.messagebox.showinfo("Error",str(e))

def write_into_file(filename,lat,lon,Geo2Dvariable):
    print("Writing to file")
    f = open(f'{filename}.txt',"w")
    for i in range(len(lon)):
        for j in range(len(lat)):
            f.write(str(float(Geo2Dvariable[i][j]))+" ")
        f.write('\n')
    print("Done")
    f.close()
    response=tk.messagebox.showinfo("Success","Created the complete view file")

def DrawArray(grid,filepath,variable_to_plot):

    main_frame = tk.Frame(grid)
    main_frame.pack(fill=tk.BOTH,expand=1)
    
    sec = tk.Frame(main_frame)
    sec.pack(fill=tk.X,side=tk.BOTTOM)
    
    my_canvas = tk.Canvas(main_frame)
    my_canvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)
    
    x_scrollbar = ttk.Scrollbar(sec,orient=tk.HORIZONTAL,command=my_canvas.xview)
    x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    y_scrollbar = ttk.Scrollbar(main_frame,orient=tk.VERTICAL,command=my_canvas.yview)
    y_scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
    
    my_canvas.configure(xscrollcommand=x_scrollbar.set)
    my_canvas.configure(yscrollcommand = y_scrollbar.set)
    
    my_canvas.bind("<Configure>",lambda e:my_canvas.config(scrollregion=my_canvas.bbox(tk.ALL)))
    
    second_frame = tk.Frame(my_canvas)
    my_canvas.create_window((0,0),window=second_frame,anchor='nw')
    
    # Extract Longitude and latitude values
    dataset = xr.open_dataset(filepath)
    lat = dataset['lat']
    lon = dataset['lon']
    
    size_lat = min(len(lat),10)
    size_lon = min(len(lon),10)
    
    Geo2Dvariable = dataset[variable_to_plot]
    tk.Label(second_frame,text="Cordinates").grid(row=1,column=1,padx=5,pady=2)

    for i in range(size_lon):
        tk.Label(second_frame,text=round(float(lon[i]),4),borderwidth=1,relief="solid").grid(row=1,column=i+2,padx=5,pady=2)
        
    for i in range(size_lat):
        tk.Label(second_frame,text=round(float(lat[i]),4),borderwidth=1,relief="solid").grid(row=i+2,column=1,padx=5,pady=2)
    
    
    for i in range(size_lon):
        for j in range(size_lat):
            tk.Label(second_frame,text=round(float(Geo2Dvariable[i][j]),4)).grid(row=i+2,column=j+2,padx=5,pady=2)
    
    # Write into a file
    filename = filepath.split('/')[len(filepath.split('/'))-1]
    fileThread = threading.Thread(target = write_into_file, args=(filename,lat,lon,Geo2Dvariable,))
    fileThread.start()

