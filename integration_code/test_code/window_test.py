from tkinter import *

window = Tk()

## 창 화면 만들기 ##
window.title("diary")
window.geometry("800x500")
window.resizable(width=FALSE, height=FALSE)

init_frame = Frame(window) # 초기화면
calendar_frame = Frame(window) # 캘린더 화면

frame_list = (init_frame, calendar_frame)

## 함수 불러오기 ##

def clicknext(window, frame):
    window.destroy()
    frame.tkraise()

for frame in frame_list:
    frame.grid(row = 0, column = 0)
    
## 첫 화면 ##
# 화면 속 글자 #
label1 = Label(init_frame, text="거북이가 그리는 만국기", font =("고딕",15))
label2 = Label(init_frame, text="환영합니다.", font =("궁서체",30), fg = "blue")
label3 = Label(init_frame, text="게임을 시작하려면 게임 시작를 누르시오", font =("고딕",15), bg="magenta", width=55, height=7)

label1.pack()
label2.pack()
label3.pack()


# 시작 및 종료 버튼 #
button1 = Button(init_frame, text="게임 시작", fg = "red", command=lambda:clicknext(window, calendar_frame))
button2 = Button(init_frame, text="게임 종료", fg = "red", command=quit)

button1.pack(side = LEFT, fill = X, padx = 130, pady = 20)
button2.pack(side = LEFT, fill = X, padx = 100, pady = 20)


## 두번째 화면 ##
# 화면 속 글자 #
label4 = Label(calendar_frame, text = "어떻게 국기를 그릴까요?", font =("고딕",15), bg = "magenta", width = 55, height = 7)

label4.pack()


# 게임 시작 및 버튼 #
button3 = Button(calendar_frame, text = "처음 화면으로", command = lambda:clicknext(window, init_frame))

button3.pack(side = TOP, fill = X, padx = 20, pady = 5)


## 화면 실행하기 ##
init_frame.tkraise()
window.mainloop()