#!/usr/bin/env python3

from tkinter import *
import tkinter as tk
import tkinter.messagebox
import tkinter.font as font
import cv2
from tkinter import filedialog,Text
from PIL import ImageTk, Image, ImageDraw
import os.path
import numpy as np
from time import strftime
from tkinter import ttk
from style_functions.HoverInfo import HoverInfo
from style_functions.ToolTip import CreateToolTip
from file_functions.select_local_file import FileSelection,describeFile
from plot_functions.plot import basePlot,DrawArray
from file_functions.manipulation import concatinate
import threading 
from advanced_functions.anamolies import CalculateAnamolies

window=tk.Tk()
window.title("Oceanographic Software Toolkit")
window.geometry('1100x700')
window.resizable(True, True)
window.update_idletasks()

__width__ = tk.IntVar()
__height__ = tk.IntVar()
__width__.set(window.winfo_width())
__height__.set(window.winfo_height())


colormaps = ["thermal","haline","solar","ice","gray","oxy","deep","dense","algae","matter","turbid","speed","amp","tempo","rain","phase","topo","balance","delta","curl","diff","tarn"]
colormap_images = {
        "thermal":PhotoImage(file = r"colormaps/1.PNG"),"haline":PhotoImage(file = r"colormaps/2.PNG"),"solar":PhotoImage(file = r"colormaps/3.PNG"),"ice":PhotoImage(file = r"colormaps/4.PNG"),"gray":PhotoImage(file = r"colormaps/5.PNG"),"oxy":PhotoImage(file = r"colormaps/6.PNG"),"deep":PhotoImage(file = r"colormaps/7.PNG"),"dense":PhotoImage(file = r"colormaps/8.PNG"),"algae":PhotoImage(file = r"colormaps/9.PNG"),"matter":PhotoImage(file = r"colormaps/10.PNG"),"turbid":PhotoImage(file = r"colormaps/11.PNG"),"speed":PhotoImage(file = r"colormaps/12.PNG"),"amp":PhotoImage(file = r"colormaps/13.PNG"),"tempo":PhotoImage(file = r"colormaps/14.PNG"),"rain":PhotoImage(file = r"colormaps/15.PNG"),"phase":PhotoImage(file = r"colormaps/16.PNG"),"topo":PhotoImage(file = r"colormaps/17.PNG"),"balance":PhotoImage(file = r"colormaps/18.PNG"),"delta":PhotoImage(file = r"colormaps/19.PNG"),
        "curl":PhotoImage(file = r"colormaps/20.PNG"),"diff":PhotoImage(file = r"colormaps/21.PNG"),"tarn":PhotoImage(file = r"colormaps/22.PNG")}


# Additional Variables
filepath = ""
selectedVariable = StringVar()
t = Text()
clicked = tk.StringVar()
LatStart = tk.StringVar()
LatEnd = tk.StringVar()
LongStart = tk.StringVar()
LongEnd = tk.StringVar()
title = tk.StringVar()
VMIN = tk.StringVar()
VMAX = tk.StringVar()
groupby = tk.StringVar()
dim = tk.StringVar()

clicked.set(colormaps[0])
LatStart.set("None")
LatEnd.set("None")
LongStart.set("None")
LongEnd.set("None")
VMIN.set("0")
VMAX.set("5")

# Concatinate variables
folderpath = tk.StringVar()
destinationfilename = tk.StringVar()
concat_dim = tk.StringVar()
product_for_anomoly = tk.StringVar()

def OnResize(event):
    window.update_idletasks()
    __width__.set(window.winfo_width())
    __height__.set(window.winfo_height())
    #FileScreen.config(width=__width__.get()*0.5)
    PlotScreen.config(height=__height__.get()*0.45)
    t.config(height=ConsoleScreen.winfo_height())
    statsLabel.config(width=ConsoleScreen.winfo_width())
    PlotsLabel.config(width=PlotScreen.winfo_width())

