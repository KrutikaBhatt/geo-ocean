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
from functions.HoverInfo import HoverInfo
from functions.ToolTip import CreateToolTip
from tkinter import ttk

window=tk.Tk()
window.title("Oceanographic Software Toolkit")
window.geometry('1100x700')
window.resizable(True, True)

# Loading the images
folder_icon = PhotoImage(file = r"icons\folder.png")
cursor_icon = PhotoImage(file = r"icons\hand_cursor.png")
pointer_icon = PhotoImage(file = r"icons\pointer.png")
zoomIn = PhotoImage(file = r"icons\zoomIn.png")
zoomOut = PhotoImage(file = r"icons\zoomOut.png")
select_screen = PhotoImage(file = r"icons\select.png")

# Loading Font
myFont = font.Font(family='Helvetica',size=13, weight='bold')

def open_file():
    pass
    
def recent_projects():
    pass


#  MENUBAR 

menubar=Menu(window)
filemenu=Menu(menubar,tearoff=0)
filemenu.add_command(label="Open File",command=open_file)
filemenu.add_command(label="Recent projects",command=recent_projects)
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
separator = ttk.Separator(window, orient='vertical')
separator.place(relx=0.47, rely=0, relwidth=0.2, relheight=1)

window.config(menu = menubar)
window.mainloop()