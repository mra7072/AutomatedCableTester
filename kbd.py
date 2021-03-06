import tkinter as tk

alphabets = [
    ['`','1','2','3','4','5','6','7','8','9','0','del'],
    ['Tab','q','w','e','r','t','y','u','i','o','p',"\\"],
    ['Caps','a','s','d','f','g','h','j','k','l',':',"'",],
    ['Shift','z','x','c','v','b','n','m',',','.','/','Shift'],
    ['Space']
]    

uppercase = False  # use uppercase chars. 

def select(entry, value):
    global uppercase

    if value == "Space":
        value = ' '
    elif value == 'Enter':
        value = '\n'
    elif value == 'Tab':
        value = '\t'

    if value == "del":
        if isinstance(entry, tk.Entry):
            entry.delete(len(entry.get())-1, 'end')
        #elif isinstance(entry, tk.Text):
        else: # tk.Text
            entry.delete('end - 2c', 'end')
    elif value in ('Caps', 'Shift'):
        uppercase = not uppercase # change True to False, or False to True
    else:
        if uppercase:
            value = value.upper()
        entry.insert('end', value)

def create(root, entry):

    window = tk.Toplevel(root)

    window.configure(background="black")
    window.wm_attributes("-alpha", 0.7)

    for y, row in enumerate(alphabets):

        x = 0

        #for x, text in enumerate(row):
        for text in row:
# 
#             if text in ('Enter', 'Shift','Caps','Tab'):
#                 width = 4
#                 columnspan = 1
            if text == 'Space':
                width = 45
                columnspan = 48
            else:                
                width = 1
                columnspan = 1

            tk.Button(window, text=text, width=width, 
                      command=lambda value=text: select(entry, value),
                      padx=4, pady=4, bd=6, bg="black", fg="white"
                     ).grid(row=y, column=x, columnspan=columnspan)

            x += columnspan
   # window.protocol("WM_DELETE_WINDOW", window.destroy())
    return window
# --- main ---


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Test Keyboard')

    label = tk.Label(root, text='Keyboard')
    label.grid(row=0, column=0, columnspan=2)

    entry1 = tk.Entry(root)
    entry1.grid(row=1, column=0, sticky='news')

    button1 = tk.Button(root, text='Keyboard', command=lambda:create(root, entry1))
    button1.grid(row=1, column=1, sticky='news')

    entry2 = tk.Entry(root)
    entry2.grid(row=2, column=0, sticky='news')

    button2 = tk.Entry(root, text='Keyboard')
    button2.grid(row=2, column=1, sticky='news')

    text1 = tk.Text(root)
    text1.grid(row=3, column=0, sticky='news')

    button3 = tk.Button(root, text='Keyboard', command=lambda:create(root, text1))
    button3.grid(row=3, column=1, sticky='news')

    root.mainloop()
