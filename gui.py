import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as tkMessageBox
import os
import sys
import time
import os
import threading
import PayloadTester as PT
import kbd as kb
from tkinter import ttk
import time
from tkcalendar import Calendar, DateEntry
from pandastable import Table

#Global variables
progressBar = None
status = None
keyboard = None

"""
Event Handler for Exporting results. Displays popup depending on status of export
"""
def Export():
    exportSuccess = PT.exportResults()
    if exportSuccess == False:
        tkMessageBox.showerror("Status","No device connected, export unsuccessful")
    else:
        tkMessageBox.showinfo("STATUS", "Results were sucessfully exported")



"""
Event handler for cabibration 
"""
def calibrateCable():
    CT = Type.get()
    yesNo = tkMessageBox.askyesno("Confirm",
                                  "Are you sure you would like to calibrate cable type:" + CT + "." + "Existing calibration file will be overriden")
    group1.update()
    if yesNo:
            lut = PT.determine_measure_left_or_right(PT.CABLET2)
            yesSwap = tkMessageBox.showinfo("Confirm", "Please swap to test other side, click ok when ready")
            group1.update()
            if yesSwap:
                group1.update()
                print("hello")
                t = run_thread_calib('prepare', PT.performSpecialCalibration, CT)
                t.start()
                while t.is_alive():
                    group1.update()
                PT.performSpecialCalibration(PT.CABLET2, lut)
                if PT.calibrationState:
                    tkMessageBox.showinfo("Information", "Calibration successful")
                else:
                    tkMessageBox.showerror("Calibration", "Error occured during calibration")


"""
Event handler for starting automated test
"""
def runTest():
    SN = SerialNumber.get()
    CT = Type.get()
    D = cal.get()
    T = timeEntered.get()
    AM_PM = var.get()
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
        yesNo = tkMessageBox.askyesno("Confirm", "Are you sure you would like to test Cable:" + SN)
        if yesNo:
            global progressBar
            global status
            global root
            group1.update()
            t = run_thread('prepare', PT.executeAutomatedTest, SN, CT, D, T + AM_PM)
            t.start()
            while t.is_alive():
                group1.update()
            tk.Toplevel()
            if PT.CableState:
                tkMessageBox.showinfo("STATUS", "PASS")
            else:
                tkMessageBox.showerror("STATUS", "FAIL")


def help_advice():
    tkMessageBox.showinfo("Help", "This tool is the Rocket Payload Cable tester")


"""
Spawn a thread to execute test
"""
def run_thread(name, func, SN, CT, D, T):
    return threading.Thread(target=run_function, args=(name, func, SN, CT, D, T))


"""
Spawn a thread execute calibration
"""
def run_thread_calib(name, func, CT):
    return threading.Thread(target=run_function_calib, args=(name, func, CT))


"""
Executes automated test with indefinite progress bar 
"""
def run_function(name, func, SN, CT, D, T):
    # Disable all buttons
    global status
    global progressBar
    progressBar = ttk.Progressbar(group1, orient="horizontal", length=800, mode="indeterminate")
    print(name, 'started')
    progressBar.start()
    buttons_frame.pack_forget()
    testlabel = tk.Label(window, text="Please wait testing in progress...", font=('Helvetica', 30, 'bold'))
    testlabel.pack()
    progressBar.pack()
    status = func(SN, CT, D, T)
    progressBar.stop()
    progressBar.pack_forget()
    buttons_frame.pack(expand="yes", fill="both")
    testlabel.pack_forget()


"""
Executes calibration with indefinite progress bar 
"""
def run_function_calib(name, func, CT):
    global status
    global progressBar
    progressBar = ttk.Progressbar(group1, orient="horizontal", length=800, mode="indeterminate")
    print(name, 'started')
    progressBar.start()
    buttons_frame.pack_forget()
    testlabel = tk.Label(window, text="Please wait calibration in progress...", font=('Helvetica', 30, 'bold'))
    testlabel.pack()
    progressBar.pack()
    status = func(CT)
    progressBar.stop()
    progressBar.pack_forget()
    buttons_frame.pack(expand="yes", fill="both")
    testlabel.pack_forget()


