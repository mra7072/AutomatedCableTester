import Tkinter as tk
# from Tkinkter.Tkk import Combobox
import ttk
import tkMessageBox
import tkFileDialog
import sys
# import ttkcalendar
import time
import os
import NewMult



from tkcalendar import Calendar, DateEntry

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk

kb = None

buttons = [
    '~', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', 'L',
    'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '\\', '7', '8', '9', 'BACK',
    'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '[', ']', '4', '5', '6'
    , 'SHIFT',
    'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '?', '/', '1', '2', '3', 'SPACE',
]


def select(value):
    if value == "BACK":

        snobj.delete(len(snobj.get()) - 1, tk.END)

    elif value == "SPACE":
        snobj.insert(tk.END, ' ')
    elif value == " Tab ":
        snobj.insert(tk.END, '    ')
    else:
        snobj.insert(tk.END, value)


def openKeyboard():
    global kb
    if kb is not None and kb.state() == "normal":
        kb.focus()
    else:
        kb = tk.Tk()

    varRow = 2
    varColumn = 0
    for button in buttons:
        command = lambda x=button: select(x)
        if button == "SPACE" or button == "SHIFT" or button == "BACK":
            tk.Button(kb, text=button, width=6, bg="#3c4987", fg="#ffffff",
                      activebackground="#ffffff", activeforeground="#3c4987", relief='raised', padx=1,
                      pady=1, bd=1, command=command).grid(row=varRow, column=varColumn)

        else:
            tk.Button(kb, text=button, width=4, bg="#3c4987", fg="#ffffff",
                      activebackground="#ffffff", activeforeground="#3c4987", relief='raised', padx=1,
                      pady=1, bd=1, command=command).grid(row=varRow, column=varColumn)

        varColumn += 1

        if varColumn > 14 and varRow == 2:
            varColumn = 0
            varRow += 1
        if varColumn > 14 and varRow == 3:
            varColumn = 0
            varRow += 1
        if varColumn > 14 and varRow == 4:
            varColumn = 0
            varRow += 1


# TODO
def Export():
    return


def Calibrate():
    return

def runTest():
    status = False
    if tkMessageBox.askyesno("Confirm", "Are you sure you would like to test Cable #"):
        SN = SerialNumber.get()
        CT = Type.get()
        D = cal.get()
        T = timeEntered.get()
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
        if status:
            tkMessageBox.showinfo("Status", "TEST PASSED!")
        else:
            tkMessageBox.showerror("Status", "TEST FAILED!")


def handle_click(event):
    # if kb != None:
    print(kb)
    openKeyboard()


def isTimeFormatted(input):
    try:
        time.strptime(input, '%I:%M')
        return True
    except ValueError:
        return False


# def openCalendar():
#     root = tk.Tk()
#     root.title('Ttk Calendar')
#     ttkcal = ttkcalendar.Calendar(firstweekday=ttkcalendar.calendar.SUNDAY)
#     ttkcal.pack(expand=1, fill='both')
#
#     if 'win' not in sys.platform:
#         style = ttk.Style()
#         style.theme_use('clam')
#
#
#     x = ttkcal.selection
#     print 'x is: ', x

#
# def openCalendar():
# 		top = tk.Toplevel(window)
# 		cal = Calendar(top, selectmode='none')
# 		date = cal.datetime.today() + cal.timedelta(days=2)
# 		cal.calevent_create(date, 'Hello World', 'message')
# 		cal.calevent_create(date, 'Reminder 2', 'reminder')
# 		cal.calevent_create(date + cal.timedelta(days=-2), 'Reminder 1', 'reminder')
# 		cal.calevent_create(date + cal.timedelta(days=3), 'Message', 'message')
#
# 		cal.tag_config('reminder', background='red', foreground='yellow')
#
# 		cal.pack(fill="both", expand=True)
# 		ttk.Label(top, text="Hover over the events.").pack()
#
# def example1():
#     def print_sel():
#         print(cal.selection_get())
#         cal.see(datetime.date(year=2016, month=2, day=5))
#
#     top = tk.Toplevel(window)
#
#     import datetime
#     today = datetime.date.today()
#
#     mindate = datetime.date(year=2018, month=1, day=21)
#     maxdate = today + datetime.timedelta(days=5)
#     print(mindate, maxdate)
#
#     cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
#                    mindate=mindate, maxdate=maxdate, disabledforeground='red',
#                    cursor="hand1", year=2018, month=2, day=5)
#     cal.pack(fill="both", expand=True)
#     ttk.Button(top, text="ok", command=print_sel).pack()

# def example3():
# 	top = tk.Toplevel(window)
# 	ttk.Label(top, text='Choose date').pack(padx=10, pady=10)
#
# 	cal = DateEntry(top, width=12, background='darkblue',
# 	                foreground='white', borderwidth=2, year=2010)
# 	cal.pack(padx=10, pady=10)
#
#
#
def sel():
    selection = "You selected the option " + str(var.get())


group1 = tk.Tk()

window = tk.LabelFrame(group1, text="Data Entry", padx=5, pady=5)
window.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky=tk.E + tk.W + tk.N + tk.S)

group1.title("Sandia National Labs - Automatic Cable Tester")
tk.Label(window, text="Enter Serial #: ").grid(row=0)

# path = "Aaron.jpg"
# img = ImageTk.PhotoImage(Image.open(path))
#
# #The Label widget is a standard Tkinter widget used to display a text or image on the screen.
# panel = tk.Label(window, image = img)
#
# #The Pack geometry manager packs widgets in rows or columns.
# panel.pack(side = "bottom", fill = "both", expand = "yes")

# Start the GUI


SerialNumber = tk.StringVar()
snobj = tk.Entry(window, width=10, textvariable=SerialNumber)
snobj.grid(row=0, column=1, padx=10, pady=10)

snobj.bind('<Button-1>', handle_click)

tk.Label(window, text="Select Cable Type:").grid(row=1, column=0)
data = ("T1", "T2", "T3", "T4")
Type = tk.StringVar()
Types = ttk.Combobox(window, values=data, width=5, textvariable=Type).grid(row=1, column=1, padx=10, pady=10)

tk.Label(window, text="Select Date: ").grid(row=2, column=0, padx=10, pady=10)

cal = DateEntry(window, width=12, background='darkblue',
                foreground='white', borderwidth=2)
cal.grid(row=2, column=1)

tk.Label(window, text="Enter time:").grid(row=3, column=0)

timeEntered = tk.StringVar()
timeEntry = tk.Entry(window, width=10, textvariable=timeEntered).grid(row=3, column=1)

var = tk.StringVar()
var.set("am")
R1 = tk.Radiobutton(window, text="am", variable=var, value="am",
                    command=sel).grid(row=3, column=2)

R2 = tk.Radiobutton(window, text="pm", variable=var, value="pm",
                    command=sel).grid(row=3, column=3)

# calendarBttn = tk.Button(window, text = "Select date", command = example3).grid(columnspan = 2)

buttons_frame = tk.Frame(group1)
buttons_frame.grid(row=5, column=0, sticky=tk.W + tk.E)
B1 = tk.Button(buttons_frame, height=2, width=10, text="Start", command=runTest).grid(padx=10, pady=10, columnspan=1)

# tk.Button(window, text = "Open Keyboard", command = openKeyboard()).grid(columnspan = 2)


group1.mainloop()