def select_file():
    global filepath
    global t
    window.update_idletasks()
    filepath = filedialog.askopenfilename(initialdir = '/',title = 'Select a dataset',filetypes = (('NC','*.nc'),('All files','*.*')))
    if os.path.exists(filepath):
        filename = filepath.split('/')[len(filepath.split('/'))-1]
        title.set(filename)
        filelabelname = Label(FileScreen, text="  "+filename,image=file_icon,compound=LEFT, font=fileFont,bg="gainsboro")
        filelabelname.pack(ipady=10, ipadx=10, anchor=W)
        description,variables,variable_description = describeFile(filepath)

        for i in variables:
            for x,y in i.items():
                labelname = "  "+str(x)+str(y)
                thisRadio = Radiobutton(FileScreen,text=labelname,compound=LEFT,font=fileFont,bg="gainsboro",variable = selectedVariable,value=str(x))
                thisRadio.pack(ipady=1, ipadx=40, anchor=W)

        t = Text(ConsoleScreen,wrap = NONE,xscrollcommand = scrollX.set,yscrollcommand = scrollY.set,height= ConsoleScreen.winfo_height(),pady=10)

        for x,y in description.items():
            desc_name = "  "+str(x)
            t.insert(END,desc_name+"\n")
            t.insert(END,"      "+str(y)+"\n")
        
        t.insert(END,"\n  --- Variable Description ---\n")
        for descItems in variable_description:
            for x,y in descItems.items():
                t.insert(END,str(x)+"\n")
                t.insert(END,"      "+str(y)+"\n")
        t.pack(side=TOP, fill=X)
    else:
        response=tk.messagebox.showinfo("Error","Please select the dataset again")

def displayColorMap(event):
    colormap = clicked.get()
    print(colormap)
    imageLabel.config(image = colormap_images[colormap])
    

def plotModal():
    clicked.set(colormaps[0])
    LatStart.set("None")
    LatEnd.set("None")
    LongStart.set("None")
    LongEnd.set("None")
    VMIN.set("0")
    VMAX.set("5")
    global imageLabel
    global pop
    pop = tk.Toplevel(window,bg="white")
    pop.title("Attributes for plots")
    pop.geometry("650x500")
    label = tk.Label(pop,text="Title",bg="white",anchor="w").grid(row=0,column=0,pady=10)
    titleText = tk.Entry(pop,width=40,textvariable=title).grid(row=0,column=1,pady=15)
    
    
    selectedlabel = tk.Label(pop,text="Selected ",bg="white").place(x=20,y=130)
    imageLabel = tkinter.Label(pop, text="Select File",image = colormap_images['thermal'],bg="white")
    imageLabel.place(x=90,y=120)
    
    colorlabel = tk.Label(pop,text="Color-Map",bg="white").grid(row=1,column=0,padx=20)
    drop = tk.OptionMenu(pop,clicked,*colormaps,command=displayColorMap)
    drop.config(width=30)
    drop.grid(row=1,column=1)
    
    tk.Label(pop,text="Start-Lat",bg="white").place(x=20,y=190)
    tk.Entry(pop,textvariable=LatStart).place(x=90,y=190)
    
    tk.Label(pop,text="End-Lat",bg="white").place(x=250,y=190)
    tk.Entry(pop,textvariable=LatEnd).place(x=310,y=190)
    
    tk.Label(pop,text="Start-Long",bg="white").place(x=20,y=250)
    tk.Entry(pop,textvariable=LongStart).place(x=90,y=250)
    
    tk.Label(pop,text="End-Long",bg="white").place(x=250,y=250)
    tk.Entry(pop,textvariable=LongEnd).place(x=310,y=250)
    
    # Vmin Vmax
    tk.Label(pop,text="Vmin",bg="white").place(x=20,y=310)
    tk.Entry(pop,textvariable=VMIN).place(x=70,y=310)
    
    tk.Label(pop,text="Vmax",bg="white").place(x=230,y=310)
    tk.Entry(pop,textvariable=VMAX).place(x=290,y=310)
    
    tk.Button(pop, text="Submit",fg="black",cursor="hand2",bd=1,bg="lightblue",font=myFont,command=plot_base_graph,padx=3,pady=3).place(x=280,y=400)

    
def plot_base_graph():
    variable_to_plot = selectedVariable.get()
    Title = title.get()
    ColorMapSelected = clicked.get()
    lat_start = LatStart.get()
    lat_end = LatEnd.get()
    long_start = LongStart.get()
    long_end = LongEnd.get()
    vmin = VMIN.get()
    vmax = VMAX.get()
    plotThread = threading.Thread(target = basePlot,args=(filepath,variable_to_plot,Title,PlotScreen,vmin,vmax,ColorMapSelected,long_start,long_end,lat_start,lat_end,))
    plotThread.start()
    pop.destroy()


