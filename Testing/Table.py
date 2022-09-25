#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 11:38:35 2022

@author: Krutika
"""
import tkinter as tk
  
class Table(tk.Frame):
    """2D matrix of Entry widgets"""
    def __init__(self, parent, rows=0, columns=0, width=16, data=None):
        super().__init__(parent)
  
        if data is not None:
            rows = len(data)
            columns = len(data[0])
        self.rows = rows
        self.columns = columns
        self.cells = []
        self.values = []
        for row in range(rows): 
            for col in range(columns):
                var = tk.StringVar()
                cell = tk.Entry(self, width=width, textvariable=var)
                cell.grid(row=row, column=col)
                self.cells.append(cell)
                self.values.append(var)
                if data:
                    var.set(data[row][col])
  
    def __setitem__(self, name, value):
        """For setting attributes using instance['attribute'] = value"""
        if name in ('bg'):
            for cell in self.cells:
                cell[name] = value
            super().__setitem__(name, value)
        elif name in ('font', 'fg'):
            for cell in self.cells:
                cell[name] = value
        else:
            super().__setitem__(name, value)
 
    def value(self, row=None, column=None):
        """Get StringVar or group of StringVars"""
        if row is None:
            return [self.value(row, column) for row in range(self.rows)]
        elif column is None:
            return [self.value(row, column) for column in range(self.columns)]
        return self.values[row * self.columns + column]
  
    def cell(self, row=None, column=None):
        """Get an Entry widget or group of Entry widgets"""
        if row is None:
            return [self.cell(row, column) for row in range(self.rows)]
        elif column is None:
            return [self.cell(row, column) for column in range(self.columns)]
        return self.cells[row * self.columns + column]
 
table_values = [
    ('Temp.Strand', 10),
    ('Temp. Kamer', 18),
    ('Temp. Keuken', 20),
    ('Temp. Zee', 20),
    ('Luchtdruk', 1020.520),
    ('Luchtdruk Max', 1020.520),
    ('Datum', '22-01-2020 10:30'),
    ('Luchtdruk Min', 1020.520),
    ('Datum', '22-01-2020 10:30')
]
 
root = tk.Tk()
tk.Label(root, text='This is a table').grid(row=0, column=0)
  
table = Table(root, data=table_values)
table['font'] = ('Arial', 16, 'bold')
table['bg'] = 'black'
table['fg'] = 'white'
for cell in table.cell(column=0):
    cell['fg'] = 'green'
 
for cell in table.cell(column=1):
     cell['justify'] = tk.RIGHT
  
for cell, value in zip(table.cell(column=1), table_values):
    cell['fg'] = 'red' if isinstance(value[1], str) else 'white'
 
table.grid(row=1, column=0, padx=10, pady=10)
  
root.mainloop()
