import Tkinter as tk
# from Tkinkter.Tkk import Combobox
import ttk
import tkMessageBox
import tkFileDialog
import sys
# import ttkcalendar
import time
import thread
import os
import threading
import PayloadTester as PT
import kbd as kb

from tkcalendar import Calendar, DateEntry

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk



progressBar = None
status = None
keyboard = None


def _check_state(self, event):
    '''finite state machine'''
    if self.state == 'idle':
        if event == 'focusin':
            self._call_popup()
            self.state = 'virtualkeyboard'
    elif self.state == 'virtualkeyboard':
        if event == 'focusin':
            self._destroy_popup()
            self.state = 'typing'
        elif event == 'keypress':
            self._destroy_popup()
            self.state = 'typing'
    elif self.state == 'typing':
        if event == 'focusout':
            self.state = 'idle'


# TODO
def Export():
    return

#TODO
def Calibrate():
    return


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
        if tkMessageBox.askyesno("Confirm", "Are you sure you would like to test Cable:" + SN):
            global progressBar
            global status
            root = tk.Tk()
            #root.overrideredirect(1) make window borderless
            root.title('Progress Bar')
            progressBar = ttk.Progressbar(root, orient="horizontal", length=286, mode="indeterminate")
            progressBar.grid(padx=10, pady=10, columnspan=2)
            t = run_thread('prepare', PT.executeAutomatedTest, SN, CT, D, T + AM_PM)
            t.start()
            # wait till thread dies off
            while t.isAlive():
                root.update()
            print("hello")
            print(t.is_alive())
            print(status)
            root.destroy()
            if(status == "fuck u"):
                tkMessageBox.showinfo("STATUS","PASS")
            else:
                tkMessageBox.showinfo("STATUS","FAIL")



def run_thread(name, func, SN, CT, D, T):
    return threading.Thread(target=run_function, args=(name, func, SN, CT, D, T))


def run_function(name, func, SN, CT, D, T):
    # Disable all buttons
    global status
    global progressBar
    print(name, 'started')
    progressBar.start()
    status = func(SN, CT, D, T)
    progressBar.stop()
    print(name, 'stopped')




def handle_click(event):
    global keyboard
    if keyboard == None or not tk.Toplevel.winfo_exists(keyboard):
            keyboard = kb.create(group1,snobj)


    print(keyboard)

# def on_closing_keyboard():
#     global keyboard
#     keyboard = None




def isTimeFormatted(input):
    try:
        time.strptime(input, '%I:%M')
        return True
    except ValueError:
        return False


def sel():
    selection = "You selected the option " + str(var.get())

    # Function responsible for the updation
    # of the progress bar value


group1 = tk.Tk()

window = tk.LabelFrame(group1, text="Data Entry", padx=5, pady=5)
window.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky=tk.E + tk.W + tk.N + tk.S)



group1.title("Sandia National Labs - Automatic Cable Tester")
tk.Label(window, text="Enter Serial #: ").grid(row=0)

SerialNumber = tk.StringVar()
snobj = tk.Entry(window, width=20, textvariable=SerialNumber)
snobj.grid(row=0, column=1, padx=10, pady=10)

#snobj.bind('<Button-1>', handle_click)
snobj.bind('<Button-1>', handle_click)



tk.Label(window, text="Select Cable Type:").grid(row=1, column=0)
data = (PT.CABLET1, PT.CABLET2, PT.CABLET3, PT.CABLET4)
Type = tk.StringVar()
Types = ttk.Combobox(window, values=data, width=20, textvariable=Type).grid(row=1, column=1, padx=10, pady=10)

tk.Label(window, text="Select Date: ").grid(row=2, column=0, padx=10, pady=10)

cal = DateEntry(window, width=20, background='darkblue',
                foreground='white', borderwidth=2)
cal.grid(row=2, column=1)

tk.Label(window, text="Enter time:").grid(row=3, column=0)

timeEntered = tk.StringVar()
timeEntry = tk.Entry(window, width=20, textvariable=timeEntered)
timeEntry.grid(row=3, column=1)

timeEntry.bind('<Button-1>', handle_click)

var = tk.StringVar()
var.set("am")
R1 = tk.Radiobutton(window, text="am", variable=var, value="am",
                    command=sel).grid(row=3, column=2)

R2 = tk.Radiobutton(window, text="pm", variable=var, value="pm",
                    command=sel).grid(row=3, column=3)

# # calendarBttn = tk.Button(window, text = "Select date", command = example3).grid(columnspan = 2)
#
buttons_frame = tk.Frame(group1)
buttons_frame.grid(row=5, column=0, sticky=tk.W + tk.E)
B1 = tk.Button(buttons_frame, height=2, width=10, text="Start", command=runTest).grid(padx=10, pady=10,
                                                                                      columnspan=1)

# calibrate = tk.LabelFrame(group1, text="Data Entry", padx=5, pady=5)
# calibrate.grid(row=4, column=2, columnspan=3, padx=10, pady=10, sticky=tk.E + tk.W + tk.N + tk.S)

# tk.Button(window, text = "Open Keyboard", command = openKeyboard()).grid(columnspan = 2)




group1.mainloop()