def ViewArray():
    variable_to_plot = selectedVariable.get()
    grid_window = tk.Toplevel(window,bg="white")
    grid_window.title("Preview Array")
    grid_window.geometry("500x500")
    DrawArray(grid_window,filepath,variable_to_plot)

def select_folder_location():
    folderselect = tk.filedialog.askdirectory()
    folderpath.set(folderselect)

def concatinate_helper():
    concatinate(folderpath.get(),destinationfilename.get(),concat_dim.get())

def concatinateFiles():
    folderpath.set("")
    filemerger = tk.Toplevel(window,bg="white")
    filemerger.title("Concatinate files")
    filemerger.geometry("650x300")
    tk.Label(filemerger,text="Destination Filename",bg="white").place(x=30,y=30)
    tk.Entry(filemerger,width=40,textvariable=destinationfilename).place(x=160,y=30)
    
    tk.Label(filemerger,text="Directory",bg="white").place(x=30,y=70)
    tk.Entry(filemerger,width=60,textvariable=folderpath).place(x=100,y=70)
    tk.Button(filemerger, text="Select File",image = pathselect, fg="black",cursor="hand2",bd=1,bg="gainsboro",font=myFont,command=select_folder_location).place(x=450,y=71)
    
    tk.Label(filemerger,text="Along axis",bg="white").place(x=30,y=110)
    tk.Entry(filemerger,width=20,textvariable=concat_dim).place(x=110,y=110)
    
    tk.Button(filemerger, text="Concatinate",fg="black",cursor="hand2",bd=1,bg="lightblue",font=myFont,command=concatinate_helper,padx=3,pady=3).place(x=280,y=200)

def calculateAnalmolies():
    CalculateAnamolies(destinationfilename.get(),folderpath.get(),groupby.get(),dim.get(),product_for_anomoly.get())

def Anamolies_popup():
    anamoliesPop = tk.Toplevel(window,bg="white")
    anamoliesPop.title("Calculate Anamolies")
    anamoliesPop.geometry("650x300")
    destinationfilename.set("")
    folderpath.set("")
    product_for_anomoly.set("")
    
    tk.Label(anamoliesPop,text="Destination Filename",bg="white").place(x=30,y=30)
    tk.Entry(anamoliesPop,width=40,textvariable=destinationfilename).place(x=160,y=30)
    
    tk.Label(anamoliesPop,text="Directory",bg="white").place(x=30,y=70)
    tk.Entry(anamoliesPop,width=60,textvariable=folderpath).place(x=100,y=70)
    tk.Button(anamoliesPop, text="Select File",image = pathselect, fg="black",cursor="hand2",bd=1,bg="gainsboro",font=myFont,command=select_folder_location).place(x=450,y=71)
    
    tk.Label(anamoliesPop,text="Group By",bg="white").place(x=30,y=110)
    tk.Entry(anamoliesPop,width=20,textvariable=groupby).place(x=110,y=110)
    
    tk.Label(anamoliesPop,text="Dimension",bg="white").place(x=30,y=150)
    tk.Entry(anamoliesPop,width=20,textvariable=dim).place(x=110,y=150)
    
    tk.Label(anamoliesPop,text="Product",bg="white").place(x=30,y=190)
    tk.Entry(anamoliesPop,width=20,textvariable=product_for_anomoly).place(x=110,y=190)
    
    tk.Button(anamoliesPop, text="Calculate",fg="black",cursor="hand2",bd=1,bg="lightblue",font=myFont,command=calculateAnalmolies,padx=3,pady=3).place(x=280,y=240)


def get_all_children(Screen):
    _list = Screen.winfo_children()
    for item in _list:
        if item.winfo_children():
            _list.extend(item.winfo_children())
            
    return _list

def clearAll():
    file_widget_list = get_all_children(FileScreen)
    for item in file_widget_list:
        item.pack_forget()
        
    plot_widget_list = get_all_children(PlotScreen)
    for item in plot_widget_list:
        item.pack_forget()
        
    console_widget_list = get_all_children(ConsoleScreen)
    for item in console_widget_list:
        item.pack_forget()


