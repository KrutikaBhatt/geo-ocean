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

window=tk.Tk()
window.title("Oceanographic Software Toolkit")
window.geometry('1100x700')
window.resizable(True, True)
window.update_idletasks()

__width__ = tk.IntVar()
__height__ = tk.IntVar()
selectedVariable = IntVar()
__width__.set(window.winfo_width())
__height__.set(window.winfo_height())

# Additional Variables
filepath = ""


def OnResize(event):
    __width__.set(window.winfo_width())
    __height__.set(window.winfo_height())
    FileScreen.config(width=__width__.get()*0.5)
    PlotScreen.config(height=__height__.get()*0.45)

def select_file():
    global filepath
    filepath = filedialog.askopenfilename(initialdir = '/',title = 'Select a dataset',filetypes = (('NC','*.nc'),('All files','*.*')))
    if os.path.exists(filepath):
        filename = filepath.split('/')[len(filepath.split('/'))-1]
        filelabelname = Label(FileScreen, text="  "+filename,image=file_icon,compound=LEFT, font=fileFont,bg="gainsboro")
        filelabelname.pack(ipady=10, ipadx=10, anchor=W)
        description,variables = describeFile(filepath)
        displaylist=[]

        for i in variables:
            for x,y in i.items():
                labelname = "  "+str(x)+str(y)
                thisRadio = Radiobutton(FileScreen,text=labelname,compound=LEFT,font=fileFont,bg="gainsboro",variable = selectedVariable,value=x)
                thisRadio.pack(ipady=1, ipadx=40, anchor=W)

        t = Text(ConsoleScreen,wrap = NONE,xscrollcommand = scrollX.set,yscrollcommand = scrollY.set)

        for x,y in description.items():
            desc_name = "  "+str(x)
            t.insert(END,desc_name+"\n")
            t.insert(END,"      "+str(y)+"\n")
            
        t.pack(side=TOP, fill=X)
    else:
        response=tk.messagebox.showinfo("Error","Please select the dataset again")

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

menu_button7=tkinter.Button(window, text="Plot a graph",image = plot_icon, fg="black",cursor="hand2",bd=1,bg="gainsboro",font=myFont,command=None)
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

PlotsLabel = tk.Label(text="PLOTS",font=myFont,padx=3,pady=3,background="lightblue",fg="black")
panel2.add(PlotsLabel)
# Add to Plot Screen here

PlotScreen = tk.Frame(panel2, bg = "gainsboro",height=__height__.get()*0.45)
statsLabel = tk.Label(text="STATISTICS",font=myFont,padx=3,pady=3,background="lightblue",fg="black")
panel2.add(PlotScreen)
panel2.add(statsLabel)
# Add to statistic screen here


# ConsoleScreen = tk.Canvas(panel2, bg = "gainsboro")
ConsoleScreen = LabelFrame(panel2, bg = "gainsboro",padx=3,pady=3) 
ConsoleScreen.pack()
ConsoleScreen.pack_propagate(False)
scrollX = Scrollbar(ConsoleScreen, orient = 'horizontal')
scrollX.pack(side = BOTTOM, fill = X)
scrollY = Scrollbar(ConsoleScreen)
scrollY.pack(side = RIGHT, fill = Y)

panel2.add(ConsoleScreen)


window.config(menu = menubar)
window.bind("<Configure>",OnResize)
window.mainloop()
