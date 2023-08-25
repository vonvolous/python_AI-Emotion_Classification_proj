## import module ##
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.simpledialog import *
from calendar_test import *

window = Tk()

## 화면 구성 ##
window.title("Init Window")
window.geometry("800x500")
window.resizable(width=FALSE, height=FALSE)

name_entry = ''

## 함수 ##
# 아이디 입력 창
def name_window():
    global name_entry
    name_entry = askstring("아이디", "아이디를 입력하세요")
    my_name_lbl.configure(text = name_entry)
    return name_entry

# 다음 캘린더 화면으로 넘어가기
def open_window():
    if name_entry == '':
        messagebox.showinfo("아이디 미 입력", "아이디를 입력하지 않으면 저장되지 않습니다.")
        # print(name_entry, "저장되지 않습니다.")
    root = Tk()
    root.geometry("800x500")
    agenda = Agenda(root, selectmode='none')
    date = agenda.datetime.today() + agenda.timedelta(days=2)

    agenda.tag_config('reminder', background='red', foreground='yellow')

    agenda.pack(fill="both", expand=True)
    root.mainloop()    


## 초기화면 ##
app_name_lbl = Label(window, text="앱 이름")
my_name_lbl = Label(window, text= "no name")

app_name_lbl.pack()
my_name_lbl.pack()

name_btn = Button(window, text = "이름 입력하기", command=name_window)
start_btn = Button(window, text = "일기 시작하기", command=open_window)
quit_btn = Button(window, text = "일기 종료하기", command=quit)

name_btn.pack()
start_btn.pack()
quit_btn.pack()


window.mainloop()