def configure():
    ConfigurePop = tk.Toplevel(window,bg="white")
    ConfigurePop.title("Configure constants")
    ConfigurePop.geometry("400x300")

    tk.Label(ConfigurePop,text="Author Name: ",bg="white").place(x=20,y=20)
    tk.Entry(ConfigurePop,textvariable=LatStart).place(x=110,y=20)

    tk.Label(ConfigurePop,text="Log folder destination: ",bg="white").place(x=20,y=60)
    tk.Entry(ConfigurePop,textvariable=LatStart).place(x=150,y=60)
    tk.Button(ConfigurePop, text="Select",image = pathselect, fg="black",cursor="hand2",bd=1,bg="gainsboro",font=myFont,command=select_folder_location).place(x=270,y=60)
    
    tk.Label(ConfigurePop,text="Download folder destination: ",bg="white").place(x=20,y=100)
    tk.Entry(ConfigurePop,textvariable=LatStart).place(x=190,y=100)
    tk.Button(ConfigurePop, text="Select",image = pathselect, fg="black",cursor="hand2",bd=1,bg="gainsboro",font=myFont,command=select_folder_location).place(x=300,y=100)
    
    # folder_selected = filedialog.askdirectory()

# Loading the images
folder_icon = PhotoImage(file = r"icons/folder.png")
cursor_icon = PhotoImage(file = r"icons/hand_cursor.png")
pointer_icon = PhotoImage(file = r"icons/pointer.png")
zoomIn = PhotoImage(file = r"icons/zoomIn.png")
zoomOut = PhotoImage(file = r"icons/zoomOut.png")
select_screen = PhotoImage(file = r"icons/select.png")
file_icon = PhotoImage(file=r"icons/file.png")
variable_icon = PhotoImage(file=r"icons/grey.png")
plot_icon = PhotoImage(file=r"icons/plot.png")
array_icon = PhotoImage(file=r'icons/grid.png')
clear_icon = PhotoImage(file=r'icons/clear.png')
pathselect = PhotoImage(file=r'icons/pathselect.png')
# Loading Font
myFont = font.Font(family='Helvetica',size=10, weight='bold')
fileFont = font.Font(family='Helvetica',size=10)
    
#  MENUBAR 
menubar=Menu(window)
filemenu=Menu(menubar,tearoff=0)
filemenu.add_command(label="Open File",command=select_file)

subMenu = tk.Menu(filemenu,tearoff=0)
filemenu.add_cascade(label="Recent Projects",menu=subMenu)

filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label ='File', menu = filemenu)

edit = Menu(menubar, tearoff = 0)
menubar.add_cascade(label ='Edit', menu = edit)
edit.add_command(label ='Cut', command = None)
edit.add_command(label ='Copy', command = None)
edit.add_command(label ='Paste', command = None)
edit.add_command(label ='Select All', command = None)
edit.add_separator()
edit.add_command(label ='Find...', command = None)


# Adding the Advanced Menu Bar
advance = Menu(menubar, tearoff = 0)
menubar.add_cascade(label ='Advance', menu = advance)
advance.add_command(label ='Concatinate', command = concatinateFiles)
advance.add_command(label ='Calculate Anamolies', command = Anamolies_popup)
advance.add_command(label = 'Configuration', command=configure)


# Adding Help Menu
help_ = Menu(menubar, tearoff = 0)
menubar.add_cascade(label ='Help', menu = help_)
help_.add_command(label ='Official Docs', command = None)
help_.add_command(label ='Report', command = None)
help_.add_separator()
help_.add_command(label ='About Toolkit', command = None)
  
# Ending the Menubar

# Menubar Buttons
menu_button1=tkinter.Button(window, text="Select File",image = folder_icon, fg="black",cursor="hand2",bd=1,bg="gainsboro",font=myFont,command=None)
menu_button1.pack(side=LEFT, anchor=NW, padx=2, pady=3)
CreateToolTip(menu_button1, text = "Select File")

menu_button7=tkinter.Button(window, text="Plot a graph",image = plot_icon, fg="black",cursor="hand2",bd=1,bg="gainsboro",font=myFont,command=plotModal)
menu_button7.pack(side=LEFT, anchor=NW, padx=2, pady=3)
CreateToolTip(menu_button7, text = "Plot a graph")

menu_button2=tkinter.Button(window, text="Span",image = cursor_icon, fg="black",cursor="hand2",bd=1,bg="gainsboro",font=myFont,command=None)
menu_button2.pack(side=LEFT, anchor=NW, padx=2, pady=3)
CreateToolTip(menu_button2, text = "Spanning tool")

