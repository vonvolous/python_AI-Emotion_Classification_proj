from tkinter import *
import tkinter.ttk as ttk

window = Tk()

def new_window():
    global new_window
    new = Toplevel()
    
making_window_btn = Button(window, text = "일기 시작하기", command = new_window)
making_window_btn.pack()

window.title('new')
window.geometry("500x800")

window.mainloop()