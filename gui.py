import Tkinter as tk
#from Tkinkter.Tkk import Combobox
import ttk
import tkMessageBox
import tkFileDialog

import os



global kb
kb = ""
buttons = [
'~','`','!','@','#','$','%','^','&','*','(',')','-','_','L',
'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p','\\','7','8','9','BACK',
'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l','[',']','4','5','6'
,'SHIFT',
'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.','?','/','1','2','3','SPACE',
]


def select(value):
    if value == "BACK":
        # allText = entry.get()[:-1]
        # entry.delete(0, tkinter,END)
        # entry.insert(0,allText)

        snobj.delete(len(snobj.get())-1,tk.END)

    elif value == "SPACE":
        snobj.insert(tk.END, ' ')
    elif value == " Tab ":
        snobj.insert(tk.END, '    ')
    else :
        snobj.insert(tk.END,value)



def openKeyboard():
    kb = tk.Tk()

    varRow = 2
    varColumn = 0


    for button in buttons:

        command = lambda x=button: select(x)

        if button == "SPACE" or button == "SHIFT" or button == "BACK":
            tk.Button(kb,text= button,width=6, bg="#3c4987", fg="#ffffff",
                activebackground = "#ffffff", activeforeground="#3c4987", relief='raised', padx=1,
                pady=1, bd=1,command=command).grid(row=varRow,column=varColumn)

        else:
            tk.Button(kb,text= button,width=4, bg="#3c4987", fg="#ffffff",
                activebackground = "#ffffff", activeforeground="#3c4987", relief='raised', padx=1,
                pady=1, bd=1,command=command).grid(row=varRow,column=varColumn)

        varColumn +=1

        if varColumn > 14 and varRow == 2:
            varColumn = 0
            varRow+=1
        if varColumn > 14 and varRow == 3:
            varColumn = 0
            varRow+=1
        if varColumn > 14 and varRow == 4:
            varColumn = 0
            varRow+=1

        #kb.mainloop()

def handle_click(event):
    openKeyboard()


window = tk.Tk()
window.title("GUI")
window.geometry("300x200")
# creating 2 text labels and input labels
tk.Label(window, text = "Cable #").grid(row = 0) # this is placed in 0 0
# 'Entry' is used to display the input-field
SerialNumber = tk.StringVar()
global snobj
snobj = tk.Entry(window,width=10,textvariable=SerialNumber)
snobj.grid(row = 0, column = 1)
snobj.bind("<Button-1>",handle_click)
 # this is placed in 0 1


tk.Label(window, text = "Select Cable Type").grid(row = 1, column = 0)# this is placed in 1 0
data=("T1", "T2", "T3", "T4")
Type = tk.StringVar()
Types = ttk.Combobox(window,values=data,width=5,textvariable=Type).grid(row = 1, column = 1) # this is placed in 1 1
# 'Checkbutton' is used to create the check buttons
#tk.Checkbutton(window, text = "Keep Me Logged In").grid(columnspan = 2)
 # 'columnspan' tells to take the width of 2 columns
# you can also use 'rowspan' in the similar manner
def runTest():
   if tkMessageBox.askyesno("Confirm", "Are you sure you would like to test Cable #"):
       #os.system('python AutomationScript.py')
       SN = SerialNumber.get()
       CT = Type.get()
       errmsg = ""
       if SN == "":
           errmsg+= "Please enter a cable number\n"
       if CT == "":
           errmsg+="Please select a valid cable Type\n"
       if errmsg != "":
           tkMessageBox.showerror("Incomplete fields",errmsg)
        
       os.system('python3 NewMult.py')
           
        

#bind("<Button-1>", lambda e: openKeyboard())
# def callback():
#     name= tkFileDialog.askopenfilename()
#     print(name)


# tk.Button(window, text='File Open',
#        command=callback).grid(columnspan = 2)

B1 = tk.Button(window, text = "Start", command = runTest).grid(columnspan = 2)
#tk.Button(window, text = "Open Keyboard", command = openKeyboard()).grid(columnspan = 2)

window.mainloop()
