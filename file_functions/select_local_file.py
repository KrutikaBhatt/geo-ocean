import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog,Text
import os.path
import numpy as np
import pickle

class FileSelection():
    def __init__(self,name=None):
        self.name = name
        self.recent_file = 'cache/recent.txt'
        self.workspace = []

    def recent_projects(self):
        try:
            with open(self.recent_file, "rb") as fp:
                b = pickle.load(fp)
            return b,len(b)
        except (OSError,IOError,EOFError) as e:
            return [],0
    
    def save_into_recent(self,filename):
        recent_used_files,size = self.recent_projects()
        if size <= 4:
            recent_used_files.append(filename)
        else:
            recent_used_files.pop()
            recent_used_files.insert(0,filename)
        with open(self.recent_file, "wb") as fp:   #Pickling
            pickle.dump(recent_used_files, fp)
            
    def newfile(self):
        filename = ""
        filename = filedialog.askopenfilename(initialdir = '/',title = 'Select a dataset',filetypes = (('NC','*.nc'),('All files','*.*')))
        if os.path.exists(filename):
            print("The file got selected",filename)
            self.name = filename
            self.save_into_recent(filename)
            self.save_to_workspace(filename)
            return filename
        else:
            response=tk.messagebox.showinfo("Error","Please select the dataset again")
            
    def save_to_workspace(self,filename):
        self.workspace.append(filename)
    
    def return_selected_filename(self):
        return self.name