menu_button3=tkinter.Button(window, text="Cursor",image = pointer_icon, fg="black",cursor="hand2",bd=1,bg="gainsboro",font=myFont,command=None)
menu_button3.pack(side=LEFT, anchor=NW, padx=2, pady=3)
CreateToolTip(menu_button3, text = "pointer")

menu_button4=tkinter.Button(window, text="Zoom In",image = zoomIn, fg="black",cursor="hand2",bd=1,bg="gainsboro",font=myFont,command=None)
menu_button4.pack(side=LEFT, anchor=NW, padx=2, pady=3)
CreateToolTip(menu_button4, text = "Zoom In")

menu_button5=tkinter.Button(window, text="Zoom Out",image = zoomOut, fg="black",cursor="hand2",bd=1,bg="gainsboro",font=myFont,command=None)
menu_button5.pack(side=LEFT, anchor=NW, padx=2, pady=3)
CreateToolTip(menu_button5, text = "Zoom Out")

menu_button6=tkinter.Button(window, text="Select",image = select_screen, fg="black",cursor="hand2",bd=1,bg="gainsboro",font=myFont,command=None)
menu_button6.pack(side=LEFT, anchor=NW, padx=2, pady=3)
CreateToolTip(menu_button6, text = "Select an area")

menu_button8=tkinter.Button(window, text="Array",image = array_icon, fg="black",cursor="hand2",bd=1,bg="gainsboro",font=myFont,command=ViewArray)
menu_button8.pack(side=LEFT, anchor=NW, padx=2, pady=3)
CreateToolTip(menu_button8, text = "View the array components")

menu_button9=tkinter.Button(window, text="Clear All",image = clear_icon, fg="black",cursor="hand2",bd=1,bg="gainsboro",font=myFont,command=clearAll)
menu_button9.pack(side=LEFT, anchor=NW, padx=2, pady=3)
CreateToolTip(menu_button9, text = "Clear all")
# Ending Menu buttons

# Seperators and orientation
separator = ttk.Separator(window, orient='horizontal')
separator.place(relx=0, y=38, relwidth=1)
DisplayScreen = tk.Canvas(window, bg = "gainsboro")
DisplayScreen.place(relx = 0, y = 40, relwidth = 1,relheight=1)


# PANELS 
main_panel = tk.PanedWindow(DisplayScreen,bd=2,bg="grey")

FileScreen = LabelFrame(main_panel, text="File View", relief=GROOVE, bg = "gainsboro",width=__width__.get()*0.5,padx=3,pady=3)  # do NOT pack it yet!
FileScreen.pack()
FileScreen.pack_propagate(False)
main_panel.add(FileScreen)
main_panel.pack(fill=tk.BOTH, expand=1)

panel2 = tk.PanedWindow(main_panel,orient=tk.VERTICAL,bd=2,relief="raised",bg="grey")
main_panel.add(panel2)

# Add to Plot Screen here

PlotScreen = LabelFrame(panel2, bg = "gainsboro",height=__height__.get()*0.45)
PlotScreen.pack()
PlotsLabel = tk.Label(panel2,text="PLOTS",font=myFont,padx=3,pady=3,background="lightblue",fg="black",width=PlotScreen.winfo_width(),relief=GROOVE)
PlotsLabel.pack(side=TOP,fill=X)
PlotScreen.pack_propagate(False)
panel2.add(PlotScreen)

window.update_idletasks()
ConsoleScreen = Label(panel2, bg = "gainsboro",padx=3,pady=3) 
ConsoleScreen.pack()
statsLabel = tk.Label(ConsoleScreen, text="STATISTICS",font=myFont,padx=3,pady=3,background="lightblue",fg="black",width=ConsoleScreen.winfo_width(),relief=GROOVE)
statsLabel.pack(side=TOP,fill=X)
scrollX = Scrollbar(ConsoleScreen, orient = 'horizontal')
scrollX.pack(side = BOTTOM, fill = X)
scrollY = Scrollbar(ConsoleScreen)
scrollY.pack(side = RIGHT, fill = Y)

panel2.add(ConsoleScreen)


window.config(menu = menubar)
window.bind("<Configure>",OnResize)
window.mainloop()
