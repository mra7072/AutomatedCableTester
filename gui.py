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





progressBar = None
status = None
keyboard = None
root = None

def Export():
       #t = tkMessageBox.showinfo("Export","Started exporting results")
       exportSuccess = PT.exportResults()
       if exportSuccess == False:
        tkMessageBox.showerror("No device connected, export unsuccessful", errmsg)
       else:
            tkMessageBox.showinfo("STATUS","Results were sucessfully exported")
        
#TODO
def calibrateSpecialCable():
    lut = PT.determine_measure_left_or_right(PT.CABLET2)
    yesSwap =  tkMessageBox.showinfo("Confirm", "Please swap to test other side, click ok when ready")
    group1.update()
    if yesSwap:
        group1.update()
        print("hello")
        PT.performSpecialCalibration(PT.CABLET2,lut)
        if PT.calibrationState:
            tkMessageBox.showinfo("Information","Calibration successful")
        else:
            tkMessageBox.showerror("Calibration", "Error occured during calibration")
        
        
        
        
    
def calibrateCable():
    CT = Type.get()
    yesNo =  tkMessageBox.askyesno("Confirm", "Are you sure you would like to calibrate cable type:" + CT + "." + "Existing calibration file will be overriden")
    group1.update()
    if yesNo:
        if CT == PT.CABLET2:
            lut = PT.determine_measure_left_or_right(PT.CABLET2)
            yesSwap =  tkMessageBox.showinfo("Confirm", "Please swap to test other side, click ok when ready")
            group1.update()
            if yesSwap:
                group1.update()
#                 print("hello")
#                 t = run_thread_calib('prepare', PT.performSpecialCalibration, CT)
#                 t.start()
#                 while t.is_alive():
#                      group1.update()
                PT.performSpecialCalibration(PT.CABLET2,lut)
                if PT.calibrationState:
                    tkMessageBox.showinfo("Information","Calibration successful")
                else:
                    tkMessageBox.showerror("Calibration", "Error occured during calibration")
                        
        else:
#             t = threading.Thread(target=PT.performCalibration(CT))
#             t.start()
            t = run_thread_calib('prepare', PT.performCalibration, CT)
            t.start()
            while t.is_alive():
                 group1.update()
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
            group1.update()
            #status = PT.testTest()
            #t = threading.Thread(target=PT.executeAutomatedTest(SN, CT, D, T + AM_PM))
            t = run_thread('prepare', PT.executeAutomatedTest, SN, CT, D, T + AM_PM)
            t.start()
            while t.is_alive():
                 group1.update()
            #t.join()
            tk.Toplevel()
            if PT.CableState:
                tkMessageBox.showinfo("STATUS","PASS")
            else:
                tkMessageBox.showerror("STATUS","FAIL")


#             while t.is_alive():
#                 root.update()
#          #
                    
            #progressBar.stop()
            #root.destroy()
            
                                 
                                 
                                 
                            
            #print(t.status())
            #root.mainloop()
    
           # print(status + "hello")
        
def donothing ():
    pass

def help_advice():
    tkMessageBox.showinfo("Help","This tool is the Rocket Payload Cable tester")
    
def run_thread(name, func, SN, CT, D, T):
   return threading.Thread(target=run_function, args=(name, func, SN, CT, D, T))

def run_thread_calib(name, func, CT):
   return threading.Thread(target=run_function_calib, args=(name, func, CT))


def run_function_calib(name, func, CT):
    # Disable all buttons
    global status
    global progressBar
    global root
    #s = ttk.Style()
    #s.theme_use('clam')
   # s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
    progressBar = ttk.Progressbar(group1,orient="horizontal", length=800, mode="indeterminate")  
    print(name, 'started')
    progressBar.start()
    buttons_frame.pack_forget()
    testlabel = tk.Label(window, text="Please wait calibration in progress...",font=('Helvetica',30,'bold'))
    testlabel.pack()
    progressBar.pack() 
    status = func(CT)
    progressBar.stop()
    progressBar.pack_forget()
    buttons_frame.pack(expand="yes",fill="both")
    testlabel.pack_forget()
#     v = StringVar()
#     Label(master, textvariable=v).pack()
    print(name, 'stopped')
    print("hello")  
    


from pandastable import Table

