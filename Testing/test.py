
from tkinter import *
 
root = Tk()
root.attributes('-fullscreen', True)
root.configure(background='SteelBlue4')
scrW = root.winfo_screenwidth()
scrH = root.winfo_screenheight()
workwindow = str(1024) + "x" + str(768) + "+" + str(int((scrW - 1024) / 2)) + "+" + str(int((scrH - 768) / 2))
top1 = Toplevel(root, bg="light blue")
top1.geometry(workwindow)
top1.title("Top 1 - Workwindow")
top1.attributes("-topmost", 1)  # make sure top1 is on top to start
root.update()  # but don't leave it locked in place
top1.attributes("-topmost", 0)  # in case you use lower or lift
# exit button - note: uses grid
b3 = Button(root, text="Egress", command=root.destroy)
b3.grid(row=0, column=0, ipadx=10, ipady=10, pady=5, padx=5, sticky=W + N)
# ____________________________
 
icontype=StringVar()
initvar = IntVar()
initvar.set(0)
font1="Arial 16 bold"
iconList = ['error', 'gray75', 'gray50', 'gray25', 'gray12', 'hourglass', 'info', 'questhead', 'question', 'warning']
iconDict = {'error': 'system', 'gray75': "shade", 'gray50': "shade", 'gray25': "shade", 'gray12': "shade",
            'hourglass': 'system', 'info': 'notice', 'questhead': 'question', 'question': 'question',
            'warning': 'notice'}
# we have arbitrarilly assigned each internal icon to a category: system, notice, question or shade
# so we can display a category the user chooses
 
def constructdisplaylist(icontype):
    displaylist=[]
    for iconitem in iconDict:
        if iconDict[iconitem]==icontype:
            displaylist.append(iconitem)
    for icon in displaylist:
        counter=1
        iconpic=icon
        icontext="   "+ icon
        thislabelname="L"+str(counter)
        counter+=1
        thislabelname=Label(lbfrm1, bitmap=iconpic, text=icontext, compound=LEFT, font="Arial 18")
        thislabelname.pack(ipady=10, ipadx=10, anchor=W)
    return(displaylist)
 
def destroydisplaylist():
    kidslist=lbfrm1.winfo_children()
    print(len(kidslist))
    for i in range(0,len(kidslist)):
        kidslist[i].destroy()
 
def seticontype():
    print(icontype.get())
 
 
# take up all the toplevel window with pw1 being the big framework
pw1 = PanedWindow(top1, height=768)
# pw1.pack(fill=BOTH, expand=1)  # use a simple pack geometry to install this widget, use it all
 
# fill the left side with a big LabelFrame
lbfrm1 = LabelFrame(pw1, text="left pane", relief=GROOVE, width=399, height=768)  # do NOT pack it yet!
 
# and finally for the big left side
# pack the LabelFrame and THEN you...
lbfrm1.pack()
lbfrm1.pack_propagate(False)
#  ....can insert it into the big Panedwindow and pack the Panedwindow
pw1.add(lbfrm1)  # pw has its own "geometry" for arranging things internally
pw1.pack(fill=BOTH, expand=1)
 
# now create ANOTHER paned window INSIDE the first one using the "add" method
subpw1 = PanedWindow(pw1, orient=VERTICAL)  # NOTE orientation on this one is vertical
pw1.add(subpw1)
# and divide it up between 2 more LabelFrames,
# _____
labelframeTOP = LabelFrame(subpw1, text="upper pane - Choose the Type of Icon to View", relief=GROOVE, height=384)
subpw1.add(labelframeTOP)  # the add command is what activates a widget in the PanedWindow
# _____
lbfrm2=LabelFrame(labelframeTOP, width=30, height=5, relief=FLAT) # use this one to as a spacer
lbfrm2.grid(column=0, row=0,)
frameforrb = Frame(labelframeTOP, width=30, height=10, relief=SUNKEN, bd=12) # and use this one to hold button with a frame
rb1 = Radiobutton(frameforrb, text="Shade", variable=icontype, value="shade", command=seticontype, font=font1)
rb2 = Radiobutton(frameforrb, text="System", variable=icontype, value="system", command=seticontype, font=font1)
rb3 = Radiobutton(frameforrb, text="Notice", variable=icontype, value="notice", command=seticontype, font=font1)
rb4 = Radiobutton(frameforrb, text="Question", variable=icontype, value="question", command=seticontype, font=font1)
rb1.grid(column=1, row=1, stick=W)
rb2.grid(column=1, row=2, stick=W)
rb3.grid(column=1, row=3, stick=W)
rb4.grid(column=1, row=4, stick=W)
frameforrb.grid(column=1,row=1, pady=50)
icontype.set("question")
labelframeTOP.pack_propagate(False)
 
# _____
labelframeBOTTOM = LabelFrame(subpw1, text="lower pane- Display and Remove Your Selection", relief=GROOVE)
subpw1.add(labelframeBOTTOM)
# _____
b1 = Button(labelframeBOTTOM, text='Display Selected Icons', width=30, bg="blanched almond", takefocus=False, command=lambda: constructdisplaylist(icontype.get()))
b1.pack(padx=20, pady=30, ipadx=7, ipady=7)
b2= Button(labelframeBOTTOM, text='Remove Displayed Icons', width=30, bg="linen", takefocus=False, command=destroydisplaylist)
b2.pack(padx=20, pady=10, ipadx=7, ipady=7)
 
labelframeBOTTOM.pack_propagate(False)
 
# ____________________________
root.mainloop()