"""
Opens File dialog to select a CSV file for viewing
"""
def open_file():
    file = filedialog.askopenfilename(initialdir="/home/pi/Desktop/AutomatedCableTester", title="Select file",
                                      filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    if len(file) != 0 and ".csv" in file:
        t = tk.Toplevel()
        pt = Table(t)
        pt.importCSV(file)
        pt.redraw()
        pt.show()
        # os.system("libreoffice --calc " + file)


"""
Handling click events on entrys to popup the keyboard and destroy off click
"""
def handle_click(event):
    print(event)
    global keyboard
    if keyboard == None or not tk.Toplevel.winfo_exists(keyboard):
        keyboard = kb.create(group1, event.widget)
    else:
        keyboard.destroy()
        keyboard = kb.create(group1, event.widget)

    print(keyboard)


"""
Time validator according to format (H:MM)
"""
def isTimeFormatted(input):
    try:
        time.strptime(input, '%I:%M')
        return True
    except ValueError:
        return False


"""
Main function to create GUI and setup eventhandlers 
"""
if __name__ == '__main__':
    # Group1 is the root window
    group1 = tk.Tk()
    # group1.attributes('-fullscreen', True)
    # group1.attributes('-zoomed', True)

    # Menu widget with respective submenus
    menu_widget = tk.Menu(group1, title="Hello", activebackground="white", activeforeground="blue")
    submenu_widget = tk.Menu(menu_widget, tearoff=False)
    submenu_widget.add_command(label="Open file",
                               command=open_file)
    submenu_widget.add_command(label="Export Results Automatically",
                               command=Export)
    submenu_widget.add_command(label="Quit",
                               command=sys.exit)
    submenu_widget.add_command(label="Help",
                               command=help_advice)
    submenu_widget.add_command(label="About",
                               command=help_advice)

    menu_widget.add_cascade(label="File", menu=submenu_widget)

    group1.config(menu=menu_widget)

    window = tk.LabelFrame(group1, padx=20, pady=20)
    window.pack(fill="both", expand="yes")

    # Date widget
    tk.Label(window, text="Select Date: ", font=('Helvetica', 12, 'bold')).pack()
    cal = DateEntry(window, width=20, background='darkblue',
                    foreground='white', borderwidth=2, font=('Helvetica', 20))
    cal.pack()
    cableTypeFrame = tk.Frame(window)

    # Cable selection dropdown
    tk.Label(window, text="Select Cable Type:", font=('Helvetica', 12, 'bold')).pack()
    data = (PT.CABLET1, PT.CABLET2, PT.CABLET3, PT.CABLET4)
    Type = tk.StringVar()
    Types = ttk.Combobox(cableTypeFrame, values=data, width=12, textvariable=Type, font=('Helvetica', 20)).pack(padx=12,
                                                                                                                side=LEFT)
    cableTypeFrame.pack()
    # Appended suffix to cable type
    suffixvar = tk.StringVar()
    suffix = tk.Entry(cableTypeFrame, width=12, bd=5, textvariable=suffixvar, font=('Helvetica', 20))
    suffix.bind('<Button-1>', handle_click)
    suffix.pack(side=LEFT)

    group1.title("Sandia National Labs - Automatic Cable Tester")
    yo = tk.Label(window, text="Enter Serial #: ", anchor="w", font=('Helvetica', 12, 'bold'))
    yo.pack()

    SerialNumber = tk.StringVar()
    # Serial number entry
    snobj = tk.Entry(window, width=20, bd=5, textvariable=SerialNumber, font=('Helvetica', 20))

    snobj.pack()

    snobj.bind('<Button-1>', handle_click)

    # Time entry
    tk.Label(window, text="Enter time:", font=('Helvetica', 12, 'bold')).pack()
    timeEntered = tk.StringVar()
    timeEntry = tk.Entry(window, width=20, bd=5, textvariable=timeEntered, font=('Helvetica', 20))
    timeEntry.pack()

    timeEntry.bind('<Button-1>', handle_click)

    var = tk.StringVar()
    var.set("am")
    # Buttons for toggling am/pm
    R1 = tk.Radiobutton(window, text="am", variable=var, font=('Helvetica', 12, 'bold'), value="am",
                        ).pack()

    R2 = tk.Radiobutton(window, text="pm", variable=var, font=('Helvetica', 12, 'bold'), value="pm",
                        anchor="w").pack()

    # Button for Start
    buttons_frame = tk.Frame(group1)
    buttons_frame.pack(expand="yes", fill="both")
    B1 = tk.Button(buttons_frame, bg="#006400", height=2, width=12, text="START", font=('Helvetica', 30, 'bold'),
                   command=runTest)
    B1.pack(side=LEFT, expand="yes", fill="both")

    # Button for Calibrate
    B2 = tk.Button(buttons_frame, bg="#00008b", height=2, width=12, text="CALIBRATE", font=('Helvetica', 30, 'bold'),
                   command=calibrateCable)
    B2.pack(side=LEFT, expand="yes", fill="both")
    group1.mainloop()
