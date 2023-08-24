from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.simpledialog import *
win = Tk ()
win.title("Raspberry Pi UI")
win.geometry('200x100+200+200')
def clickMe():
    new_text = askstring("아이디", "아이디를 입력하세요")
    label.configure(text = new_text)
label = ttk.Label(win, text = 'InputText : ')
label.grid(column = 0, row = 0)
action=ttk.Button(win, text="Change Text", command=clickMe)
action.grid(column=0, row=2)
win.mainloop()