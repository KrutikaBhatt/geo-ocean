from tkinter import *

root = Tk()
#Same variable but different values
radiobutton_variable = IntVar()
Radiobutton(root, text="Radiobutton only one", variable = radiobutton_variable, value = 1).grid(row = 0, column = 0)
Radiobutton(root, text="Radiobutton only one",  variable = radiobutton_variable, value = 2).grid(row = 0, column = 1)

#Same variable but different values
checkbutton_variable = IntVar()
Checkbutton(root, text="Checkbutton only one",   variable = checkbutton_variable, onvalue = 3).grid(row = 1, column = 0)
Checkbutton(root, text="Checkbutton only one",  variable = checkbutton_variable, onvalue = 4).grid(row = 1, column = 1)

#Same variable, same values or no value
#Select both radio button
both_select_radiobutton_variable = IntVar()
Radiobutton(root, text="radiobutton both", variable = both_select_radiobutton_variable).grid(row = 2, column = 0)
Radiobutton(root, text="radiobutton both",  variable = both_select_radiobutton_variable).grid(row = 2, column = 1)

#Same variable, same values or no value
#Select both check button
both_select_checkbutton_variable = IntVar()
Checkbutton(root, text="Checkbutton both", variable = both_select_checkbutton_variable).grid(row = 3, column = 0)
Checkbutton(root, text="Checkbutton both",  variable = both_select_checkbutton_variable).grid(row = 3, column = 1)

mainloop()