def open_file():
   file = filedialog.askopenfilename(initialdir = "/home/pi/Desktop/AutomatedCableTester",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
   
#assuming parent is the frame in which you want to place the table
  
   print(file)
   if len(file) != 0 and ".csv" in file:
         t = tk.Toplevel()
         pt = Table(t)
         pt.importCSV(file)
         pt.redraw()
         pt.show()
           #os.system("libreoffice --calc " + file)
         
def run_function(name, func, SN, CT, D, T):
    # Disable all buttons
    global status
    global progressBar
    global root
    #s = ttk.Style()
    #s.theme_use('clam')
   # s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
    progressBar = ttk.Progressbar(group1,orient="horizontal", length=800, mode="indeterminate")  
    print(name, 'started')
    progressBar.start()
    buttons_frame.pack_forget()
    testlabel = tk.Label(window, text="Please wait testing in progress...",font=('Helvetica',30,'bold'))
    testlabel.pack()
    progressBar.pack() 
    status = func(SN, CT, D, T)
    progressBar.stop()
    progressBar.pack_forget()
    buttons_frame.pack(expand="yes",fill="both")
    testlabel.pack_forget()
#     v = StringVar()
#     Label(master, textvariable=v).pack()
    print(name, 'stopped')
    print("hello")  
    




def handle_click(event):
    print(event)
    global keyboard
    #no keyboard
    if keyboard == None or not tk.Toplevel.winfo_exists(keyboard):
            keyboard = kb.create(group1,event.widget)
    else:
        keyboard.destroy()
        keyboard = kb.create(group1,event.widget)
        
        #keyboard exists just focus
      #  keyboard.focus()


    print(keyboard)


def isTimeFormatted(input):
    try:
        time.strptime(input, '%I:%M')
        return True
    except ValueError:
        return False


def sel():
    selection = "You selected the option " + str(var.get())



def menu_callback():
    print("I'm in the menu callback!")
def submenu_callback():
    print("I'm in the submenu callback!")

group1 = tk.Tk()
group1.attributes('-fullscreen', True)
#group1.attributes('-zoomed', True)

menu_widget = tk.Menu(group1,title="Hello",activebackground="white",activeforeground="blue")
submenu_widget = tk.Menu(menu_widget, tearoff=False)
submenu_widget.add_command(label="Open file",
                           command=open_file)
submenu_widget.add_command(label="Export Results Automatically",
                           command=Export)
submenu_widget.add_command(label="Clear Results Folder",
                           command=submenu_callback)
submenu_widget.add_command(label="Quit",
                           command=sys.exit)
submenu_widget.add_command(label="Help",
                           command=help_advice)
submenu_widget.add_command(label="About",
                           command=help_advice)

menu_widget.add_cascade(label="File", menu=submenu_widget)
#menu_widget.add_command(label="Item2",
    #                    command=menu_callback)
#menu_widget.add_command(label="Item3",
 #                       command=menu_callback)
group1.config(menu=menu_widget)



window = tk.LabelFrame(group1, padx=20, pady=20)
#window.grid(row=4, column=0, columnspan=3, padx=20, pady=20, sticky=tk.E + tk.W + tk.N + tk.S)

window.pack(fill="both",expand="yes")

tk.Label(window, text="Select Date: ",font=('Helvetica',12,'bold')).pack()
cal = DateEntry(window, width=20, background='darkblue',
                foreground='white', borderwidth=2,font=('Helvetica',20))
cal.pack()

cableTypeFrame = tk.Frame(window)

tk.Label(window, text="Select Cable Type:",font=('Helvetica',12,'bold')).pack()

data = (PT.CABLET1, PT.CABLET2, PT.CABLET3, PT.CABLET4)
Type = tk.StringVar()
Types = ttk.Combobox(cableTypeFrame, values=data, width=12, textvariable=Type,font=('Helvetica',20)).pack(padx=12,side=LEFT)
cableTypeFrame.pack()

suffixvar = tk.StringVar()
suffix = tk.Entry(cableTypeFrame, width=12,bd=5,textvariable=suffixvar,font=('Helvetica',20))
suffix.bind('<Button-1>', handle_click)
suffix.pack(side=LEFT)

group1.title("Sandia National Labs - Automatic Cable Tester")
yo = tk.Label(window, text="Enter Serial #: ",anchor="w",font=('Helvetica',12,'bold'))
yo.pack()
#yo.pack()


SerialNumber = tk.StringVar()
snobj = tk.Entry(window, width=20,bd=5, textvariable=SerialNumber,font=('Helvetica',20))

snobj.pack()
#snobj.grid(row=0, column=1, padx=12, pady=12)

#snobj.bind('<Button-1>', handle_click)
snobj.bind('<Button-1>', handle_click)




tk.Label(window, text="Enter time:",font=('Helvetica',12,'bold')).pack()
timeEntered = tk.StringVar()
timeEntry = tk.Entry(window, width=20, bd=5, textvariable=timeEntered,font=('Helvetica',20))
timeEntry.pack()

timeEntry.bind('<Button-1>', handle_click)

var = tk.StringVar()
var.set("am")
R1 = tk.Radiobutton(window, text="am", variable=var, font=('Helvetica',12,'bold'),value="am",
                    command=sel).pack()

R2 = tk.Radiobutton(window, text="pm", variable=var, font=('Helvetica',12,'bold'),value="pm",
                    command=sel,anchor="w").pack()


# # calendarBttn = tk.Button(window, text = "Select date", command = example3).grid(columnspan = 2)
#
buttons_frame = tk.Frame(group1)
buttons_frame.pack(expand="yes", fill="both")
B1 = tk.Button(buttons_frame, bg="green",height=2, width=12, text="START", font=('Helvetica',30,'bold'),command=runTest)
#B1.grid(row=0, column=0)
B1.pack(side=LEFT,expand="yes",fill="both")

#calibrate = tk.LabelFrame(group1, text="Data Entry", padx=5, pady=5)

# tk.Button(window, text = "Open Keyboard", command = openKeyboard()).grid(columnspan = 2)
B2 = tk.Button(buttons_frame, bg="blue", height=2, width=12, text="CALIBRATE",font=('Helvetica',30,'bold'), command=calibrateCable)
#B2.grid(padx=12, pady=12,row=0, column=1)
B2.pack(side=LEFT,expand="yes",fill="both")



group1.mainloop()



