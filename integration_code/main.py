## import module ##
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.simpledialog import *
from main_calendar import *

window = Tk()

## 화면 구성 ##
window.title("Init Window")
window.geometry("800x500")
window.resizable(width=FALSE, height=FALSE)

name_entry = ''
global picLabel, textLabel, photo, new_window


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
        
        #print(name_entry, "저장되지 않습니다.")

    ## 사용 될 함수 ##
        
    # 감정 분석 
    def emotion_classification(img_path):
        global cur_emotion
        emotion_list = {0: "angry", 1: "disgust", 2: "fear", 3: "happy", 4: "neutral", 5: "sad", 6: "surprise"}
        
        # load the trained model
        print('\n\nmodel training...\n')
        with open(r'C:\Users\admin\Desktop\python_AI-Emotion_Classification_proj-main\yoojin\trained_network.json', 'r') as trained_network_json:
            trained_model_json = trained_network_json.read()
        
        network = tf.keras.models.model_from_json(trained_model_json)
        network.load_weights(r'C:\Users\admin\Desktop\python_AI-Emotion_Classification_proj-main\yoojin\weights_emotions.hdf5')
        network.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])
        
        # inference with the input image
        image = cv2.imread(img_path)
        
        # 사진에서 얼굴 인식을 위해 haarcascade 불러오기
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # 얼굴 찾기, face : top, right, bottom, left
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # crop the region of interest over a copy
        x, y, w, h = face[0]
        roi = image[y:y+h, x:x+w]
        
        # Resize image to 48, 48
        roi = cv2.resize(roi, (48, 48))
        
        # Normalize
        roi = roi / 255
        
        roi = np.expand_dims(roi, axis=0)
        pred_probability = network.predict(roi)
        pred = np.argmax(pred_probability)
        cur_emotion = emotion_list[pred]
        print('현재 감정:', cur_emotion)
        
        return cur_emotion

    # GPT 답변을 띄우는 함수
    def reply_gpt():
        #history_messages = [{"role": "system", "content": "You are a kind helpful assistant"},]
        #history_messages.append({
        #    "role": "user", "content": "내가" + cur_emotion + "한데 2줄 일기 쓰고 2개의 해쉬태그 달아줘"
        #},)
        #chat = openai.ChatCompletion.create(
        #    model='gpt-3.5-turbo', messages=history_messages
        #)
        #reply = chat.choices[0].message.content
        reply = 'GPT:Hello'
        return reply

    # 선택된 날짜 이미지 업로드 창 띄우는 함수
    def uploading_window(e):
        selected_date = de.get_date()

        new_window = tk.Toplevel(root)
        new_window.title(selected_date)
        new_window.geometry("300x500")
        
        # choose image button
        chooseBtn = tk.Button(new_window, text ='Choose File', command = lambda:upload_photo(selected_date)) 
        chooseBtn.grid(row=2, column=1)
        chooseBtn.pack(side="top")
        
        # show image label
        photo = tk.PhotoImage(file=r'C:\Users\admin\Desktop\python_AI-Emotion_Classification_proj-main\yoojin\initial_upload_image.png')
        picLabel = tk.Label(new_window, image=photo)
        picLabel.pack()
        
        # show emotion classification result label
        textLabel = tk.Label(new_window, text='')
        textLabel.pack()

    # uploading_window에 사진 업로드하는 함수
    def upload_photo(selected_date):
        emotion_icon = {"happy" : "\U0001f600", "sad":"\U0001F62D", "fear": "\U0001F62C", "angry": "\U0001F621", "disgust": "\U0001F92E" ,"neutral": "\U0001F610" ,"surprise": "\U0001F632"}


        file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*')])
        #file_path.replace('\\','/')
        print('파일 경로', file_path)
        
        # 이미지 분석 결과 아이콘을 캘린더에 삽입
        my_emotion = emotion_classification(file_path)
        my_emoticon = emotion_icon[my_emotion]
        agenda.calevent_create(selected_date, my_emoticon, 'emotion')
        agenda.tag_config('emotion', background='yellow', foreground='black')

        photo = Image.open(file_path, mode='r').resize((290, 290))
        picLabel.img = ImageTk.PhotoImage(photo)
        picLabel.configure(image=picLabel.img)
        textLabel.configure(text=my_emotion)
        response = reply_gpt()
        label = tk.Label(new_window, text=response)
        label.place(x=0, y=340)

    root = Tk()
    root.geometry("800x500")
    agenda = Agenda(root, selectmode='none')
    date = agenda.datetime.today()
    
    agenda.tag_config('reminder', background='red', foreground='yellow')
    agenda.pack(fill="both", expand=True)
    #agenda.bind("<<CalendarSelected>>", lambda event: uploading_window(agenda.get_date()))
    
    de = DateEntry(root, selectmode="day")
    de.pack()
    de.bind("<<DateEntrySelected>>", uploading_window)

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