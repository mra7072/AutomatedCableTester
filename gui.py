import tkinter as tk
# from Tkinkter.Tkk import Combobox
#from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox as tkMessageBox
import sys
# import ttkcalendar
import time
#import thread
import os
import threading
import PayloadTester as PT
import kbd as kb
from tkinter import ttk

from tkcalendar import Calendar, DateEntry





progressBar = None
status = None
keyboard = None
root = None


def Export():
    return

#TODO
def calibrateCable():
    CT = Type.get()
    yesNo =  tkMessageBox.askyesno("Confirm", "Are you sure you would like to calibrate cable type:" + CT + "." + "Existing calibration file will be overriden")
    if yesNo:
        t = threading.Thread(target=PT.performCalibration(CT))
        t.start()
        print("hey")
        while t.is_alive():
                pass
        if PT.calibrationState:
            tkMessageBox.showinfo("Information","Calibration successful")
        else:
            tkMessageBox.showerror("Calibration", "Error occured during calibration")
                        
        
                 

def runTest():
    SN = SerialNumber.get()
    CT = Type.get()
    D = cal.get()
    T = timeEntered.get()
    AM_PM = var.get()
    print(SN)
    print(CT)
    print(D)
    print(T)
    errmsg = ""
    if SN == "":
        errmsg += "Please enter a cable number\n"
    if CT == "":
        errmsg += "Please select a valid cable Type\n"
    if D == "":
        errmsg += "Please Select a date\n"
    if not isTimeFormatted(T):
        errmsg += "Please enter a valid time\n"
    if errmsg != "":
        tkMessageBox.showerror("Incomplete fields", errmsg)

    if errmsg == "":
        # run test, grab status
        yesNo =  tkMessageBox.askyesno("Confirm", "Are you sure you would like to test Cable:" + SN)
        if yesNo:
            global progressBar
            global status
            global root
           
                        #status = PT.testTest()
            t = threading.Thread(target=PT.executeAutomatedTest(SN, CT, D, T + AM_PM))
            #t = run_thread('prepare', PT.executeAutomatedTest, SN, CT, D, T + AM_PM)
            t.start()
            while t.is_alive():
                pass
         #
            if PT.CableState:
                tkMessageBox.showinfo("STATUS","PASS")
            else:
                tkMessageBox.showerror("STATUS","FAIL")

            
            #progressBar.stop()
            #root.destroy()
            
                                 
                                 
                                 
                            
            #print(t.status())
            #root.mainloop()
    
           # print(status + "hello")
        

def run_thread(name, func, SN, CT, D, T):
     return threading.Thread(target=run_function, args=(name, func, SN, CT, D, T))


def run_function(name, func, SN, CT, D, T):
    # Disable all buttons
    global status
    global progressBar
    global root
    global B1
    global B2
    progressBar = ttk.Progressbar(group1, orient="horizontal", length=286, mode="indeterminate")  
    print(name, 'started')
    progressBar.start()
    buttons_frame.pack_forget()
    testlabel = tk.Label(window, text="Testing in Progress...")
    testlabel.pack()
    progressBar.pack() 

    status = func(SN, CT, D, T)
    progressBar.stop()
    progressBar.pack_forget()
    buttons_frame.pack()
    testlabel.pack_forget()
#     v = StringVar()
#     Label(master, textvariable=v).pack()
    print(name, 'stopped')
    print("hello")  
    




def handle_click(event):
    global keyboard
    if keyboard == None or not tk.Toplevel.winfo_exists(keyboard):
            keyboard = kb.create(group1,snobj)


    print(keyboard)


def isTimeFormatted(input):
    try:
        time.strptime(input, '%I:%M')
        return True
    except ValueError:
        return False


def sel():
    selection = "You selected the option " + str(var.get())

group1 = tk.Tk()

window = tk.LabelFrame(group1, text="Data Entry", padx=20, pady=20)
#window.grid(row=4, column=0, columnspan=3, padx=20, pady=20, sticky=tk.E + tk.W + tk.N + tk.S)

window.pack(fill="x", expand="yes")

tk.Label(window, text="Select Date: ",font=('Verdana',10)).pack()
cal = DateEntry(window, width=20, background='darkblue',
                foreground='white', borderwidth=2,font=('Verdana',20))
cal.pack()

tk.Label(window, text="Select Cable Type:",font=('Verdana',10)).pack()
data = (PT.CABLET1, PT.CABLET2, PT.CABLET3, PT.CABLET4)
Type = tk.StringVar()
Types = ttk.Combobox(window, values=data, width=20, textvariable=Type,font=('Verdana',20)).pack()


group1.title("Sandia National Labs - Automatic Cable Tester")
yo = tk.Label(window, text="Enter Serial #: ",anchor="w",font=('Verdana',10))
yo.pack()
#yo.pack()


SerialNumber = tk.StringVar()
snobj = tk.Entry(window, width=20, textvariable=SerialNumber,font=('Verdana',20))

snobj.pack()
#snobj.grid(row=0, column=1, padx=10, pady=10)

#snobj.bind('<Button-1>', handle_click)
snobj.bind('<Button-1>', handle_click)




tk.Label(window, text="Enter time:").pack()

timeEntered = tk.StringVar()
timeEntry = tk.Entry(window, width=20, textvariable=timeEntered,font=('Verdana',20))
timeEntry.pack()

timeEntry.bind('<Button-1>', handle_click)

var = tk.StringVar()
var.set("am")
R1 = tk.Radiobutton(window, text="am", variable=var, value="am",
                    command=sel).pack()

R2 = tk.Radiobutton(window, text="pm", variable=var, value="pm",
                    command=sel,anchor="w").pack()


# # calendarBttn = tk.Button(window, text = "Select date", command = example3).grid(columnspan = 2)
#
buttons_frame = tk.Frame(group1)
buttons_frame.pack()
B1 = tk.Button(buttons_frame, height=2, width=10, text="Start", command=runTest)
B1.grid(row=0, column=0)

#calibrate = tk.LabelFrame(group1, text="Data Entry", padx=5, pady=5)

# tk.Button(window, text = "Open Keyboard", command = openKeyboard()).grid(columnspan = 2)
B2 = tk.Button(buttons_frame, height=2, width=10, text="Calibrate", command=calibrateCable)
B2.grid(padx=10, pady=10,row=0, column=1)



group1.mainloop()


